from data_m.database import Database
db = Database()
LEVEL_TO_ROLE = db.LEVEL_TO_ROLE
ROLE_TO_LEVEL = db.ROLE_TO_LEVEL

def extract_arguments(args_list, arg):
    if isinstance(args_list, dict) and arg in args_list:
        return args_list[arg]
    return None

def normalize_role(role):
    if isinstance(role, int):
        return LEVEL_TO_ROLE.get(role, None)
    if isinstance(role, str):
        # si viene string pero es número en texto, lo convertimos
        if role.isdigit():
            return LEVEL_TO_ROLE.get(int(role), None)
        return role.lower()
    return None