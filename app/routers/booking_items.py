from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.booking import Booking
from app.models.booking_item import BookingItem
from app.models.ticket_type import TicketType
from app.models.user import User
from app.schemas.booking_item import (
    BookingItemCreate,
    BookingItemResponse
)
from app.routers.users import get_current_user

router = APIRouter(
    prefix="/booking-items",
    tags=["Booking Items"]
)


@router.post("/{booking_id}", response_model=BookingItemResponse)
def add_booking_item(
    booking_id: int,
    item_data: BookingItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status != "PENDING":
        raise HTTPException(
        status_code=400,
        detail="Cannot add items to a non-pending booking"
    )

    ticket_type = db.query(TicketType).filter(
        TicketType.id == item_data.ticket_type_id
    ).with_for_update().first()

    if not ticket_type:
        raise HTTPException(status_code=404, detail="Ticket type not found")
    if not ticket_type.is_active:
        raise HTTPException(
        status_code=400,
        detail="Ticket type is not active"
    )

    if item_data.quantity > ticket_type.available_quantity:
        raise HTTPException(
        status_code=400,
        detail="Not enough tickets available"
    )

    price = ticket_type.price
    subtotal = price * item_data.quantity
    ticket_type.available_quantity -= item_data.quantity

    new_item = BookingItem(
        booking_id=booking_id,
        ticket_type_id=item_data.ticket_type_id,
        quantity=item_data.quantity,
        price=price,
        subtotal=subtotal
    )

    try:
        db.add(new_item)
        booking.total_amount += subtotal
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to add booking item")