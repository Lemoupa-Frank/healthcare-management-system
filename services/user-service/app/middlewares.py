from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.models import User

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user_data = User.find_by_username(current_user)
            if user_data and user_data['role'] == role:
                return func(*args, **kwargs)
            else:
                return jsonify({'message': 'Access forbidden: insufficient rights'}), 403
        return wrapper
    return decorator
