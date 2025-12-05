UPDATE books
SET 
    isbn_no     = :isbn,
    book_title  = :title,
    category_id = :category_id,
    publisher_id = :publisher_id
WHERE 
    book_id = :book_id;
