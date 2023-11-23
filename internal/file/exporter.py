import os
from internal import constants
from internal.util import Util
from internal.exporter_abstract import ExporterAbstract

class FileExporter(ExporterAbstract):
    def __init__(self, source_directory):
        self.source_directory                        = Util.remove_trailing_slash(source_directory)
        self.target_table_directory             = os.path.join(self.source_directory, constants.TABLE_DIRECTORY)
        self.target_stored_procedures_directory = os.path.join(self.source_directory, constants.STORED_PROCEDURES_DIRECTORY)
        self.target_trigger_directory           = os.path.join(self.source_directory, constants.TRIGGER_DIRECTORY)
        self.target_json_data_directory         = os.path.join(self.source_directory, constants.JSON_DATA_DIRECTORY)

    def export(self, writer):
        self.table_exporter(writer.table_writer)
        self.sp_exporter(writer.sp_writer)
        self.trigger_exporter(writer.trigger_writer)
        self.data_exporter(writer.data_writer)
        self.finish()
        writer.finish()

    def table_exporter(self, callback):
        file_list = sorted(os.listdir(self.target_table_directory))
        for file_name in file_list:
            file_path = os.path.join(self.target_table_directory, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                callback({'file_name': file_name, 'content': content})

    def sp_exporter(self, callback):
        file_list = sorted(os.listdir(self.target_stored_procedures_directory))
        for file_name in file_list:
            file_path = os.path.join(self.target_stored_procedures_directory, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                callback({'file_name': file_name, 'content': content})

    def trigger_exporter(self, callback):
        file_list = sorted(os.listdir(self.target_trigger_directory))
        for file_name in file_list:
            file_path = os.path.join(self.target_trigger_directory, file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                callback({'file_name': file_name, 'content': content})

    def data_exporter(self, callback):
        file_list = sorted(os.listdir(self.target_json_data_directory))
        for file_name in file_list:
            file_path = os.path.join(self.target_json_data_directory, file_name)
            table_name = os.path.splitext(file_name)[0][3:]
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                callback({'table_name': table_name, 'file_name': file_name, 'content': content})
                
    def finish(self):
        pass