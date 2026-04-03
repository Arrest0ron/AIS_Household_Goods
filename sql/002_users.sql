CREATE TABLE users (
    user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    login VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(10) NOT NULL CHECK (role IN ('admin', 'user')),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS login_history (
    history_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    is_success BOOLEAN NOT NULL,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (login, password_hash, role)
VALUES ('admin', '$2b$12$JquVBctX0zU69d1e8kvpvOEOd8X9g5tdCCjgk8gX5jWN3.XQAkveS', 'admin');
