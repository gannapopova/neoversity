-- =====================================================================
--  Завдання 2. DML — наповнення таблиць тестовими даними
-- =====================================================================
USE LibraryManagement;

-- Автори
INSERT INTO authors (author_name) VALUES
    ('Тарас Шевченко'),
    ('Ліна Костенко');

-- Жанри
INSERT INTO genres (genre_name) VALUES
    ('Поезія'),
    ('Роман');

-- Книги
-- Примітка: тип YEAR у MySQL підтримує роки 1901–2155, тож для тестових
-- даних беремо роки видань у цьому діапазоні.
INSERT INTO books (title, publication_year, author_id, genre_id) VALUES
    ('Кобзар (видання)',  1961, 1, 1),
    ('Маруся Чурай',      1979, 2, 2);

-- Користувачі
INSERT INTO users (username, email) VALUES
    ('oksana',  'oksana@example.com'),
    ('andrii',  'andrii@example.com');

-- Видані книги
INSERT INTO borrowed_books (book_id, user_id, borrow_date, return_date) VALUES
    (1, 1, '2024-01-10', '2024-01-24'),
    (2, 2, '2024-02-05', NULL);

-- Перевірка
SELECT * FROM authors;
SELECT * FROM genres;
SELECT * FROM books;
SELECT * FROM users;
SELECT * FROM borrowed_books;
