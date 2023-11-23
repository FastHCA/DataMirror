import unittest
from unittest.mock import patch
import main

class TestMain(unittest.TestCase):
    def test_main(self):
        source_type = "file"
        source = "/path/to/source/directory"
        target_type = "postgres"
        target = "postgresql://user:password@localhost:5432/database"

        with patch('main.ExporterFactory.create_exporter') as mock_create_exporter, \
             patch('main.WriterFactory.create_writer') as mock_create_writer:
            exporter_mock = mock_create_exporter.return_value
            writer_mock = mock_create_writer.return_value

            main.main(source_type, source, target_type, target)

            mock_create_exporter.assert_called_once_with(source_type, source)
            mock_create_writer.assert_called_once_with(target_type, target)
            exporter_mock.export.assert_called_once_with(writer_mock)

# python -m unittest test_main.py
if __name__ == '__main__':
    unittest.main()
