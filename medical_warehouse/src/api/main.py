from fastapi import FastAPI
from src.api.routers import health, analytics

app = FastAPI(
    title="Medical Telegram Analytics API",
    description="Analytics platform for Ethiopian medical Telegram channels",
    version="1.0.0"
)

app.include_router(health.router)
app.include_router(analytics.router, prefix="/analytics")
