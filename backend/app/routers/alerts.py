from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api", tags=["alerts"])


@router.get("/alerts", response_model=List[schemas.AlertOut])
def get_alerts(db: Session = Depends(get_db)):
    """Return active service announcements, newest first."""
    return (
        db.query(models.Alert)
        .filter(models.Alert.is_active == True)
        .order_by(models.Alert.created_at.desc())
        .all()
    )


@router.get("/timings")
def get_timings(db: Session = Depends(get_db)):
    """Return service timing info for all active lines."""
    lines = db.query(models.Line).filter(models.Line.is_active == True).all()
    return [
        {
            "line_code": l.code,
            "line_name": l.name,
            "color_hex": l.color_hex,
            "first_bus": "06:00 AM",
            "last_bus":  "10:00 PM",
            "frequency_peak":    f"Every {l.frequency_peak_min} min"    if l.frequency_peak_min    else "See station",
            "frequency_offpeak": f"Every {l.frequency_offpeak_min} min" if l.frequency_offpeak_min else "See station",
            "operating_days": "Daily" if l.code != "pink" else "Daily (Sat & Sun for ST routes)",
        }
        for l in lines
    ]
