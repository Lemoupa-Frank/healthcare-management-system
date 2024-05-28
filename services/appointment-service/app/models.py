from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client.appointment_service

class Appointment:
    @staticmethod
    def find_by_id(appointment_id):
        return db.appointments.find_one({'_id': ObjectId(appointment_id)})

    @staticmethod
    def find_by_user(username):
        return list(db.appointments.find({'username': username}))

    @staticmethod
    def find_by_doctor_and_slot(doctor, date_time, slot):
        return db.appointments.find_one({'doctor': doctor, 'date_time': date_time, 'slot': slot})

    def __init__(self, username, doctor, date_time, slot, status='scheduled', email=None, phone=None, reminder_method='email'):
        self.username = username
        self.doctor = doctor
        self.date_time = date_time
        self.slot = slot
        self.status = status
        self.email = email
        self.phone = phone
        self.reminder_method = reminder_method

    def save_to_db(self):
        db.appointments.insert_one(self.__dict__)

    @staticmethod
    def update_appointment(appointment_id, update_fields):
        db.appointments.update_one({'_id': ObjectId(appointment_id)}, {'$set': update_fields})

    @staticmethod
    def delete_appointment(appointment_id):
        db.appointments.delete_one({'_id': ObjectId(appointment_id)})

    @staticmethod
    def find(criteria):
        return db.appointments.find(criteria)
