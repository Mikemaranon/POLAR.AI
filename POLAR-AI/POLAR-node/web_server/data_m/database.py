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

    ROLE_TO_LEVEL = {
        'user': 1,
        'trainer': 2,
        'developer': 3,
        'admin': 4
    }

    LEVEL_TO_ROLE = {
        1: 'user',
        2: 'trainer',
        3: 'developer',
        4: 'admin'
    }
    
    def __init__(self):
        if hasattr(self, 'initialized') and self.initialized:
            return

        # connect to the db_connector
        self.connector = DBConnector()

        try:
            self.conn = self.connector.connect()
            self.cursor = self.conn.cursor()
            self.initialized = True
        except Exception as e:
            print(f"[ERROR] No se pudo conectar a la base de datos al iniciar Database: {e}")
            self.conn = None
            self.cursor = None
            self.initialized = False # Indicar que la inicialización falló

    # =============================================
    #           BASIC DATABASE METHODS
    # =============================================

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

    # ||============================================================||
    # ||      USER MANAGEMENT METHODS: USERS AND SESSIONS           ||
    # || ---------------------------------------------------------- ||
    # ||    method                query            min_role         ||
    # || ---------------------------------------------------------- ||
    # ||  - get_user()            SELECT            1               ||
    # ||  - add_user()            INSERT            3               ||
    # ||  - delete_user()         DELETE            3               ||
    # ||  - get_session()         SELECT            1               ||
    # ||  - save_session()        INSERT            1               ||
    # ||  - delete_session()      DELETE            1               ||
    # ||============================================================||

    # USER METHODS
    def get_user(self, username: str):

        query = "SELECT id, username, password, role FROM users WHERE username = %s"
        try:
            self.execute(query, (username,), fetch=True)
            user_data = self.fetchone()
            if user_data:
                # returns dictionary to set compatibility with user_manager
                return {
                    "id": user_data[0],
                    "username": user_data[1],
                    "password": user_data[2],
                    "role": user_data[3]
                }
        except Exception as e:
            print(f"[SELECT ERROR] fetching user failed: {e}")
        return None

    def add_user(self, username: str, password_hash: str, role_level: int):

        role_string = self.LEVEL_TO_ROLE.get(role_level)
        if not role_string:
            print(f"[ROLE ERROR] role level  '{role_level}' not valid. operation aborted.")
            return None

        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s) RETURNING id;"
        try:
            self.execute(query, (username, password_hash, role_string), fetch=True) # Pasamos el string del rol
            user_id = self.fetchone()
            if user_id:
                print(f"Usuario '{username}' añadido con ID: {user_id[0]} y rol '{role_string}' (nivel {role_level})")
                return user_id[0]
        except Exception as e:
            print(f"[INSERT ERROR] saving user '{username}' failed: {e}")
        return None

    def delete_user(self, username: str):
        user_data = self.get_user(username)
        if user_data:
            user_id = user_data["id"]
            delete_sessions_query = "DELETE FROM sessions WHERE user_id = %s;"
            try:
                self.execute(delete_sessions_query, (user_id,))
            except Exception as e:
                print(f"[SESSION WARNING] Session for user with ID '{user_id}' not found: {e}")

        delete_user_query = "DELETE FROM users WHERE username = %s;"
        try:
            self.execute(delete_user_query, (username,))
            return True
        except Exception as e:
            print(f"[DELETE ERROR] failed to delete user '{username}': {e}")
            return False

    # SESSION METHODS
    def get_session(self, token: str):

        query = "SELECT id, user_id, token, created_at FROM sessions WHERE token = %s;"
        try:
            self.execute(query, (token,), fetch=True)
            session_data = self.fetchone()
            if session_data:
                return {
                    "id": session_data[0],
                    "user_id": session_data[1],
                    "token": session_data[2],
                    "created_at": session_data[3]
                }
        except Exception as e:
            print(f"[SELECT ERROR] fetching session failed: {e}")
        return None

    def save_session(self, user_id: int, token: str):

        query = "INSERT INTO sessions (user_id, token) VALUES (%s, %s) RETURNING id;"
        try:
            self.execute(query, (user_id, token), fetch=True) # Fetch True for RETURNING id
            session_id = self.fetchone()
            return session_id[0] if session_id else None
        except Exception as e:
            print(f"[INSERT ERROR] saving session failed: {e}")
            return None

    def delete_session(self, token: str):
        
        query = "DELETE FROM sessions WHERE token = %s;"
        try:
            self.execute(query, (token,))
            return True
        except Exception as e:
            print(f"[DELETE ERROR] deleting session failed: {e}")
            return False