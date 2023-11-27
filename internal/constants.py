# const

FILE_TYPE = "file"
DRIVER_POSTGRESQL = "postgresql"

# path
TABLE_DIRECTORY             = 'table'
STORED_PROCEDURES_DIRECTORY = 'stored_procedures'
TRIGGER_DIRECTORY           = 'trigger'
JSON_DATA_DIRECTORY         = 'json_data'

# file
MANIFEST_FILE = 'manifest.mf'


class DatabaseNotFoundError(Exception):
    def __init__(self, message, database_name=None):
        super().__init__(message)
        self.database_name = database_name