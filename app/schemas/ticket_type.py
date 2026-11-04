from pydantic import BaseModel, ConfigDict, Field


class TicketTypeCreate(BaseModel):
    event_id: int
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    total_quantity: int = Field(gt=0)


class TicketTypeResponse(BaseModel):
    id: int
    event_id: int
    name: str
    description: str | None
    price: float
    total_quantity: int
    available_quantity: int
    is_active: str

    model_config = ConfigDict(from_attributes=True)