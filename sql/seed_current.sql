-- Seed: текущие данные AIS_Shop (дамп 2026-06-05)
-- Использовать: psql -U ais_admin -d ais_shop_db -f sql/seed_current.sql

TRUNCATE TABLE orderitems, orders, supplyitems, supplies, items, customers, warehouses, suppliers, categories, users CASCADE;

-- categories
INSERT INTO categories (category_id, category_name, adult_flag) OVERRIDING SYSTEM VALUE VALUES (1, 'Бытовая химия', false);
INSERT INTO categories (category_id, category_name, adult_flag) OVERRIDING SYSTEM VALUE VALUES (2, 'Кухонные принадлежности', false);
INSERT INTO categories (category_id, category_name, adult_flag) OVERRIDING SYSTEM VALUE VALUES (3, 'Электроника', false);
INSERT INTO categories (category_id, category_name, adult_flag) OVERRIDING SYSTEM VALUE VALUES (4, 'Мебель', false);
INSERT INTO categories (category_id, category_name, adult_flag) OVERRIDING SYSTEM VALUE VALUES (5, 'Товары для ванной', false);
INSERT INTO categories (category_id, category_name, adult_flag) OVERRIDING SYSTEM VALUE VALUES (6, 'Инструменты', false);
INSERT INTO categories (category_id, category_name, adult_flag) OVERRIDING SYSTEM VALUE VALUES (7, 'Пиротехника', true);
INSERT INTO categories (category_id, category_name, adult_flag) OVERRIDING SYSTEM VALUE VALUES (8, 'Освещение', false);
INSERT INTO categories (category_id, category_name, adult_flag) OVERRIDING SYSTEM VALUE VALUES (9, 'Для розжига', false);

-- customers
INSERT INTO customers (customer_id, customer_name, phone, email, registration_date) OVERRIDING SYSTEM VALUE VALUES (1, 'Иванов Иван', '+7 (900) 111-11-11', 'ivanov@mail.ru', '2026-06-04');
INSERT INTO customers (customer_id, customer_name, phone, email, registration_date) OVERRIDING SYSTEM VALUE VALUES (2, 'Петрова Анна', '+7 (900) 222-22-22', 'petrova@yandex.ru', '2026-06-04');
INSERT INTO customers (customer_id, customer_name, phone, email, registration_date) OVERRIDING SYSTEM VALUE VALUES (3, 'Сидоров Петр', '+7 (900) 333-33-33', 'sidorov@bk.ru', '2026-06-04');
INSERT INTO customers (customer_id, customer_name, phone, email, registration_date) OVERRIDING SYSTEM VALUE VALUES (4, 'Козлова Мария', '+7 (900) 444-44-44', 'kozlova@mail.ru', '2026-06-04');
INSERT INTO customers (customer_id, customer_name, phone, email, registration_date) OVERRIDING SYSTEM VALUE VALUES (5, 'Смирнов Алексей', '+7 (900) 555-55-55', 'smirnov@gmail.com', '2026-06-04');
INSERT INTO customers (customer_id, customer_name, phone, email, registration_date) OVERRIDING SYSTEM VALUE VALUES (6, 'Новикова Елена', '+7 (900) 666-66-66', 'novikova@yandex.ru', '2026-06-04');

-- warehouses
INSERT INTO warehouses (warehouse_id, warehouse_address, capacity, type) OVERRIDING SYSTEM VALUE VALUES (1, 'ул. Ленина, 10', 500, 'Основной');
INSERT INTO warehouses (warehouse_id, warehouse_address, capacity, type) OVERRIDING SYSTEM VALUE VALUES (2, 'ул. Советская, 25', 300, 'Дополнительный');
INSERT INTO warehouses (warehouse_id, warehouse_address, capacity, type) OVERRIDING SYSTEM VALUE VALUES (3, 'пр. Мира, 5', 200, 'Малый');

-- suppliers
INSERT INTO suppliers (supplier_id, supplier_name, contact_info) OVERRIDING SYSTEM VALUE VALUES (1, 'ООО "БытХим"', '+7 (495) 111-22-33, bythim@mail.ru');
INSERT INTO suppliers (supplier_id, supplier_name, contact_info) OVERRIDING SYSTEM VALUE VALUES (2, 'ИП КухняПро', '+7 (495) 222-33-44, kuhnya@yandex.ru');
INSERT INTO suppliers (supplier_id, supplier_name, contact_info) OVERRIDING SYSTEM VALUE VALUES (3, 'ООО "ЭлектроМир"', '+7 (495) 333-44-55, electro@mail.ru');
INSERT INTO suppliers (supplier_id, supplier_name, contact_info) OVERRIDING SYSTEM VALUE VALUES (4, 'МебельОпт', '+7 (495) 444-55-66, mobelopt@bk.ru');
INSERT INTO suppliers (supplier_id, supplier_name, contact_info) OVERRIDING SYSTEM VALUE VALUES (5, 'СантехСнаб', '+7 (495) 555-66-77, santeh@mail.ru');
INSERT INTO suppliers (supplier_id, supplier_name, contact_info) OVERRIDING SYSTEM VALUE VALUES (6, 'ИнструментСервис', '+7 (495) 666-77-88, instrument@mail.ru');

-- items
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (1, 'Стиральный порошок 3кг', 1, 450.00, 120, 3.00);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (2, 'Средство для мытья посуды 500мл', 1, 180.00, 194, 0.50);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (3, 'Кастрюля 5л нержавейка', 2, 1200.00, 30, 2.50);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (4, 'Сковорода антипригарная 28см', 2, 1500.00, 25, 1.80);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (5, 'Чайник электрический 1.7л', 3, 2100.00, 38, 1.20);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (6, 'Утюг паровой', 3, 3500.00, 13, 2.00);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (7, 'Стол письменный', 4, 4500.00, 9, 25.00);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (8, 'Стул деревянный', 4, 2500.00, 20, 8.00);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (9, 'Полка для ванной угловая', 5, 800.00, 35, 1.50);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (10, 'Шторка для душа', 5, 1200.00, 18, 0.80);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (11, 'Набор отверток', 6, 650.00, 50, 0.60);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (12, 'Молоток 500г', 6, 400.00, 40, 0.50);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (13, 'Лампа светодиодная 12Вт', 8, 250.00, 100, 0.10);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (14, 'Люстра потолочная', 8, 3200.00, 8, 3.50);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (16, 'Люстра', 8, 110.00, 4, 4.00);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (17, 'Отбеливатель 2л', 1, 320.00, 80, 2.10);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (18, 'Гель для стирки 3л', 1, 580.00, 95, 3.20);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (19, 'Средство для пола 1л', 1, 220.00, 150, 1.10);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (20, 'Антижир 500мл', 1, 190.00, 110, 0.55);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (21, 'Набор ножей 5шт', 2, 2800.00, 18, 1.20);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (22, 'Разделочная доска', 2, 350.00, 60, 0.80);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (23, 'Контейнеры для еды 4шт', 2, 650.00, 45, 0.90);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (24, 'Блендер стационарный', 2, 4200.00, 12, 2.80);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (25, 'Мультиварка 5л', 2, 5500.00, 14, 4.50);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (26, 'Пылесос робот', 3, 18900.00, 8, 3.50);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (27, 'Фен для волос', 3, 1800.00, 35, 0.60);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (28, 'Микроволновка 20л', 3, 8500.00, 11, 12.00);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (29, 'Вентилятор напольный', 3, 2400.00, 22, 2.10);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (30, 'Шкаф 2-дверный', 4, 12000.00, 6, 45.00);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (31, 'Журнальный столик', 4, 3800.00, 9, 12.00);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (32, 'Комод 4-ярусный', 4, 8500.00, 5, 30.00);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (33, 'Зеркало с подсветкой', 5, 4500.00, 10, 3.20);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (34, 'Держатель для полотенец', 5, 650.00, 40, 0.50);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (35, 'Коврик противоскользящий', 5, 900.00, 28, 0.70);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (36, 'Дрель электрическая', 6, 3200.00, 15, 1.80);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (37, 'Рулетка 5м', 6, 180.00, 70, 0.15);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (38, 'Набор ключей 12шт', 6, 1100.00, 30, 0.90);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (39, 'Петарды 100шт', 7, 350.00, 200, 0.50);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (40, 'Фейерверк «Звезда»', 9, 1200.00, 45, 1.20);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (41, 'Бенгальские огни 10шт', 7, 150.00, 300, 0.10);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (42, 'Торшер напольный', 8, 3500.00, 10, 5.00);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (43, 'Светильник настольный', 8, 1200.00, 25, 1.20);
INSERT INTO items (item_id, item_name, category_id, price, stock_quantity, mass) OVERRIDING SYSTEM VALUE VALUES (44, 'Гирлянда LED 10м', 8, 800.00, 55, 0.30);

-- users
INSERT INTO users (user_id, login, password_hash, role, is_active, customer_id) OVERRIDING SYSTEM VALUE VALUES (1, 'admin', '$2b$12$JquVBctX0zU69d1e8kvpvOEOd8X9g5tdCCjgk8gX5jWN3.XQAkveS', 'admin', true, NULL);
INSERT INTO users (user_id, login, password_hash, role, is_active, customer_id) OVERRIDING SYSTEM VALUE VALUES (2, 'user1', '$2b$12$bQpFElAao5w65dyhkaLQueS2BKHtAztOXnR09PN3akkr6FmIT1g7G', 'user', true, 1);

-- supplies
INSERT INTO supplies (supply_id, supplier_id, warehouse_id, supply_date) OVERRIDING SYSTEM VALUE VALUES (1, 1, 1, '2026-05-10');
INSERT INTO supplies (supply_id, supplier_id, warehouse_id, supply_date) OVERRIDING SYSTEM VALUE VALUES (2, 2, 2, '2026-05-12');
INSERT INTO supplies (supply_id, supplier_id, warehouse_id, supply_date) OVERRIDING SYSTEM VALUE VALUES (3, 3, 1, '2026-05-14');
INSERT INTO supplies (supply_id, supplier_id, warehouse_id, supply_date) OVERRIDING SYSTEM VALUE VALUES (4, 4, 2, '2026-05-15');
INSERT INTO supplies (supply_id, supplier_id, warehouse_id, supply_date) OVERRIDING SYSTEM VALUE VALUES (5, 5, 3, '2026-05-17');
INSERT INTO supplies (supply_id, supplier_id, warehouse_id, supply_date) OVERRIDING SYSTEM VALUE VALUES (6, 6, 3, '2026-05-19');

-- supplyitems
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (1, 1, 1, 50);
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (2, 1, 2, 100);
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (3, 2, 3, 20);
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (4, 2, 4, 15);
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (5, 3, 5, 30);
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (6, 3, 6, 20);
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (7, 4, 7, 10);
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (8, 4, 8, 15);
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (9, 5, 9, 40);
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (10, 5, 10, 25);
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (11, 6, 11, 30);
INSERT INTO supplyitems (income_id, supply_id, item_id, quantity) OVERRIDING SYSTEM VALUE VALUES (12, 6, 12, 50);

-- orders
INSERT INTO orders (order_id, customer_id, description, order_date, delivery_needed, delivery_time, discount) OVERRIDING SYSTEM VALUE VALUES (1, 1, 'Заказ кухонной утвари', '2026-05-15', true, '10:00:00', 0.00);
INSERT INTO orders (order_id, customer_id, description, order_date, delivery_needed, delivery_time, discount) OVERRIDING SYSTEM VALUE VALUES (2, 2, 'Техника для дома', '2026-05-16', false, NULL, 5.00);
INSERT INTO orders (order_id, customer_id, description, order_date, delivery_needed, delivery_time, discount) OVERRIDING SYSTEM VALUE VALUES (3, 3, 'Мебель в гостиную', '2026-05-18', true, '14:00:00', 10.00);
INSERT INTO orders (order_id, customer_id, description, order_date, delivery_needed, delivery_time, discount) OVERRIDING SYSTEM VALUE VALUES (4, 4, 'Моющие средства', '2026-05-20', false, NULL, 0.00);
INSERT INTO orders (order_id, customer_id, description, order_date, delivery_needed, delivery_time, discount) OVERRIDING SYSTEM VALUE VALUES (5, 5, 'Инструменты', '2026-05-22', true, '09:00:00', 3.00);
INSERT INTO orders (order_id, customer_id, description, order_date, delivery_needed, delivery_time, discount) OVERRIDING SYSTEM VALUE VALUES (6, 1, 'Освещение', '2026-05-25', false, NULL, 0.00);
INSERT INTO orders (order_id, customer_id, description, order_date, delivery_needed, delivery_time, discount) OVERRIDING SYSTEM VALUE VALUES (8, 1, '', '2026-06-05', false, NULL, 0.00);
INSERT INTO orders (order_id, customer_id, description, order_date, delivery_needed, delivery_time, discount) OVERRIDING SYSTEM VALUE VALUES (9, 1, '', '2026-06-05', false, NULL, 0.00);

-- orderitems
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (1, 1, 3, 1);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (2, 1, 4, 1);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (3, 2, 5, 2);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (4, 2, 6, 1);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (5, 3, 7, 1);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (6, 3, 8, 4);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (7, 4, 1, 3);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (8, 4, 2, 2);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (9, 5, 11, 2);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (10, 5, 12, 1);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (11, 6, 13, 5);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (12, 6, 14, 1);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (13, 8, 7, 1);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (14, 9, 2, 6);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (15, 9, 5, 2);
INSERT INTO orderitems (position_id, order_id, item_id, amount) OVERRIDING SYSTEM VALUE VALUES (16, 9, 6, 2);

-- sequences
SELECT setval('categories_category_id_seq', 9);
SELECT setval('customers_customer_id_seq', 7);
SELECT setval('items_item_id_seq', 44);
SELECT setval('orders_order_id_seq', 9);
SELECT setval('orderitems_position_id_seq', 16);
SELECT setval('suppliers_supplier_id_seq', 7);
SELECT setval('supplies_supply_id_seq', 7);
SELECT setval('supplyitems_income_id_seq', 13);
SELECT setval('users_user_id_seq', 2);
SELECT setval('warehouses_warehouse_id_seq', 4);
