from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api", tags=["fares"])


@router.get("/fare", response_model=schemas.FareOut)
def calculate_fare(from_id: int, to_id: int, db: Session = Depends(get_db)):
    """
    Calculate fare between two stations by their IDs.
    GET /api/fare?from_id=1&to_id=8
    """
    from_station = db.query(models.Station).filter(models.Station.id == from_id).first()
    to_station   = db.query(models.Station).filter(models.Station.id == to_id).first()

    if not from_station or not to_station:
        raise HTTPException(status_code=404, detail="One or both stations not found")

    if from_station.line_id != to_station.line_id:
        raise HTTPException(
            status_code=400,
            detail="Cross-line journeys not yet supported. Please use an interchange station."
        )

    stops_count = abs(from_station.stop_order - to_station.stop_order)
    if stops_count == 0:
        raise HTTPException(status_code=400, detail="From and To stations are the same")

    # Look up fare tier for this line
    fare = (
        db.query(models.Fare)
        .filter(
            models.Fare.line_id == from_station.line_id,
            models.Fare.min_stops <= stops_count,
            models.Fare.max_stops >= stops_count,
        )
        .first()
    )

    if not fare:
        # Fallback to highest tier
        fare = (
            db.query(models.Fare)
            .filter(models.Fare.line_id == from_station.line_id)
            .order_by(models.Fare.max_stops.desc())
            .first()
        )

    line = db.query(models.Line).filter(models.Line.id == from_station.line_id).first()

    return schemas.FareOut(
        from_station=from_station.name,
        to_station=to_station.name,
        line_name=line.name if line else "Unknown",
        stops_count=stops_count,
        single_pkr=fare.single_pkr,
        card_pkr=fare.card_pkr,
        label=fare.label,
    )


@router.post("/fare/multileg", response_model=schemas.MultiFareOut)
def calculate_fare_multileg(request: dict, db: Session = Depends(get_db)):
    """
    Calculate fare between two stations across multiple lines using interchange transfers.
    POST /api/fare/multileg  {"from_id":1, "to_id":8}
    """
    from_id = request.get('from_id')
    to_id = request.get('to_id')
    if from_id is None or to_id is None:
        raise HTTPException(status_code=400, detail="from_id and to_id are required")

    stations = db.query(models.Station).all()
    stations_by_id = {s.id: s for s in stations}
    if from_id not in stations_by_id or to_id not in stations_by_id:
        raise HTTPException(status_code=404, detail="One or both stations not found")

    # Build adjacency: neighbor stations on same line
    adj = {s.id: set() for s in stations}
    # group by line
    lines = {}
    for s in stations:
        lines.setdefault(s.line_id, []).append(s)
    for line_id, stops in lines.items():
        stops_sorted = sorted(stops, key=lambda x: x.stop_order)
        for i in range(len(stops_sorted)-1):
            a = stops_sorted[i].id
            b = stops_sorted[i+1].id
            adj[a].add(b); adj[b].add(a)

    # Link interchanges by station name (case-insensitive)
    name_map = {}
    for s in stations:
        key = (s.name or '').strip().lower()
        name_map.setdefault(key, []).append(s.id)
    for ids in name_map.values():
        if len(ids) > 1:
            for i in range(len(ids)):
                for j in range(i+1, len(ids)):
                    adj[ids[i]].add(ids[j]); adj[ids[j]].add(ids[i])

    # BFS shortest path
    from collections import deque
    q = deque([from_id])
    prev = {from_id: None}
    while q:
        cur = q.popleft()
        if cur == to_id:
            break
        for nb in adj[cur]:
            if nb not in prev:
                prev[nb] = cur
                q.append(nb)

    if to_id not in prev:
        raise HTTPException(status_code=404, detail="No route found between stations")

    # Reconstruct path
    path_ids = []
    cur = to_id
    while cur is not None:
        path_ids.append(cur)
        cur = prev[cur]
    path_ids.reverse()

    # Build legs grouped by continuous same line segments
    legs = []
    if not path_ids:
        raise HTTPException(status_code=400, detail="Invalid path")
    seg_start = path_ids[0]
    seg_line = stations_by_id[seg_start].line_id
    seg_prev = seg_start
    for sid in path_ids[1:]:
        s = stations_by_id[sid]
        if s.line_id != seg_line:
            # close previous segment from seg_start to seg_prev
            start_station = stations_by_id[seg_start]
            end_station   = stations_by_id[seg_prev]
            legs.append((start_station, end_station))
            seg_start = sid
            seg_line = s.line_id
        seg_prev = sid
    # close last
    start_station = stations_by_id[seg_start]
    end_station   = stations_by_id[seg_prev]
    legs.append((start_station, end_station))

    # For each leg compute fare
    leg_res = []
    total_single = 0
    total_card = 0
    for (a,b) in legs:
        stops_count = abs(a.stop_order - b.stop_order)
        if stops_count == 0:
            continue
        fare = (
            db.query(models.Fare)
            .filter(models.Fare.line_id == a.line_id,
                    models.Fare.min_stops <= stops_count,
                    models.Fare.max_stops >= stops_count)
            .first()
        )
        if not fare:
            fare = (
                db.query(models.Fare)
                .filter(models.Fare.line_id == a.line_id)
                .order_by(models.Fare.max_stops.desc())
                .first()
            )
        line = db.query(models.Line).filter(models.Line.id == a.line_id).first()
        single = fare.single_pkr if fare else 0
        card = fare.card_pkr if fare else 0
        total_single += single
        total_card += card
        leg_res.append({
            'from_station': a.name,
            'to_station': b.name,
            'line_name': line.name if line else 'Unknown',
            'stops_count': stops_count,
            'single_pkr': single,
            'card_pkr': card,
            'label': fare.label if fare else ''
        })

    path_names = [stations_by_id[sid].name for sid in path_ids]

    return schemas.MultiFareOut(
        total_single_pkr=total_single,
        total_card_pkr=total_card,
        legs=[schemas.FareLeg(**l) for l in leg_res],
        path=path_names,
    )
