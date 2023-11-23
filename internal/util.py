import os
import re

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
        if re.match(r'^(/[^/ ]*)+/?$', input_str):
            return "FILE"
        elif re.match(r'^[a-zA-Z]+://', input_str):
            return "DSN"
        else:
            return "UNKNOWN"

    @staticmethod
    def extract_db_name(connection_string):
        return connection_string.split("://")[0]
