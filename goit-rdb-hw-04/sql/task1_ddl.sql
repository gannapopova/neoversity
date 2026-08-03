-- =====================================================================
--  Завдання 1. DDL — створення БД "LibraryManagement"
--  СУБД: MySQL 8.x
-- =====================================================================

DROP SCHEMA IF EXISTS LibraryManagement;
CREATE SCHEMA LibraryManagement
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE LibraryManagement;

-- Таблиця авторів
CREATE TABLE authors (
    author_id   INT AUTO_INCREMENT PRIMARY KEY,
    author_name VARCHAR(100) NOT NULL
);

-- Таблиця жанрів
CREATE TABLE genres (
    genre_id   INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL
);

-- Таблиця книг (FK на authors та genres)
CREATE TABLE books (
    book_id          INT AUTO_INCREMENT PRIMARY KEY,
    title            VARCHAR(255) NOT NULL,
    publication_year YEAR,
    author_id        INT,
    genre_id         INT,
    CONSTRAINT fk_books_author FOREIGN KEY (author_id) REFERENCES authors (author_id),
    CONSTRAINT fk_books_genre  FOREIGN KEY (genre_id)  REFERENCES genres (genre_id)
);

-- Таблиця користувачів
CREATE TABLE users (
    user_id  INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email    VARCHAR(150)
);

-- Таблиця виданих книг (FK на books та users)
CREATE TABLE borrowed_books (
    borrow_id   INT AUTO_INCREMENT PRIMARY KEY,
    book_id     INT,
    user_id     INT,
    borrow_date DATE,
    return_date DATE,
    CONSTRAINT fk_borrowed_book FOREIGN KEY (book_id) REFERENCES books (book_id),
    CONSTRAINT fk_borrowed_user FOREIGN KEY (user_id) REFERENCES users (user_id)
);

SHOW TABLES;
