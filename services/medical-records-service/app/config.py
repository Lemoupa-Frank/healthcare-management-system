import os

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-very-secret-key')
    MONGO_URI = 'mongodb://localhost:27017/medical_records_service'
    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://localhost:5000')
