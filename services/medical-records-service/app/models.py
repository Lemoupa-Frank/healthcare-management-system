from pymongo import MongoClient
from bson import ObjectId
from flask import current_app, g
from flask_pymongo import PyMongo
from datetime import datetime, timezone

client = MongoClient('mongodb://localhost:27017/')
db = client.medical_records_service

class MedicalRecord:
    @staticmethod
    def find_by_id(record_id):
        return db.medical_records.find_one({'_id': ObjectId(record_id)})

    @staticmethod
    def find_by_user(user_id):
        return list(db.medical_records.find({'user_id': ObjectId(user_id)}))

    def __init__(self, user_id, doctor_id, record_type, details, patient_info, medical_history, consultation_details, created_at=None, updated_at=None):
        self.user_id = user_id
        self.doctor_id = doctor_id
        self.record_type = record_type
        self.details = details
        self.patient_info = patient_info
        self.medical_history = medical_history
        self.consultation_details = consultation_details
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def save_to_db(self):
        self.created_at = datetime.now(timezone.utc)
        return db.medical_records.insert_one(self.__dict__)

    @staticmethod
    def update_record(record_id, update_fields):
        update_fields['updated_at'] = datetime.now(timezone.utc)
        db.medical_records.update_one({'_id': ObjectId(record_id)}, {'$set': update_fields})

    @staticmethod
    def delete_record(record_id):
        db.medical_records.delete_one({'_id': ObjectId(record_id)})

    @staticmethod
    def find(criteria):
        return db.medical_records.find(criteria)

def get_db():
    if 'mongo' not in g:
        g.mongo = PyMongo(current_app)
    return g.mongo.db
