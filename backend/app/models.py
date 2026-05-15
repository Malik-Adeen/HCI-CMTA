from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Line(Base):
    """A metro bus line — Orange, Green, Blue, Red, Pink, Electric."""
    __tablename__ = "lines"

    id        = Column(Integer, primary_key=True, index=True)
    code      = Column(String(20), unique=True, nullable=False)   # e.g. "orange"
    name      = Column(String(100), nullable=False)               # e.g. "Orange Line"
    name_urdu = Column(String(200), nullable=True)
    color_hex = Column(String(7), nullable=False)                 # e.g. "#D4500A"
    from_stop = Column(String(100), nullable=False)
    to_stop   = Column(String(100), nullable=False)
    length_km = Column(Float, nullable=True)
    total_stops = Column(Integer, nullable=True)
    travel_time_min = Column(Integer, nullable=True)              # one-way
    frequency_peak_min = Column(Integer, nullable=True)
    frequency_offpeak_min = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    notes     = Column(Text, nullable=True)

    stations  = relationship("Station", back_populates="line", order_by="Station.stop_order")


class Station(Base):
    """A bus stop / station on a line."""
    __tablename__ = "stations"

    id           = Column(Integer, primary_key=True, index=True)
    line_id      = Column(Integer, ForeignKey("lines.id"), nullable=False)
    name         = Column(String(150), nullable=False)
    name_urdu    = Column(String(300), nullable=True)
    stop_order   = Column(Integer, nullable=False)               # position on line (1-based)
    is_terminus  = Column(Boolean, default=False)
    is_interchange = Column(Boolean, default=False)
    landmark     = Column(String(200), nullable=True)            # nearby landmark hint
    latitude     = Column(Float, nullable=True)
    longitude    = Column(Float, nullable=True)

    line         = relationship("Line", back_populates="stations")


class Fare(Base):
    """Fare between two stations on the same line (distance-based)."""
    __tablename__ = "fares"

    id           = Column(Integer, primary_key=True, index=True)
    line_id      = Column(Integer, ForeignKey("lines.id"), nullable=False)
    min_stops    = Column(Integer, nullable=False)   # journey covers this many stops
    max_stops    = Column(Integer, nullable=False)
    single_pkr   = Column(Integer, nullable=False)   # single-use token price
    card_pkr     = Column(Integer, nullable=False)   # metro card price
    label        = Column(String(50), nullable=True) # e.g. "Short Journey"


class Alert(Base):
    """Service announcements and updates."""
    __tablename__ = "alerts"

    id         = Column(Integer, primary_key=True, index=True)
    tag        = Column(String(50), nullable=False)       # "Service Update" / "Infrastructure" / "Smart Card"
    tag_urdu   = Column(String(100), nullable=True)
    tag_type   = Column(String(20), nullable=False)       # "green" / "orange" / "blue"
    title      = Column(String(200), nullable=False)
    title_urdu = Column(String(300), nullable=True)
    body       = Column(Text, nullable=False)
    body_urdu  = Column(Text, nullable=True)
    date_label = Column(String(50), nullable=False)       # e.g. "May 2025"
    date_label_urdu = Column(String(100), nullable=True)
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
