import jwt
import zipfile
from flask import render_template, redirect, request, url_for, jsonify
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
    
    # ==================================================================================
    #                     REGISTERING APIs
    # ================================================================================== 

    def _register_APIs(self):
        self.app.add_url_rule("/api/check", "check", self.API_check, methods=["GET"])
    
    # =========================================
    #       API protocols start from here
    # =========================================
        
    # endpoint to check if the API is working
    def API_check(self):
        return jsonify({"status": "ok"}), 200
    
    