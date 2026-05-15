# HCI Final Project — Context Vault
> Single source of truth. Last updated: May 2025

---

## Project Identity

| Field | Value |
|---|---|
| Course | Human Computer Interaction (HCI) — Bahria University Islamabad |
| Students | Malik Adeen Rizwan (01-134232-095) · M Waiz Ahmed (01-134232-142) |
| Title | Gap Analysis and Elderly-Friendly Redesign of the CMTA Metro Bus Website |
| Target System | Capital Mass Transit Authority (CMTA) — https://cmta.com.pk |
| Target Users | Elderly individuals aged 60 and above |
| Project Path | D:\HCI-Final\ |

---

## Research Summary (Assignments 1–4)

### Core Problem
The CMTA website is inaccessible to elderly users due to:
- English-only interface (14/15 users wanted Urdu)
- Small font sizes (12/15 users reported discomfort)
- Complex multi-click navigation (11/15 felt confused)
- Cluttered homepage with too many promotional banners
- No quick-access route/fare search on landing page

### Usability Testing Results
| Metric | Old System | New Design |
|---|---|---|
| Avg task time | ~82 seconds | ~31 seconds |
| Avg errors | ~3.2 | ~0.4 |
| Avg satisfaction | 2/5 | 4.6/5 |

### Personas
- **Tariq Mehmood** (68, Android) — needs Urdu + large text, one-click journey search
- **Mrs. Salma** (62, Tablet) — needs clean layout, icon-based nav, prominent alerts

---

## Tech Stack (All Decided & Implemented)

| Layer | Technology | Status |
|---|---|---|
| Backend | FastAPI (Python) | ✅ Done |
| Database | SQLite (file: cmta.db) | ✅ Seeded |
| ORM | SQLAlchemy | ✅ Done |
| AI | OpenRouter API — google/gemini-2.0-flash-lite | ✅ Wired |
| Frontend | Vanilla HTML + Tailwind CDN | ✅ Done |
| Icons | Material Symbols Outlined (Google Fonts) | ✅ Done |
| Mobile | PWA (manifest.json + service worker) | ✅ Done |
| Server | Uvicorn | ✅ Running |

---

## Current Project State

### Backend — COMPLETE ✅
All endpoints live at http://localhost:8000

| Method | Endpoint | Status |
|---|---|---|
| GET | /api/lines | ✅ |
| GET | /api/lines/{code} | ✅ |
| GET | /api/stations?line={code} | ✅ |
| GET | /api/fare?from_id={id}&to_id={id} | ✅ |
| GET | /api/timings | ✅ |
| GET | /api/alerts | ✅ |
| POST | /api/ai/chat | ✅ |
| POST | /api/ai/route | ✅ |
| GET | /docs | ✅ Swagger UI |

### Frontend — COMPLETE ✅
| File | Status | Notes |
|---|---|---|
| frontend/index.html | ✅ | Homepage, journey planner, live API data |
| frontend/routes.html | ✅ | Line tabs, station timeline, interchange badges |
| frontend/fares.html | ✅ | Fare calculator + AI NLP route finder |
| frontend/timings.html | ✅ | Per-line timing cards, peak hours guide |
| frontend/help.html | ✅ | AI chat, FAQ, contact cards |
| frontend/static/shared.js | ✅ | Lang persistence, font persistence, global helpers |
| frontend/static/shared.css | ✅ | Custom select styling, Urdu RTL overrides |
| frontend/static/manifest.json | ✅ | PWA manifest |

### Known Issues / TODO
- [ ] Material Symbols icons may show as text on first load (font CDN delay) — workaround: hard refresh
- [ ] Urdu toggle switches font/RTL but does NOT translate page text (no data-en/data-ur attributes added yet)

---

## File Structure

```
D:\HCI-Final\
├── backend\
│   ├── app\
│   │   ├── __init__.py
│   │   ├── config.py          Reads .env settings
│   │   ├── database.py        SQLite connection + session
│   │   ├── main.py            FastAPI app entry point
│   │   ├── models.py          SQLAlchemy: Line, Station, Fare, Alert
│   │   ├── schemas.py         Pydantic schemas
│   │   ├── seed_data.py       Real CMTA data (run once)
│   │   └── routers\
│   │       ├── __init__.py
│   │       ├── routes.py      /api/lines, /api/stations
│   │       ├── fares.py       /api/fare
│   │       ├── alerts.py      /api/alerts, /api/timings
│   │       └── ai.py          /api/ai/chat, /api/ai/route
│   ├── cmta.db                SQLite database (auto-created)
│   ├── requirements.txt
│   ├── .env                   Secrets (not in git)
│   ├── .env.example
│   └── README.md
│
├── frontend\
│   ├── index.html
│   ├── routes.html
│   ├── fares.html
│   ├── timings.html
│   ├── help.html
│   └── static\
│       ├── shared.js          Global lang/font persistence (localStorage)
│       ├── shared.css         Custom select styling, RTL overrides
│       └── manifest.json      PWA manifest
│
└── docs\
    ├── PROJECT_CONTEXT.md     ← this file
    ├── CMTA_DATA.md           Real routes/stations/fares data + sources
    ├── DESIGN_SYSTEM.md       CSS variables, colors, fonts, patterns
    ├── STITCH_DESIGN.md       Stitch design tokens (adopted as baseline)
    └── stitch_routes_reference.html  Original Stitch output (reference only)
```

---

## Environment (.env)

```
DATABASE_URL=sqlite:///./cmta.db
OPENROUTER_API_KEY=<user's key>
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
AI_MODEL=google/gemini-2.0-flash-lite
APP_NAME=CMTA Metro Bus API
DEBUG=True
```

---

## How to Run

```bash
cd D:\HCI-Final\backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Then open: http://localhost:8000

---

## Design System (Quick Reference)

| Token | Value | Usage |
|---|---|---|
| primary | #00502c | Dark green, headings |
| primary-mid | #006B3C | Green, navbar border, buttons |
| primary-light | #e8f5ee | Green tint backgrounds |
| secondary | #a63b00 | Orange-red, CTAs |
| orange-line | #D4500A | Orange Line, CTA buttons |
| blue-line | #1A4D8F | Blue Line |
| red-line | #B91C1C | Red Line |
| electric-line | #065F46 | Electric Bus |
| pink-line | #9D174D | Pink Bus |
| surface | #fcf9f8 | Page background |
| on-surface | #1c1b1b | Body text |
| Font (body) | Source Sans 3 | 20px base minimum |
| Font (headings) | Source Serif 4 | Bold |
| Font (Urdu) | Noto Nastaliq Urdu | RTL, loaded but not auto-applied to content yet |

---

## Remaining Work (Priority Order)

1. **Fix Urdu content translation** — add data-en/data-ur to key nav/heading elements, shared.js already reads them
2. **Demo polish** — test all pages end-to-end, fix any edge cases
3. **Presentation prep** — screenshots, demo flow, HCI justification writeup
