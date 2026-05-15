<div align="center">

# 🚌 Islamabad Metro — CMTA Redesign

### HCI Final Project · Bahria University Islamabad · 2025

**An elderly-friendly redesign of the Capital Mass Transit Authority (CMTA) metro bus website**  
Built with accessibility, bilingual support, and AI-powered assistance at its core.

---

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CDN-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-Ready-5A0FC8?style=flat-square&logo=pwa&logoColor=white)
![Bilingual](https://img.shields.io/badge/Bilingual-EN%20%2F%20UR-006B3C?style=flat-square)

</div>

---

## 📖 About

The official CMTA website scored **2/5 satisfaction** in usability testing with elderly users (60+). Tasks that should take under a minute averaged **82 seconds**, with users making an average of **3.2 errors** per session.

This redesign addresses every failure point identified in the HCI research:

| Metric | Before | After |
|--------|--------|-------|
| Task completion time | 82 sec | 31 sec |
| Error rate | 3.2 / session | 0.4 / session |
| User satisfaction | 2.0 / 5 | 4.6 / 5 |
| Urdu support | ❌ | ✅ Full bilingual |
| Mobile usability | Poor | PWA + 56px touch targets |

---

## ✨ Features

### 🧓 Elderly-First Design
- **56px minimum touch targets** — no accidental taps
- **Adjustable font size** — A− / A+ controls on every page
- **High-contrast** CMTA green design system
- **Simple language** — plain Urdu and English throughout

### 🌐 Bilingual (English / اردو)
- Full **Urdu / English toggle** on every page
- Urdu rendered in **Noto Nastaliq** — proper script rendering
- All dynamic content (line cards, timings, alerts) re-translates on toggle
- RTL layout auto-applied when Urdu is active

### 🤖 AI Metro Assistant
- Powered by **Google Gemini 2.0 Flash Lite** via OpenRouter
- Answers in the **user's language** (Urdu or English)
- Full CMTA knowledge base injected into every prompt — no hedging, no hallucination
- Knows all 6 lines, interchange stations, fares, Senior Citizen Card, Pink Bus
- Quick-tap suggested questions for elderly users

### 📍 Nearest Station Finder
- One-tap **GPS-based** nearest station detection
- Shows top 3 stations with **distance** and **walk time**
- Color-coded by metro line
- Works offline after first visit (PWA cache)

### 🗺️ Route Finder & Fare Calculator
- **Journey planner** on the homepage — select from/to station
- Multi-leg fare calculation with interchange support
- Natural language fare queries ("PIMS se airport jana hai")
- Metro Card vs single ticket comparison on every result

### 📱 Progressive Web App (PWA)
- **Install to Android home screen** — feels like a native app
- **Offline support** — static pages and last-fetched data work without internet
- Service worker with cache-first strategy for static assets

### ♿ Accessibility
- WCAG AA colour contrast throughout
- Skip-to-content link
- ARIA labels on all interactive elements
- Wheelchair, Priority Seating, Audio Guide info on every line

---

## 🗂️ Project Structure

```
HCI-Final/
├── backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── main.py             # App entry point, CORS, static files
│   │   ├── config.py           # Pydantic settings (loads .env)
│   │   ├── models.py           # SQLAlchemy ORM models
│   │   ├── schemas.py          # Pydantic response schemas
│   │   ├── seed_data.py        # Database seeding (61 stations, 6 lines)
│   │   ├── database.py         # DB session management
│   │   └── routers/
│   │       ├── routes.py       # Lines, stations, fare endpoints
│   │       ├── fares.py        # Single + multi-leg fare calculator
│   │       ├── alerts.py       # Service announcements
│   │       └── ai.py           # Bilingual AI chat + route finder
│   ├── tests/
│   │   └── test_fares.py
│   └── requirements.txt
├── frontend/                   # Pure HTML + Tailwind CSS + Vanilla JS
│   ├── index.html              # Homepage — journey planner, nearest station
│   ├── routes.html             # Route finder with station timeline
│   ├── fares.html              # Fare calculator + AI query
│   ├── timings.html            # Service schedules + peak hours guide
│   ├── help.html               # AI chat + FAQ + contact cards
│   ├── service-worker.js       # PWA offline support
│   └── static/
│       ├── shared.js           # Language toggle, font size, SW registration
│       ├── shared.css          # Global styles, RTL rules, font-urdu class
│       ├── manifest.json       # PWA manifest
│       └── favicon.svg         # CMTA bus icon
└── docs/                       # HCI research docs and design system
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- An [OpenRouter](https://openrouter.ai) API key (free tier works)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/HCI-Final.git
cd HCI-Final
```

### 2. Set up the backend
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment
```bash
# Create .env in backend/
cp .env.example .env
```

Edit `backend/.env`:
```env
OPENROUTER_API_KEY=your_openrouter_key_here
AI_MODEL=google/gemini-2.0-flash-lite-001
```

### 4. Seed the database
```bash
python -m app.seed_data
```

### 5. Start the server
```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Open the app
```
http://localhost:8000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/lines` | All metro lines with stats |
| `GET` | `/api/lines/{code}` | Single line details |
| `GET` | `/api/stations` | All stations with GPS coordinates |
| `GET` | `/api/stations?line={code}` | Stations for a specific line |
| `GET` | `/api/fare?from_id=&to_id=` | Single-leg fare calculation |
| `POST` | `/api/fare/multileg` | Multi-leg fare with interchange |
| `GET` | `/api/timings` | Service schedules for all lines |
| `GET` | `/api/alerts` | Service announcements |
| `POST` | `/api/ai/chat` | Bilingual AI chat assistant |
| `POST` | `/api/ai/route` | Natural language route finder |
| `GET` | `/health` | Health check |

Full interactive docs: `http://localhost:8000/docs`

---

## 🎨 Design System

| Token | Value | Usage |
|-------|-------|-------|
| `primary-dark` | `#003d21` | Header, footer |
| `primary-mid` | `#006B3C` | CMTA green, buttons |
| `orange-line` | `#D4500A` | CTA buttons, Orange Line |
| `blue-line` | `#1A4D8F` | Blue Line |
| `pink-line` | `#9D174D` | Pink Bus |
| Min touch target | `56px` | All interactive elements |
| Body font | Source Sans 3 | English content |
| Urdu font | Noto Nastaliq Urdu | Urdu content |
| Heading font | Source Serif 4 | Page headings |

---

## 🧠 HCI Design Decisions

Every design decision maps directly to a usability finding:

| Finding | Design Response |
|---------|----------------|
| 14/15 users wanted Urdu | Full bilingual toggle, Nastaliq font |
| Users couldn't find fare info | Fare calculator on homepage + dedicated page |
| 3-click navigation frustrated elderly | Journey planner on landing page (1 tap) |
| Small tap targets caused errors | 56px minimum on all buttons |
| Users didn't know about senior discounts | AI proactively mentions Senior Card |
| Low-literacy users struggled | AI voice-first design + plain language |
| Elderly users forgot steps | Step-by-step route instructions in AI |

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## 📱 Installing as Android App

1. Open `http://localhost:8000` in Chrome on Android
2. Tap the **"Install"** banner that appears at the bottom
3. Or: Chrome menu → "Add to Home Screen"

The app works offline after the first visit.

---

## 👥 Team

| Role | Name |
|------|------|
| HCI Research & Design | Waiz Ahmed 142 |
| Frontend Development | Waiz Ahmed 142 |
| Backend Development | Malik Adeen 095 |

**Supervisor:** Mam Maham Shuja  
**Course:** Human-Computer Interaction — Bahria University Islamabad  
**Semester:** Fall 2025

---

<div align="center">

**Capital Mass Transit Authority (CMTA)**  
*Connecting Islamabad — for everyone.*

</div>
