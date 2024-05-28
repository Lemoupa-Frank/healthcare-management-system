from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app.utils import generate_token, generate_confirmation_token, confirm_token
from app.middlewares import role_required
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from bson import ObjectId

auth = Blueprint('auth', __name__)

def convert_objectid_to_str(data):
    """ Convert ObjectId to string in a dictionary. """
    if isinstance(data, list):
        for item in data:
            if '_id' in item and isinstance(item['_id'], ObjectId):
                item['_id'] = str(item['_id'])
    elif isinstance(data, dict):
        if '_id' in data and isinstance(data['_id'], ObjectId):
            data['_id'] = str(data['_id'])
    return data

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role', 'patient')

    if User.find_by_username(username):
        return jsonify({'message': 'User already exists'}), 400

    user = User(username, password, email, phone, role)
    user.save_to_db()

    token = create_access_token(identity=username)
    return jsonify({'token': token}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user_data = User.find_by_username(username)
    if not user_data or not User.check_password(user_data['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = create_access_token(identity=username)
    return jsonify({'token': token}), 200

@auth.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user_data = User.find_by_username(current_user)
    if not user_data:
        return jsonify({'message': 'User not found'}), 404

    user_data.pop('password')
    user_data = convert_objectid_to_str(user_data)  # Convert ObjectId to string
    return jsonify(user_data), 200

@auth.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    data = request.get_json()
    current_user = get_jwt_identity()
    user_data = User.find_by_username(current_user)
    
    if not user_data:
        return jsonify({'message': 'User not found'}), 404

    client = MongoClient(current_app.config['MONGO_URI'])
    db = client.healthcare
    users = db.users

    email = data.get('email', user_data['email'])
    phone = data.get('phone', user_data['phone'])
    profile_picture = data.get('profile_picture', user_data.get('profile_picture'))

    users.update_one({'username': current_user}, {'$set': {
        'email': email,
        'phone': phone,
        'profile_picture': profile_picture
    }})

    return jsonify({'message': 'Profile updated successfully'}), 200

@auth.route('/request-reset-password', methods=['POST'])
def request_reset_password():
    data = request.get_json()
    email = data.get('email')

    user_data = User.find_by_email(email)
    if not user_data:
        return jsonify({'message': 'User not found'}), 404

    reset_token = create_access_token(identity=user_data['username'])

    # TODO: Send email with the reset token (omitted for brevity)
    
    return jsonify({'message': 'Password reset email sent'}), 200

@auth.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    try:
        username = get_jwt_identity(token)
        user_data = User.find_by_username(username)
        if not user_data:
            return jsonify({'message': 'Invalid token'}), 400

        hashed_password = generate_password_hash(new_password)
        client = MongoClient(current_app.config['MONGO_URI'])
        db = client.healthcare
        users = db.users
        users.update_one({'username': username}, {'$set': {'password': hashed_password}})

        return jsonify({'message': 'Password has been reset successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Invalid token or token has expired'}), 400

@auth.route('/send-verification-email', methods=['POST'])
def send_verification_email():
    data = request.get_json()
    email = data.get('email')

    user_data = User.find_by_email(email)
    if not user_data:
        return jsonify({'message': 'User not found'}), 404

    verification_token = generate_confirmation_token(user_data['email'])

    # TODO: Send email with the verification token (omitted for brevity)
    
    return jsonify({'message': 'Verification email sent'}), 200

@auth.route('/verify-email', methods=['GET'])
def verify_email():
    token = request.args.get('token')

    try:
        email = confirm_token(token)
        user_data = User.find_by_email(email)
        if not user_data:
            return jsonify({'message': 'Invalid token'}), 400

        client = MongoClient(current_app.config['MONGO_URI'])
        db = client.healthcare
        users = db.users
        users.update_one({'email': email}, {'$set': {'email_verified': True}})

        return jsonify({'message': 'Email has been verified successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Invalid token or token has expired'}), 400

@auth.route('/admin-only', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_only():
    return jsonify({'message': 'Welcome, admin!'}), 200

@auth.route('/setup-mfa', methods=['POST'])
@jwt_required()
def setup_mfa():
    current_user = get_jwt_identity()
    data = request.get_json()
    mfa_enabled = data.get('mfa_enabled')

    user_data = User.find_by_username(current_user)
    if not user_data:
        return jsonify({'message': 'User not found'}), 404

    client = MongoClient(current_app.config['MONGO_URI'])
    db = client.healthcare
    users = db.users
    users.update_one({'username': current_user}, {'$set': {'mfa_enabled': mfa_enabled}})

    return jsonify({'message': 'MFA setting updated successfully'}), 200
