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
        self.assertEqual(free_connections, self.p.number)

    def test_get_first_free_connection(self):
        conn = self.p.get_first_free_connection(self.p.pool)
        self.assertIsInstance(conn, list)
        self.assertTrue(conn[1] is False)

    def test_check_all_connection_occupied(self):
        result = self.p2.get_first_free_connection(self.p2.pool)
        self.assertIsInstance(result, str)

    def test_connection_is_ocupied(self):
        conn = self.p.pool[0]
        self.p.set_connection_status_occupied(conn)
        self.assertTrue(conn[1] is True)

    def test_check_that_pool_is_growing(self):
        self.p2.create_additional_connection_if_needed()
        self.assertTrue(len(self.p2.pool) > self.p.number)

    def test_adding_new_conn_to_pool_when_others_occupied(self):
        additional_conn = self.p2.create_additional_connection_if_needed()
        self.assertTrue(all([additional_conn[1] is False,
                            len(self.p2.pool) == self.p2.number + 1]))

    def test_given_connection_status_on_clean_pool(self):
        conn = self.p.get_connection()

        self.assertTrue(self.p.check_free_connections() < self.p.number)
        self.assertTrue(len(self.p.pool) == self.p.number)
        self.assertTrue(conn[1] is True)
        self.assertTrue(self.p.pool[0][1] is True)

    def test_given_connection_status_on_busy_pool(self):
        conn = self.p2.get_connection()

        self.assertTrue(len(self.p2.pool) > self.p.number)
        self.assertTrue(conn[1] is True)
        self.assertTrue(self.p2.pool[-1][1] is True)

    def test_return_connection(self):
        c1 = self.p.get_connection() # firs obj in pool
        c2 = self.p2.get_connection() # last obj in pool

        self.assertTrue(all([self.p.return_connection(c1)[1] is False,
                            self.p.pool[0][1] is False]))
        self.assertTrue(all([self.p2.return_connection(c2)[1] is False,
                            self.p2.pool[-1][1] is False]))

    def test_if_additional_free_conn_is_deleted(self):
        additional_conn = self.p2.get_connection()
        self.p2.return_connection(additional_conn)
        self.assertEqual(len(self.p2.pool), self.p2.number + 1)

        self.p2.destroy_additional_free_connection()
        self.assertEqual(len(self.p2.pool), self.p2.number)

    def test_if_pool_is_cleaned_up(self):
        for _ in range(10):
            additional_conn = self.p2.create_additional_connection_if_needed()
            self.p2.set_connection_status_occupied(additional_conn)

        self.p2.pool[12][1] = False 
        self.p2.pool[15][1] = False

        self.p2.clean_pool()
        self.assertTrue(all([conn[1] for conn in self.p2.pool]))
