from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(100), nullable=False)

    description = Column(Text, nullable=True)

    location = Column(String(200), nullable=False)

    event_date = Column(DateTime, nullable=False)

    price = Column(Float, default=0.0)

    available_tickets = Column(Integer, default=0)

    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    is_active = Column(Boolean, default=True)