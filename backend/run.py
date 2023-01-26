import logging
import os

from app import create_app


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG")
    ENVIRONMENT_PORT = os.environ.get("APP_PORT")
    ENVIRONMENT_HOST = os.environ.get("APP_HOST")
    application = create_app()
    application.run(
        host=ENVIRONMENT_HOST,
        port=ENVIRONMENT_PORT,
        debug=ENVIRONMENT_DEBUG,
    )
else:
    gunicorn_app = create_app()
    gunicorn_logger = logging.getLogger('gunicorn.error')
    gunicorn_app.logger.handlers = gunicorn_logger.handlers
    gunicorn_app.logger.setLevel(gunicorn_logger.level)
