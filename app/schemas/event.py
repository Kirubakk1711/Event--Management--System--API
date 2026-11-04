from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    event_date: datetime
    price: float = 0.0
    available_tickets: int = 0

class EventResponse(EventCreate):
    id: int
    created_by: int
    is_active: bool

    class Config:
        from_attributes = True