from flask import Flask
from app.routes import records_ns

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.register_blueprint(records_ns)
    return app
