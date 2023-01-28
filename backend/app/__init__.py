from flask import Flask
from config import config
from flask_cors import CORS

from app.controllers.query import query_bp
from app.controllers.feature import feature_bp
from app.services import model 
def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    api_prefix = app.config["APP_API_PREFIX"]
    
    model.init_net(app)
    
    CORS(
          app, resources={
            rf"{api_prefix}/*": {
              "origins": [
                "*"
              ],
              "supports_credentials": True,
            }
          }
        )
    # Import a module / component using its blueprint handler variable
    app.register_blueprint(query_bp, url_prefix=api_prefix)
    app.register_blueprint(feature_bp, url_prefix=api_prefix)
    
    return app
