# goit-rdb-hw-03

Домашнє завдання до Теми 3 — **Завантаження даних та основи SQL. DQL-команди**.
Набір SQL-запитів (DQL) до датасету, завантаженого з CSV у Темі 3 (схема `mydb`,
таблиці `products`, `shippers` тощо).

Повний текст SQL-коду: [`sql/queries.sql`](sql/queries.sql).

> Усі 6 команд перевірено на MySQL 8.4 — виконуються без помилок і повертають потрібні дані.

## Передумова — датасет Теми 3

У MySQL Workbench має бути завантажений датасет із Теми 3 (Northwind): схема `mydb` з
таблицями `products`, `shippers`, `suppliers`, `categories`, `orders`, `order_details`,
`customers`, `employees`. Перед запитами: `USE mydb;`

Для зручності датасет зібрано в один файл [`sql/dataset.sql`](sql/dataset.sql)
(згенеровано з CSV-архіву Теми 3, 8 таблиць). Достатньо відкрити його у Workbench і
виконати цілком (⚡) — усі дані завантажаться (products — 77, shippers — 3,
suppliers — 29, categories — 8, orders — 196, order_details — 518).

> ⚠️ `dataset.sql` перестворює схему `mydb`. Якщо в ній лишились таблиці з ДЗ2 —
> вони заміняться. Це нормально (скриншоти ДЗ2 вже збережені); за потреби схему ДЗ2
> легко відтворити з `goit-rdb-hw-02/sql/create_tables.sql`.

## Завдання та запити

### Завдання 1 — вибірка стовпчиків

**1a. Усі стовпчики таблиці `products`:**
```sql
SELECT * FROM products;
```

**1b. Тільки `name`, `phone` з таблиці `shippers`:**
```sql
SELECT name, phone FROM shippers;
```

### Завдання 2 — агрегати по `price`
```sql
SELECT AVG(price) AS avg_price,
       MAX(price) AS max_price,
       MIN(price) AS min_price
FROM products;
```

### Завдання 3 — унікальні `(category_id, price)`, топ-10 за спаданням `price`
```sql
SELECT DISTINCT category_id, price
FROM products
ORDER BY price DESC
LIMIT 10;
```
`DISTINCT` прибирає повторювані пари, `ORDER BY price DESC` сортує від найдорожчих,
`LIMIT 10` залишає 10 рядків.

### Завдання 4 — кількість продуктів із ціною 20–100
```sql
SELECT COUNT(*) AS products_20_100
FROM products
WHERE price BETWEEN 20 AND 100;
```
`BETWEEN 20 AND 100` включає межі (20 і 100).

### Завдання 5 — кількість продуктів і середня ціна по постачальниках
```sql
SELECT supplier_id,
       COUNT(*)   AS products_count,
       AVG(price) AS avg_price
FROM products
GROUP BY supplier_id;
```

## Очікувані результати (на реальних даних Теми 3)

| Запит | Результат |
|-------|-----------|
| 2. AVG/MAX/MIN price | avg ≈ **28.87**, max = **263.50**, min = **2.50** |
| 3. топ-10 за ціною | найдорожчий — category_id 1, price 263.50 |
| 4. COUNT price 20–100 | **36** продуктів |
| 5. GROUP BY supplier_id | 29 рядків (по одному на постачальника) з count та avg_price |

## Як виконати у MySQL Workbench

1. Підключіться до локального сервера (`Local instance 3306`).
2. **Спочатку завантажте дані:** File → Open SQL Script… → [`sql/dataset.sql`](sql/dataset.sql)
   → виконати цілком (⚡). У панелі SCHEMAS оновіть (🔄) — з'явиться `mydb` з 8 таблицями.
3. **Потім запити:** File → Open SQL Script… → [`sql/queries.sql`](sql/queries.sql).
4. Виконуйте запити по черзі (курсор на запиті → ⚡ *Execute Current Statement*),
   щоб бачити результат кожного окремо.
5. Для кожного запиту зробіть скриншот **самого запиту та його результату**.

## Скриншоти в `screenshots/`

Пронумеровані за завданнями:

| Файл             | Завдання |
|------------------|----------|
| `p1_products.png`, `p1_shippers.png` | 1a та 1b |
| `p2_aggregates.png` | 2 |
| `p3_distinct_top10.png` | 3 |
| `p4_between.png` | 4 |
| `p5_group_by_supplier.png` | 5 |
