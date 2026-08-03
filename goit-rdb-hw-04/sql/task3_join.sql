-- =====================================================================
--  Завдання 3. INNER JOIN усіх 8 таблиць бази з Теми 3 (mydb)
--  Спільні ключі:
--    order_details.order_id   = orders.id
--    orders.customer_id       = customers.id
--    orders.employee_id       = employees.employee_id
--    orders.shipper_id        = shippers.id
--    order_details.product_id = products.id
--    products.category_id     = categories.id
--    products.supplier_id     = suppliers.id
-- =====================================================================
USE mydb;

SELECT *
FROM order_details
INNER JOIN orders     ON order_details.order_id   = orders.id
INNER JOIN customers  ON orders.customer_id       = customers.id
INNER JOIN employees  ON orders.employee_id       = employees.employee_id
INNER JOIN shippers   ON orders.shipper_id        = shippers.id
INNER JOIN products   ON order_details.product_id = products.id
INNER JOIN categories ON products.category_id     = categories.id
INNER JOIN suppliers  ON products.supplier_id     = suppliers.id;
