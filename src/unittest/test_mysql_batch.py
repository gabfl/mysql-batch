import unittest
from unittest.mock import patch

import pymysql

from src import mysql_batch


class Test(unittest.TestCase):

    host = 'localhost'
    user = 'root'
    database = 'my_db'
    password = 'root'
    port = 3306

    # Sample schema
    schema_path = 'sample_table/schema.sql'

    def setUp(self):
        # Connect to the database
        connection = mysql_batch.connect(
            self.host, self.user, self.port, self.password, self.database)

        # Read sample schema
        with open(self.schema_path, 'r') as f:
            schema = f.read()

        # Apply schema for test
        with connection.cursor() as cursor:
            cursor.execute(schema)
            connection.commit()

    def test_update_batch(self):
        mysql_batch.connection = mysql_batch.connect(
            self.host, self.user, self.port, self.password, self.database)
        mysql_batch.confirmed_write = True

        self.assertTrue(mysql_batch.update_batch(
            [4, 5, 6], 'batch_test', 'date=NOW()'))

    def test_update_batch_2(self):
        mysql_batch.connection = mysql_batch.connect(
            self.host, self.user, self.port, self.password, self.database)
        mysql_batch.confirmed_write = True

        # Return should be none if there are no `ids`
        self.assertIsNone(mysql_batch.update_batch(
            [], 'batch_test', 'date=NOW()'))

    def test_update_batch_3(self):
        with unittest.mock.patch('builtins.input', return_value='no'):
            mysql_batch.connection = mysql_batch.connect(
                self.host, self.user, self.port, self.password, self.database)
            mysql_batch.confirmed_write = False

            # Should exit if the client refuses the update
            self.assertRaises(SystemExit, mysql_batch.update_batch,
                              [1, 2, 3], 'batch_test', 'date=NOW()')

    def test_delete_batch(self):
        mysql_batch.connection = mysql_batch.connect(
            self.host, self.user, self.port, self.password, self.database)
        mysql_batch.confirmed_write = True

        self.assertTrue(mysql_batch.delete_batch([1, 2, 3], 'batch_test'))

    def test_delete_batch_2(self):
        mysql_batch.connection = mysql_batch.connect(
            self.host, self.user, self.port, self.password, self.database)
        mysql_batch.confirmed_write = True

        # Return should be none if there are no `ids`
        self.assertIsNone(mysql_batch.delete_batch([], 'batch_test'))

    def test_delete_batch_3(self):
        with unittest.mock.patch('builtins.input', return_value='no'):
            mysql_batch.connection = mysql_batch.connect(
                self.host, self.user, self.port, self.password, self.database)
            mysql_batch.confirmed_write = False

            # Should exit if the client refuses the update
            self.assertRaises(SystemExit, mysql_batch.delete_batch,
                              [1, 2, 3], 'batch_test')

    def test_run_query(self):
        mysql_batch.connection = mysql_batch.connect(
            self.host, self.user, self.port, self.password, self.database)

        self.assertTrue(mysql_batch.run_query('SELECT 1'))
        self.assertTrue(mysql_batch.run_query('SELECT 1', 0.001))

    def test_get_input(self):
        with unittest.mock.patch('builtins.input', return_value='yes'):
            self.assertEqual(mysql_batch.get_input(), 'yes')

        with unittest.mock.patch('builtins.input', return_value='no'):
            self.assertEqual(mysql_batch.get_input(), 'no')

    def test_query_yes_no(self):
        with unittest.mock.patch('builtins.input', return_value='yes'):
            self.assertTrue(mysql_batch.query_yes_no('some question?'))

        with unittest.mock.patch('builtins.input', return_value='yes'):
            self.assertTrue(mysql_batch.query_yes_no('some question?', None))

        with unittest.mock.patch('builtins.input', return_value='yes'):
            self.assertTrue(mysql_batch.query_yes_no('some question?', 'no'))

        with unittest.mock.patch('builtins.input', return_value='no'):
            self.assertFalse(mysql_batch.query_yes_no('some question?'))

        # Test invalid default
        self.assertRaises(ValueError, mysql_batch.query_yes_no,
                          'unknown_engine', 'invalid_value')

        # Test empty input with a default value
        with unittest.mock.patch('builtins.input', return_value=''):
            self.assertTrue(mysql_batch.query_yes_no('some question?', 'yes'))

    def test_connect(self):
        connection = mysql_batch.connect(
            self.host, self.user, self.port, self.password, self.database)

        self.assertIsInstance(connection, pymysql.connections.Connection)

    def test_connect_2(self):
        # Test exception for connection error
        self.assertRaises(RuntimeError, mysql_batch.connect,
                          self.host, 'invalid_value', self.port, self.password, self.database)

    def test_execute(self):
        self.assertTrue(mysql_batch.execute(self.host, self.user, self.port, self.password, self.database,
                                            action='update',
                                            table='batch_test',
                                            where='date IS NULL',
                                            set_='date=NOW()',
                                            no_confirm=True,
                                            read_batch_size=35,
                                            write_batch_size=15))

    def test_execute_2(self):
        with unittest.mock.patch('builtins.input', return_value='yes'):
            self.assertTrue(mysql_batch.execute(self.host, self.user, self.port, self.password, self.database,
                                                action='update',
                                                table='batch_test',
                                                where='date IS NULL',
                                                set_='date=NOW()',
                                                read_batch_size=35,
                                                write_batch_size=15))

    def test_execute_3(self):
        self.assertTrue(mysql_batch.execute(self.host, self.user, self.port, self.password, self.database,
                                            action='delete',
                                            table='batch_test',
                                            where='date IS NULL',
                                            no_confirm=True,
                                            read_batch_size=35,
                                            write_batch_size=15))

    def test_execute_4(self):
        # Test exception for update without a set
        self.assertRaises(RuntimeError, mysql_batch.execute,
                          self.host, self.user, self.port, self.password, self.database,
                          action='update',
                          table='batch_test',
                          where='date IS NULL',
                          no_confirm=True)
