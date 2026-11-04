from pydantic import BaseModel, ConfigDict, Field


class BookingItemCreate(BaseModel):
    ticket_type_id: int
    quantity: int = Field(gt=0)


class BookingItemResponse(BaseModel):
    id: int
    booking_id: int
    ticket_type_id: int
    quantity: int
    price: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)