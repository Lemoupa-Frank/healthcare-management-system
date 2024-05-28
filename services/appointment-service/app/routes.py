import requests
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Appointment
from datetime import datetime

appointments = Blueprint('appointments', __name__)

def user_exists(username):
    user_service_url = current_app.config['USER_SERVICE_URL']
    response = requests.get(f"{user_service_url}/api/auth/user/{username}")
    return response.status_code == 200

@appointments.route('', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    current_user = get_jwt_identity()
    doctor = data.get('doctor')
    date_time_str = data.get('date_time')
    slot = data.get('slot')
    email = data.get('email')
    phone = data.get('phone')
    reminder_method = data.get('reminder_method', 'email')

    if not user_exists(current_user):
        return jsonify({'message': 'User does not exist'}), 404

    try:
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Invalid date format'}), 400

    if Appointment.find_by_doctor_and_slot(doctor, date_time, slot):
        return jsonify({'message': 'Doctor already booked for this slot'}), 409

    appointment = Appointment(current_user, doctor, date_time, slot, email=email, phone=phone, reminder_method=reminder_method)
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
    if 'slot' in data:
        existing_appointment = Appointment.find_by_id(appointment_id)
        if existing_appointment and (existing_appointment['doctor'] != data['doctor'] or existing_appointment['slot'] != data['slot']):
            if Appointment.find_by_doctor_and_slot(update_fields.get('doctor', existing_appointment['doctor']), update_fields.get('date_time', existing_appointment['date_time']), data['slot']):
                return jsonify({'message': 'Doctor already booked for this slot'}), 409
        update_fields['slot'] = data['slot']
    if 'status' in data:
        update_fields['status'] = data['status']
    if 'email' in data:
        update_fields['email'] = data['email']
    if 'phone' in data:
        update_fields['phone'] = data['phone']
    if 'reminder_method' in data:
        update_fields['reminder_method'] = data['reminder_method']
    
    Appointment.update_appointment(appointment_id, update_fields)
    return jsonify({'message': 'Appointment updated successfully'}), 200

@appointments.route('/<appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    Appointment.delete_appointment(appointment_id)
    return jsonify({'message': 'Appointment deleted successfully'}), 200
