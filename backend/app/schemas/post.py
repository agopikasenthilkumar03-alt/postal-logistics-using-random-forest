from datetime import date
from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    post_id: str = Field(..., max_length=32)
    source_post_office: str
    destination_post_office: str
    sender_phone: str
    receiver_phone: str
    booking_date: date
    current_delivery_status: str = "Booked"


class PostRead(PostCreate):
    id: int

    class Config:
        orm_mode = True
