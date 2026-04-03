DROP TABLE IF EXISTS OrderItems CASCADE;
DROP TABLE IF EXISTS SupplyItems CASCADE;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS Items CASCADE;
DROP TABLE IF EXISTS Supplies CASCADE;
DROP TABLE IF EXISTS Customers CASCADE;
DROP TABLE IF EXISTS Suppliers CASCADE;
DROP TABLE IF EXISTS Warehouses CASCADE;
DROP TABLE IF EXISTS Categories CASCADE;

CREATE TABLE Categories (
    category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    adult_flag BOOLEAN DEFAULT FALSE
);

CREATE TABLE Warehouses (
    warehouse_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    warehouse_address VARCHAR(255),
    capacity INT,
    type VARCHAR(50)
);

CREATE TABLE Suppliers (
    supplier_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255)
);

CREATE TABLE Customers (
    customer_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    registration_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE Items (
    item_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    category_id INT REFERENCES Categories(category_id),
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    mass DECIMAL(10,2)
);

CREATE TABLE Supplies (
    supply_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_id INT REFERENCES Suppliers(supplier_id),
    warehouse_id INT REFERENCES Warehouses(warehouse_id),
    supply_date DATE NOT NULL
);

CREATE TABLE SupplyItems (
    income_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supply_id INT REFERENCES Supplies(supply_id) ON DELETE CASCADE,
    item_id INT REFERENCES Items(item_id),
    quantity INT NOT NULL
);

CREATE TABLE Orders (
    order_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INT REFERENCES Customers(customer_id),
    description TEXT,
    order_date DATE DEFAULT CURRENT_DATE,
    delivery_needed BOOLEAN DEFAULT FALSE,
    delivery_time TIME,
    discount DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE OrderItems (
    position_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INT REFERENCES Orders(order_id) ON DELETE CASCADE,
    item_id INT REFERENCES Items(item_id),
    amount INT NOT NULL
);
