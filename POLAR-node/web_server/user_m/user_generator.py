from werkzeug.security import generate_password_hash
import json


with open('web_server/data_m/users.json', 'r') as f:
    users = json.load(f)

username = input("Introduce el nombre de usuario: ")

password = input("Introduce la contraseña: ")

hashed_password = generate_password_hash(password)

users[username] = {"password": hashed_password}

with open('web_server/data_m/users.json', 'w') as f:
    json.dump(users, f, indent=4)

print(f"Usuario {username} añadido con la contraseña hasheada.")