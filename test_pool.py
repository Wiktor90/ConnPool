import unittest

from pool import ConnectionPool
from database import db

class TestConnectionPool(unittest.TestCase):

    def setUp(self):
        self.p = ConnectionPool(db)
        self.p2 = ConnectionPool(db)
        self.p2.pool = [self.p2.set_connection_status_occupied(conn) for conn in self.p2.pool]

    def test_check_free_conn_amout(self):
        free_connections = self.p.check_free_connections()
        self.assertEqual(free_connections, 10)

    def test_get_first_free_connection(self):
        conn = self.p.get_first_free_connection()
        self.assertIsInstance(conn, list)
        self.assertTrue(conn[1] is False)

    def test_check_all_connection_occupied(self):
        result = self.p2.get_first_free_connection()
        self.assertIsInstance(result, str)

    def test_connection_is_ocupied(self):
        conn = self.p.pool[0]
        conn_occupied = self.p.set_connection_status_occupied(conn)
        self.assertTrue(conn_occupied[1] is True)

    def test_check_that_pool_is_growing(self):
        self.p2.create_additional_connection()
        self.assertTrue(len(self.p2.pool) > self.p.number)

    def test_adding_new_conn_to_pool_when_others_occupied(self):
        additional_conn = self.p2.create_additional_connection()
        self.assertTrue(all([additional_conn[1] is False,
                            self.p2.pool.index(additional_conn) == 10]))

    def test_given_connection_status(self):
        conn = self.p.get_connection
