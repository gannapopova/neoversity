-- =====================================================================
--  goit-rdb-hw-02 : Проєктування БД з використанням семантичних моделей
--  Створення нормалізованої (3НФ) схеми на основі ER-діаграми.
--  СУБД: MySQL 8.x
--
--  Схема моделює процес замовлень інтернет-магазину, отриманий шляхом
--  нормалізації початкової таблиці замовлень до 3НФ.
-- =====================================================================

-- Створюємо та обираємо базу даних
CREATE DATABASE IF NOT EXISTS mydb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE mydb;

-- Для чистого повторного запуску прибираємо таблиці у зворотному порядку залежностей
DROP TABLE IF EXISTS order_details;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS customers;

-- ---------------------------------------------------------------------
-- 1. categories — категорії товарів
-- ---------------------------------------------------------------------
CREATE TABLE categories (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

-- ---------------------------------------------------------------------
-- 2. customers — клієнти (винесено, бо адреса залежить від клієнта, а не
--    від замовлення — усунення транзитивної залежності у 3НФ)
-- ---------------------------------------------------------------------
CREATE TABLE customers (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    contact VARCHAR(100),
    address VARCHAR(150),
    city    VARCHAR(100),
    country VARCHAR(100)
);

-- ---------------------------------------------------------------------
-- 3. products — товари. Кожен товар належить одній категорії.
-- ---------------------------------------------------------------------
CREATE TABLE products (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    price       DECIMAL(10, 2),
    category_id INT,
    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id) REFERENCES categories (id)
);

-- ---------------------------------------------------------------------
-- 4. orders — замовлення. Кожне замовлення належить одному клієнту.
-- ---------------------------------------------------------------------
CREATE TABLE orders (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    order_date  DATE NOT NULL,
    customer_id INT,
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES customers (id)
);

-- ---------------------------------------------------------------------
-- 5. order_details — позиції замовлення (зв'язкова таблиця "багато-до-багатьох"
--    між orders та products; тут зберігається кількість кожного товару).
-- ---------------------------------------------------------------------
CREATE TABLE order_details (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    order_id   INT NOT NULL,
    product_id INT NOT NULL,
    quantity   INT NOT NULL,
    CONSTRAINT fk_details_order
        FOREIGN KEY (order_id)   REFERENCES orders (id),
    CONSTRAINT fk_details_product
        FOREIGN KEY (product_id) REFERENCES products (id)
);

-- ---------------------------------------------------------------------
-- Перевірка створеної схеми
-- ---------------------------------------------------------------------
SHOW TABLES;
