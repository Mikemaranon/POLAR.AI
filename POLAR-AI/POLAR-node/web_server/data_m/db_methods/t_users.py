# web_server/data_m/db_methods/t_users.py

from werkzeug.security import generate_password_hash

class UsersTable:
    def __init__(self, connector, close, execute, fetchone, fetchall, LEVEL_TO_ROLE, ROLE_TO_LEVEL):
        self.connector = connector
        self.table_name = 'users'

        self.close = close
        self.execute = execute
        self.fetchone = fetchone
        self.fetchall = fetchall
        self.LEVEL_TO_ROLE = LEVEL_TO_ROLE
        self.ROLE_TO_LEVEL = ROLE_TO_LEVEL

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
            self.execute(query, (username, password_hash, role_string)) # Pasamos el string del rol
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
                password_hash = generate_password_hash(new_password)
                updates.append("password = %s")
                params.append(password_hash)

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
            self.execute(delete_user_query, (username,))
            return True
        except Exception as e:
            print(f"[DELETE ERROR] failed to delete user '{username}': {e}")
            return False