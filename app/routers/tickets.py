from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ticket import Ticket
from app.models.event import Event
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketResponse
from app.routers.users import get_current_user
from app.dependencies.roles import require_role


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


# 1. Book Ticket
@router.post("/book", response_model=TicketResponse)
def book_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("CUSTOMER"))
):
    event = db.query(Event).filter(
        Event.id == ticket_data.event_id,
        Event.is_active == True
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if ticket_data.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    if ticket_data.quantity > event.available_tickets:
        raise HTTPException(
            status_code=400,
            detail="Not enough tickets available"
        )

    total_amount = event.price * ticket_data.quantity

    new_ticket = Ticket(
        event_id=event.id,
        user_id=current_user.id,
        quantity=ticket_data.quantity,
        total_amount=total_amount,
        status="PENDING"
    )

    try:
        event.available_tickets -= ticket_data.quantity

        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)

        return new_ticket

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Ticket booking failed"
        )


# 2. Get My Bookings
@router.get("/my-bookings", response_model=list[TicketResponse])
def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("CUSTOMER"))
):
    bookings = db.query(Ticket).filter(
        Ticket.user_id == current_user.id
    ).all()

    return bookings


# 3. Cancel Ticket
@router.patch("/{ticket_id}/cancel", response_model=TicketResponse)
def cancel_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("CUSTOMER"))
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id,
        Ticket.user_id == current_user.id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if ticket.status == "CANCELLED":
        raise HTTPException(
            status_code=400,
            detail="Booking already cancelled"
        )

    event = db.query(Event).filter(
        Event.id == ticket.event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    try:
        ticket.status = "CANCELLED"
        event.available_tickets += ticket.quantity

        db.commit()
        db.refresh(ticket)

        return ticket

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Cancellation failed"
        )