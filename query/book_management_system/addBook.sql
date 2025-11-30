-- check if the book already exists by ISBN
SELECT 
    book_id INTO @book_id
FROM 
    books
WHERE 
    isbn_no = :isbn_no;

-- if the book does NOT exist, insert it
IF @book_id IS NULL THEN
    INSERT INTO 
        books (isbn_no, book_title, category_id, publisher_id)
    VALUES 
        (:input_isbn, :input_title, :input_category_id, :input_publisher_id);
    SET 
        @book_id = LAST_INSERT_ID();
END IF;

-- insert a record into books_location
INSERT INTO 
    books_location (book_id, loc_id, create_date, book_status)
VALUES
    (:book_id, :input_loc_id, :input_create_date, 'O');    -- default as O (on shelf)