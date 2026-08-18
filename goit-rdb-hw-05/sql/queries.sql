-- =====================================================================
--  goit-rdb-hw-05 : Вкладені запити. Повторне використання коду
--  База даних: mydb (датасет Теми 3 / Northwind)
--  СУБД: MySQL 8.x
-- =====================================================================
USE mydb;

-- ---------------------------------------------------------------------
-- Завдання 1. Вкладений запит в операторі SELECT.
--   Вивести таблицю order_details і додати поле customer_id з orders
--   (для кожного рядка order_details — customer_id відповідного замовлення).
-- ---------------------------------------------------------------------
SELECT
    order_details.*,
    (SELECT orders.customer_id
     FROM orders
     WHERE orders.id = order_details.order_id) AS customer_id
FROM order_details;

-- ---------------------------------------------------------------------
-- Завдання 2. Вкладений запит в операторі WHERE.
--   Вивести order_details, залишивши лише ті рядки, у яких відповідне
--   замовлення (orders) має shipper_id = 3.
-- ---------------------------------------------------------------------
SELECT *
FROM order_details
WHERE order_id IN (
    SELECT id
    FROM orders
    WHERE shipper_id = 3
);

-- ---------------------------------------------------------------------
-- Завдання 3. Вкладений запит в операторі FROM.
--   З order_details обрати рядки з quantity > 10, а для отриманих даних
--   знайти середнє значення quantity, згрупувавши за order_id.
-- ---------------------------------------------------------------------
SELECT
    temp.order_id,
    AVG(temp.quantity) AS avg_quantity
FROM (
    SELECT order_id, quantity
    FROM order_details
    WHERE quantity > 10
) AS temp
GROUP BY temp.order_id;

-- ---------------------------------------------------------------------
-- Завдання 4. Те саме, що Завдання 3, але через оператор WITH (CTE).
--   Тимчасова таблиця temp (потребує MySQL 8.0+).
-- ---------------------------------------------------------------------
WITH temp AS (
    SELECT order_id, quantity
    FROM order_details
    WHERE quantity > 10
)
SELECT
    temp.order_id,
    AVG(temp.quantity) AS avg_quantity
FROM temp
GROUP BY temp.order_id;

-- ---------------------------------------------------------------------
-- Завдання 5. Функція з двома параметрами FLOAT, що ділить перший на
--   другий. Застосувати до order_details.quantity (другий параметр —
--   довільне число, напр. 2).
-- ---------------------------------------------------------------------
DROP FUNCTION IF EXISTS divide_values;

DELIMITER //
CREATE FUNCTION divide_values(a FLOAT, b FLOAT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    RETURN a / b;
END //
DELIMITER ;

-- Застосування функції до атрибута quantity (ділимо на 2)
SELECT
    quantity,
    divide_values(quantity, 2) AS quantity_divided
FROM order_details;
