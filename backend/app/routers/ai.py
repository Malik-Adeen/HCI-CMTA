from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from openai import OpenAI
from app.database import get_db
from app.config import settings
from app import models, schemas

router = APIRouter(prefix="/api/ai", tags=["ai"])

client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL,
    default_headers={
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "CMTA Islamabad Metro Assistant",
    },
)

# ── CMTA KNOWLEDGE BASE ───────────────────────────────────────────────────────
# Single source of truth injected into every prompt.
# Keeps the AI factual, confident, and hallucination-free.
# ─────────────────────────────────────────────────────────────────────────────
CMTA_KNOWLEDGE = """
=== CMTA ISLAMABAD METRO — OFFICIAL KNOWLEDGE BASE ===

OPERATOR : Capital Mass Transit Authority (CMTA)
CITY     : Islamabad, Pakistan
HELPLINE : 051-2258066  |  Mon–Fri 9:00 AM – 12:00 AM
WEBSITE  : cmta.com.pk
HOURS    : 6:00 AM – 10:00 PM  •  Daily (all days including weekends)

── METRO LINES ──

1. ORANGE LINE
   Faiz Ahmed Faiz (FAF) / Saddar → NUST/G-12 → G-11 Markaz → Golra Morr
   → Peshawar Morr → Islamabad International Airport
   Stations: 10  |  Peak: every 5 min  |  Off-peak: every 10 min

2. GREEN LINE
   PIMS Hospital → G-7 Markaz → Aabpara → Serena Hotel
   → Super Market (F-6) → F-7 Markaz → F-8 Markaz → Bara Kahu
   Stations: 8  |  Peak: every 8 min  |  Off-peak: every 15 min

3. BLUE LINE
   PIMS Hospital → Children Hospital → Secretariat → Faizabad
   → I-8 Markaz → I-10 Markaz → I-14 → Koral Chowk
   Stations: 14  |  Peak: every 8 min  |  Off-peak: every 12 min

4. RED LINE (BRT)
   Saddar → Aabpara → G-6 → Secretariat → D-Chowk → F-5 → F-7 Markaz
   Peak: every 5 min  |  Off-peak: every 10 min  |  Dedicated BRT corridor

5. ELECTRIC BUS
   NUST Depot (G-11) → G-11 Markaz → Aabpara → Serena Hotel
   → PIMS Hospital → G-8 Markaz → G-9 Markaz → Bari Imam
   Stations: 10  |  Every 10 min  |  Zero-emission, climate-controlled

6. PINK BUS SERVICE
   Multiple routes across Islamabad
   FOR WOMEN ONLY — 100% FREE, no ticket required
   All-female crew. Daily (Sat & Sun for special routes).

── INTERCHANGE STATIONS ──

PIMS Hospital   : Blue Line ↔ Green Line ↔ Electric Bus
Aabpara         : Green Line ↔ Red Line BRT ↔ Electric Bus
G-11 Markaz     : Orange Line ↔ Electric Bus
Saddar (FAF)    : Orange Line ↔ Red Line BRT
Serena Hotel    : Green Line ↔ Electric Bus

── FARES (by stops travelled) ──

 1–2 stops  : Rs. 20   (Metro Card: Rs. 16)
 3–5 stops  : Rs. 25   (Metro Card: Rs. 20)
 6–8 stops  : Rs. 30   (Metro Card: Rs. 24)
 9–12 stops : Rs. 40   (Metro Card: Rs. 32)
 13+ stops  : Rs. 50   (Metro Card: Rs. 40)
 Cross-line : Rs. 50 flat (Metro Card: Rs. 40)
 Pink Bus   : FREE for women

METRO CARD  : 20% cheaper on every journey. Buy at any station counter.
              Minimum top-up: Rs. 100. Requires valid CNIC.

SENIOR CITIZEN CARD (age 60+):
  50% discount on all fares. Apply at any station with CNIC — issued same day.

STUDENT CARD: 30% discount with valid student ID.

── COMMON ROUTES ──

Airport → City Centre  : Orange Line, Airport → Saddar (~30 min, Rs. 50)
PIMS → Secretariat     : Blue Line, 2 stops (~8 min, Rs. 20)
F-7 Markaz → PIMS      : Green Line, 4 stops (~12 min, Rs. 25)
G-11 → Airport         : Orange Line, 5 stops (~15 min, Rs. 25)
Saddar → Bara Kahu     : Orange to Saddar, change to Green Line at PIMS

── ACCESSIBILITY ──

All stations: wheelchair ramps, lifts, priority seating (blue seats at front)
Audio announcements at every station and inside buses
Staff trained to assist elderly and disabled passengers
Braille signage at major stations

── TIPS FOR ELDERLY PASSENGERS ──

Best travel time: 10:00 AM – 2:00 PM (least crowded, easiest boarding)
Avoid peak hours: 7:00–9:30 AM and 4:30–7:30 PM
Ask any staff for boarding assistance — always available
Senior Citizen Card saves 50% — apply free at any station
"""

# ── SYSTEM PROMPTS ────────────────────────────────────────────────────────────

SYSTEM_PROMPT_EN = f"""You are the official AI assistant for Islamabad's CMTA Metro Bus service.

PERSONA (never break these rules):
- You are CMTA's official assistant. Answer with confidence at all times.
- NEVER say "I'm not sure", "I don't know", "I cannot confirm", or anything that hedges.
  You have the complete CMTA knowledge base below — use it.
- Be warm and patient, like a helpful family member.
- Keep answers SHORT: 2–4 sentences for simple questions. No walls of text.
- For route questions: state the line name, boarding station, alighting station, fare, and time.
- Always mention the Senior Citizen Card (50% off) when talking to or about elderly passengers.
- Only give the helpline number (051-2258066) when the user is confused or distressed.
- Use plain English. Spell out abbreviations once (e.g. "FAF — Faiz Ahmed Faiz station").

{CMTA_KNOWLEDGE}"""


SYSTEM_PROMPT_UR = f"""آپ اسلام آباد کے سی ایم ٹی اے میٹرو بس سروس کے سرکاری اے آئی اسسٹنٹ ہیں۔

اصول (کبھی نہ توڑیں):
- آپ سی ایم ٹی اے کے سرکاری نمائندہ ہیں۔ ہمیشہ اعتماد سے جواب دیں۔
- کبھی یہ نہ کہیں کہ مجھے نہیں معلوم یا میں یقین سے نہیں کہہ سکتا۔
  آپ کے پاس مکمل سی ایم ٹی اے کا ڈیٹا ہے — اسے استعمال کریں۔
- مختصر جواب دیں — صرف ۲-۴ جملے۔ سادہ اور آسان اردو۔
- راستے کے سوال پر: لائن کا نام، سوار ہونے کا اسٹیشن، اترنے کا اسٹیشن، کرایہ اور وقت بتائیں۔
- بزرگ مسافروں کو سینئر سٹیزن کارڈ (۵۰٪ چھوٹ) کا ذکر ضرور کریں۔
- ہیلپ لائن نمبر (051-2258066) صرف تب دیں جب مسافر پریشان لگے۔

{CMTA_KNOWLEDGE}"""


# ─────────────────────────────────────────────────────────────────────────────

def get_live_route_context(db: Session) -> str:
    """Inject live DB station data on top of the static knowledge base."""
    lines = db.query(models.Line).filter(models.Line.is_active == True).all()
    ctx = []
    for line in lines:
        stops = [s.name for s in sorted(line.stations, key=lambda x: x.stop_order)]
        interchanges = [s.name for s in line.stations if s.is_interchange]
        entry = f"{line.name} ({line.from_stop} ↔ {line.to_stop}): {' → '.join(stops)}"
        if interchanges:
            entry += f"  [Interchanges: {', '.join(interchanges)}]"
        ctx.append(entry)
    return "\n".join(ctx)


@router.post("/chat", response_model=schemas.ChatResponse)
def ai_chat(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    """
    Bilingual AI chat assistant.
    Accepts {message, language ('en'|'ur'), history}.
    Returns a confident, plain-language reply.
    """
    base_prompt = SYSTEM_PROMPT_UR if request.language == "ur" else SYSTEM_PROMPT_EN
    live_data   = get_live_route_context(db)
    full_system = f"{base_prompt}\n\n=== LIVE STATION DATA (exact stop names from database) ===\n{live_data}"

    messages = [{"role": "system", "content": full_system}]
    for h in request.history[-6:]:
        messages.append(h)
    messages.append({"role": "user", "content": request.message})

    try:
        response = client.chat.completions.create(
            model=settings.AI_MODEL,
            messages=messages,
            max_tokens=350,
            temperature=0.3,  # Lower = more factual, less hallucination
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service error: {str(e)}")

    return schemas.ChatResponse(reply=reply, language=request.language)


@router.post("/route", response_model=schemas.RouteQueryResponse)
def ai_route_finder(request: schemas.RouteQueryRequest, db: Session = Depends(get_db)):
    """
    Natural language route finder.
    User types: 'PIMS se airport jana hai' → structured route + fare.
    """
    live_data = get_live_route_context(db)

    prompt = f"""You are a CMTA metro route expert. A passenger asked: "{request.query}"

{CMTA_KNOWLEDGE}

Live station data (use these exact names):
{live_data}

Respond ONLY with valid JSON — no markdown, no explanation:
{{
  "from_station": "exact station name from live data, or null",
  "to_station": "exact station name from live data, or null",
  "suggested_line": "line name (list both if interchange needed)",
  "fare_pkr": estimated single fare as integer,
  "instructions": "step-by-step directions in the SAME language as the user query. Include line name, board at, alight at, fare, journey time. Mention Senior Card savings if applicable.",
  "confidence": "high"
}}"""

    try:
        response = client.chat.completions.create(
            model=settings.AI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=450,
            temperature=0.1,
        )
        import json
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)
    except Exception:
        fallback = (
            "براہ کرم دوبارہ پوچھیں یا ہیلپ لائن پر کال کریں: 051-2258066"
            if request.language == "ur"
            else "Please try again or call the helpline: 051-2258066."
        )
        return schemas.RouteQueryResponse(
            from_station=None, to_station=None,
            suggested_line=None, fare_pkr=None,
            instructions=fallback, confidence="low",
        )

    return schemas.RouteQueryResponse(**data)
