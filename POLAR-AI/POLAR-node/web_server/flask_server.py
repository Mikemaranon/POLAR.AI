import threading, os
from flask import Flask
from data_m.database import Database
from user_m.user_manager import UserManager
from cli_m.cli_manager import CliManager
from api_m.api_manager import ApiManager
from app_routes import AppRoutes

class Server:
    def __init__(self, app: Flask):
        self.app = app
        self.app.secret_key = os.urandom(24)

        self.database = self.ini_database()
        self.cli_manager = self.ini_cli_manager()
        self.user_manager = self.ini_user_manager()
        self.app_routes = self.ini_app_routes()
        self.api_manager = self.ini_api_manager()

        # Configuración del puerto (para Render o local)
        port = int(os.environ.get('PORT', 5000))

        # Detectar si estamos en el hilo principal
        is_main_thread = threading.current_thread() is threading.main_thread()
        if not is_main_thread:
            print("⚠️ Flask running in a secondary thread: disabling debug and reloader.")

        self.app.run(
            debug=is_main_thread,           # Enable debug only in the main thread
            use_reloader=is_main_thread,    # Avoid reloader in secondary threads
            host='0.0.0.0',
            port=port
        )
        
        # Clear sessions on initialization
        self.database.t_sessions.clear_sessions()
        
    def ini_database(self):
        return Database()
    
    def ini_cli_manager(self):
        return CliManager()

    def ini_user_manager(self):
        return UserManager()
    
    def ini_app_routes(self):
        return AppRoutes(self.app, self.user_manager, self.database)
    
    def ini_api_manager(self):
        return ApiManager(self.app, self.user_manager, self.database, self.cli_manager)