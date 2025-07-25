
from flask import render_template, redirect, request, url_for, jsonify, make_response
from user_m.user_manager import UserManager
from data_m.database import Database

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
        self.app.add_url_rule("/login", "login", self.get_login, methods=["GET", "POST"])
        self.app.add_url_rule("/logout", "logout", self.get_logout, methods=["POST"])

        # userconfig routes
        self.app.add_url_rule("/sites/shell", "shell", self.get_cli, methods=["GET"])
        self.app.add_url_rule("/sites/database", "database", self.get_database, methods=["GET"])
        self.app.add_url_rule("/sites/command-forge", "command_forge", self.get_command_forge, methods=["GET"])

    # ==================================================================================
    #                           BASIC ROUTINGS URLs
    #
    #            [get_home]             check user and redirect to get_index
    #            [get_index]            go to index.html
    #            [get_login]            log user and send his token
    #            [get_logout]           log user out, send to index.html 
    # ================================================================================== 
    
    def get_home(self):
        user = self.user_manager.check_user(request)
        if user:            
            return render_template("index.html", user=user)  # Redirect to index.html
        return render_template("login.html")

    def index(self):
        return None

    def get_login(self):
        if request.method == "POST":
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            token = self.user_manager.login(username, password)
            if token:
                response = jsonify(success=True)
                response.set_cookie(
                    'token',
                    token,
                    httponly=True,
                    secure=False,     
                    samesite='Strict',
                    max_age=3600      
                )
                return response
            
            return jsonify(error="Incorrect user data, try again"), 401

        return render_template("login.html")

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
    #            [get_cli]              redirect to the admin config terminal
    #            [get_command_forge]    redirect to the command forge page
    # ================================================================================== 

    def get_cli(self):
        # Check if the user is authenticated
        user = self.user_manager.check_user(request)
        if user:
            return render_template("sites/shell.html")
        
        return render_template("login.html")
    
    def get_database(self):
        # Check if the user is authenticated
        user = self.user_manager.check_user(request)
        if user:
            return render_template("sites/database.html")
        
        return render_template("login.html")
    
    def get_command_forge(self):
        # TODO: implement the command forge functionality
        return jsonify({"message": "Command forge functionality is not implemented yet."}), 501