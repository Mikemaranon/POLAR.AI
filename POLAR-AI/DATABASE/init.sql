-- DATABASE/init.sql

-- VARIABLES
CREATE TYPE user_role AS ENUM ('user', 'trainer', 'developer', 'admin');

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role user_role NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    username INTEGER REFERENCES users(username),
    token TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- COMMANDS FOR POLAR NODE
CREATE TABLE IF NOT EXISTS commands (
    id TEXT PRIMARY KEY,
    module TEXT NOT NULL,
    function TEXT NULL,
    sub_commands JSONB
);

INSERT INTO commands (id, module, function, sub_commands)
VALUES (
    'user',
    'user_commands',
    NULL,
    '{
        "list": {
            "description": "List all users",
            "function": "list_users",
            "args": {
                "r": "not-req"
            }
        },
        "info": {
            "description": "Prints selected user info",
            "function": "print_info"
            "args": {
                "n": "required",
            }
        },
        "add": {
            "description": "Add a new user",
            "function": "add_user",
            "args": {
                "n": "required",
                "r": "required",
                "p": "required"
            }
        },
        "update": {
            "description": "Updates a selected user",
            "function": "update_user",
            "args": {
                "username": "required",
                "n": "required",
                "r": "not-req",
                "p": "required"
            }
        },
        "delete": {
            "description": "Deletes a selected user",
            "function": "delete_user"
            "args": {
                "username": "required"
            }
        },
        "block": {
            "description": "Blocks access to a selected user",
            "function": "block_user"
            "args": {
                "username": "required", 
                "t": "required"
            }
        },
        "help": {
            "description": "Prints all the info related to this command",
            "function": "command_help"
        }
    }'::jsonb
);

INSERT INTO commands (id, module, function, sub_commands)
VALUES (
    'status',                   -- ID
    'system_commands',          -- module
    'system_status',            -- function
    '{
        "long": {
            "description": "Prints long system status",
            "function": "system_status_long"
        },
        "short": {
            "description": "Prints short system status",
            "function": "system_status_short"
        },
    }'
);
