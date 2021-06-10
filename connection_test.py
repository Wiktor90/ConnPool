import time
from configparser import ConfigParser
from database import DataBase


config = ConfigParser()
config.read("config.ini")
db = DataBase(
    config["DATABASE"]["db_user"],
    config["DATABASE"]["password"],
    config["DATABASE"]["host"],
    config["DATABASE"]["port"],
    config["DATABASE"]["database"],
)

query = """SELECT * FROM actor LIMIT 5"""


def time_wraper(func):
    def wraper_func(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        stop = time.perf_counter()
        x = [x for x in args][-1]
        print(f"""Performance of {func.__name__}(loops: {x}): {round(stop - start, 2)} second(s)""")
        return result
    return wraper_func


@time_wraper
def multi_connection_test(db, query, n):
    for _ in range(n):
        with db.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                cursor.fetchall()
    return True


@time_wraper
def multi_query_test(db, query, n):
    with db.connection as conn:
        with conn.cursor() as cursor:
            for _ in range(n):
                cursor.execute(query)
                cursor.fetchall()
    return True


multi_connection_test(db, query, 10000)
multi_query_test(db, query, 10000)
