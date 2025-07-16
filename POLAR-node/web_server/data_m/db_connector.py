# web_server/data_m/db_connector.py

import psycopg2
from .config import DB_CONFIG

class DBConnector:
    def __init__(self):
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(**DB_CONFIG)
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
