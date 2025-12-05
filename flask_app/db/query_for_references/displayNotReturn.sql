SELECT
  lr.loan_records_id,
  lr.reader_id,
  b.book_id,
  b.book_title,
  bl.books_location_id,
  lr.loan_date,
  lr.due_date
FROM
  loan_records AS lr
JOIN
  books_location AS bl
ON
  (lr.books_location_id = bl.books_location_id)
JOIN 
  books AS b
ON
  (bl.book_id = b.book_id)
WHERE
  lr.reader_id = :rId
AND
  lr.ret_date IS NULL;