import logging
from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from flask_restx import Api
from app.routes import records_ns
from app.config import Config
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    jwt = JWTManager(app)

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        logger.debug(f"Checking if token is revoked: {jwt_header}, {jwt_payload}")
        return False  # Adjust according to your token revocation logic

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        logger.debug(f"Expired token: {jwt_header}, {jwt_payload}")
        return jsonify({"message": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        logger.debug(f"Invalid token: {error}")
        return jsonify({"message": "Invalid token"}), 422

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api = Api(blueprint, doc='/docs', title='Medical Records API', version='1.0', description='A simple Medical Records API')
    app.register_blueprint(blueprint)
    
    api.add_namespace(records_ns, path='/records')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5002)
