# web_server/data_m/db_connector.py

import psycopg2

#   ||==============================================================||
#   ||    MAIN CONFIGURATION OF NODE POSTGRE-SQL. DO NOT EDIT       ||
#   ||    ORIGINAL VALUES BELOW                                     ||
#   ||                                                              ||
#   ||    - dbname: node_db                                         ||
#   ||    - user: node_admin                                        ||
#   ||    - password: admin123                                      ||
#   ||    - host: localhost                                         ||
#   ||    - port: 5400                                              ||  
#   ||==============================================================||

DB_CONFIG = {
    "dbname": "node_db",
    "user": "node_admin",
    "password": "admin123",
    "host": "localhost",
    "port": 5400
}

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
