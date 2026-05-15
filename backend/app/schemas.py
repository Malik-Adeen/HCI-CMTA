from pydantic import BaseModel
from typing import Optional, List


# ── Lines ──────────────────────────────────────────────────────────────
class LineOut(BaseModel):
    id: int
    code: str
    name: str
    name_urdu: Optional[str]
    color_hex: str
    from_stop: str
    to_stop: str
    length_km: Optional[float]
    total_stops: Optional[int]
    travel_time_min: Optional[int]
    frequency_peak_min: Optional[int]
    frequency_offpeak_min: Optional[int]
    is_active: bool
    notes: Optional[str]

    class Config:
        from_attributes = True


# ── Stations ───────────────────────────────────────────────────────────
class StationOut(BaseModel):
    id: int
    name: str
    name_urdu: Optional[str]
    stop_order: int
    is_terminus: bool
    is_interchange: bool
    landmark: Optional[str]
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    line_id: int

    class Config:
        from_attributes = True


# ── Fares ──────────────────────────────────────────────────────────────
class FareOut(BaseModel):
    from_station: str
    to_station: str
    line_name: str
    stops_count: int
    single_pkr: int
    card_pkr: int
    label: str

    class Config:
        from_attributes = True


class FareLeg(BaseModel):
    from_station: str
    to_station: str
    line_name: str
    stops_count: int
    single_pkr: int
    card_pkr: int
    label: str


class MultiFareOut(BaseModel):
    total_single_pkr: int
    total_card_pkr: int
    legs: List[FareLeg]
    path: List[str]

    class Config:
        from_attributes = True


# ── Alerts ─────────────────────────────────────────────────────────────
class AlertOut(BaseModel):
    id: int
    tag: str
    tag_urdu: Optional[str]
    tag_type: str
    title: str
    title_urdu: Optional[str]
    body: str
    body_urdu: Optional[str]
    date_label: str
    date_label_urdu: Optional[str]

    class Config:
        from_attributes = True


# ── AI Chat ────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    language: str = "en"          # "en" or "ur"
    history: Optional[List[dict]] = []


class ChatResponse(BaseModel):
    reply: str
    language: str


# ── AI Route Finder ────────────────────────────────────────────────────
class RouteQueryRequest(BaseModel):
    query: str                    # natural language, e.g. "PIMS se airport jana hai"


class RouteQueryResponse(BaseModel):
    from_station: Optional[str]
    to_station: Optional[str]
    suggested_line: Optional[str]
    fare_pkr: Optional[int]
    instructions: str             # plain language answer
    confidence: str               # "high" / "medium" / "low"
