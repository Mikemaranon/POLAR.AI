import jwt
import zipfile
from flask import render_template, redirect, request, url_for, jsonify
from user_m.user_manager import UserManager
from data_m.database import Database, USERNAME, PASSWORD
import os
import json

class AppRoutes:
    def __init__(self, app, user_manager: UserManager, database: Database):
        self.app = app
        self.user_manager = user_manager
        self.database = database
        self._register_routes()
    
    # ==================================================================================
    #                           REGISTERING ROUTES
    #
    #            [_register_routes]     instance of every basic route 
    # ================================================================================== 

    def _register_routes(self):
        self.app.add_url_rule("/", "home", self.get_home, methods=["GET"])
        self.app.add_url_rule("/index", "index", self.get_index)
        self.app.add_url_rule("/login", "login", self.get_login, methods=["GET", "POST"])
        self.app.add_url_rule("/logout", "logout", self.get_logout, methods=["POST"])

        # chat routes
        self.app.add_url_rule("/chat", "chat", self.get_chat, methods=["POST"])

        # train routes
        self.app.add_url_rule("/train", "train", self.get_train, methods=["POST"])

        # userconfig routes
        self.app.add_url_rule("/userconf", "userconf", self.get_userconf, methods=["POST"])

    # ==================================================================================
    #                           BASIC ROUTINGS URLs
    #
    #            [get_home]             check user and redirect to get_index
    #            [get_index]            go to index.html
    #            [get_login]            log user and send his token
    #            [get_logout]           log user out, send to index.html 
    # ================================================================================== 
    
    def get_index(self):
        return render_template("index.html")
    
    def get_home(self):
        user = self.user_manager.check_user(request)
        if user:            
            return redirect(url_for("index"))  # Redirect to index.html
        return render_template("login.html")

    def get_login(self):
        error_message = None
        if request.method == "POST":
            data = request.get_json()

            username = data.get("username")
            password = data.get("password")

            token = self.user_manager.login(username, password)
            if token:
                response = jsonify({"token": token})
                return response
            
            error_message = "incorrect user data, try again"

        return render_template("login.html", error_message=error_message)

    def get_logout(self):
        
        token = self.user_manager.get_request_token(request)
        
        self.user_manager.logout(token)
        response = redirect(url_for("login"))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    
    # ==================================================================================
    #                           SPECIFIC ROUTINGS URLs
    #
    #            [get_chat]             redirect to a chat connected to an API
    #            [get_train]            redirect to a training playground interface
    #                                    to tune an specific model
    # ================================================================================== 

    def get_chat(self):
        user = self.user_manager.check_user(request)
        if user:            
            return 0
            # Redirect to chat.html
        return render_template("login.html")

    def get_train(self):
        return 0

    def get_userconf(self):
        return 0