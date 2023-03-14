from os import environ


def convert_list_object_from_string(string):
    """Convert a string to a list of objects"""
    return [] if not string else \
        list(map(lambda x: x.strip(), string.split(",")))


class Config():
    APP_API_PREFIX = environ.get("APP_API_PREFIX")
    SECRET_KEY = environ.get("SECRET_KEY")
    NETWORK_PATH = environ.get("NETWORK_PATH")
    IMAGE_SIZE = int(environ.get("IMAGE_SIZE"))
    # DATASET_PATH = environ.get("DATASET_PATH")
    # FEATURE_PATH = environ.get("FEATURE_PATH")
    VEC_MAP_PATH = environ.get("VEC_MAP_PATH")
    QUERY_PATH = environ.get("QUERY_PATH")
    IMAGEFILE_PATH=environ.get("IMAGEFILE_PATH")
    NUM_IMAGE= int(environ.get("NUM_IMAGE"))