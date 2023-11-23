from .util import Util
from internal import constants
from internal.file.writer import FileWriter
from internal.postgresql.writer import PostgreSQLWriter

class WriterFactory:
    @staticmethod
    def create_writer(target):
        target_type = Util.check_type(target)
        print(f'INFO: target type is {target_type}')
        if target_type == constants.FILE_TYPE:
            return FileWriter(target)
        elif target_type == constants.DSN_TYPE:
            db_name = Util.extract_db_name(target)
            print(f'INFO: target database type is {db_name}')
            if db_name == constants.DATABASE_POSTGRESQL:
                return PostgreSQLWriter(target)
            else:
                raise ValueError("target connection type unsupported")
        else:
            raise ValueError("Invalid target type")