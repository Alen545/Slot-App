# Schedule

**Schedule** is a Django-based project that helps manage interview scheduling between candidates and interviewers. It consists of two main apps: **Account** and **Booking**. The **Account** app handles user registration (candidates and interviewers), while the **Booking** app allows users to register their available time slots, avoiding overlaps and helping HR find common slots for scheduling interviews.

## Features

- **User Registration:** Register users as either candidates or interviewers via the **Account** app.
- **Time Slot Registration:** Allow users to register their available time slots through the **Booking** app.
- **Overlap Prevention:** Prevent overlapping time slots for users.
- **View All Users:** HR can view all registered users, including their roles (candidate or interviewer).
- **Find Available Slots:** Determine common available slots between a candidate and an interviewer, and send those details to their email addresses.

## Prerequisites

- Python 3.x
- Django 3.x or higher
- Django REST Framework
- SMTP configuration for sending emails

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/schedule.git
cd schedule
```
### Create and Activate a Virtual Environment

Create a virtual environment to isolate dependencies:

```bash
python -m venv venv
```
Activate the virtual environment:
- Windows:
  ```bash
  venv\Scripts\activate

- macOS and Linux:
  ```bash
  source venv/bin/activate

# Install Dependencies

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

# Run Migrations

Set up the database by running the migrations:

```bash
python manage.py migrate
```

# Configure Email Settings

Set up your email settings in settings.py for sending notifications:

```bash

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your_smtp_server'
EMAIL_PORT = your_smtp_port
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
```

# Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

# Register Users

- Register users as candidates or interviewers via the Account app.
- Log in to the Django admin to manage user roles and data.

# Usage

**Register Time Slot**

- Endpoint: POST /register-timeslot/
- Payload example

```json
{
  "user": 1,
  "date": "2024-09-15",
  "start_time": "10:00:00",
  "end_time": "12:00:00"
}
```
- Description: Registers a time slot for a user (candidate or interviewer).

# View Users

- Endpoint: GET /users/
- Description: Retrieves a list of all users, including their details.
  
# Get Available Slots

- Endpoint: GET /get-available-slots/
- Query Parameters:
- candidate_id: The ID of the candidate.
- interviewer_id: The ID of the interviewer.
- Description: Finds common available slots between the candidate and interviewer and sends an email notification.
