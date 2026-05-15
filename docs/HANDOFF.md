# New Session Handoff — HCI Metro Bus Project

## What this project is
Elderly-friendly redesign of the CMTA Metro Bus website (Islamabad, Pakistan) — HCI Final Project, Bahria University. Students: Malik Adeen Rizwan + M Waiz Ahmed.

## Project path on disk
D:\HCI-Final\  (connected via Filesystem MCP)

## Current state — what is DONE
- Backend: FastAPI + SQLite fully working. All 8 API endpoints live.
- Database: Seeded with real CMTA data (6 lines, 50+ stations, fares, alerts).
- AI: OpenRouter wired (google/gemini-2.0-flash-lite). /api/ai/chat and /api/ai/route working.
- Frontend: 5 pages done (index, routes, fares, timings, help). Tailwind CDN. All pages fetch from API.
- PWA: service worker in place and served by backend; offline/install ready.
- Shared: static/shared.js handles language + font size persistence via localStorage. static/shared.css handles custom select styling.

## How to start the backend
```
cd D:\HCI-Final\backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

## What is NOT done yet (priority order)
1. Urdu content translation — shared.js reads data-en/data-ur attributes but they haven't been added to HTML elements yet. Currently toggle only switches font/RTL direction, doesn't translate text.
2. Final demo polish and end-to-end testing.

## Key files to read before making changes
- D:\HCI-Final\docs\PROJECT_CONTEXT.md — full project state, file structure, API contract
- D:\HCI-Final\docs\CMTA_DATA.md — all real CMTA route/station/fare data with sources
- D:\HCI-Final\docs\DESIGN_SYSTEM.md — color palette, fonts, Tailwind tokens
- D:\HCI-Final\docs\STITCH_DESIGN.md — Stitch design tokens (baseline for all pages)

## Design system (critical — must match on any new code)
- Framework: Tailwind CDN (no build step)
- Primary green: #006B3C / Tailwind: primary-mid
- CTA orange: #D4500A / Tailwind: orange-line
- Body font: Source Sans 3 (min 20px)
- Heading font: Source Serif 4
- Urdu font: Noto Nastaliq Urdu
- Border radius: rounded-card (16px), rounded-btn (12px)
- Min touch target: 56px (elderly users)
- Icons: Material Symbols Outlined (Google Fonts CDN)
- Every page must include: /static/shared.css + /static/shared.js

## API base URL
http://localhost:8000  (backend must be running)

## .env location
D:\HCI-Final\backend\.env  (has real OpenRouter key — do not overwrite)
