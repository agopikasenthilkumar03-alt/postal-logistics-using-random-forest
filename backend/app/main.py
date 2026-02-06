from fastapi import FastAPI

from app.api import post, predictions, weather
from app.core.config import settings
from app.models.base import Base
from app.db.session import engine

app = FastAPI(title=settings.app_name)

app.include_router(post.router)
app.include_router(weather.router)
app.include_router(predictions.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
