# web_server/data_m/database.py

import json
import psycopg2
import threading
from werkzeug.security import generate_password_hash
from data_m.db_connector import DBConnector

HOST = '0.0.0.0'
PORT = 5555
ENCODING = 'utf-8'
BUFFER_SIZE = 1024

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

class Database:

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # This runs every time Database() is called, but does not reinitialize if already initialized
        if hasattr(self, 'initialized') and self.initialized:
            return

        self.connector = DBConnector()

        try:
            self.conn = self.connector.connect()
            self.cursor = self.conn.cursor()
            self.initialized = True
        except Exception as e:
            print(f"[ERROR] Could not connect to the database when initializing Database: {e}")
            self.conn = None
            self.cursor = None
            self.initialized = False

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

        query = "SELECT username, password, role, created_at FROM users WHERE username = %s"
        try:
            self.execute(query, (username,))
            user_data = self.fetchone()
            if user_data:
                # returns dictionary to set compatibility with user_manager
                return {
                    "username": user_data[0],
                    "password": user_data[1],
                    "role": user_data[2],
                    "creation": user_data[3]
                }
        except Exception as e:
            print(f"[SELECT ERROR] fetching user failed: {e}")
        return None

    def add_user(self, username: str, password: str, role_level: int):

        password_hash = generate_password_hash(password)
        
        role_string = self.LEVEL_TO_ROLE.get(role_level)
        if not role_string:
            print(f"[ROLE ERROR] role level  '{role_level}' not valid. operation aborted.")
            return None

        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s);"
        try:
            self.execute(query, (username, password_hash, role_string), fetch=True) # Pasamos el string del rol
            print(f"User '{username}' added with role '{role_string}' (level: {role_level})")
            return True
        except Exception as e:
            print(f"[INSERT ERROR] saving user '{username}' failed: {e}")
        return None

    def update_user(self, username: str, new_name: str = None, new_password: str = None, new_role: int = None):
        # TODO: finish the method
        try:
            user_data = self.get_user(username)
            if not user_data:
                print(f"[UPDATE ERROR] User '{username}' not found.")
                return False

            updates = []
            params = []

            if new_name:
                updates.append("username = %s")
                params.append(new_name)
                
            if new_password:
                updates.append("password = %s")
                params.append(new_password)

            if new_role is not None:
                role_string = self.LEVEL_TO_ROLE.get(new_role)
                if not role_string:
                    print(f"[ROLE ERROR] role level '{new_role}' not valid. operation aborted.")
                    return False
                updates.append("role = %s")
                params.append(role_string)

            if not updates:
                print("[UPDATE WARNING] No fields were found to update.")
                return False

            params.append(username)  # Add username for WHERE clause
            query = f"UPDATE users SET {', '.join(updates)} WHERE username = %s;"

            self.execute(query, tuple(params))
            print(f"[SYSTEM] User '{username}' successfully updated.")
            return True
        except Exception as e:
            print(f"[UPDATE ERROR] failed to update user '{username}': {e}")
        return None

    def delete_user(self, username: str):
        user_data = self.get_user(username)
        if user_data:
            delete_sessions_query = "DELETE FROM sessions WHERE username = %s;"
            try:
                self.execute(delete_sessions_query, (username,))
            except Exception as e:
                print(f"[SESSION WARNING] Session for user '{username}' not found: {e}")

        delete_user_query = "DELETE FROM users WHERE username = %s;"
        try:
            self.execute(delete_user_query, (username))
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

        query = "SELECT id, username, token, created_at FROM sessions WHERE token = %s;"
        try:
            self.execute(query, (token,))
            session_data = self.fetchone()
            if session_data:
                return {
                    "id": session_data[0],
                    "username": session_data[1],
                    "token": session_data[2],
                    "created_at": session_data[3]
                }
        except Exception as e:
            print(f"[SELECT ERROR] fetching session failed: {e}")
        return None

    def save_session(self, username: int, token: str):

        query = "INSERT INTO sessions (username, token) VALUES (%s, %s) RETURNING id;"
        try:
            self.execute(query, (username, token)) # Fetch True for RETURNING id
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

    def get_command(self, command_id: str):
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

    def save_new_command(self, conn, command_data: dict):
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