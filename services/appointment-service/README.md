
# Appointment Service User Manual

## 1. Introduction

The Appointment Service is a microservice designed to manage appointments in a healthcare system. It allows users to book, update, cancel, and view appointments with doctors. The service also includes features like appointment reminders via email and SMS.

## 2. System Requirements

- Python 3.8+
- MongoDB
- Flask
- Twilio account for SMS notifications (optional)

## 3. Installation

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/your-repo/healthcare-management-system.git
   cd healthcare-management-system/services/appointment-service
   ```

2. **Create a Virtual Environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # For Unix
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## 4. Configuration

### Environment Variables

Create a `.env` file in the root of the `appointment-service` directory with the following content:

```plaintext
SECRET_KEY=your_secret_key
MONGO_URI=mongodb://localhost:27017/appointment_service
JWT_SECRET_KEY=your_jwt_secret_key
USER_SERVICE_URL=http://localhost:5000

EMAIL_ADDRESS=your_email_address@gmail.com
EMAIL_PASSWORD=your_email_password

TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

### Configuration File

Ensure the `config.py` file loads these variables:

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/appointment_service')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5000')
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
```

## 5. Running the Service

1. **Start MongoDB**: Ensure MongoDB is running on your machine.

2. **Run the Application**:
   ```sh
   python run.py
   ```

3. **Access the Service**: The service will be available at `http://localhost:5001`.

## 6. API Endpoints

### User Endpoints

1. **Create Appointment**: `POST /api/appointments`
   - Request Body:
     ```json
     {
       "doctor": "doctor_id",
       "date_time": "YYYY-MM-DD HH:MM:SS",
       "slot": "slot_id",
       "email": "user@example.com",
       "phone": "+1234567890",
       "reminder_method": "email" // or "sms"
     }
     ```
   - Response:
     ```json
     {
       "message": "Appointment created successfully"
     }
     ```

2. **Get Appointment**: `GET /api/appointments/<appointment_id>`
   - Response:
     ```json
     {
       "_id": "appointment_id",
       "username": "username",
       "doctor": "doctor_id",
       "date_time": "YYYY-MM-DD HH:MM:SS",
       "slot": "slot_id",
       "status": "scheduled",
       "email": "user@example.com",
       "phone": "+1234567890",
       "reminder_method": "email"
     }
     ```

3. **Get User Appointments**: `GET /api/appointments`
   - Response:
     ```json
     [
       {
         "_id": "appointment_id",
         "username": "username",
         "doctor": "doctor_id",
         "date_time": "YYYY-MM-DD HH:MM:SS",
         "slot": "slot_id",
         "status": "scheduled",
         "email": "user@example.com",
         "phone": "+1234567890",
         "reminder_method": "email"
       },
       ...
     ]
     ```

4. **Update Appointment**: `PUT /api/appointments/<appointment_id>`
   - Request Body:
     ```json
     {
       "doctor": "new_doctor_id",
       "date_time": "YYYY-MM-DD HH:MM:SS",
       "slot": "new_slot_id",
       "status": "rescheduled",
       "email": "new_email@example.com",
       "phone": "+1234567890",
       "reminder_method": "sms"
     }
     ```
   - Response:
     ```json
     {
       "message": "Appointment updated successfully"
     }
     ```

5. **Delete Appointment**: `DELETE /api/appointments/<appointment_id>`
   - Response:
     ```json
     {
       "message": "Appointment deleted successfully"
     }
     ```

## 7. Features

### Appointment Reminders

The service can send reminders via email and SMS. Reminders are sent 24 hours before the scheduled appointment.

### Flexible Management

Users can create, update, cancel, and view their appointments. The system prevents double-booking of doctors and allows for easy rescheduling.

### Integration with User Service

The appointment service integrates with the user service to verify user existence before creating appointments.

## 8. Scheduler

The `scheduler.py` module uses APScheduler to periodically run the `send_reminders` function every hour. This function checks for appointments scheduled within the next 24 hours and sends reminders accordingly.

#### `scheduler.py`

```python
from apscheduler.schedulers.background import BackgroundScheduler
from app.reminders import send_reminders

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_reminders, 'interval', hours=1)  # Run every hour
    scheduler.start()
```

## 9. Environment Variables

Ensure the following environment variables are set in your `.env` file:

- `SECRET_KEY`: Secret key for Flask application.
- `MONGO_URI`: MongoDB connection URI.
- `JWT_SECRET_KEY`: Secret key for JWT.
- `USER_SERVICE_URL`: URL of the user service.
- `EMAIL_ADDRESS`: Email address for sending notifications.
- `EMAIL_PASSWORD`: Password for the email address.
- `TWILIO_ACCOUNT_SID`: Twilio account SID for SMS.
- `TWILIO_AUTH_TOKEN`: Twilio auth token for SMS.
- `TWILIO_PHONE_NUMBER`: Twilio phone number for sending SMS.

## 10. Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Ensure MongoDB is running and accessible at the specified `MONGO_URI`.

2. **Environment Variables Not Loaded**:
   - Ensure the `.env` file is present in the root directory and contains all required variables.
   - Ensure `python-dotenv` is installed and correctly loaded in your application.

3. **Dependency Conflicts**:
   - Ensure compatible versions of dependencies are installed as specified in `requirements.txt`.

4. **Email or SMS Not Sent**:
   - Verify email and Twilio credentials are correct and have the necessary permissions.

## Conclusion

This user manual provides a comprehensive guide to setting up, configuring, and running the appointment service. For further assistance, consult the project's documentation or seek support from the development team.
```
