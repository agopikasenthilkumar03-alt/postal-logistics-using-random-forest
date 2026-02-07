from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import ROLE_ADMIN, ROLE_STAFF, require_role
from app.db.session import get_db
from app.models.weather import WeatherSnapshot
from app.schemas.weather import WeatherCreate, WeatherRead
from app.services.weather_service import fetch_weather_for_office

router = APIRouter(prefix="/weather", tags=["weather"])


@router.post("/fetch", response_model=WeatherRead, dependencies=[Depends(require_role({ROLE_ADMIN, ROLE_STAFF}))])
def fetch_weather(post_office: str, db: Session = Depends(get_db)):
    weather_payload = fetch_weather_for_office(post_office)
    weather = WeatherSnapshot(**weather_payload.dict())
    db.add(weather)
    db.commit()
    db.refresh(weather)
    return weather


@router.post("", response_model=WeatherRead, dependencies=[Depends(require_role({ROLE_ADMIN, ROLE_STAFF}))])
def create_weather(payload: WeatherCreate, db: Session = Depends(get_db)):
    weather = WeatherSnapshot(**payload.dict())
    db.add(weather)
    db.commit()
    db.refresh(weather)
    return weather


@router.get("", response_model=list[WeatherRead], dependencies=[Depends(require_role({ROLE_ADMIN, ROLE_STAFF}))])
def list_weather(db: Session = Depends(get_db)):
    return db.query(WeatherSnapshot).all()
