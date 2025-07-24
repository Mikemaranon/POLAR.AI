import jwt
import zipfile
from flask import request, jsonify
from user_m.user_manager import UserManager
from data_m.database import Database
import os
import json

class ApiManager:
    def __init__(self, app, user_manager: UserManager, database: Database):
        self.app = app
        self.user_manager = user_manager
        self.database = database
        self._register_APIs()
    
    # =========================================================
    #                     REGISTERING APIs
    # =========================================================

    def _register_APIs(self):
        self.app.add_url_rule("/api/check", "check", self.API_check, methods=["GET"])
        self.app.add_url_rule("/api/db/tables", "get_tables", self.API_get_tables, methods=["GET"])
        self.app.add_url_rule("/api/db/table-content", "get_table_content", self.API_get_table_content, methods=["POST"])
    
    # =========================================
    #       API protocols start from here
    # =========================================
        
    # endpoint to check if the API is working
    def API_check(self):
        return jsonify({"status": "ok"}), 200
    
    # endpoint to get the list of tables in the database
    def API_get_tables(self):
        try:
            tables = self.database.get_tables()
            return jsonify({"tables": tables}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    # endpoint to get the content of a specific table
    def API_get_table_content(self):
        data = request.get_json(silent=True)
        if not data or 'table_name' not in data:
            return jsonify({"error": "Table name is required in JSON body"}), 400
        
        table_name = data['table_name']
        try:
            columns = self.database.get_table_content(table_name)
            return jsonify({"content": columns}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    