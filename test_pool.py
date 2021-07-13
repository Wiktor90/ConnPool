import unittest

from pool import ConnectionPool
from database import db

class TestConnectionPool(unittest.TestCase):

    def setUp(self):
        self.p = ConnectionPool(db)
        self.p2 = ConnectionPool(db, in_use = True)

    def test_check_free_conn_amout(self):
        free_connections = self.p.check_free_connections()
        self.assertEqual(free_connections, 10)

    def test_check_all_connection_ocupited(self):
        result = self.p2.get_first_free_connection()
        self.assertIsInstance(result, str)
