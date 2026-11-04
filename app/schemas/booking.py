from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BookingCreate(BaseModel):
    total_amount: float


class BookingResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    booked_at: datetime

    model_config = ConfigDict(from_attributes=True)