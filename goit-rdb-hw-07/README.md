# goit-rdb-hw-07

Домашнє завдання до Теми 7 — **Додаткові вбудовані SQL-функції. Робота з часом**.
Функції для роботи з датою/часом та JSON на таблиці `orders` бази `mydb`
(датасет Теми 3 / Northwind).

Повний текст SQL: [`sql/queries.sql`](sql/queries.sql).

> Усі 5 запитів перевірено на MySQL 8.4 — виконуються й повертають потрібні дані.

## Передумова

Має бути завантажений датасет Теми 3 (схема `mydb` з таблицею `orders`). Його зібрано у
[`../goit-rdb-hw-03/sql/dataset.sql`](../goit-rdb-hw-03/sql/dataset.sql). Перед запитами:
`USE mydb;`

## Завдання та запити

### Завдання 1 — рік, місяць, число (5 атрибутів)
```sql
SELECT id, date,
       YEAR(date)  AS `year`,
       MONTH(date) AS `month`,
       DAY(date)   AS `day`
FROM orders;
```

### Завдання 2 — додати один день
```sql
SELECT id, date,
       DATE_ADD(date, INTERVAL 1 DAY) AS date_plus_one_day
FROM orders;
```

### Завдання 3 — timestamp (секунди від початку відліку)
```sql
SELECT id, date,
       UNIX_TIMESTAMP(date) AS timestamp_seconds
FROM orders;
```
Функція **`UNIX_TIMESTAMP()`** повертає кількість секунд від епохи Unix (1970-01-01).

### Завдання 4 — кількість рядків у діапазоні дат
```sql
SELECT COUNT(*) AS rows_count
FROM orders
WHERE date BETWEEN '1996-07-10 00:00:00' AND '1996-10-08 00:00:00';
```
Результат: **72 рядки**.

### Завдання 5 — JSON-об'єкт
```sql
SELECT id, date,
       JSON_OBJECT('id', id, 'date', date) AS json_object
FROM orders;
```
Функція **`JSON_OBJECT()`** будує `{"id": <id>, "date": <date>}`.

## Скриншоти в `screenshots/`

| Файл | Завдання |
|---|---|
| `p1_year_month_day.png` | 1 — YEAR / MONTH / DAY |
| `p2_add_day.png` | 2 — DATE_ADD (+1 день) |
| `p3_timestamp.png` | 3 — UNIX_TIMESTAMP |
| `p4_count_between.png` | 4 — COUNT у діапазоні дат (72) |
| `p5_json_object.png` | 5 — JSON_OBJECT |
