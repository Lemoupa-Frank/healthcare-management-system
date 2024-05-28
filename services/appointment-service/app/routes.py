from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Appointment
from datetime import datetime

appointments = Blueprint('appointments', __name__)

@appointments.route('', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    current_user = get_jwt_identity()
    doctor = data.get('doctor')
    date_time_str = data.get('date_time')
    
    try:
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Invalid date format'}), 400

    appointment = Appointment(current_user, doctor, date_time)
    appointment.save_to_db()
    return jsonify({'message': 'Appointment created successfully'}), 201

@appointments.route('/<appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    appointment = Appointment.find_by_id(appointment_id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404

    appointment['_id'] = str(appointment['_id'])
    return jsonify(appointment), 200

@appointments.route('', methods=['GET'])
@jwt_required()
def get_user_appointments():
    current_user = get_jwt_identity()
    appointments = Appointment.find_by_user(current_user)
    for appointment in appointments:
        appointment['_id'] = str(appointment['_id'])
    return jsonify(appointments), 200

@appointments.route('/<appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    data = request.get_json()
    update_fields = {}
    
    if 'doctor' in data:
        update_fields['doctor'] = data['doctor']
    if 'date_time' in data:
        try:
            update_fields['date_time'] = datetime.strptime(data['date_time'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'message': 'Invalid date format'}), 400
    if 'status' in data:
        update_fields['status'] = data['status']
    
    Appointment.update_appointment(appointment_id, update_fields)
    return jsonify({'message': 'Appointment updated successfully'}), 200

@appointments.route('/<appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    Appointment.delete_appointment(appointment_id)
    return jsonify({'message': 'Appointment deleted successfully'}), 200
