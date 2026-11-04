from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base


class BookingItem(Base):
    __tablename__ = "booking_items"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False
    )

    ticket_type_id = Column(
        Integer,
        ForeignKey("ticket_types.id"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    price = Column(Float, nullable=False)

    subtotal = Column(Float, nullable=False)