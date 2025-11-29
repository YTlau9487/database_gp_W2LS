CREATE TABLE IF NOT EXISTS category (
  category_id int PRIMARY KEY AUTO_INCREMENT,
  category_name varchar(100),
  UNIQUE (category_name)
);
CREATE TABLE IF NOT EXISTS publisher (
  publisher_id int PRIMARY KEY AUTO_INCREMENT,
  publisher_name varchar(100),
  UNIQUE (publisher_name)
);
CREATE TABLE IF NOT EXISTS author_info (
  author_id int PRIMARY KEY AUTO_INCREMENT,
  author_name varchar(100),
  UNIQUE (author_name)
);
CREATE TABLE IF NOT EXISTS books (
  book_id int PRIMARY KEY AUTO_INCREMENT,
  isbn_no varchar(20),
  book_title varchar(100),
  category_id int,
  publisher_id int,
  UNIQUE (isbn_no)
);
CREATE TABLE IF NOT EXISTS book_authors (
  book_author_id int PRIMARY KEY AUTO_INCREMENT,
  book_id int,
  author_id int,
  CONSTRAINT unq_book_author UNIQUE (book_id, author_id)
);
CREATE TABLE IF NOT EXISTS locations (
  loc_id int PRIMARY KEY AUTO_INCREMENT,
  loc_district varchar(50),
  book_shelf varchar(3),
  shelf_level int,
  CONSTRAINT unq_loc UNIQUE (loc_district, book_shelf, shelf_level)
);
CREATE TABLE IF NOT EXISTS books_location (
  books_location_id int PRIMARY KEY AUTO_INCREMENT,
  book_id int,
  loc_id int,
  create_date date,
  book_status varchar(2),
  CHECK (
    book_status = 'O' 
    OR book_status = 'L' 
    OR book_status = 'D' 
  ),
  CONSTRAINT unq_book_loc UNIQUE (book_id, loc_id)
);
CREATE TABLE IF NOT EXISTS loan_records (
  loan_records_id int PRIMARY KEY AUTO_INCREMENT,
  reader_id int,
  books_location_id int,
  loan_date date,
  due_date date,
  ret_date date
);
CREATE TABLE IF NOT EXISTS reader_info (
  reader_id int PRIMARY KEY AUTO_INCREMENT,
  reader_name varchar(100),
  reader_contact_phone varchar(10),
  reader_addr varchar(200),
  CONSTRAINT unq_reader UNIQUE (reader_name, reader_contact_phone)
);
ALTER TABLE books
ADD FOREIGN KEY (publisher_id) REFERENCES publisher (publisher_id);
ALTER TABLE books
ADD FOREIGN KEY (category_id) REFERENCES category (category_id);
ALTER TABLE books_location
ADD FOREIGN KEY (loc_id) REFERENCES locations (loc_id);
ALTER TABLE books_location
ADD FOREIGN KEY (book_id) REFERENCES books (book_id);
ALTER TABLE loan_records
ADD FOREIGN KEY (reader_id) REFERENCES reader_info (reader_id);
ALTER TABLE loan_records
ADD FOREIGN KEY (books_location_id) REFERENCES books_location (books_location_id);
ALTER TABLE book_authors
ADD FOREIGN KEY (author_id) REFERENCES author_info (author_id);
ALTER TABLE book_authors
ADD FOREIGN KEY (book_id) REFERENCES books (book_id);

CREATE VIEW IF NOT EXISTS search_book AS
SELECT book_id,
  isbn_no,
  book_title,
  author_name,
  category_name,
  publisher_name,
  loc_district,
  book_shelf,
  shelf_level,
  book_status
FROM books
  INNER JOIN category USING (category_id)
  INNER JOIN publisher USING (publisher_id)
  INNER JOIN book_authors USING (book_id)
  INNER JOIN author_info USING (author_id)
  INNER JOIN books_location USING (book_id)
  INNER JOIN locations USING (loc_id);
