from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    amount = Column(Float, nullable=False)

    payment_method = Column(String(50), default="SIMULATED")

    transaction_id = Column(
        String(100),
        unique=True,
        nullable=False
    )

    status = Column(String(20), default="PENDING")

    paid_at = Column(DateTime, default=datetime.utcnow)