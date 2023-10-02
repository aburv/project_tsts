import unittest
from unittest import mock

from flask import Flask

from src.logger import LoggerAPI
from src.responses import ValidResponse, SecurityException, SchemaNotFoundException, DBConnectionException


class ExceptionTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    def test_should_return_the_valid_response_with_context(self,
                                                           mock_log_init,
                                                           mock_info_entry):
        expected = b'{"data":"content"}\n'

        with self.app.app_context():
            actual = ValidResponse('message', 'content', detail='details').get_response_json()

            mock_info_entry.assert_called_once_with("Success message details : content")
            self.assertEqual(expected, actual.data)
            self.assertEqual(200, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    def test_should_return_the_auth_exception_with_context(self,
                                                           mock_log_init,
                                                           mock_error_entry):
        expected = b'{"error":{"detail":"content","message":"message","type":"SecurityException"}}\n'

        with self.app.app_context():
            actual = SecurityException('message', 'content').get_response_json()

            mock_error_entry.assert_called_once_with("401 SecurityException message : content")
            self.assertEqual(expected, actual.data)
            self.assertEqual(401, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    def test_should_return_the_schema_not_found_exception_with_context(self,
                                                           mock_log_init,
                                                           mock_error_entry):
        expected = b'{"error":{"detail":"","message":"table","type":"SchemaNotFoundException"}}\n'

        with self.app.app_context():
            actual = SchemaNotFoundException('table').get_response_json()

            mock_error_entry.assert_called_once_with("0 SchemaNotFoundException table : ")
            self.assertEqual(expected, actual.data)
            self.assertEqual(0, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    @mock.patch.object(LoggerAPI, '__init__', return_value=None)
    def test_should_return_the_db_connection_exception_with_context(self,
                                                           mock_log_init,
                                                           mock_error_entry):
        expected = b'{"error":{"detail":"","message":"message","type":"DBConnectionException"}}\n'

        with self.app.app_context():
            actual = DBConnectionException('message').get_response_json()

            mock_error_entry.assert_called_once_with("0 DBConnectionException message : ")
            self.assertEqual(expected, actual.data)
            self.assertEqual(0, actual.status_code)
