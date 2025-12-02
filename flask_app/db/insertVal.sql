-- =============================================
-- SAFE DUMMY DATA – works every time, no hard-coded IDs
-- =============================================

-- 1. Categories (idempotent – ignores duplicates because of UNIQUE)
INSERT IGNORE INTO category (category_name) VALUES
('Fiction'), ('Science Fiction'), ('Mystery & Thriller'), ('Romance'),
('Non-Fiction'), ('History'), ('Biography'), ('Self-Help'),
('Fantasy'), ('Computer Science');

-- 2. Publishers
INSERT IGNORE INTO publisher (publisher_name) VALUES
('Penguin Random House'), ('HarperCollins'), ('Simon & Schuster'),
('Hachette Book Group'), ('Macmillan'), ('O''Reilly Media'), ('Bloomsbury');

-- 3. Authors
INSERT IGNORE INTO author_info (author_name) VALUES
('George Orwell'), ('J.K. Rowling'), ('Agatha Christie'), ('Stephen King'),
('Yuval Noah Harari'), ('Michelle Obama'), ('Brandon Sanderson'),
('Colleen Hoover'), ('Andrzej Sapkowski'), ('Robert C. Martin');

-- 4. Books – using sub-queries so it always finds the correct IDs
INSERT IGNORE INTO books (isbn_no, book_title, category_id, publisher_id) VALUES
('978-0141036144', '1984', 
    (SELECT category_id FROM category WHERE category_name = 'Fiction'),
    (SELECT publisher_id FROM publisher WHERE publisher_name = 'Penguin Random House')),

('978-0545010221', 'Harry Potter and the Philosopher''s Stone',
    (SELECT category_id FROM category WHERE category_name = 'Fantasy'),
    (SELECT publisher_id FROM publisher WHERE publisher_name = 'Bloomsbury')),

('978-0007121021', 'Murder on the Orient Express',
    (SELECT category_id FROM category WHERE category_name = 'Mystery & Thriller'),
    (SELECT publisher_id FROM publisher WHERE publisher_name = 'HarperCollins')),

('978-0307743657', 'The Shining',
    (SELECT category_id FROM category WHERE category_name = 'Fiction'),
    (SELECT publisher_id FROM publisher WHERE publisher_name = 'Penguin Random House')),

('978-0062316097', 'Sapiens: A Brief History of Humankind',
    (SELECT category_id FROM category WHERE category_name = 'History'),
    (SELECT publisher_id FROM publisher WHERE publisher_name = 'HarperCollins')),

('978-1524763138', 'Becoming',
    (SELECT category_id FROM category WHERE category_name = 'Biography'),
    (SELECT publisher_id FROM publisher WHERE publisher_name = 'Penguin Random House')),

('978-0765326355', 'The Way of Kings',
    (SELECT category_id FROM category WHERE category_name = 'Fantasy'),
    (SELECT publisher_id FROM publisher WHERE publisher_name = 'Macmillan')),

('978-1501110368', 'It Ends With Us',
    (SELECT category_id FROM category WHERE category_name = 'Romance'),
    (SELECT publisher_id FROM publisher WHERE publisher_name = 'Simon & Schuster')),

('978-0316029186', 'The Witcher: The Last Wish',
    (SELECT category_id FROM category WHERE category_name = 'Fantasy'),
    (SELECT publisher_id FROM publisher WHERE publisher_name = 'Hachette Book Group')),

('978-0132350884', 'Clean Code',
    (SELECT category_id FROM category WHERE category_name = 'Computer Science'),
    (SELECT publisher_id FROM publisher WHERE publisher_name = 'O''Reilly Media'));

-- 5. Book ↔ Authors (also safe with sub-queries)
INSERT IGNORE INTO book_authors (book_id, author_id) VALUES
((SELECT book_id FROM books WHERE isbn_no='978-0141036144'), (SELECT author_id FROM author_info WHERE author_name='George Orwell')),
((SELECT book_id FROM books WHERE isbn_no='978-0545010221'), (SELECT author_id FROM author_info WHERE author_name='J.K. Rowling')),
((SELECT book_id FROM books WHERE isbn_no='978-0007121021'), (SELECT author_id FROM author_info WHERE author_name='Agatha Christie')),
((SELECT book_id FROM books WHERE isbn_no='978-0307743657'), (SELECT author_id FROM author_info WHERE author_name='Stephen King')),
((SELECT book_id FROM books WHERE isbn_no='978-0062316097'), (SELECT author_id FROM author_info WHERE author_name='Yuval Noah Harari')),
((SELECT book_id FROM books WHERE isbn_no='978-1524763138'), (SELECT author_id FROM author_info WHERE author_name='Michelle Obama')),
((SELECT book_id FROM books WHERE isbn_no='978-0765326355'), (SELECT author_id FROM author_info WHERE author_name='Brandon Sanderson')),
((SELECT book_id FROM books WHERE isbn_no='978-1501110368'), (SELECT author_id FROM author_info WHERE author_name='Colleen Hoover')),
((SELECT book_id FROM books WHERE isbn_no='978-0316029186'), (SELECT author_id FROM author_info WHERE author_name='Andrzej Sapkowski')),
((SELECT book_id FROM books WHERE isbn_no='978-0132350884'), (SELECT author_id FROM author_info WHERE author_name='Robert C. Martin'));

-- 6. Locations
INSERT IGNORE INTO locations (loc_district, book_shelf, shelf_level) VALUES
('Colombo', 'A', 1), ('Colombo', 'A', 2), ('Kandy',   'B', 1),
('Galle',   'C', 3), ('Jaffna',  'D', 2), ('Colombo', 'F', 4),
('Kandy',   'E', 1), ('Galle',   'A', 5), ('Colombo', 'B', 3),
('Matara',  'C', 2);

-- 7. One physical copy of each book in the library
INSERT IGNORE INTO books_location (book_id, loc_id, create_date, book_status) VALUES
((SELECT book_id FROM books WHERE isbn_no='978-0141036144'), (SELECT loc_id FROM locations WHERE loc_district='Colombo' AND book_shelf='A' AND shelf_level=1), '2024-01-15', 'O'),
((SELECT book_id FROM books WHERE isbn_no='978-0545010221'), (SELECT loc_id FROM locations WHERE loc_district='Colombo' AND book_shelf='A' AND shelf_level=2), '2024-02-20', 'L'),
((SELECT book_id FROM books WHERE isbn_no='978-0007121021'), (SELECT loc_id FROM locations WHERE loc_district='Kandy'   AND book_shelf='B' AND shelf_level=1), '2024-03-10', 'O'),
((SELECT book_id FROM books WHERE isbn_no='978-0307743657'), (SELECT loc_id FROM locations WHERE loc_district='Galle'   AND book_shelf='C' AND shelf_level=3), '2024-04-05', 'O'),
((SELECT book_id FROM books WHERE isbn_no='978-0062316097'), (SELECT loc_id FROM locations WHERE loc_district='Jaffna'  AND book_shelf='D' AND shelf_level=2), '2024-05-12', 'O'),
((SELECT book_id FROM books WHERE isbn_no='978-1524763138'), (SELECT loc_id FROM locations WHERE loc_district='Colombo' AND book_shelf='F' AND shelf_level=4), '2024-06-18', 'L'),
((SELECT book_id FROM books WHERE isbn_no='978-0765326355'), (SELECT loc_id FROM locations WHERE loc_district='Kandy'   AND book_shelf='E' AND shelf_level=1), '2024-07-22', 'O'),
((SELECT book_id FROM books WHERE isbn_no='978-1501110368'), (SELECT loc_id FROM locations WHERE loc_district='Galle'   AND book_shelf='A' AND shelf_level=5), '2024-08-30', 'O'),
((SELECT book_id FROM books WHERE isbn_no='978-0316029186'), (SELECT loc_id FROM locations WHERE loc_district='Colombo' AND book_shelf='B' AND shelf_level=3), '2024-09-15', 'O'),
((SELECT book_id FROM books WHERE isbn_no='978-0132350884'), (SELECT loc_id FROM locations WHERE loc_district='Matara'  AND book_shelf='C' AND shelf_level=2), '2024-10-01', 'O');

-- 8. Readers
INSERT IGNORE INTO reader_info (reader_name, reader_contact_phone, reader_addr) VALUES
('Amara Silva',        '0771234567', 'No 45, Galle Road, Colombo 03'),
('Kasun Perera',       '0719876543',   '123 Kandy Road, Kandy'),
('Nisansala Fernando', '0785551111', '56/2 Sea View, Galle'),
('Ruwan Jayasinghe',   '0754443322', 'Main Street, Jaffna'),
('Saman Kumara',       '0768887766', 'Temple Road, Matara');

-- 9. Current loans (status = 'L')
INSERT INTO loan_records (reader_id, books_location_id, loan_date, due_date, ret_date) VALUES
((SELECT reader_id FROM reader_info WHERE reader_name='Kasun Perera'),
 (SELECT books_location_id FROM books_location bl JOIN books b ON bl.book_id=b.book_id WHERE b.isbn_no='978-0545010221'), '2025-11-15', '2025-12-15', NULL),

((SELECT reader_id FROM reader_info WHERE reader_name='Amara Silva'),
 (SELECT books_location_id FROM books_location bl JOIN books b ON bl.book_id=b.book_id WHERE b.isbn_no='978-1524763138'), '2025-11-20', '2025-12-20', NULL);

-- 10. Some returned loans (for history)
INSERT INTO loan_records (reader_id, books_location_id, loan_date, due_date, ret_date) VALUES
((SELECT reader_id FROM reader_info WHERE reader_name='Nisansala Fernando'),
 (SELECT books_location_id FROM books_location bl JOIN books b ON bl.book_id=b.book_id WHERE b.isbn_no='978-0141036144'), '2025-10-01', '2025-10-31', '2025-10-28'),

((SELECT reader_id FROM reader_info WHERE reader_name='Ruwan Jayasinghe'),
 (SELECT books_location_id FROM books_location bl JOIN books b ON bl.book_id=b.book_id WHERE b.isbn_no='978-0007121021'), '2025-09-10', '2025-10-10', '2025-10-05'),

((SELECT reader_id FROM reader_info WHERE reader_name='Saman Kumara'),
 (SELECT books_location_id FROM books_location bl JOIN books b ON bl.book_id=b.book_id WHERE b.isbn_no='978-0765326355'), '2025-08-20', '2025-09-20', '2025-09-18');