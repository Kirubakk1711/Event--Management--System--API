from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ticket_type import TicketType
from app.models.event import Event
from app.models.user import User
from app.schemas.ticket_type import TicketTypeCreate, TicketTypeResponse
from app.dependencies.roles import require_role


router = APIRouter(
    prefix="/ticket-types",
    tags=["Ticket Types"]
)


# 1. Create Ticket Type - Admin / Organizer
@router.post("/", response_model=TicketTypeResponse)
def create_ticket_type(
    ticket_data: TicketTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "ORGANIZER")
    )
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

    if (
        current_user.role != "ADMIN"
        and event.created_by != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only manage ticket types for your own events"
        )

    new_ticket_type = TicketType(
        event_id=ticket_data.event_id,
        name=ticket_data.name,
        description=ticket_data.description,
        price=ticket_data.price,
        total_quantity=ticket_data.total_quantity,
        available_quantity=ticket_data.total_quantity,
        is_active="TRUE"
    )

    db.add(new_ticket_type)
    db.commit()
    db.refresh(new_ticket_type)

    return new_ticket_type


# 2. Get Ticket Types - Public
@router.get("/{event_id}", response_model=list[TicketTypeResponse])
def get_ticket_types(
    event_id: int,
    db: Session = Depends(get_db)
):
    return db.query(TicketType).filter(
        TicketType.event_id == event_id,
        TicketType.is_active == "TRUE"
    ).all()


# 3. Update Ticket Type - Owner Organizer / Admin
@router.put("/{ticket_type_id}", response_model=TicketTypeResponse)
def update_ticket_type(
    ticket_type_id: int,
    ticket_data: TicketTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "ORGANIZER")
    )
):
    ticket_type = db.query(TicketType).filter(
        TicketType.id == ticket_type_id,
        TicketType.is_active == "TRUE"
    ).first()

    if not ticket_type:
        raise HTTPException(
            status_code=404,
            detail="Ticket type not found"
        )

    event = db.query(Event).filter(
        Event.id == ticket_type.event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if (
        current_user.role != "ADMIN"
        and event.created_by != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only update your own event ticket types"
        )

    if ticket_data.event_id != ticket_type.event_id:
        raise HTTPException(
            status_code=400,
            detail="Ticket type cannot be moved to another event"
        )

    booked_quantity = (
        ticket_type.total_quantity - ticket_type.available_quantity
    )

    if ticket_data.total_quantity < booked_quantity:
        raise HTTPException(
            status_code=400,
            detail="Total quantity cannot be less than already booked tickets"
        )

    ticket_type.name = ticket_data.name
    ticket_type.description = ticket_data.description
    ticket_type.price = ticket_data.price
    ticket_type.total_quantity = ticket_data.total_quantity
    ticket_type.available_quantity = (
        ticket_data.total_quantity - booked_quantity
    )

    db.commit()
    db.refresh(ticket_type)

    return ticket_type


# 4. Delete Ticket Type - Owner Organizer / Admin
@router.delete("/{ticket_type_id}")
def delete_ticket_type(
    ticket_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "ORGANIZER")
    )
):
    ticket_type = db.query(TicketType).filter(
        TicketType.id == ticket_type_id,
        TicketType.is_active == "TRUE"
    ).first()

    if not ticket_type:
        raise HTTPException(
            status_code=404,
            detail="Ticket type not found"
        )

    event = db.query(Event).filter(
        Event.id == ticket_type.event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if (
        current_user.role != "ADMIN"
        and event.created_by != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own event ticket types"
        )

    if ticket_type.available_quantity != ticket_type.total_quantity:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete ticket type after tickets have been booked"
        )

    ticket_type.is_active = "FALSE"

    db.commit()

    return {
        "message": "Ticket type deleted successfully"
    }