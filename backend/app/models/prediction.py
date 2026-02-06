from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class DelayPrediction(Base):
    __tablename__ = "delay_predictions"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    weather_snapshot_id = Column(Integer, ForeignKey("weather_snapshots.id"), nullable=False)
    predicted_delay = Column(Boolean, nullable=False)
    predicted_delay_days = Column(Integer, nullable=False)
    model_version = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)

    post = relationship("Post", back_populates="predictions")
    weather_snapshot = relationship("WeatherSnapshot", back_populates="predictions")
    approval = relationship("AdminApproval", back_populates="prediction", uselist=False)


class AdminApproval(Base):
    __tablename__ = "admin_approvals"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("delay_predictions.id"), nullable=False)
    approved = Column(Boolean, nullable=False)
    approved_by = Column(String(80), nullable=False)
    approved_at = Column(DateTime, nullable=False)
    remarks = Column(String(255), nullable=True)

    prediction = relationship("DelayPrediction", back_populates="approval")


class SmsLog(Base):
    __tablename__ = "sms_logs"

    id = Column(Integer, primary_key=True, index=True)
    post_reference = Column(String(32), nullable=False)
    phone_number = Column(String(20), nullable=False)
    message_body = Column(String(255), nullable=False)
    sent_at = Column(DateTime, nullable=False)
    provider_reference = Column(String(120), nullable=True)
