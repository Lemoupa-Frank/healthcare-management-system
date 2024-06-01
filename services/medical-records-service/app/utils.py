import requests
from flask import current_app

def user_exists(username):
    user_service_url = current_app.config['USER_SERVICE_URL']
    response = requests.get(f"{user_service_url}/api/auth/user/{username}")
    return response.status_code == 200
