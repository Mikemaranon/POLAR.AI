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
    # ||             USER MANAGEMENT METHODS: USERS                 ||
    # || ---------------------------------------------------------- ||
    # ||    method                query            min_role         ||
    # || ---------------------------------------------------------- ||
    # ||  - get_user()            SELECT            1               ||
    # ||  - add_user()            INSERT            3               ||
    # ||  - edit_user()           UPDATE            3               ||
    # ||  - delete_user()         DELETE            3               ||
    # ||============================================================||

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

    def update_user():
        # TODO: finish the method
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

    # ||============================================================||
    # ||            USER MANAGEMENT METHODS: SESSIONS               ||
    # || ---------------------------------------------------------- ||
    # ||    method                query            min_role         ||
    # || ---------------------------------------------------------- ||
    # ||  - get_session()         SELECT            1               ||
    # ||  - save_session()        INSERT            1               ||
    # ||  - delete_session()      DELETE            1               ||
    # ||============================================================||

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

    # ||============================================================||
    # ||                COMMAND MANAGEMENT METHODS                  ||
    # || ---------------------------------------------------------- ||
    # ||    method                query            min_role         ||
    # || ---------------------------------------------------------- ||
    # ||  - get_command()         SELECT            4               ||
    # ||  - save_new_command()    INSERT            4               ||
    # ||  - update_command()      UPDATE            4               ||
    # ||  - delete_command()      DELETE            4               ||
    # ||============================================================||

    def get_command(self, command_id: str) -> dict or None:
        query = "SELECT id, module, function, sub_commands FROM commands WHERE id = %s;"
        try:
            self.execute(query, (command_id,))
            row = self.fetchone()
            if row:
                return {
                    "id": row[0],
                    "module": row[1],
                    "function": row[2],
                    "sub_commands": row[3]
                }
            return None
        except Exception as e:
            print(f"[SELECT ERROR] fetching command failed: {e}")
            return None

    def save_new_command(conn, command_data: dict):
        query = "INSERT INTO commands (id, module, function, sub_commands) VALUES (%s, %s, %s, %s)"
        try:
            self.execute(query,
                (
                    command_data.get("id"),
                    command_data.get("module"),
                    command_data.get("function"),
                    json.dumps(command_data.get("sub_commands")) # Ensures its a JSON
                )
            )
            return True
        except psycopg2.errors.UniqueViolation:
            print(f"[INSERT ERROR] Command with ID '{command_data.get('id')}' already exists.")
            return False
        except Exception as e:
            print(f"[INSERT ERROR] saving command failed: {e}")
            return False

    def update_command(self, command_id: str, new_module: str = None, new_function: str = None, new_sub_commands: dict = None):

        updates = []
        params = []

        if new_module is not None:
            updates.append("module = %s")
            params.append(new_module)

        if new_function is not None:
            updates.append("function = %s")
            params.append(new_function)

        if new_sub_commands is not None:
            updates.append("sub_commands = %s")
            params.append(json.dumps(new_sub_commands)) # Transform dict to JSON

        if not updates:
            print("[UPDATE WARNING] No fields were found to update.")
            return False

        # Añadir el ID del comando al final de los parámetros para la cláusula WHERE
        params.append(command_id)

        query = f"UPDATE commands SET {', '.join(updates)} WHERE id = %s;"

        try:
            self.execute(query, tuple(params))
            if self.cursor.rowcount > 0:
                print(f"[SYSTEM] Command '{command_id}' succesfully updated.")
                return True
            else:
                print(f"[UPDATE ERROR] Command '{command_id}' not found.")
                return False
        except Exception as e:
            print(f"[UPDATE ERROR] failed to update command '{command_id}': {e}")
            return False

    def delete_command(self, command_id: str):
        query = "DELETE FROM commands WHERE id = %s;"
        try:
            self.execute(query, (command_id,))
            if self.cursor.rowcount > 0:
                print(f"[SYSTEM] Comand'{command_id}' succesfully deleted.")
                return True
            else:
                print(f"[DELETE ERROR] Command '{command_id}' not found.")
                return False
        except Exception as e:
            print(f"[DELETE ERROR] failed to delete command '{command_id}': {e}")
            return False