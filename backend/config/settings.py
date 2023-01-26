from os import environ


def convert_list_object_from_string(string):
    """Convert a string to a list of objects"""
    return [] if not string else \
        list(map(lambda x: x.strip(), string.split(",")))


class Config():
    APP_API_PREFIX = environ.get("APP_API_PREFIX")
    SECRET_KEY = environ.get("SECRET_KEY")


    