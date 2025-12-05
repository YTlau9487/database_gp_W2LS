-- create a new loan record, but need two parameters: rid and blid
INSERT INTO loan_records (reader_id, books_location_id, loan_date, due_date, ret_date) 
VALUES (:rid, :blid, CURDATE(), CURDATE() + INTERVAL 14 DAY, NULL);

SELECT bl.books_location_id
FROM locations l
JOIN books_location bl
ON (l.loc_id = bl.loc_id)
JOIN books b
ON (b.book_id = bl.book_id)
WHERE b.book_id = :bId;