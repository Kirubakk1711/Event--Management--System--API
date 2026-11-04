from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class TicketType(Base):
    __tablename__ = "ticket_types"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    name = Column(
        String(50),
        nullable=False
    )

    description = Column(String(255))

    price = Column(Float, nullable=False)

    total_quantity = Column(Integer, nullable=False)

    available_quantity = Column(Integer, nullable=False)

    is_active = Column(
        String(10),
        default="TRUE"
    )