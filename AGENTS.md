# AIS_Shop — Информационная система магазина

PyQt6 + PostgreSQL (Docker) desktop-приложение.

## Быстрый старт

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
docker compose up -d          # PostgreSQL + pgAdmin
python sql/003_shop_schema.sql  # развернуть схему (через psql или docker cp + psql -f)
python main.py                 # запустить приложение
build_exe.bat                  # собрать .exe (dist\AIS_Shop.exe)
```

## Docker (PostgreSQL + pgAdmin)

`docker compose up -d` в корне проекта.

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
├── db.py                       # Database-синглтон (RealDictCursor, client_encoding='UTF8')
├── session.py                  # Session.current_user
├── sql/
│   └── 003_shop_schema.sql   # DDL + seed
├── database/
│   ├── __init__.py
│   └── connection.py           # DbConfig
├── repositories/
│   ├── __init__.py
│   ├── auth_repository.py
│   ├── category_repository.py
│   ├── warehouse_repository.py
│   ├── supplier_repository.py
│   ├── item_repository.py
│   ├── customer_repository.py
│   ├── order_repository.py     # get_order_detail() — joins customer
│   ├── supply_repository.py    # get_items_with_prices(), get_supply_detail()
│   └── report_repository.py
├── services/
│   ├── __init__.py
│   ├── auth_service.py         # bcrypt
│   └── pdf_reports.py          # reportlab: 8 отчётов + supply_contract() + purchase_contract()
├── ui/
│   ├── __init__.py
│   ├── styles.py               # PURPLE_STYLESHEET (пастельно-фиолетовая тема)
│   ├── dialogs.py              # BaseDialog + entity-диалоги
│   ├── login_window.py         # карточка входа 520×440
│   ├── admin_main_window.py    # 8 вкладок, showMaximized + maxWidth 1400
│   ├── user_main_window.py     # 4 вкладки, showMaximized + maxWidth 1200
│   ├── categories_tab.py       # CRUD + PDF
│   ├── warehouses_tab.py       # CRUD + PDF
│   ├── suppliers_tab.py        # CRUD + PDF
│   ├── items_tab.py            # CRUD + PDF
│   ├── customers_tab.py        # CRUD + PDF
│   ├── supplies_tab.py         # master/detail splitter + PDF + договор поставки
│   ├── orders_tab.py           # master/detail splitter + PDF + договор купли-продажи
│   ├── reports_tab.py          # сводка + 8 preview (grid 4 cols) + PDF
│   ├── user_categories_tab.py
│   ├── user_items_tab.py
│   ├── user_new_order_tab.py
│   └── user_history_tab.py     # история заказов + PDF + договор
├── dist/
│   └── AIS_Shop.exe            # .exe (~49 MB)
└── .venv/                      # virtualenv
```

## Схема БД

```sql
-- 9 таблиц + users/login_history
CREATE TABLE Categories (category_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, category_name VARCHAR(255) NOT NULL, adult_flag BOOLEAN DEFAULT FALSE);
CREATE TABLE Warehouses (warehouse_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, warehouse_address VARCHAR(255), capacity INT, type VARCHAR(50));
CREATE TABLE Suppliers (supplier_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, supplier_name VARCHAR(255) NOT NULL, contact_info VARCHAR(255));
CREATE TABLE Customers (customer_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, customer_name VARCHAR(255) NOT NULL, phone VARCHAR(50), email VARCHAR(255), registration_date DATE DEFAULT CURRENT_DATE);
CREATE TABLE Items (item_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, item_name VARCHAR(255) NOT NULL, category_id INT REFERENCES Categories(category_id), price DECIMAL(10,2) NOT NULL, stock_quantity INT DEFAULT 0, mass DECIMAL(10,2));
CREATE TABLE Supplies (supply_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, supplier_id INT REFERENCES Suppliers(supplier_id), warehouse_id INT REFERENCES Warehouses(warehouse_id), supply_date DATE NOT NULL);
CREATE TABLE SupplyItems (income_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, supply_id INT REFERENCES Supplies(supply_id) ON DELETE CASCADE, item_id INT REFERENCES Items(item_id), quantity INT NOT NULL);
CREATE TABLE Orders (order_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, customer_id INT REFERENCES Customers(customer_id), description TEXT, order_date DATE DEFAULT CURRENT_DATE, delivery_needed BOOLEAN DEFAULT FALSE, delivery_time TIME, discount DECIMAL(10,2) DEFAULT 0);
CREATE TABLE OrderItems (position_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, order_id INT REFERENCES Orders(order_id) ON DELETE CASCADE, item_id INT REFERENCES Items(item_id), amount INT NOT NULL);
CREATE TABLE users (user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, login VARCHAR(255) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL, role VARCHAR(20) NOT NULL DEFAULT 'user', is_active BOOLEAN DEFAULT TRUE);
CREATE TABLE login_history (history_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, user_id INT REFERENCES users(user_id), login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, success BOOLEAN);
```

## Пользователи

| Таблица | Назначение |
|---------|-----------|
| `users` | `login`, `password_hash` (bcrypt), `role` ('admin'/'user'), `is_active` |
| `login_history` | логи попыток входа |

Админ по умолчанию: `admin` / `admin123`

## Состояние проекта

### Реализовано
- [x] Схема БД (9 таблиц с GENERATED ALWAYS AS IDENTITY, FK, каскады)
- [x] Auth (users + bcrypt, app-level, не PostgreSQL roles)
- [x] Seed данные
- [x] Admin: 8 вкладок (CRUD), master/detail splitter для Supplies и Orders
- [x] User: 4 вкладки (read-only каталог + поиск + создание заказа + история)
- [x] PDF отчёты (reportlab): 8 видов, A4/landscape, стилизованные таблицы
- [x] PDF кнопки на каждой вкладке (прямой экспорт)
- [x] Договор поставки (supply_contract) — ч/б, поставщик/склад/позиции/подписи
- [x] Договор купли-продажи (purchase_contract) — ч/б, клиент/доставка/скидка/подписи
- [x] Кириллица в PDF: Helvetica → Arial через pdfmetrics.registerFont(TTFont(...))
- [x] Фиолетовая тема (#7C3AED), gradient header, card login, hover effects
- [x] Окна: showMaximized() + setMaximumWidth (admin 1400, user 1200)
- [x] Макет кнопок отчётов — QGridLayout (4 колонки), PDF кнопка в группе "Сводка"
- [x] Login: 520×440, заголовок «АИС Магазина бытовых товаров»
- [x] Git: 16 коммитов (01.04–26.04.2026), remote: github.com/Arrest0ron/AIS_Household_Goods.git

### Ключевые решения
- Auth через таблицу `users` + bcrypt, не через PostgreSQL roles — соответствует архитектуре аналога
- `GENERATED ALWAYS AS IDENTITY` для автоинкремента
- `RealDictCursor` + `client_encoding='UTF8'` в db.py — строки как dict, принудительная UTF-8 с сервера
- reportlab для PDF (не QPrinter) — профессиональная вёрстка
- Глобальный stylesheet НЕ использует селектор `QWidget` — крашит Qt; используем `QMainWindow, QDialog`
- Helvetica → Arial через `pdfmetrics.registerFont(TTFont('Helvetica', 'arial.ttf'))` — прозрачная замена для кириллицы во всех PDF
- Договоры — отдельные функции (не через PDFReport), свой layout, ч/б TableStyle
- PowerShell `Get-Content | docker exec -i` портит UTF-8 → `?`; используем `docker cp` + `psql -f`
- `.exe` в `dist\AIS_Shop.exe` (убить процесс перед заменой: `taskkill /f /im AIS_Shop.exe`)

### Известные проблемы
- `lab6_user` спамит в логи PostgreSQL (~каждые 5с) — НЕ от этого приложения
- При сборке PyInstaller предупреждения: `_cffi_backend` и `mx.DateTime` не найдены — не влияют на работу
