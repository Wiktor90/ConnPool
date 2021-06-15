import psycopg2 as ps2
from configparser import ConfigParser


class DataBase:
    def __init__(self, db_user, password, host, port, database):
        self.db_user = db_user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = ps2.connect(
            user=self.db_user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


config = ConfigParser()
config.read("config.ini")
db = DataBase(
    config["DATABASE"]["db_user"],
    config["DATABASE"]["password"],
    config["DATABASE"]["host"],
    config["DATABASE"]["port"],
    config["DATABASE"]["database"],
)