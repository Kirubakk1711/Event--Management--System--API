from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.user import User
from app.models.event import Event
from app.models.ticket import Ticket
from app.models.payment import Payment
from app.dependencies.roles import require_role


router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"]
)


# 1. Admin Dashboard Summary
@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN")
    )
):
    total_users = db.query(User).count()

    total_events = db.query(Event).filter(
        Event.is_active == True
    ).count()

    total_bookings = db.query(Ticket).count()

    total_payments = db.query(Payment).filter(
        func.upper(Payment.status) == "SUCCESS"
    ).count()

    total_revenue = db.query(
        func.coalesce(func.sum(Payment.amount), 0)
    ).filter(
        func.upper(Payment.status) == "SUCCESS"
    ).scalar()

    return {
        "total_users": total_users,
        "total_events": total_events,
        "total_bookings": total_bookings,
        "total_successful_payments": total_payments,
        "total_revenue": float(total_revenue)
    }


# 2. Booking Status Report
@router.get("/booking-report")
def booking_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("ADMIN")
    )
):
    results = db.query(
        Ticket.status,
        func.count(Ticket.id).label("total")
    ).group_by(
        Ticket.status
    ).all()

    return {
        "booking_report": [
            {
                "status": status,
                "total": total
            }
            for status, total in results
        ]
    }