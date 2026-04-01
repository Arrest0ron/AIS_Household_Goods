# AIS_Shop — Информационная система магазина

PyQt6 + PostgreSQL (Docker) desktop-приложение.

## Быстрый старт

```powershell
cd D:\Study\AIS_Shop
.venv\Scripts\activate      # активировать venv
python main.py               # запустить приложение
build_exe.bat                # собрать .exe (dist\AIS_Shop.exe)
```

## Docker (PostgreSQL + pgAdmin)

Контейнеры уже запущены. Если нет — `docker compose up -d` в корне проекта.

| Сервис       | Доступ                           |
|-------------|-----------------------------------|
| PostgreSQL  | `localhost:5432`, user: `ais_admin`, pass: `ais_admin_pass`, db: `ais_shop_db` |
| pgAdmin     | http://localhost:5050 — `admin@ais-shop.com` / `admin123` |

## Структура кода

```
AIS_Shop/
├── main.py                     # точка входа → LoginWindow
├── AGENTS.md                   # этот файл
├── requirements.txt
├── build_exe.bat
├── docker-compose.yml        # PostgreSQL + pgAdmin
├── db.py                       # Database-синглтон (RealDictCursor)
├── session.py                  # Session.current_user
├── sql/                        # DDL-скрипты
├── database/
│   ├── __init__.py
│   └── connection.py           # DbConfig
├── repositories/
│   ├── __init__.py
│   └── auth_repository.py     # AuthRepository
├── services/
│   ├── __init__.py
│   └── auth_service.py        # AuthService (bcrypt)
├── ui/
│   ├── __init__.py
│   ├── login_window.py         # форма входа
│   ├── admin_main_window.py    # 8 вкладок (админ)
│   └── user_main_window.py     # 4 вкладки (пользователь)
├── dist/
│   └── AIS_Shop.exe            # .exe (40+ MB)
└── .venv/                      # virtualenv
```

## Схема БД (развёрнута)

```sql
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
```

## Пользователи

| Таблица | Назначение |
|---------|-----------|
| `users` | `login`, `password_hash` (bcrypt), `role` ('admin'/'user'), `is_active` |
| `login_history` | логи попыток входа |

Админ по умолчанию: `admin` / `admin123`


