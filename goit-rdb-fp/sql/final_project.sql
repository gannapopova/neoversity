-- =====================================================================
--  goit-rdb-fp : Фінальний проєкт. Схема pandemic, нормалізація,
--  аналітичні запити, робота з датами та власна функція.
--  СУБД: MySQL 8.x
-- =====================================================================

-- =====================================================================
--  ЗАВДАННЯ 1. Завантаження даних
-- =====================================================================

-- Створюємо схему та обираємо її за замовчуванням
CREATE SCHEMA IF NOT EXISTS pandemic;
USE pandemic;

-- Далі через Table Data Import Wizard імпортуємо файл infectious_cases.csv
-- у таблицю `infectious_cases` (як у Темі 3).
-- Після імпорту таблиця має 12 колонок:
--   Entity, Code, Year, Number_yaws, polio_cases, cases_guinea_worm,
--   Number_rabies, Number_malaria, Number_hiv, Number_tuberculosis,
--   Number_smallpox, Number_cholera_cases
-- (Import Wizard створює текстові колонки; порожні клітинки — це '').

-- Перегляд даних:
SELECT * FROM infectious_cases LIMIT 20;

-- Скільки записів завантажено з файла:
SELECT COUNT(*) AS total_rows FROM infectious_cases;


-- =====================================================================
--  ЗАВДАННЯ 2. Нормалізація infectious_cases до 3НФ (2 таблиці)
--  Атрибути Entity та Code постійно повторюються -> виносимо їх в
--  окрему таблицю-довідник, а факти лишаємо з посиланням (entity_id).
-- =====================================================================

-- Таблиця 1: довідник країн/сутностей (унікальні пари Entity + Code)
DROP TABLE IF EXISTS infectious_cases_normalized;
DROP TABLE IF EXISTS entities;

CREATE TABLE entities (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    entity VARCHAR(255),
    code   VARCHAR(10)
);

INSERT INTO entities (entity, code)
SELECT DISTINCT Entity, Code
FROM infectious_cases;

-- Таблиця 2: факти (роки + показники) з посиланням на entities
CREATE TABLE infectious_cases_normalized (
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    entity_id             INT,
    `Year`                INT,
    Number_yaws           VARCHAR(50),
    polio_cases           VARCHAR(50),
    cases_guinea_worm     VARCHAR(50),
    Number_rabies         VARCHAR(50),
    Number_malaria        VARCHAR(50),
    Number_hiv            VARCHAR(50),
    Number_tuberculosis   VARCHAR(50),
    Number_smallpox       VARCHAR(50),
    Number_cholera_cases  VARCHAR(50),
    CONSTRAINT fk_cases_entity FOREIGN KEY (entity_id) REFERENCES entities (id)
);

INSERT INTO infectious_cases_normalized
    (entity_id, `Year`, Number_yaws, polio_cases, cases_guinea_worm,
     Number_rabies, Number_malaria, Number_hiv, Number_tuberculosis,
     Number_smallpox, Number_cholera_cases)
SELECT e.id, ic.Year, ic.Number_yaws, ic.polio_cases, ic.cases_guinea_worm,
       ic.Number_rabies, ic.Number_malaria, ic.Number_hiv, ic.Number_tuberculosis,
       ic.Number_smallpox, ic.Number_cholera_cases
FROM infectious_cases ic
JOIN entities e
     ON e.entity = ic.Entity AND e.code = ic.Code;

-- Перевірка нормалізованих таблиць
SELECT COUNT(*) AS entities_count FROM entities;
SELECT COUNT(*) AS normalized_rows FROM infectious_cases_normalized;

-- Кількість записів у вихідній таблиці (для ментора)
SELECT COUNT(*) AS infectious_cases_count FROM infectious_cases;


-- =====================================================================
--  ЗАВДАННЯ 3. Аналіз: для кожної унікальної Entity/Code —
--  AVG, MIN, MAX, SUM за Number_rabies (порожні '' відфільтровуємо),
--  сортування за середнім спаданням, топ-10.
-- =====================================================================
SELECT
    e.entity,
    e.code,
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


-- =====================================================================
--  ЗАВДАННЯ 4. Колонка різниці в роках (вбудовані функції).
--   - дата 1 січня відповідного року (1996 -> 1996-01-01)
--   - поточна дата
--   - різниця в роках між ними
-- =====================================================================
SELECT
    `Year`,
    MAKEDATE(`Year`, 1)                                  AS year_start_date,  -- 1 січня
    CURDATE()                                            AS current_date_value,
    TIMESTAMPDIFF(YEAR, MAKEDATE(`Year`, 1), CURDATE())  AS years_difference
FROM infectious_cases_normalized;


-- =====================================================================
--  ЗАВДАННЯ 5. Власна функція: приймає рік, повертає різницю в роках
--  між поточною датою та 1 січня цього року.
-- =====================================================================
DROP FUNCTION IF EXISTS year_difference;

DELIMITER //
CREATE FUNCTION year_difference(year_value INT)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN TIMESTAMPDIFF(YEAR, MAKEDATE(year_value, 1), CURDATE());
END //
DELIMITER ;

-- Застосування функції до даних
SELECT
    `Year`,
    year_difference(`Year`) AS years_difference
FROM infectious_cases_normalized;
