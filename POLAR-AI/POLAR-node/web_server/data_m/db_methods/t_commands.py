# web_server/data_m/db_methods/t_commands.py

import psycopg2
import json

class CommandsTable:
    def __init__(self, connector, close, execute, fetchone, fetchall, LEVEL_TO_ROLE, ROLE_TO_LEVEL):
        self.connector = connector
        self.table_name = 'commands'

        self.close = close
        self.execute = execute
        self.fetchone = fetchone
        self.fetchall = fetchall
        self.LEVEL_TO_ROLE = LEVEL_TO_ROLE
        self.ROLE_TO_LEVEL = ROLE_TO_LEVEL    

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