from fastapi import FastAPI

from app.database import Base, engine
from app.models.user import User
from app.routers import users, events,tickets, payments, notifications, admin, ticket_types, bookings, booking_items
from app.routers import notifications
from app.routers import ticket_types
from app.routers import payments
from app.models.event import Event
from app.models.ticket import Ticket
from app.models.payment import Payment
from app.models.notification import Notification
from app.models.ticket_type import TicketType
from app.models.booking import Booking
from app.models.booking_item import BookingItem

app = FastAPI(
    title="Event Management System API",
    description="Backend API for event management and ticket booking",
    version="1.0.0",
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(users.router)
app.include_router(events.router)
app.include_router(tickets.router)
app.include_router(payments.router)
app.include_router(notifications.router)
app.include_router(admin.router)
app.include_router(ticket_types.router)
app.include_router(bookings.router)
app.include_router(booking_items.router)

@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Event Management System API is running successfully"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy"
    }