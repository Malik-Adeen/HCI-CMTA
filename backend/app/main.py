from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os

from app.config import settings
from app.database import engine
from app import models
from app.routers import routes, fares, alerts, ai

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="API for the elderly-friendly CMTA Metro Bus redesign — HCI Final Project",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)
app.include_router(fares.router)
app.include_router(alerts.router)
app.include_router(ai.router)

# Paths
FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
)
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

# Mount static files if folder exists
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/health")
def health():
    return JSONResponse({"status": "ok", "app": settings.APP_NAME})


@app.get("/")
def serve_index():
    path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.isfile(path):
        return FileResponse(path)
    return JSONResponse({"message": "Frontend not built yet"}, status_code=200)


@app.get("/{page}.html")
def serve_page(page: str):
    path = os.path.join(FRONTEND_DIR, f"{page}.html")
    if os.path.isfile(path):
        return FileResponse(path)
    index = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.isfile(index):
        return FileResponse(index)
    return JSONResponse({"message": f"{page}.html not found"}, status_code=404)
