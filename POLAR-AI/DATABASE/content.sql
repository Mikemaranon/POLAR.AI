
-- user ADMIN
INSERT INTO users (username, password, role)
VALUES ('admin', 'pbkdf2:sha256:260000$qSDTHmM7uN6aInpW$5870269c1620466e556cf03d090f9eda04a4aa66ecc251872abb6f6f1a79680e', 'admin');

-- COMMANDS FOR POLAR NODE
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
            "function": "print_info",
            "args": {
                "n": "required"
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
            "function": "delete_user",
            "args": {
                "username": "required"
            }
        },
        "block": {
            "description": "Blocks access to a selected user",
            "function": "block_user",
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
        "test": {
            "description": "Test command for status",
            "function": "status_test"
        }
    }'::jsonb
);
