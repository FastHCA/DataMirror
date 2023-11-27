import configparser
import os
from internal import constants
from internal.util import Util
from internal.exporter_abstract import ExporterAbstract

class FileExporter(ExporterAbstract):
    def __init__(self, source_directory):
        self.source_directory                   = Util.remove_trailing_slash(source_directory)
        self.source_table_directory             = os.path.join(self.source_directory, constants.TABLE_DIRECTORY)
        self.source_stored_procedures_directory = os.path.join(self.source_directory, constants.STORED_PROCEDURES_DIRECTORY)
        self.source_trigger_directory           = os.path.join(self.source_directory, constants.TRIGGER_DIRECTORY)
        self.source_json_data_directory         = os.path.join(self.source_directory, constants.JSON_DATA_DIRECTORY)
        self.manifest_file_path                 = os.path.join(self.source_directory, constants.MANIFEST_FILE)
        self.validate()

    def validate(self):
        if not os.path.exists(self.source_directory):
            raise FileNotFoundError("Error: source director does not exist.")
        # if not os.path.exists(self.source_table_directory):
        #     raise FileNotFoundError("Error: source table director does not exist.")
        # if not os.path.exists(self.source_stored_procedures_directory):
        #     raise FileNotFoundError("Error: source stored procedures director does not exist.")
        # if not os.path.exists(self.source_trigger_directory):
        #     raise FileNotFoundError("Error: source trigger director does not exist.")
        # if not os.path.exists(self.source_json_data_directory):
        #     raise FileNotFoundError("Error: source json data director does not exist.")
        if not os.path.exists(self.manifest_file_path):
            raise FileNotFoundError("Error: manifest.mf does not exist.")

    def export(self, writer):
        self.table_exporter(writer.table_writer)
        self.sp_exporter(writer.sp_writer)
        self.trigger_exporter(writer.trigger_writer)
        self.data_exporter(writer.data_writer)
        self.manifest_exporter(writer.manifest_writer)
        self.finish()
        writer.finish()

    def table_exporter(self, callback):
        if not os.path.exists(self.source_table_directory):
            return
        file_list = sorted(os.listdir(self.source_table_directory))
        for file_name in file_list:
            file_path = os.path.join(self.source_table_directory, file_name)
            if os.path.isfile(file_path):
                with open(file_path, mode='r', encoding='utf-8') as file:
                    content = file.read()
                callback({'file_name': file_name, 'content': content})

    def sp_exporter(self, callback):
        if not os.path.exists(self.source_stored_procedures_directory):
            return
        file_list = sorted(os.listdir(self.source_stored_procedures_directory))
        for file_name in file_list:
            file_path = os.path.join(self.source_stored_procedures_directory, file_name)
            if os.path.isfile(file_path):
                with open(file_path, mode='r', encoding='utf-8') as file:
                    content = file.read()
                callback({'file_name': file_name, 'content': content})

    def trigger_exporter(self, callback):
        if not os.path.exists(self.source_trigger_directory):
            return
        file_list = sorted(os.listdir(self.source_trigger_directory))
        for file_name in file_list:
            file_path = os.path.join(self.source_trigger_directory, file_name)
            if os.path.isfile(file_path):
                with open(file_path, mode='r', encoding='utf-8') as file:
                    content = file.read()
                callback({'file_name': file_name, 'content': content})

    def data_exporter(self, callback):
        if not os.path.exists(self.source_json_data_directory):
            return
        file_list = sorted(os.listdir(self.source_json_data_directory))
        for file_name in file_list:
            file_path = os.path.join(self.source_json_data_directory, file_name)
            table_name = os.path.splitext(file_name)[0][3:]
            if os.path.isfile(file_path):
                with open(file_path, mode='r', encoding='utf-8') as file:
                    content = file.read()
                callback({'table_name': table_name, 'file_name': file_name, 'content': content})

    def manifest_exporter(self, callback):
        file_path = os.path.join(self.source_directory, 'manifest.mf')
        if os.path.isfile(file_path):
            config = configparser.ConfigParser()
            config.read(file_path)
            driver = config.get('default', 'driver')
            callback(driver)

    def finish(self):
        pass