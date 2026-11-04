from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TicketCreate(BaseModel):
    event_id: int
    quantity: int = Field(gt=0)


class TicketResponse(BaseModel):
    id: int
    event_id: int
    user_id: int
    quantity: int
    total_amount: float
    status: str
    booked_at: datetime

    model_config = ConfigDict(from_attributes=True)