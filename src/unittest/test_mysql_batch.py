import unittest
from unittest.mock import patch

import pymysql

from src import mysql_batch


class Test(unittest.TestCase):

    host = 'localhost'
    user = 'travis'
    database = 'my_db'
    password = ''
    port = 3306

    def test_update_batch(self):
        mysql_batch.connection = mysql_batch.connect(
            self.host, self.user, self.port, self.password, self.database)
        mysql_batch.confirmed_write = True

        self.assertTrue(mysql_batch.update_batch(
            [4, 5, 6], 'batch_test', 'date=NOW()'))

    def test_delete_batch(self):
        mysql_batch.connection = mysql_batch.connect(
            self.host, self.user, self.port, self.password, self.database)
        mysql_batch.confirmed_write = True

        self.assertTrue(mysql_batch.delete_batch([1, 2, 3], 'batch_test'))

    def test_run_query(self):
        mysql_batch.connection = mysql_batch.connect(
            self.host, self.user, self.port, self.password, self.database)

        self.assertTrue(mysql_batch.run_query('SELECT 1'))

    def test_get_input(self):
        with unittest.mock.patch('builtins.input', return_value='yes'):
            self.assertEqual(mysql_batch.get_input(), 'yes')

        with unittest.mock.patch('builtins.input', return_value='no'):
            self.assertEqual(mysql_batch.get_input(), 'no')

    def test_query_yes_no(self):
        with unittest.mock.patch('builtins.input', return_value='yes'):
            self.assertTrue(mysql_batch.query_yes_no('some question?'))

        with unittest.mock.patch('builtins.input', return_value='no'):
            self.assertFalse(mysql_batch.query_yes_no('some question?'))

    def test_connect(self):
        connection = mysql_batch.connect(
            self.host, self.user, self.port, self.password, self.database)

        self.assertIsInstance(connection, pymysql.connections.Connection)

    def test_execute(self):
        self.assertTrue(mysql_batch.execute(self.host, self.user, self.port, self.password, self.database,
                                            action='update',
                                            table='batch_test',
                                            where='id > 1',
                                            set_='date=NOW()',
                                            no_confirm=True))

        self.assertTrue(mysql_batch.execute(self.host, self.user, self.port, self.password, self.database,
                                            action='delete',
                                            table='batch_test',
                                            where='id > 20',
                                            no_confirm=True))
