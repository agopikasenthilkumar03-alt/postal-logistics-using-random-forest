from datetime import datetime
import random

from app.schemas.weather import WeatherCreate


def fetch_weather_for_office(post_office: str) -> WeatherCreate:
    random.seed(post_office)
    rainfall = round(random.uniform(0, 30), 2)
    wind_speed = round(random.uniform(5, 40), 2)
    temperature = round(random.uniform(18, 38), 2)
    flood_risk_level = "High" if rainfall > 20 else "Medium" if rainfall > 10 else "Low"
    return WeatherCreate(
        post_office=post_office,
        captured_at=datetime.utcnow(),
        rainfall_intensity=rainfall,
        wind_speed=wind_speed,
        temperature=temperature,
        flood_risk_level=flood_risk_level,
        forecast_window="forecast_24h",
    )
