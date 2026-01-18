-- Справочники
CREATE TABLE IF NOT EXISTS order_statuses (
    id SERIAL PRIMARY KEY,
    code INTEGER UNIQUE,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS order_priorities (
    id SERIAL PRIMARY KEY,
    code INTEGER UNIQUE,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS payment_methods (
    id SERIAL PRIMARY KEY,
    code INTEGER UNIQUE,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS payment_statuses (
    id SERIAL PRIMARY KEY,
    code INTEGER UNIQUE,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS delivery_types (
    id SERIAL PRIMARY KEY,
    code INTEGER UNIQUE,
    name VARCHAR(255),
    has_address BOOLEAN
);

CREATE TABLE IF NOT EXISTS order_sources (
    id SERIAL PRIMARY KEY,
    code INTEGER UNIQUE,
    name VARCHAR(255)
);

-- Основные таблицы
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id INTEGER REFERENCES categories(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    name VARCHAR(255) NOT NULL,
    quantity INTEGER DEFAULT 0,
    price DECIMAL(12, 2)
);

CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES clients(id),
    order_number VARCHAR(100) UNIQUE,
    subtotal DECIMAL(12, 2),
    discount_amount DECIMAL(12, 2),
    tax_amount DECIMAL(12, 2),
    shipping_amount DECIMAL(12, 2),
    total_amount DECIMAL(12, 2),
    paid_amount DECIMAL(12, 2),
    delivery_address TEXT,
    city VARCHAR(100),
    zipcode VARCHAR(20),
    recipient_name VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(100),
    tracking_number VARCHAR(100),
    order_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_id INTEGER REFERENCES order_statuses(id),
    priority_id INTEGER REFERENCES order_priorities(id),
    payment_method_id INTEGER REFERENCES payment_methods(id),
    payment_status_id INTEGER REFERENCES payment_statuses(id),
    delivery_type_id INTEGER REFERENCES delivery_types(id),
    source_id INTEGER REFERENCES order_sources(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_id INTEGER REFERENCES products(id),
    product_name TEXT,
    quantity INTEGER,
    unit_price DECIMAL(12, 2),
    discount_percent INTEGER,
    discount_amount DECIMAL(12, 2),
    total_price DECIMAL(12, 2),
    variant JSONB
);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    payment_method_id INTEGER REFERENCES payment_methods(id),
    transaction_id VARCHAR(255),
    amount DECIMAL(12, 2),
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_status_history (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    status_id INTEGER REFERENCES order_statuses(id),
    changed_by VARCHAR(255),
    notes TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_comments (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    author_name VARCHAR(255),
    comment_text TEXT,
    is_internal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);