from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.event import Event
from app.models.user import User
from app.schemas.event import EventCreate, EventResponse
from app.dependencies.roles import require_role


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


# 1. Create Event - Admin / Organizer
@router.post("/", response_model=EventResponse)
def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "ORGANIZER")
    )
):
    new_event = Event(
        **event_data.model_dump(),
        created_by=current_user.id,
        is_active=True
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


# 2. Get All Events - Search, Filter, Sort, Pagination
@router.get("/", response_model=list[EventResponse])
def get_events(
    search: str = None,
    location: str = None,
    min_price: float = Query(None, ge=0),
    max_price: float = Query(None, ge=0),
    sort_by: str = "event_date",
    order: str = "asc",
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Event).filter(
        Event.is_active == True
    )

    # Search by title or description
    if search:
        query = query.filter(
            or_(
                Event.title.ilike(f"%{search}%"),
                Event.description.ilike(f"%{search}%")
            )
        )

    # Filter by location
    if location:
        query = query.filter(
            Event.location.ilike(f"%{location}%")
        )

    # Minimum price filter
    if min_price is not None:
        query = query.filter(
            Event.price >= min_price
        )

    # Maximum price filter
    if max_price is not None:
        query = query.filter(
            Event.price <= max_price
        )

    # Sorting
    allowed_sort_fields = {
        "event_date": Event.event_date,
        "price": Event.price,
        "title": Event.title
    }

    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    if order.lower() == "asc":
        query = query.order_by(
            allowed_sort_fields[sort_by].asc()
        )
    elif order.lower() == "desc":
        query = query.order_by(
            allowed_sort_fields[sort_by].desc()
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Order must be asc or desc"
        )

    # Pagination
    return query.offset(skip).limit(limit).all()


# 3. Get Event by ID - Public
@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(
        Event.id == event_id,
        Event.is_active == True
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


# 4. Update Event - Owner Organizer / Admin
@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_data: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "ORGANIZER")
    )
):
    event = db.query(Event).filter(
        Event.id == event_id,
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
            detail="You can only update your own events"
        )

    for key, value in event_data.model_dump().items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)

    return event


# 5. Delete Event - Owner Organizer / Admin
@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN", "ORGANIZER")
    )
):
    event = db.query(Event).filter(
        Event.id == event_id,
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
            detail="You can only delete your own events"
        )

    event.is_active = False

    db.commit()

    return {
        "message": "Event deleted successfully"
    }