import jwt
import zipfile
from flask import render_template, redirect, request, url_for, jsonify
from user_m.user_manager import UserManager
from data_m.database import Database, USERNAME, PASSWORD
import os
import json

class ApiManager:
    def __init__(self, app, user_manager: UserManager, database: Database):
        self.app = app
        self.user_manager = user_manager
        self.database = database
        self._register_APIs()
    
    # ==================================================================================
    #                     REGISTERING APIs
    # ================================================================================== 

    def _register_APIs(self):
        self.app.add_url_rule("/api/check", "check", self.API_check, methods=["GET"])
        self.app.add_url_rule("/api/register", "register", self.API_register, methods=["POST"])
    
    # =========================================
    #       API protocols start from here
    # =========================================
        
    # endpoint to check if the API is working
    def API_check(self):
        return jsonify({"status": "ok"}), 200
    
    def API_register(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        users = self.database.load_users()  # Ensure users are loaded before checking
        # Check if the user already exist
        if username in users:
            return jsonify({"error": "User already exist"}), 400

        self.database.add_user(username, password)
        return jsonify({"message": "User registered successfully"}), 201
    