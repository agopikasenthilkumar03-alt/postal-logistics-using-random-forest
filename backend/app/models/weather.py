from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class WeatherSnapshot(Base):
    __tablename__ = "weather_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    post_office = Column(String(120), nullable=False, index=True)
    captured_at = Column(DateTime, nullable=False)
    rainfall_intensity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    flood_risk_level = Column(String(20), nullable=False)
    forecast_window = Column(String(40), nullable=False, default="current")

    predictions = relationship("DelayPrediction", back_populates="weather_snapshot")
