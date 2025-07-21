from werkzeug.security import generate_password_hash
import json
 
# Solicitar la contraseña al usuario
password = input("Introduce la contraseña: ")
 
# Generar el hash de la contraseña
hashed_password = generate_password_hash(password)
 
print(f"contraseña hash: {hashed_password}")