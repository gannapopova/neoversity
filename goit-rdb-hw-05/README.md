# goit-rdb-hw-05

Домашнє завдання до Теми 5 — **Вкладені запити. Повторне використання коду**.
Вкладені запити (subqueries) в `SELECT`, `WHERE`, `FROM`, оператор `WITH` (CTE) та
збережена функція. База даних — `mydb` (датасет Теми 3 / Northwind).

Повний текст SQL: [`sql/queries.sql`](sql/queries.sql).

> Усі 5 запитів перевірено на MySQL 8.4 — виконуються й дають очікуваний результат.

## Передумова

Має бути завантажений датасет Теми 3 (схема `mydb`). Його зібрано у
[`../goit-rdb-hw-03/sql/dataset.sql`](../goit-rdb-hw-03/sql/dataset.sql). Перед запитами:
`USE mydb;`

## Завдання та запити

### Завдання 1 — вкладений запит у `SELECT`
Для кожного рядка `order_details` додаємо `customer_id` відповідного замовлення.
```sql
SELECT order_details.*,
       (SELECT orders.customer_id FROM orders WHERE orders.id = order_details.order_id) AS customer_id
FROM order_details;
```
Результат: **518 рядків** (усі рядки order_details + колонка customer_id).

### Завдання 2 — вкладений запит у `WHERE`
Лише ті `order_details`, чиє замовлення має `shipper_id = 3`.
```sql
SELECT *
FROM order_details
WHERE order_id IN (SELECT id FROM orders WHERE shipper_id = 3);
```
Результат: **181 рядок**.

### Завдання 3 — вкладений запит у `FROM`
З рядків `quantity > 10` рахуємо середню кількість, згруповану за `order_id`.
```sql
SELECT temp.order_id, AVG(temp.quantity) AS avg_quantity
FROM (SELECT order_id, quantity FROM order_details WHERE quantity > 10) AS temp
GROUP BY temp.order_id;
```

### Завдання 4 — те саме через `WITH` (CTE)
```sql
WITH temp AS (
    SELECT order_id, quantity FROM order_details WHERE quantity > 10
)
SELECT temp.order_id, AVG(temp.quantity) AS avg_quantity
FROM temp
GROUP BY temp.order_id;
```
Результат ідентичний Завданню 3 (перевірено). Потребує MySQL 8.0+.

### Завдання 5 — функція ділення (FLOAT)
Функція з двома параметрами `FLOAT`, що ділить перший на другий; застосована до
`order_details.quantity` (другий параметр — 2).
```sql
DROP FUNCTION IF EXISTS divide_values;
DELIMITER //
CREATE FUNCTION divide_values(a FLOAT, b FLOAT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    RETURN a / b;
END //
DELIMITER ;

SELECT quantity, divide_values(quantity, 2) AS quantity_divided
FROM order_details;
```
Приклад: 12 → 6, 5 → 2.5, 9 → 4.5.

> У MySQL Workbench блок `CREATE FUNCTION` із `DELIMITER` виконується цілком (не по
> одному рядку). `DETERMINISTIC` потрібен, щоб функція створилася при увімкненому
> бінарному лозі.

## Скриншоти в `screenshots/`

| Файл | Завдання |
|---|---|
| `p1_select_subquery.png` | 1 — subquery у SELECT |
| `p2_where_subquery.png` | 2 — subquery у WHERE |
| `p3_from_subquery.png` | 3 — subquery у FROM |
| `p4_with_cte.png` | 4 — WITH (CTE) |
| `p5_function.png` | 5 — функція divide_values |
