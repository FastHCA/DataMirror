from .util import Util
from internal import constants
from internal.file.exporter import FileExporter
from internal.postgresql.exporter import PostgreSQLExporter

class ExporterFactory:
    @staticmethod
    def create_exporter(source):
        source_type = Util.check_type(source)
        print(f'INFO: source type is {source_type}')
        if source_type == constants.FILE_TYPE:
            return FileExporter(source)
        elif source_type == constants.DSN_TYPE:
            db_name = Util.extract_db_name(source)
            print(f'INFO: source database type is {db_name}')
            if db_name == constants.DATABASE_POSTGRESQL:
                return PostgreSQLExporter(source)
            else:
                raise ValueError("source connection type unsupported")
        else:
            raise ValueError("Invalid source type")
