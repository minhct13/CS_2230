from flask import Flask
from config import config
from app.controllers.query import query_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    api_prefix = app.config["APP_API_PREFIX"]
    # Import a module / component using its blueprint handler variable
    app.register_blueprint(query_bp, url_prefix=api_prefix)
    return app
