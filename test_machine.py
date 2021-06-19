import concurrent.futures
import time
import random

from datetime import datetime
from pool import ConnectionPool
from database import db


pool = ConnectionPool(db.connection)
query = """SELECT * FROM film"""
worker_list = [i for i in range(100)]


def timer(start_time):
    now = datetime.now()
    delta = str(now - start_time)
    return float(delta[:-7])


def connect_to_db(pool):
    return pool.get_connection()


def test_operation(connection, query):
    conn = connection[0][0]
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            time.sleep(random.randint(0,5))
            return records

def worker(num):
    conn = connect_to_db(pool)
    test_operation(conn, query)
    pool.return_connection(conn[0], conn[1])
    print(len(pool.check_free_connections()))
    print(f'worker-{num} -> connection: {conn[1]}')
    

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(worker, worker_list)


# async def myWorker(semafor, num):
#     async with semafor:
#         print(f"IN - {num}")
#         await asyncio.sleep(random.randint(0,5))
#         print(f"OUT - {num}")

# async def main():
#     mySemafor = asyncio.Semaphore(3)
#     tasks = ([
#         myWorker(mySemafor,1),
#         myWorker(mySemafor,2),
#         myWorker(mySemafor,3),
#         myWorker(mySemafor,4),
#         myWorker(mySemafor,5),
#         myWorker(mySemafor,6),
#         myWorker(mySemafor,7),
#         myWorker(mySemafor,8),
#         myWorker(mySemafor,9),
#         myWorker(mySemafor,10),
#     ])
#     await asyncio.gather(*tasks, return_exceptions = True)
#     print('FINISH WORK')

# asyncio.run(main())
# print('FINISH LOOP')