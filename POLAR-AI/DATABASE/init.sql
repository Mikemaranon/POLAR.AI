-- DATABASE/init.sql

-- VARIABLES
CREATE TYPE user_role AS ENUM ('user', 'trainer', 'developer', 'admin');

-- TABLES
CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role user_role NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) REFERENCES users(username),
    token TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS commands (
    id TEXT PRIMARY KEY,
    module TEXT NOT NULL,
    function TEXT NULL,
    sub_commands JSONB
);
