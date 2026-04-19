-- Example database schema for PostgreSQL
-- Modify this to match your actual database structure

-- Drop tables if they exist (for clean initialization)
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Sample data
INSERT INTO users (name, email, age) VALUES 
    ('Alice Johnson', 'alice@example.com', 28),
    ('Bob Smith', 'bob@example.com', 35),
    ('Charlie Brown', 'charlie@example.com', 42),
    ('Diana Prince', 'diana@example.com', 31),
    ('Eve Wilson', 'eve@example.com', 26);

INSERT INTO products (name, category, price, stock) VALUES
    ('Laptop', 'Electronics', 999.99, 50),
    ('Mouse', 'Electronics', 29.99, 200),
    ('Keyboard', 'Electronics', 79.99, 150),
    ('Monitor', 'Electronics', 299.99, 75),
    ('Desk Chair', 'Furniture', 199.99, 30),
    ('Standing Desk', 'Furniture', 499.99, 20),
    ('Notebook', 'Stationery', 5.99, 500),
    ('Pen Set', 'Stationery', 12.99, 300);

INSERT INTO orders (user_id, product_name, quantity, price) VALUES
    (1, 'Laptop', 1, 999.99),
    (1, 'Mouse', 2, 29.99),
    (2, 'Desk Chair', 1, 199.99),
    (2, 'Monitor', 2, 299.99),
    (3, 'Notebook', 10, 5.99),
    (3, 'Pen Set', 3, 12.99),
    (4, 'Standing Desk', 1, 499.99),
    (4, 'Keyboard', 1, 79.99),
    (5, 'Mouse', 1, 29.99),
    (5, 'Notebook', 5, 5.99);
