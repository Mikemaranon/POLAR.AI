# web_server/cli_m/cli_server.py

import socket
import threading
from data_m.database import HOST, PORT, ENCODING, BUFFER_SIZE
from user_m.user_manager import UserManager
from cli_m.cli_manager import CliManager
from data_m.database import Database, LEVEL_TO_ROLE, ROLE_TO_LEVEL

class CliServer:
    def __init__(self):
        self.cli = CliManager()
        self.user_manager = UserManager()
        self.db = Database()

    def start(self):
        print(f"\n[CLI SERVER] Listening on {HOST}:{PORT}...\n")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind((HOST, PORT))
            server_sock.listen()

            while True:
                conn, addr = server_sock.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    # ||===============================================================================||
    # ||                      CLI SERVER CLIENT HANDLER                                ||
    # ||                                                                               ||
    # ||    - [auth_cli_user]       authenticates the user via user_manager            ||
    # ||    - [process_commands]    processes the commands from the user in a loop     ||
    # ||===============================================================================||

    def auth_cli_user(self, conn):

        self.send_msg(conn, "Username: ", end="")
        username = self.recv_line(conn).strip()

        self.send_msg(conn, "Password: ", end="")
        password = self.recv_line(conn).strip()

        if not self.user_manager.authenticate(username, password):
            self.send_msg(conn, "\n[AUTH FAILED] Invalid username or password.\n")
            self.print_log(conn, "[CLI_SERVER] Authentication failed for user: " + username)
            return None

        user_data = self.db.get_user(username)
        if not user_data or ROLE_TO_LEVEL.get(user_data.get("role")) != 4:
            self.send_msg(conn, "\n[FORBIDDEN ACCESS] Only level 4 (admin) users can access the CLI.\n")
            self.print_log(conn, "[CLI_SERVER] Unauthorized access attempt by user: " + username)
            self.send_msg(conn, "must: " + LEVEL_TO_ROLE.get(4) + " - 4")
            self.send_msg(conn, "\n your role: " + str(user_data.get("role", "unknown")) + " - " + ROLE_TO_LEVEL.get(user_data.get("role")))
            return None

        self.send_msg(conn, "\n[CLI_SERVER] Welcome, admin.")
        self.print_error(conn, f"[CLI_SERVER] User {username} authenticated successfully.")
        self.send_msg(conn, "Type 'exit' to close the session.\n")

        return {
            "username": user_data["username"],
            "role": user_data["role"]
        }
    
    def process_commands(self, conn, user_context):
        while True:
            self.send_msg(conn, user_context["username"] + "> ", end="")
            command = self.recv_line(conn).strip()
            self.print_log(conn, user_context["username"] + "> " + command)

            if not command:
                continue
            if command.lower() == "exit":
                self.send_msg(conn, "Goodbye!")
                self.print_log(conn, f"[DISCONNECTED] Client disconnected.")
                break

            try:
                output, err = self.cli.process_command(command, user_context)
                if not output:
                    output = "[OK] Command executed but returned no output."

                if err:
                    self.send_msg(conn, f" {err}")
                else:
                    self.send_msg(conn, output)
                    self.print_log(conn, f"[OK] Command '{command}' executed with output:\n{output}")
            except Exception as e:
                self.send_msg(conn, f"[ERROR] {str(e)}")
                self.print_log(conn, f"[ERROR] Exception while processing command: {str(e)}")

    def handle_client(self, conn, addr):
        with conn:
            try:
                self.send_msg(conn, "\r\n===================================================")
                self.send_msg(conn, "||          Welcome to POLAR Node Shell          ||")
                self.send_msg(conn, "===================================================\n")

                user_context = self.auth_cli_user(conn)

                if not user_context:
                    self.send_msg(conn, "Exiting CLI session.")
                    self.print_log(conn, f"[DISCONNECTED] Client {addr} disconnected after failed authentication.")
                    conn.close()
                    return

                self.process_commands(conn, user_context)

            except ConnectionResetError:
                print(f"[DISCONNECTED] Client {addr} disconnected abruptly.")
            except Exception as e:
                print(f"[ERROR] Unexpected error with client {addr}: {e}")

    def send_msg(self, conn, msg, end="\n"):
        conn.sendall((msg + end).encode(ENCODING))

    def print_log(self, conn, msg):
        try:
            client_ip, client_port = conn.getpeername()
            log_prefix = f"[{client_ip}:{client_port}]"
        except OSError:
            log_prefix = f"[CLIENT - Unknown]"
        
        print(f"{log_prefix} {msg.strip()}")

    def print_error(self, conn, msg):
        try:
            client_ip, client_port = conn.getpeername()
            log_prefix = f"[{client_ip}:{client_port}]"
        except OSError:
            log_prefix = f"[CLIENT - Unknown]"
        
        print(f"{log_prefix} {msg.strip()}")
        
    def recv_line(self, conn):
        data = b""
        while not data.endswith(b"\n"):
            chunk = conn.recv(BUFFER_SIZE)
            if not chunk:
                break
            data += chunk
        return data.decode(ENCODING)