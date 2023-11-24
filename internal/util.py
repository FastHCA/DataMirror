import os
import re

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
    def check_type(input_str):
        try:
            dsn = _parse_url(input_str)
            return "DSN"
        except ArgumentError as e:
            pass

        if os.path.isdir(input_str):
            return "FILE"

        return "UNKNOWN"

    @staticmethod
    def extract_db_name(connection_string):
        return connection_string.split("://")[0]
