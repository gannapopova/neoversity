# goit-rdb-fp

Фінальний проєкт — **схема `pandemic`**: імпорт даних про інфекційні хвороби,
нормалізація до 3НФ, аналітичні запити, робота з датами та власна функція.

Повний текст SQL: [`sql/final_project.sql`](sql/final_project.sql).
Дані: [`data/infectious_cases.csv`](data/infectious_cases.csv) (10 520 записів).

> Усе перевірено на реальному MySQL 8.4 (на цих самих даних) — скрипт виконується
> без помилок і дає очікувані результати.

## Дані

`data/infectious_cases.csv` — по країнах/регіонах та роках, з показниками
захворюваності. Колонки (12):
`Entity, Code, Year, Number_yaws, polio_cases, cases_guinea_worm, Number_rabies,
Number_malaria, Number_hiv, Number_tuberculosis, Number_smallpox, Number_cholera_cases`.
Порожні клітинки зберігаються як `''`.

## Завдання 1 — завантаження

```sql
CREATE SCHEMA pandemic;
USE pandemic;
```
Далі — **Table Data Import Wizard**: імпорт `data/infectious_cases.csv` у таблицю
`infectious_cases` (як у Темі 3). Кількість завантажених записів:
```sql
SELECT COUNT(*) FROM infectious_cases;   -- 10521
```

## Завдання 2 — нормалізація до 3НФ (2 таблиці)

Атрибути `Entity` та `Code` повторюються в кожному рядку → виносимо їх у окрему
таблицю-довідник, а факти лишаємо з посиланням `entity_id`:

- **`entities`** — унікальні пари `Entity + Code` (**245** записів);
- **`infectious_cases_normalized`** — роки та показники + FK `entity_id → entities.id`
  (**10521** рядків).

Так усувається повторення `Entity`/`Code` (3НФ), а всі дані зберігаються без втрат.

## Завдання 3 — аналіз `Number_rabies`

Для кожної унікальної `Entity`/`Code` — AVG, MIN, MAX, SUM за `Number_rabies`
(порожні `''` відфільтровано), сортування за середнім спаданням, топ-10:

```sql
SELECT e.entity, e.code,
       AVG(CAST(n.Number_rabies AS DECIMAL(15,4))) AS avg_rabies,
       MIN(CAST(n.Number_rabies AS DECIMAL(15,4))) AS min_rabies,
       MAX(CAST(n.Number_rabies AS DECIMAL(15,4))) AS max_rabies,
       SUM(CAST(n.Number_rabies AS DECIMAL(15,4))) AS sum_rabies
FROM infectious_cases_normalized n
JOIN entities e ON e.id = n.entity_id
WHERE n.Number_rabies <> ''
GROUP BY e.id, e.entity, e.code
ORDER BY avg_rabies DESC
LIMIT 10;
```
Топ за середнім: **World**, Lower Middle Income (WB), South Asia (WB), … **India**.

## Завдання 4 — різниця в роках (вбудовані функції)

```sql
SELECT `Year`,
       MAKEDATE(`Year`, 1)                                 AS year_start_date,   -- 1996 -> 1996-01-01
       CURDATE()                                           AS current_date_value,
       TIMESTAMPDIFF(YEAR, MAKEDATE(`Year`, 1), CURDATE()) AS years_difference
FROM infectious_cases_normalized;
```
- `MAKEDATE(Year, 1)` — 1 січня відповідного року;
- `CURDATE()` — поточна дата;
- `TIMESTAMPDIFF(YEAR, ...)` — різниця в роках.

## Завдання 5 — власна функція

```sql
DROP FUNCTION IF EXISTS year_difference;
DELIMITER //
CREATE FUNCTION year_difference(year_value INT)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN TIMESTAMPDIFF(YEAR, MAKEDATE(year_value, 1), CURDATE());
END //
DELIMITER ;

SELECT `Year`, year_difference(`Year`) AS years_difference
FROM infectious_cases_normalized;
```
Функція приймає рік і повертає різницю в роках між поточною датою та 1 січня цього року.

## Як виконати у MySQL Workbench

1. Виконайте початок `sql/final_project.sql` (CREATE SCHEMA pandemic; USE pandemic;).
2. **Table Data Import Wizard** → імпортуйте `data/infectious_cases.csv` у таблицю
   `infectious_cases`.
3. Виконайте решту `sql/final_project.sql` по секціях, роблячи скриншоти запитів+результатів.

## Скриншоти в `screenshots/`

| Файл | Завдання |
|---|---|
| `p1_import_count.png` | 1 — завантаження даних + `COUNT(*) FROM infectious_cases` (10521) |
| `p2_1_entities.png` | 2 — нормалізована таблиця `entities` (245) |
| `p2_2_normalized.png` | 2 — нормалізована таблиця `infectious_cases_normalized` |
| `p3_rabies_stats.png` | 3 — топ-10 за середнім Number_rabies |
| `p4_year_diff.png` | 4 — колонки дат і різниця в роках |
| `p5_function.png` | 5 — власна функція year_difference |
