from .util import Util
from internal import constants
from internal.file.writer import FileWriter
from internal.postgresql.writer import PostgreSQLWriter


class WriterFactory:
    @staticmethod
    def create_writer(target, recreate_target):
        driver_name = Util.get_driver_name(target)
        print(f'INFO: target type is {driver_name}')
        if driver_name == constants.FILE_TYPE:
            return FileWriter(target)
        elif driver_name == constants.DRIVER_POSTGRESQL:
            return PostgreSQLWriter(target, recreate_target)
        else:
            raise ValueError(f'unsupported target driver {driver_name}')
