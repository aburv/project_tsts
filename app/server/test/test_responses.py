import unittest
from unittest import mock

from flask import Flask

from src.logger import LoggerAPI
from src.responses import ValidResponse, SecurityException, TableNotFoundException, DBConnectionException, \
    DBExecutionException, DataValidationException, RuntimeException


class ExceptionTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)

    @mock.patch.object(LoggerAPI, 'info_entry', return_value=None)
    def test_should_return_the_valid_response_with_context(self,
                                                           mock_info_entry):
        expected = b'{"data":"content"}\n'

        with self.app.app_context():
            actual = ValidResponse('message', 'content', detail='details').get_response_json()

            mock_info_entry.assert_called_once_with("Success message details : content")
            self.assertEqual(expected, actual.data)
            self.assertEqual(200, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    def test_should_return_the_auth_exception_with_context(self,
                                                           mock_error_entry):
        expected = b'{"error":{"message":"message","type":"SecurityException"}}\n'

        with self.app.app_context():
            actual = SecurityException('message', 'content').get_response_json()

            mock_error_entry.assert_called_once_with("401 SecurityException message : content")
            self.assertEqual(expected, actual.data)
            self.assertEqual(401, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    def test_should_return_the_runtime_exception_with_context(self,
                                                              mock_error_entry):
        expected = b'{"error":{"message":"message","type":"RuntimeException"}}\n'

        with self.app.app_context():
            actual = RuntimeException('message', 'content').get_response_json()

            mock_error_entry.assert_called_once_with("500 RuntimeException message : content")
            self.assertEqual(expected, actual.data)
            self.assertEqual(500, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    def test_should_return_the_validation_exception_with_context(self,
                                                                 mock_error_entry):
        expected = b'{"error":{"message":"message","type":"DataValidationException"}}\n'

        with self.app.app_context():
            actual = DataValidationException('message', 'content').get_response_json()

            mock_error_entry.assert_called_once_with("400 DataValidationException message : content")
            self.assertEqual(expected, actual.data)
            self.assertEqual(400, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    def test_should_return_the_table_not_found_exception_with_context(self,
                                                                      mock_error_entry):
        expected = b'{"error":{"message":"","type":"TableNotFoundException"}}\n'

        with self.app.app_context():
            actual = TableNotFoundException('table').get_response_json()

            mock_error_entry.assert_called_once_with("2 TableNotFoundException  : table")
            self.assertEqual(expected, actual.data)
            self.assertEqual(500, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    def test_should_return_the_db_connection_exception_with_context(self,
                                                                    mock_error_entry):
        expected = b'{"error":{"message":"","type":"DBConnectionException"}}\n'

        with self.app.app_context():
            actual = DBConnectionException('message').get_response_json()

            mock_error_entry.assert_called_once_with("0 DBConnectionException  : message")
            self.assertEqual(expected, actual.data)
            self.assertEqual(500, actual.status_code)

    @mock.patch.object(LoggerAPI, 'error_entry', return_value=None)
    def test_should_return_the_db_execution_exception_with_context(self,
                                                                   mock_error_entry):
        expected = b'{"error":{"message":"operation","type":"DBExecutionException"}}\n'

        with self.app.app_context():
            actual = DBExecutionException('operation', 'message').get_response_json()

            mock_error_entry.assert_called_once_with("1 DBExecutionException operation : message")
            self.assertEqual(expected, actual.data)
            self.assertEqual(500, actual.status_code)
