import concurrent.futures
import time
import random


from pool import ConnectionPool
from database import db


c_pool = ConnectionPool(db.connection, number = 3)
query = """SELECT * FROM film"""
workers = [i for i in range(50)]


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

    if n%10 == 0:
        print('\n')
        print([conn[1] for conn in c_pool.pool])
        print(f'Removed connections: {c_pool.clean_pool()} <<<--------')
        print([conn[1] for conn in c_pool.pool])
        print('\n')


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(conn_test, workers)

print(f'pool: {len(c_pool.pool)}')
print(f'Removed connections: {c_pool.clean_pool()} <<<--------')
print(f'pool: {len(c_pool.pool)}')
