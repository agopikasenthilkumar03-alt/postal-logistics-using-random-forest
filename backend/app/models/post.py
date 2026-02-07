from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String(32), unique=True, nullable=False, index=True)
    source_post_office = Column(String(120), nullable=False)
    destination_post_office = Column(String(120), nullable=False)
    sender_phone = Column(String(20), nullable=False)
    receiver_phone = Column(String(20), nullable=False)
    booking_date = Column(Date, nullable=False)
    current_delivery_status = Column(String(80), nullable=False, default="Booked")

    predictions = relationship("DelayPrediction", back_populates="post")
