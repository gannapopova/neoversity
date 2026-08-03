# goit-rdb-hw-04

Домашнє завдання до Теми 4 — **DML та DDL команди. Складні SQL вирази**.
Створення БД бібліотеки (DDL), наповнення даними (DML) та складні запити з `JOIN`.

> Увесь SQL перевірено на реальному MySQL 8.4 — команди виконуються й дають очікуваний результат.

## Структура

```
goit-rdb-hw-04/
├── README.md
├── answers.md                 # відповіді на запитання Завдання 4 (у т.ч. LEFT/RIGHT JOIN)
├── sql/
│   ├── task1_ddl.sql          # Завдання 1 — створення схеми LibraryManagement (DDL)
│   ├── task2_dml.sql          # Завдання 2 — наповнення таблиць (DML)
│   ├── task3_join.sql         # Завдання 3 — INNER JOIN усіх 8 таблиць бази Теми 3
│   └── task4_queries.sql      # Завдання 4 — 7 запитів (COUNT, LEFT/RIGHT, WHERE, GROUP BY…)
└── screenshots/               # скриншоти p1_…p4_ (див. нижче)
```

## Завдання 1 — DDL: база `LibraryManagement`

П'ять таблиць зі зв'язками (`sql/task1_ddl.sql`):

| Таблиця | PK | Зовнішні ключі |
|---|:--:|---|
| `authors` | author_id | — |
| `genres` | genre_id | — |
| `books` | book_id | `author_id → authors`, `genre_id → genres` |
| `users` | user_id | — |
| `borrowed_books` | borrow_id | `book_id → books`, `user_id → users` |

> Примітка: `publication_year` має тип `YEAR`, який у MySQL підтримує роки **1901–2155**,
> тож тестові роки видань обрано в цьому діапазоні.

## Завдання 2 — DML: тестові дані

`sql/task2_dml.sql` — по 2 рядки в кожну таблицю (автори, жанри, книги, користувачі,
видані книги).

## Завдання 3 — INNER JOIN 8 таблиць (база Теми 3)

`sql/task3_join.sql` об'єднує `order_details, orders, customers, products, categories,
employees, shippers, suppliers` за спільними ключами. Результат — **518 рядків**.

Спільні ключі:
```
order_details.order_id   = orders.id
orders.customer_id       = customers.id
orders.employee_id       = employees.employee_id
orders.shipper_id        = shippers.id
order_details.product_id = products.id
products.category_id     = categories.id
products.supplier_id     = suppliers.id
```

## Завдання 4 — запити та відповіді

`sql/task4_queries.sql` (7 запитів). Короткі результати:

| Пункт | Результат |
|---|---|
| 4.1 COUNT | **518** рядків |
| 4.2 LEFT / RIGHT | LEFT → 518 (без змін); RIGHT на `employees` → 519 (+1). Пояснення в [`answers.md`](answers.md) |
| 4.3 `employee_id > 3 AND <= 10` | **317** рядків |
| 4.4 GROUP BY категорія + COUNT + AVG(quantity) | 8 груп |
| 4.5 HAVING avg > 21 | 7 груп (відсіяно Grains/Cereals) |
| 4.6 ORDER BY rows_count DESC | Beverages, Dairy Products, … |
| 4.7 LIMIT 4 OFFSET 1 | Dairy Products, Confections, Seafood, Meat/Poultry |

Повні відповіді на запитання — у [`answers.md`](answers.md).

## Передумова для Завдань 3–4

Має бути завантажений датасет Теми 3 (схема `mydb`). Його зібрано у
[`../goit-rdb-hw-03/sql/dataset.sql`](../goit-rdb-hw-03/sql/dataset.sql) — виконайте його
у Workbench перед Завданнями 3–4.

## Як виконати у MySQL Workbench

1. `task1_ddl.sql` → ⚡ (створює схему `LibraryManagement`).
2. `task2_dml.sql` → ⚡ (наповнює таблиці).
3. Переконайтесь, що є схема `mydb` (Тема 3); за потреби виконайте `dataset.sql`.
4. `task3_join.sql`, потім `task4_queries.sql` — виконуйте запити по одному
   (курсор на запиті → ⚡ Execute Current Statement) і робіть скриншоти запиту + результату.

## Скриншоти в `screenshots/`

| Файл | Що |
|---|---|
| `p1_tables.png` | створені таблиці `LibraryManagement` (DDL) |
| `p2_data.png` | заповнені таблиці (DML) |
| `p3_join.png` | результат INNER JOIN 8 таблиць |
| `p4_1_count.png` … `p4_7_limit.png` | результати 7 запитів Завдання 4 |
