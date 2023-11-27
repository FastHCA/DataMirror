import configparser
import json
import os
from internal import constants
from internal.util import Util
from internal.writer_abstract import WriterAbstract

class FileWriter(WriterAbstract):
    def __init__(self, target_directory):
        self.target_directory                   = Util.remove_trailing_slash(target_directory)
        self.target_table_directory             = os.path.join(self.target_directory, constants.TABLE_DIRECTORY)
        self.target_stored_procedures_directory = os.path.join(self.target_directory, constants.STORED_PROCEDURES_DIRECTORY)
        self.target_trigger_directory           = os.path.join(self.target_directory, constants.TRIGGER_DIRECTORY)
        self.target_json_data_directory         = os.path.join(self.target_directory, constants.JSON_DATA_DIRECTORY)

        Util.create_directory_if_not_exists(self.target_directory)
        Util.create_directory_if_not_exists(self.target_table_directory)
        Util.create_directory_if_not_exists(self.target_stored_procedures_directory)
        Util.create_directory_if_not_exists(self.target_trigger_directory)
        Util.create_directory_if_not_exists(self.target_json_data_directory)

    def table_writer(self, data):
        file_name = data['file_name']
        content   = data['content']
        file_path = os.path.join(self.target_table_directory, file_name)
        with open(file_path, mode='w', encoding='utf-8') as file:
            file.write(content)

    def sp_writer(self, data):
        file_name = data['file_name']
        content   = data['content']
        file_path = os.path.join(self.target_stored_procedures_directory, file_name)
        with open(file_path, mode='w', encoding='utf-8') as file:
            file.write(content)

    def trigger_writer(self, data):
        file_name = data['file_name']
        content   = data['content']
        file_path = os.path.join(self.target_trigger_directory, file_name)
        with open(file_path, mode='w', encoding='utf-8') as file:
            file.write(content)

    def data_writer(self, data):
        file_name = data['file_name']
        content   = data['content']
        file_path = os.path.join(self.target_json_data_directory, file_name)
        with open(file_path, mode='w', encoding='utf-8') as file:
            file.write(content)

    def manifest_writer(self, driver):
        file_path = os.path.join(self.target_directory, constants.MANIFEST_FILE)
        config = configparser.ConfigParser()
        config['default'] = {'driver': driver}
        with open(file_path, mode='w', encoding='utf-8') as file:
            config.write(file)

    def finish(self):
        pass
