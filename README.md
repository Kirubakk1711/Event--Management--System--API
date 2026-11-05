Event Management System API

Project Overview

The Event Management System API is a backend application developed using Python, FastAPI, and MySQL.

It provides a complete backend solution for managing users, events, ticket types, bookings, payments, and notifications.

The application includes secure authentication, role-based authorization, booking management, ticket availability validation, and administrative reporting.

Technologies Used

- Python
- FastAPI
- MySQL
- SQLAlchemy ORM
- Pydantic
- JWT Authentication
- Swagger UI
- Postman
- Git and GitHub

Key Features

1. User Management

- User registration
- User login
- JWT-based authentication
- Secure password handling

2. Role-Based Access Control

- Admin
- Organizer
- Customer
- Role-based API authorization

3. Event Management

- Create events
- View event details
- Update events
- Delete events
- Search and filter events
- Sorting and pagination

4. Ticket Management

- Create and manage ticket types
- Set ticket prices
- Manage ticket quantities
- Track available ticket inventory
- Activate and deactivate ticket types

5. Booking Management

- Create bookings
- View booking history
- Add booking items
- Calculate booking totals
- Cancel pending bookings
- Restore ticket availability after cancellation

6. Payment Management

- Simulated payment processing
- Payment status management
- Booking payment validation
- Payment history

7. Notification Management

- Generate notifications
- View notifications
- Mark notifications as read

8. Admin Dashboard

- View dashboard statistics
- Monitor users and events
- View booking reports
- Track successful payments and revenue

User Roles

Role| Permissions
Admin| Manage and monitor the system
Organizer| Manage events and related activities
Customer| Browse events, book tickets, and manage bookings

Database

Database Name: "event_management_db"

The application uses MySQL with SQLAlchemy ORM.

Main database tables include:

- Users
- Events
- Ticket Types
- Tickets
- Bookings
- Booking Items
- Payments
- Notifications

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
│   └── Event Management API.postman_collection.json
│
├── tests/
│
├── .env
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

For Windows:

venv\Scripts\activate

5. Install Dependencies

pip install -r requirement.txt

Database Configuration

1. Open MySQL Workbench.
2. Create the database:

CREATE DATABASE event_management_db;

3. Configure your database connection details in the ".env" file.

Example:

DATABASE_URL=mysql+pymysql://username:password@localhost/event_management_db

Replace "username" and "password" with your own MySQL credentials.

Do not upload your actual ".env" file or database credentials to GitHub.

Run the Application

Start the FastAPI server using:

uvicorn app.main:app --reload

The application will run at:

http://127.0.0.1:8000

API Documentation

FastAPI provides interactive API documentation through Swagger UI.

Open the following URL in your browser:

http://127.0.0.1:8000/docs

Swagger UI allows users to explore and test the available API endpoints.

Postman API Testing

The project includes a Postman collection for API testing.

- Collection Name: Event Management API
- Collection Format: Postman Collection v2.1
- Collection File: "postman/Event Management API.postman_collection.json"

Import Postman Collection

1. Open Postman.
2. Select Import.
3. Choose the exported JSON collection file.
4. Import the collection.
5. Run the API requests to test the endpoints.

The collection includes requests for user login, ticket booking, booking history, payments, notifications, admin dashboard, booking reports, and event management.

Business Validations

The application implements important business validations, including:

- Authentication and authorization checks.
- Role-based access restrictions.
- Ticket availability validation.
- Prevention of ticket overselling.
- Booking ownership validation.
- Cancellation restricted to pending bookings.
- Ticket quantity restoration after cancellation.
- Payment restrictions for cancelled bookings.

Payment Information

This project uses simulated payment processing for demonstration and testing purposes. It does not process real financial transactions.

Testing

The APIs were tested using:

- Swagger UI
- Postman

Testing includes successful API requests, authentication, role-based access, booking operations, ticket availability validation, payment processing, and notification management.

Version Control

Git and GitHub are used for source code management and project version control.

GitHub Repository:

https://github.com/Kirubakk1711/Event--Management--System--API

Author

Kirubasri S

Python Developer

Event Management System API – Backend Development Project