from app.config import Config
from app.db import DB
from app.apis.players import players_ns
from http import HTTPStatus
from flask import Flask
from flask_restx import Api
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    DB.init_app(app)

    api = Api(
        title="Player Analysis",
        version="1.0",
        description="FM26 player tracker",
    )

    api.init_app(app)

  
    api.add_namespace(players_ns, path="/players")

    @api.errorhandler(Exception)
    def handle_input_validation_error(error):
        return {"message": str(error)}, HTTPStatus.INTERNAL_SERVER_ERROR

    return app
