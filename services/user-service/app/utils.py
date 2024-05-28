from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_token(username):
    return create_access_token(identity=username)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['JWT_SECRET'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['JWT_SECRET'], max_age=expiration)
    except:
        return False
    return email
