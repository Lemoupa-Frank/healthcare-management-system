from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes import appointments
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt = JWTManager(app)

    app.register_blueprint(appointments, url_prefix='/api/appointments')

    return app
