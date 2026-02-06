from datetime import datetime
from pydantic import BaseModel


class PredictionCreate(BaseModel):
    post_id: int
    weather_snapshot_id: int
    predicted_delay: bool
    predicted_delay_days: int
    model_version: str
    created_at: datetime


class PredictionRead(PredictionCreate):
    id: int

    class Config:
        orm_mode = True


class ApprovalCreate(BaseModel):
    approved: bool
    approved_by: str
    remarks: str | None = None


class ApprovalRead(ApprovalCreate):
    id: int
    prediction_id: int
    approved_at: datetime

    class Config:
        orm_mode = True
