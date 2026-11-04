Event Management System API

Project Overview

The Event Management System API is a backend application developed using Python and FastAPI. It helps users manage events, ticket bookings, payments, and notifications.

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

Main Features

1. User Registration and Login
2. JWT Authentication and Role-Based Authorization
3. Event Management (Create, Read, Update, Delete)
4. Ticket Type Management
5. Ticket Booking and Cancellation
6. Simulated Payment Processing
7. Payment History
8. User Notifications
9. Admin Management

User Roles

- Admin
- Organizer
- Customer

Project Structure

Event_Management_API/
│
├── app/
│   ├── routers/
│   ├── schemas/
│   ├── models/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── postman/
├── tests/
├── .env
└── README.md

Installation

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

2. Navigate to the project folder

cd Event_Management_API

3. Create a virtual environment

python -m venv venv

4. Activate the virtual environment

venv\Scripts\activate

5. Install dependencies

pip install fastapi uvicorn sqlalchemy pymysql python-jose passlib[bcrypt] python-multipart

Database Configuration

Create a MySQL database named:

CREATE DATABASE event_management_db;

Configure the database connection and JWT secret key in the ".env" file.

Run the Application

uvicorn app.main:app --reload

API Documentation

After starting the server, open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Authentication

The API uses JWT Bearer Token authentication. Register and log in to obtain an access token. Use the token through the Swagger Authorize option to access protected endpoints.

Payment Information

The payment module uses simulated payment processing. No real money is transferred.

Testing

API endpoints can be tested using Swagger UI and Postman.

Author

Python Developer