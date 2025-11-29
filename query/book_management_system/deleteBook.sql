SELECT COUNT(*) AS active_loans
FROM 
    loan_records lr
JOIN 
    books_location bl ON lr.books_location_id = bl.books_location_id
WHERE 
    bl.book_id = :book_id AND lr.ret_date IS NULL;

UPDATE 
    books_location
SET 
    book_status = 'D'
WHERE 
    book_id = :book_id AND book_status <> 'L';
