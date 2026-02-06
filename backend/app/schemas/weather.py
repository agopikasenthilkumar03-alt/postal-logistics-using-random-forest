from datetime import datetime
from pydantic import BaseModel


class WeatherCreate(BaseModel):
    post_office: str
    captured_at: datetime
    rainfall_intensity: float
    wind_speed: float
    temperature: float
    flood_risk_level: str
    forecast_window: str = "current"


class WeatherRead(WeatherCreate):
    id: int

    class Config:
        orm_mode = True
