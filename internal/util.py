import os

from sqlalchemy.engine.url import _parse_url
from sqlalchemy.exc import ArgumentError


class Util:
    @staticmethod
    def remove_trailing_slash(directory):
        if directory.endswith('/'):
            return directory[:-1]
        return directory

    @staticmethod
    def create_directory_if_not_exists(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def get_driver_name(input_str):
        try:
            dsn = _parse_url(input_str)
            return dsn.drivername
        except ArgumentError as e:
            pass

        return "file"
