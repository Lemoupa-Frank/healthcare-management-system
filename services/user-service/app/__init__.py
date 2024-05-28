from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes import auth
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt = JWTManager(app)

    app.register_blueprint(auth, url_prefix='/api/auth')

    return app
