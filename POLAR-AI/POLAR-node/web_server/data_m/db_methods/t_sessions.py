# web_server/data_m/db_methods/t_sessions.py

class SessionsTable:
    def __init__(self, connector, close, execute, fetchone, fetchall, LEVEL_TO_ROLE, ROLE_TO_LEVEL):
        self.connector = connector
        self.table_name = 'sessions'

        self.close = close
        self.execute = execute
        self.fetchone = fetchone
        self.fetchall = fetchall
        self.LEVEL_TO_ROLE = LEVEL_TO_ROLE
        self.ROLE_TO_LEVEL = ROLE_TO_LEVEL

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
            self.execute(query, (username, token))
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

    def clear_sessions(self):
        query = "DELETE FROM sessions;"
        try:
            self.execute(query)
            print("[WARNING] All sessions have been deleted. This should only run in dev/test environments.")
            return True
        except Exception as e:
            print(f"[CLEAR ERROR] clearing sessions failed: {e}")
            return False