from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api", tags=["routes"])

PINK_STATIONS_FALLBACK = [
    {
        "name": "Nilore Terminal",
        "name_urdu": "نیلور ٹرمینل",
        "stop_order": 1,
        "is_terminus": True,
        "is_interchange": False,
        "landmark": "Pink Bus origin (Nilore side)",
    },
    {
        "name": "Bhara Kahu",
        "name_urdu": "بھارہ کہو",
        "stop_order": 2,
        "is_terminus": False,
        "is_interchange": True,
        "landmark": "Shared corridor with Green Line area",
    },
    {
        "name": "Humak",
        "name_urdu": "ہماک",
        "stop_order": 3,
        "is_terminus": False,
        "is_interchange": False,
        "landmark": "Humak route branch",
    },
    {
        "name": "I-14 Markaz",
        "name_urdu": "آئی ۱۴ مرکز",
        "stop_order": 4,
        "is_terminus": False,
        "is_interchange": False,
        "landmark": "I-14 route branch",
    },
    {
        "name": "B-17 Markaz",
        "name_urdu": "بی ۱۷ مرکز",
        "stop_order": 5,
        "is_terminus": False,
        "is_interchange": False,
        "landmark": "B-17 route branch",
    },
    {
        "name": "F-11 Markaz",
        "name_urdu": "ایف ۱۱ مرکز",
        "stop_order": 6,
        "is_terminus": False,
        "is_interchange": True,
        "landmark": "F-11 sector center",
    },
    {
        "name": "Pak Secretariat",
        "name_urdu": "پاکستان سیکرٹریٹ",
        "stop_order": 7,
        "is_terminus": True,
        "is_interchange": True,
        "landmark": "Government offices, Secretariat",
    },
]


def _set_total_stops_if_missing(lines: List[models.Line]) -> None:
    for line in lines:
        if line.total_stops is None and len(line.stations) > 0:
            line.total_stops = len(line.stations)


def _ensure_pink_stations(db: Session, line_obj: models.Line) -> None:
    if line_obj.code != "pink":
        return
    existing = db.query(models.Station).filter(models.Station.line_id == line_obj.id).count()
    if existing > 0:
        return
    for station in PINK_STATIONS_FALLBACK:
        db.add(models.Station(line_id=line_obj.id, **station))
    line_obj.total_stops = len(PINK_STATIONS_FALLBACK)
    db.commit()


@router.get("/lines", response_model=List[schemas.LineOut])
def get_lines(db: Session = Depends(get_db)):
    """Return all metro lines."""
    lines = db.query(models.Line).filter(models.Line.is_active == True).all()
    for line in lines:
        _ensure_pink_stations(db, line)
    _set_total_stops_if_missing(lines)
    return lines


@router.get("/lines/{code}", response_model=schemas.LineOut)
def get_line(code: str, db: Session = Depends(get_db)):
    """Return a single line by its code (e.g. 'orange')."""
    line = db.query(models.Line).filter(models.Line.code == code).first()
    if not line:
        raise HTTPException(status_code=404, detail=f"Line '{code}' not found")
    _ensure_pink_stations(db, line)
    _set_total_stops_if_missing([line])
    return line


@router.get("/stations", response_model=List[schemas.StationOut])
def get_stations(line: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Return stations. Filter by line code: GET /api/stations?line=orange
    Returns all stations if no filter provided.
    """
    query = db.query(models.Station)
    if line:
        line_obj = db.query(models.Line).filter(models.Line.code == line.lower()).first()
        if not line_obj:
            raise HTTPException(status_code=404, detail=f"Line '{line}' not found")
        _ensure_pink_stations(db, line_obj)
        query = query.filter(models.Station.line_id == line_obj.id)
    return query.order_by(models.Station.line_id, models.Station.stop_order).all()
