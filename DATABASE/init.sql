-- DATABASE/init.sql

-- VARIABLES
CREATE TYPE user_role AS ENUM ('admin', 'trainer', 'developer', 'user');

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role user_role NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  token TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);