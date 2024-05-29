import json
import requests_mock
from datetime import datetime

def test_create_appointment(client):
    with requests_mock.Mocker() as m:
        m.get('http://localhost:5000/api/auth/user/testuser', status_code=200)
        
        response = client.post('/api/appointments', json={
            'doctor': 'doctor_id',
            'date_time': '2024-06-01 10:00:00',
            'slot': 'slot_id',
            'email': 'user@example.com',
            'phone': '+1234567890',
            'reminder_method': 'email'
        }, headers={'Authorization': 'Bearer testtoken'})

        assert response.status_code == 201
        assert response.json == {'message': 'Appointment created successfully'}

def test_get_appointment(client):
    # Create an appointment first
    response = client.post('/api/appointments', json={
        'doctor': 'doctor_id',
        'date_time': '2024-06-01 10:00:00',
        'slot': 'slot_id',
        'email': 'user@example.com',
        'phone': '+1234567890',
        'reminder_method': 'email'
    }, headers={'Authorization': 'Bearer testtoken'})

    appointment_id = response.json['_id']

    # Get the appointment
    response = client.get(f'/api/appointments/{appointment_id}', headers={'Authorization': 'Bearer testtoken'})

    assert response.status_code == 200
    appointment = response.json
    assert appointment['doctor'] == 'doctor_id'
    assert appointment['date_time'] == '2024-06-01 10:00:00'

def test_update_appointment(client):
    # Create an appointment first
    response = client.post('/api/appointments', json={
        'doctor': 'doctor_id',
        'date_time': '2024-06-01 10:00:00',
        'slot': 'slot_id',
        'email': 'user@example.com',
        'phone': '+1234567890',
        'reminder_method': 'email'
    }, headers={'Authorization': 'Bearer testtoken'})

    appointment_id = response.json['_id']

    # Update the appointment
    response = client.put(f'/api/appointments/{appointment_id}', json={
        'doctor': 'new_doctor_id',
        'date_time': '2024-06-01 11:00:00',
        'slot': 'new_slot_id',
        'status': 'rescheduled',
        'email': 'new_email@example.com',
        'phone': '+1234567890',
        'reminder_method': 'sms'
    }, headers={'Authorization': 'Bearer testtoken'})

    assert response.status_code == 200
    assert response.json == {'message': 'Appointment updated successfully'}

def test_delete_appointment(client):
    # Create an appointment first
    response = client.post('/api/appointments', json={
        'doctor': 'doctor_id',
        'date_time': '2024-06-01 10:00:00',
        'slot': 'slot_id',
        'email': 'user@example.com',
        'phone': '+1234567890',
        'reminder_method': 'email'
    }, headers={'Authorization': 'Bearer testtoken'})

    appointment_id = response.json['_id']

    # Delete the appointment
    response = client.delete(f'/api/appointments/{appointment_id}', headers={'Authorization': 'Bearer testtoken'})

    assert response.status_code == 200
    assert response.json == {'message': 'Appointment deleted successfully'}
