CREATE TABLE Warehouses (
    warehouse_id INT PRIMARY KEY,
    warehouse_adress VARCHAR(255),
    capacity INT,
    type VARCHAR(50)
);

CREATE TABLE Suppliers (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(255),
    contact_info VARCHAR(255)
);

CREATE TABLE Categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(255)
);

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    phone VARCHAR(50),
    email VARCHAR(255),
    registration_date DATE,
    customer_name VARCHAR(255)
);

CREATE TABLE Supplies (
    supply_id INT PRIMARY KEY,
    warehouse_id INT REFERENCES Warehouses(warehouse_id),
    supplier_id INT REFERENCES Suppliers(supplier_id),
    supply_date DATE
);

CREATE TABLE Items (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(255),
    category_id INT REFERENCES Categories(category_id),
    price DECIMAL(10,2),
    stock_quantity INT,
    mass DECIMAL(10,2)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES Customers(customer_id),
    description TEXT,
    order_date DATE,
    delivery VARCHAR(255)
);

CREATE TABLE SupplyItems (
    income_id INT PRIMARY KEY,
    supply_id INT REFERENCES Supplies(supply_id),
    item_id INT REFERENCES Items(item_id),
    quantity INT
);

CREATE TABLE OrderItems (
    position_id INT PRIMARY KEY,
    item_id INT REFERENCES Items(item_id),
    order_id INT REFERENCES Orders(order_id),
    amount INT
);
