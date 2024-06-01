import requests
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from app.models import MedicalRecord
from app.utils import user_exists
from datetime import datetime, timezone

records_ns = Namespace('records', description='Operations related to medical records')

contact_info_model = records_ns.model('ContactInfo', {
    'phone_number': fields.String(required=True, example='+237123456789'),
    'email': fields.String(required=True, example='johndoe@example.com'),
    'address': fields.String(required=True, example='123 Example Street, Yaounde, Cameroon')
})

emergency_contact_info_model = records_ns.model('EmergencyContactInfo', {
    'name': fields.String(required=True, example='Jane Doe'),
    'relationship': fields.String(required=True, example='Wife'),
    'phone_number': fields.String(required=True, example='+237987654321')
})

patient_info_model = records_ns.model('PatientInfo', {
    'full_name': fields.String(required=True, example='John Doe'),
    'date_of_birth': fields.String(required=True, example='1980-01-01'),
    'gender': fields.String(required=True, example='Male'),
    'national_id_number': fields.String(required=True, example='123456789'),
    'contact_info': fields.Nested(contact_info_model, required=True),
    'emergency_contact_info': fields.Nested(emergency_contact_info_model, required=True)
})

medical_history_model = records_ns.model('MedicalHistory', {
    'past_medical_history': fields.String(required=True, example='No significant past medical history.'),
    'family_medical_history': fields.String(required=True, example='Father has hypertension.'),
    'allergies': fields.String(required=True, example='No known allergies.'),
    'current_medications': fields.String(required=True, example='None'),
    'previous_surgeries_or_treatments': fields.String(required=True, example='None')
})

consultation_details_model = records_ns.model('ConsultationDetails', {
    'date_time': fields.DateTime(required=True, example='2024-06-01T10:00:00Z'),
    'reason_for_visit': fields.String(required=True, example='Routine check-up'),
    'symptoms': fields.String(required=True, example='None'),
    'diagnosis': fields.String(required=True, example='Mild hypertension'),
    'treatment_plan': fields.String(required=True, example='Prescribed Amlodipine 5mg once daily.'),
    'prescribed_medications': fields.String(required=True, example='Amlodipine 5mg')
})

record_model = records_ns.model('MedicalRecord', {
    'user_id': fields.String(required=True, description='The user identifier', example='60d0fe4f5311236168a109ca'),
    'doctor_id': fields.String(required=True, description='The doctor identifier', example='60d0fe4f5311236168a109cb'),
    'record_type': fields.String(required=True, description='Type of medical record', example='consultation'),
    'details': fields.String(required=True, description='Details of the record', example='Patient diagnosed with mild hypertension. Prescribed medication includes Amlodipine 5mg once daily.'),
    'patient_info': fields.Nested(patient_info_model, required=True),
    'medical_history': fields.Nested(medical_history_model, required=True),
    'consultation_details': fields.Nested(consultation_details_model, required=True),
    'created_at': fields.DateTime(description='Record creation time'),
    'updated_at': fields.DateTime(description='Record last updated time')
})

@records_ns.route('')
class RecordsList(Resource):
    @jwt_required()
    @records_ns.expect(record_model)
    @records_ns.response(201, 'Record created successfully')
    @records_ns.response(400, 'Invalid input')
    @records_ns.response(404, 'User does not exist')
    def post(self):
        """Create a new medical record"""
        data = request.get_json()
        current_user = get_jwt_identity()

        if not user_exists(current_user):
            return {'message': 'User does not exist'}, 404

        required_fields = ['user_id', 'doctor_id', 'record_type', 'details', 'patient_info', 'medical_history', 'consultation_details']
        for field in required_fields:
            if field not in data:
                return {'message': f'Missing field: {field}'}, 400

        record = MedicalRecord(
            user_id=data['user_id'],
            doctor_id=data['doctor_id'],
            record_type=data['record_type'],
            details=data['details'],
            patient_info=data['patient_info'],
            medical_history=data['medical_history'],
            consultation_details=data['consultation_details']
        )
        result = record.save_to_db()
        return {'message': 'Record created successfully', '_id': str(result.inserted_id)}, 201

    @jwt_required()
    @records_ns.response(200, 'Success', [record_model])
    @records_ns.response(404, 'User does not exist')
    def get(self):
        """Get all medical records for the authenticated user"""
        current_user = get_jwt_identity()
        if not user_exists(current_user):
            return {'message': 'User does not exist'}, 404

        user_id = request.args.get('user_id')
        if user_id:
            records = MedicalRecord.find_by_user(user_id)
        else:
            records = list(MedicalRecord.find({}))
        for record in records:
            record['_id'] = str(record['_id'])
            if 'user_id' in record:
                record['user_id'] = str(record['user_id'])
            if 'doctor_id' in record:
                record['doctor_id'] = str(record['doctor_id'])
        return jsonify(records)

@records_ns.route('/<record_id>')
class Record(Resource):
    @jwt_required()
    @records_ns.response(200, 'Success', record_model)
    @records_ns.response(404, 'Record not found')
    def get(self, record_id):
        """Get a specific medical record by ID"""
        if not user_exists(get_jwt_identity()):
            return {'message': 'User does not exist'}, 404

        record = MedicalRecord.find_by_id(record_id)
        if not record:
            return {'message': 'Record not found'}, 404

        record['_id'] = str(record['_id'])
        return jsonify(record)

    @jwt_required()
    @records_ns.expect(record_model)
    @records_ns.response(200, 'Record updated successfully')
    @records_ns.response(404, 'User does not exist')
    def put(self, record_id):
        """Update a specific medical record by ID"""
        if not user_exists(get_jwt_identity()):
            return {'message': 'User does not exist'}, 404

        data = request.get_json()
        MedicalRecord.update_record(record_id, data)
        return {'message': 'Record updated successfully'}, 200

    @jwt_required()
    @records_ns.response(200, 'Record deleted successfully')
    @records_ns.response(404, 'User does not exist')
    def delete(self, record_id):
        """Delete a specific medical record by ID"""
        if not user_exists(get_jwt_identity()):
            return {'message': 'User does not exist'}, 404

        MedicalRecord.delete_record(record_id)
        return {'message': 'Record deleted successfully'}, 200
