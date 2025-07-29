# web_server/data_m/database.py

import json
import psycopg2
import threading
from data_m.db_connector import DBConnector
from data_m.db_methods.t_users import UsersTable
from data_m.db_methods.t_sessions import SessionsTable
from data_m.db_methods.t_commands import CommandsTable

HOST = '0.0.0.0'
PORT = 5555
ENCODING = 'utf-8'
BUFFER_SIZE = 1024

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

        # Initialize the database manager for users
        self.t_users = UsersTable(
            self.connector, self.close,
            self.execute, self.fetchone, self.fetchall,
            self.LEVEL_TO_ROLE, self.ROLE_TO_LEVEL,
        )

        # Initialize the database manager for sessions
        self.t_sessions = SessionsTable(
            self.connector, self.close,
            self.execute, self.fetchone, self.fetchall,
            self.LEVEL_TO_ROLE, self.ROLE_TO_LEVEL,
        )

        # Initialize the database manager for commands
        self.t_commands = CommandsTable(
            self.connector, self.close,
            self.execute, self.fetchone, self.fetchall,
            self.LEVEL_TO_ROLE, self.ROLE_TO_LEVEL,
        )

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

    # =============================================
    #          GENERAL DATABASE METHODS
    # =============================================

    def get_tables(self):
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """
        try:
            self.execute(query)
            tables = self.fetchall()
            return [table[0] for table in tables]
        except Exception as e:
            print(f"[SELECT ERROR] fetching tables failed: {e}")
            return []

    def get_columns(self, table_name: str) -> dict[str, str]:
        if not table_name:
            raise ValueError("Table name cannot be empty")

        query = """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = %s
            ORDER BY ordinal_position;
        """
        self.execute(query, (table_name,))
        columns = self.fetchall()
        if not columns:
            raise ValueError(f"Table '{table_name}' not found")

        return [{"name": col[0], "type": col[1]} for col in columns]

    def get_table_content(self, table_name: str) -> dict:
        columns_info = self.get_columns(table_name)
        columns = [col["name"] for col in columns_info]

        query = f'SELECT * FROM "{table_name}";'
        self.execute(query)
        rows = self.fetchall()

        import json
        data = []
        for row in rows:
            record = {}
            for i, col in enumerate(columns):
                value = row[i]
                if columns_info[i]["type"] == "jsonb" and value:
                    try:
                        value = json.loads(value) if isinstance(value, str) else value
                    except Exception:
                        pass
                record[col] = value
            data.append(record)

        return {"columns": columns_info, "data": data}



