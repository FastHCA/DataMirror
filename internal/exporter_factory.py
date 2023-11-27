from .util import Util
from internal import constants
from internal.file.exporter import FileExporter
from internal.postgresql.exporter import PostgreSQLExporter


class ExporterFactory:
    @staticmethod
    def create_exporter(source):
        driver_name = Util.get_driver_name(source)
        print(f'INFO: source driver is {driver_name}')
        if driver_name == constants.FILE_TYPE:
            return FileExporter(source)
        elif driver_name == constants.DRIVER_POSTGRESQL:
            return PostgreSQLExporter(source)
        else:
            raise ValueError(f'unsupported source driver {driver_name}')
