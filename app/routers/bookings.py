from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.booking import Booking
from app.models.booking_item import BookingItem
from app.models.ticket_type import TicketType
from app.models.user import User

from app.schemas.booking import BookingCreate, BookingResponse
from app.routers.users import get_current_user


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


# CREATE BOOKING
@router.post("/", response_model=BookingResponse)
def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_booking = Booking(
        user_id=current_user.id,
        total_amount=booking_data.total_amount,
        status="PENDING"
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


# GET MY BOOKINGS
@router.get("/my-bookings", response_model=list[BookingResponse])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).all()

    return bookings


# CANCEL BOOKING
@router.patch("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).with_for_update().first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if booking.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Only pending bookings can be cancelled"
        )

    items = db.query(BookingItem).filter(
        BookingItem.booking_id == booking_id
    ).all()

    try:
        for item in items:
            ticket_type = db.query(TicketType).filter(
                TicketType.id == item.ticket_type_id
            ).with_for_update().first()

            if ticket_type:
                ticket_type.available_quantity += item.quantity

        booking.status = "CANCELLED"

        db.commit()
        db.refresh(booking)

        return {
            "message": "Booking cancelled successfully",
            "booking_id": booking.id,
            "status": booking.status
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to cancel booking"
        )