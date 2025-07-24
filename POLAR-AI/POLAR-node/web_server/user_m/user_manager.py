# web_server/user_m/user_manager.py

import jwt
import datetime
import threading
from werkzeug.security import check_password_hash
from data_m.database import Database

class UserManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(UserManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, secret_key="your-secret-key"):
        if hasattr(self, 'initialized') and self.initialized:
            return # Already initialized
        # Initialize the singleton instance
        
        self.db = Database()
        self.initialized = True
        self.secret_key = secret_key

    def authenticate(self, username: str, password: str):
        user = self.db.t_users.get_user(username)

        if user:
            print("Stored hashed password:", user["password"])
            print("Password entered by the user:", password)

            if check_password_hash(user["password"], password):
                return True

        return False
    
    # ========================================================
    #     working with the request to get the token
    # ========================================================
    
    def get_token_from_cookie(self, request):
        token = request.cookies.get("token")
        return token


    def get_request_token(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            return token
        return None
    
    def check_user(self, request):
        token = self.get_token_from_cookie(request)
        if not token:
            token = self.get_request_token(request)  # fallback to Authorization header
        
        if token:
            user = self.get_user(token)
            if user:
                return user
        return None


    # ========================================================
    #     working with the user login and token generation
    # ========================================================

    def generate_token(self, username: str):
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        payload = {
            'username': username,
            'exp': expiration_time
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')

        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token

    def login(self, username: str, password: str):
        if self.authenticate(username, password):
            token = self.generate_token(username)
            # database: INSERT INTO sessions VALUES(username, token)
            self.db.t_sessions.save_session(username=username, token=token)
            return token
        return None

    def logout(self, token):
        # database: DELETE FROM sessions WHERE token = %s
        query = self.db.t_sessions.delete_session(token)
        if query:
            return {'status': 'success'}, 200 # TODO: CHANGE THIS TO TRUE/FALSE, JSON TO API
        return {'status': 'not found'}, 404

    def get_user(self, token):
        # database: SELECT FROM sessions WHERE token = %s
        session_query = self.db.t_sessions.get_session(token)
        if session_query != None:
            user = session_query["username"]
            # database: SELECT FROM users WHERE username = %s
            user_query = self.db.t_users.get_user(user)
            return user_query
        return None

    # ========================================================
    #     working with the tokens to extract the username
    # ========================================================

    def _get_username_from_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            username = payload.get('username')
            return username
        
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None