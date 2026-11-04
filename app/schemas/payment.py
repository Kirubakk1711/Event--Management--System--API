from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PaymentCreate(BaseModel):
    booking_id: int
    payment_method: str = "SIMULATED"


class PaymentResponse(BaseModel):
    id: int
    booking_id: int | None = None 
    user_id: int
    amount: float
    payment_method: str
    transaction_id: str
    status: str
    paid_at: datetime

    model_config = ConfigDict(from_attributes=True)