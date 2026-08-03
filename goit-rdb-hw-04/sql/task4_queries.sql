-- =====================================================================
--  Завдання 4. Запити на основі об'єднання з Завдання 3
-- =====================================================================
USE mydb;

-- ---------------------------------------------------------------------
-- 4.1. Скільки рядків повертає об'єднання (COUNT)
-- ---------------------------------------------------------------------
SELECT COUNT(*) AS rows_count
FROM order_details
INNER JOIN orders     ON order_details.order_id   = orders.id
INNER JOIN customers  ON orders.customer_id       = customers.id
INNER JOIN employees  ON orders.employee_id       = employees.employee_id
INNER JOIN shippers   ON orders.shipper_id        = shippers.id
INNER JOIN products   ON order_details.product_id = products.id
INNER JOIN categories ON products.category_id     = categories.id
INNER JOIN suppliers  ON products.supplier_id     = suppliers.id;

-- ---------------------------------------------------------------------
-- 4.2. Заміна кількох INNER на LEFT JOIN — як зміниться кількість рядків?
--      (пояснення — у answers.md)
-- ---------------------------------------------------------------------
SELECT COUNT(*) AS rows_count_left
FROM order_details
LEFT JOIN orders     ON order_details.order_id   = orders.id
LEFT JOIN customers  ON orders.customer_id       = customers.id
LEFT JOIN employees  ON orders.employee_id       = employees.employee_id
LEFT JOIN shippers   ON orders.shipper_id        = shippers.id
LEFT JOIN products   ON order_details.product_id = products.id
LEFT JOIN categories ON products.category_id     = categories.id
LEFT JOIN suppliers  ON products.supplier_id     = suppliers.id;

-- ---------------------------------------------------------------------
-- 4.3. Тільки рядки, де employee_id > 3 та <= 10
-- ---------------------------------------------------------------------
SELECT *
FROM order_details
INNER JOIN orders     ON order_details.order_id   = orders.id
INNER JOIN customers  ON orders.customer_id       = customers.id
INNER JOIN employees  ON orders.employee_id       = employees.employee_id
INNER JOIN shippers   ON orders.shipper_id        = shippers.id
INNER JOIN products   ON order_details.product_id = products.id
INNER JOIN categories ON products.category_id     = categories.id
INNER JOIN suppliers  ON products.supplier_id     = suppliers.id
WHERE orders.employee_id > 3 AND orders.employee_id <= 10;

-- ---------------------------------------------------------------------
-- 4.4. Групування за назвою категорії: кількість рядків та середня
--      кількість товару (order_details.quantity)
-- ---------------------------------------------------------------------
SELECT categories.name AS category_name,
       COUNT(*)                    AS rows_count,
       AVG(order_details.quantity) AS avg_quantity
FROM order_details
INNER JOIN orders     ON order_details.order_id   = orders.id
INNER JOIN customers  ON orders.customer_id       = customers.id
INNER JOIN employees  ON orders.employee_id       = employees.employee_id
INNER JOIN shippers   ON orders.shipper_id        = shippers.id
INNER JOIN products   ON order_details.product_id = products.id
INNER JOIN categories ON products.category_id     = categories.id
INNER JOIN suppliers  ON products.supplier_id     = suppliers.id
WHERE orders.employee_id > 3 AND orders.employee_id <= 10
GROUP BY categories.name;

-- ---------------------------------------------------------------------
-- 4.5. + фільтр груп, де середня кількість товару > 21 (HAVING)
-- ---------------------------------------------------------------------
SELECT categories.name AS category_name,
       COUNT(*)                    AS rows_count,
       AVG(order_details.quantity) AS avg_quantity
FROM order_details
INNER JOIN orders     ON order_details.order_id   = orders.id
INNER JOIN customers  ON orders.customer_id       = customers.id
INNER JOIN employees  ON orders.employee_id       = employees.employee_id
INNER JOIN shippers   ON orders.shipper_id        = shippers.id
INNER JOIN products   ON order_details.product_id = products.id
INNER JOIN categories ON products.category_id     = categories.id
INNER JOIN suppliers  ON products.supplier_id     = suppliers.id
WHERE orders.employee_id > 3 AND orders.employee_id <= 10
GROUP BY categories.name
HAVING AVG(order_details.quantity) > 21;

-- ---------------------------------------------------------------------
-- 4.6. + сортування за спаданням кількості рядків
-- ---------------------------------------------------------------------
SELECT categories.name AS category_name,
       COUNT(*)                    AS rows_count,
       AVG(order_details.quantity) AS avg_quantity
FROM order_details
INNER JOIN orders     ON order_details.order_id   = orders.id
INNER JOIN customers  ON orders.customer_id       = customers.id
INNER JOIN employees  ON orders.employee_id       = employees.employee_id
INNER JOIN shippers   ON orders.shipper_id        = shippers.id
INNER JOIN products   ON order_details.product_id = products.id
INNER JOIN categories ON products.category_id     = categories.id
INNER JOIN suppliers  ON products.supplier_id     = suppliers.id
WHERE orders.employee_id > 3 AND orders.employee_id <= 10
GROUP BY categories.name
HAVING AVG(order_details.quantity) > 21
ORDER BY rows_count DESC;

-- ---------------------------------------------------------------------
-- 4.7. + вивести 4 рядки, пропустивши перший (LIMIT 4 OFFSET 1)
-- ---------------------------------------------------------------------
SELECT categories.name AS category_name,
       COUNT(*)                    AS rows_count,
       AVG(order_details.quantity) AS avg_quantity
FROM order_details
INNER JOIN orders     ON order_details.order_id   = orders.id
INNER JOIN customers  ON orders.customer_id       = customers.id
INNER JOIN employees  ON orders.employee_id       = employees.employee_id
INNER JOIN shippers   ON orders.shipper_id        = shippers.id
INNER JOIN products   ON order_details.product_id = products.id
INNER JOIN categories ON products.category_id     = categories.id
INNER JOIN suppliers  ON products.supplier_id     = suppliers.id
WHERE orders.employee_id > 3 AND orders.employee_id <= 10
GROUP BY categories.name
HAVING AVG(order_details.quantity) > 21
ORDER BY rows_count DESC
LIMIT 4 OFFSET 1;
