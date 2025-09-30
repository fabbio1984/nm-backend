
-- Para referencia si prefieres SQL directo (init_db.py ya crea esto con ORM)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(120),
    is_borrowed BOOLEAN NOT NULL DEFAULT FALSE,
    borrowed_by VARCHAR(120)
);
