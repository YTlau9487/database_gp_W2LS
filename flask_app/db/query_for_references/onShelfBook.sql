SELECT book_id,
    isbn_no,
    book_title,
    author_name,
    category_name,
    publisher_name,
    loc_district,
    book_shelf,
    shelf_level
FROM search_book
WHERE (
        book_title LIKE CONCAT("%", :book_title, "%")
        OR (:book_title) = ""
    )
    AND (
        author_name LIKE CONCAT("%", :author_name, "%")
        OR (:author_name) = ""
    )
    AND book_status = 'O';
