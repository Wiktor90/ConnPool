import concurrent.futures
import time


from pool import ConnectionPool
from database import db


c_pool = ConnectionPool(db.connection)
query = """SELECT * FROM film"""
workers = [i for i in range(100)]


def conn_test(n):
    conn = c_pool.get_connection()
    print(f'Conn:{conn[1]} IN')
    conn = conn[0][0]
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            cursor.fetchall()
            time.sleep(3)

    c_pool.return_connection(conn[0], conn[1])
    print(f'worker-{n} -> connection: {conn[1]} OUT')
    print(f'Free conn:{c_pool.check_free_connections()}')

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(conn_test, workers)