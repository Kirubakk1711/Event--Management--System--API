import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.payment import Payment
from app.models.booking import Booking
from app.models.user import User
from app.models.notification import Notification
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.routers.users import get_current_user


router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# 1. Make Simulated Payment
@router.post("/pay", response_model=PaymentResponse)
def make_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    booking = db.query(Booking).filter(
        Booking.id == payment_data.booking_id,
        Booking.user_id == current_user.id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.status == "CANCELLED":
        raise HTTPException(
            status_code=400,
            detail="Cannot pay for a cancelled booking"
        )

    if booking.status == "CONFIRMED":
        raise HTTPException(
            status_code=400,
            detail="This booking is already paid"
        )

    payment = Payment(
        booking_id=booking.id,
        user_id=current_user.id,
        amount=booking.total_amount,
        payment_method=payment_data.payment_method,
        transaction_id=str(uuid.uuid4()),
        status="SUCCESS"
    )

    notification = Notification(
        user_id=current_user.id,
        message=f"Your payment of Rs. {booking.total_amount} was successful."
    )

    try:
        db.add(payment)
        booking.status = "CONFIRMED"
        db.add(notification)

        db.commit()
        db.refresh(payment)

        return payment

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Payment processing failed"
        )


# 2. Get My Payments
@router.get(
    "/my-payments",
    response_model=list[PaymentResponse]
)
def get_my_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    payments = db.query(Payment).filter(
        Payment.user_id == current_user.id
    ).all()

    return payments