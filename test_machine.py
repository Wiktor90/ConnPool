import concurrent.futures
import time
import random


from pool import ConnectionPool
from database import db


c_pool = ConnectionPool(db.connection, number = 10)
query = """SELECT * FROM film"""
workers = [i for i in range(100)]


def conn_test(n):
    conn = c_pool.get_connection()
    print(f'Worker {n} IN  >>> Conn num: {conn[2]}')

    with conn[0]:
        with conn[0].cursor() as cursor:
            cursor.execute(query)
            cursor.fetchall()
            time.sleep(random.randint(1,3))

    c_pool.return_connection(conn)
    print(f'Worker {n} OUT // free : {c_pool.check_free_connections()} // total: {len(c_pool.pool)}')


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(conn_test, workers)
