Event Management System API

Project Overview

The Event Management System API is a backend application developed using Python, FastAPI, and MySQL. It provides RESTful APIs to manage users, events, ticket types, bookings, payments, and notifications.

The system supports role-based access control and secure authentication using JWT.

Technologies Used

- Python
- FastAPI
- MySQL
- SQLAlchemy ORM
- Pydantic
- JWT Authentication
- Passlib Password Hashing
- Swagger UI
- Postman
- Git and GitHub

Main Features

1. User Registration and Login
2. JWT Authentication and Role-Based Authorization
3. Event Management (CRUD Operations)
4. Event Search, Filtering, Sorting, and Pagination
5. Ticket Type Management
6. Ticket Booking and Booking History
7. Booking Item Management
8. Stock Validation and Overselling Prevention
9. Booking Cancellation and Stock Restoration
10. Simulated Payment Processing
11. Payment History
12. User Notifications
13. Admin Dashboard and Reports

User Roles

- Admin: Manages the system and views dashboard reports.
- Organizer: Creates and manages events.
- Customer: Searches events and books tickets.

Project Structure

Event_Management_API/
│
├── app/
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── dependencies/
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── postman/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

Installation and Setup

1. Clone the Repository

git clone https://github.com/Kirubakk1711/Event--Management--System--API.git

2. Navigate to the Project Folder

cd Event--Management--System--API

3. Create a Virtual Environment

python -m venv venv

4. Activate the Virtual Environment

Windows:

venv\Scripts\activate

5. Install Dependencies

pip install -r requirements.txt

Database Configuration

Create a MySQL database:

CREATE DATABASE event_management_db;

Configure your database URL and JWT secret key in the ".env" file.

Use ".env.example" as a reference for the required environment variables.

Do not upload your actual ".env" file or secret keys to GitHub.

Run the Application

Start the FastAPI development server:

uvicorn app.main:app --reload

API Documentation

After starting the server, access:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Authentication

The API uses JWT Bearer Token authentication.

1. Register a user.
2. Log in to obtain an access token.
3. Click the Authorize button in Swagger UI.
4. Enter the access token to access protected endpoints.

API Modules

Module| Description
Users| Registration, login, authentication
Events| Event CRUD and search
Ticket Types| Ticket category and inventory
Bookings| Booking creation and history
Booking Items| Ticket quantity and stock validation
Payments| Simulated payment processing
Notifications| User notifications
Admin| Dashboard and booking reports

Business Validations

- Only authorized users can access protected endpoints.
- Customers cannot create or manage organizer events.
- Ticket quantities must be available before booking.
- Overselling is prevented through stock validation.
- Cancelled bookings cannot be paid.
- Booking cancellation restores ticket availability.
- Only pending bookings can be cancelled.

Payment Information

The payment module uses simulated payment processing. No real money is transferred.

Testing

API endpoints are tested using:

- Swagger UI
- Postman

Version Control

The project source code is maintained using Git and GitHub.

Author

Kirubasri S
Python Developer