from multiprocessing import cpu_count
from os import environ


def max_workers():
    # return min(4, cpu_count() * 2 + 1)
    return 3


ENVIRONMENT_DEBUG = environ.get("APP_DEBUG")
ENVIRONMENT_PORT = environ.get("APP_PORT")
ENVIRONMENT_HOST = environ.get("APP_HOST")

bind = "{}:{}".format(ENVIRONMENT_HOST, ENVIRONMENT_PORT)
reload = ENVIRONMENT_DEBUG
max_requests = 1000
timeout = 0
worker_connections = 1000
capture_output = False

loglevel = "debug" if ENVIRONMENT_DEBUG else "info"
# Access log - records incoming HTTP requests
# accesslog = "/var/log/gunicorn.access.log"
accesslog = "-"
# Error log - records Gunicorn server goings-on
# errorlog = "/var/log/gunicorn.error.log"
errorlog = "-"
workers = max_workers()
