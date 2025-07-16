# web_server/data_m/database.py

import os
import json
from data_m.db_connector import DBConnector

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

class Database:
    
    def __init__(self):
        self.connector = DBConnector()
        self.conn = self.connector.connect()
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"[ERROR] Failed to execute query: {e}")
            raise

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connector.close()
