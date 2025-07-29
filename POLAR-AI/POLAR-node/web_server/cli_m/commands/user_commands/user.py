# web_server/cli_m/commands/system_commands/user.py

from data_m.database import Database
from cli_m.commands.general_func import extract_arguments, normalize_role
db = Database()

def list_users(arg=None, user_context=None):
    output = []

    role = extract_arguments(arg, "r") if arg else None

    if role:
        role = normalize_role(role)
        output.append(f"Listing users with role: {role}")
        users = db.t_users.get_users_by_role(role)
        if not users:
            output.append("No users found with the specified role.")
            return "\n".join(output)
    else:
        output.append("Listing all users")
        users = db.t_users.get_all_users()
        if not users:
            output.append("No users found.")
            return "\n".join(output)

    output.append(f"Total users: {len(users)}")
    output.append("-" * 63)

    # Table header
    output.append(
        f"{'Username'.ljust(20)} {'Role'.ljust(12)} {'Created At'}"
    )
    output.append("-" * 63)

    for user in users:
        output.append(
            f"{user['username'].ljust(20)} "
            f"{user['role'].ljust(12)} "
            f"{user['created_at']}"
        )

    output.append("-" * 63)
    return "\n".join(output)

def print_info(user_context=None, arg=None):

    username = extract_arguments(arg, "n")

    user = db.t_users.get_user(username)
    if not user:
        return f"User '{username}' not found."

    output = [
        f"User Information for '{username}':",
        "-" * 63,
        f"{'Username:'.ljust(15)} {user['username']}",
        f"{'Role:'.ljust(15)} {user['role']}",
        f"{'Created At:'.ljust(15)} {user['created_at']}",
        "-" * 63
    ]
    return "\n".join(output)

def add_user(user_context=None, arg=None):

    username = extract_arguments(arg, "n")
    password = extract_arguments(arg, "p")
    role = extract_arguments(arg, "r") or 1  # Default to role

    try:
        role = int(role)
    except ValueError:
        return f"Invalid role '{role}'. Must be an integer."

    if db.t_users.get_user(username):
        return f"User '{username}' already exists."

    if role not in db.LEVEL_TO_ROLE:
        return f"Invalid role '{role}'. Valid roles are: {', '.join(str(k) for k in db.LEVEL_TO_ROLE.keys())}."

    success = db.t_users.add_user(username, password, role)
    if success:
        return f"User '{username}' added successfully."
    else:
        return f"Failed to add user '{username}'."
    
def update_user(user_context=None, arg=None):

    username = extract_arguments(arg, "username")
    new_name = extract_arguments(arg, "n") or None
    new_password = extract_arguments(arg, "p") or None
    new_role_str = extract_arguments(arg, "r") or None

    new_role = None
    if new_role_str:
        try:
            new_role = int(new_role_str)
        except ValueError:
            return f"Invalid role value '{new_role_str}', must be an integer."

    if not db.t_users.get_user(username):
        return f"User '{username}' not found."

    success = db.t_users.db_update_user(username, new_name, new_password, new_role)
    if success:
        return f"User '{username}' updated successfully."
    else:
        return f"Failed to update user '{username}'."

def delete_user(user_context=None, arg=None):

    username = extract_arguments(arg, "username")

    if not db.t_users.get_user(username):
        return f"User '{username}' not found."

    success = db.t_users.delete_user(username)
    if success:
        return f"User '{username}' deleted successfully."
    else:
        return f"Failed to delete user '{username}'."