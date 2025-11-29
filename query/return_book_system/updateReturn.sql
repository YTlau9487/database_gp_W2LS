# update the loan_records.ret_date and books_location.book_status = ‘O’
UPDATE
  books_location AS bl
JOIN 
  loan_records AS lr
ON
  (lr.books_location_id = bl.books_location_id)
SET
  lr.ret_date = CURDATE(),
  bl.book_status = 'O'
WHERE
  lr.loan_records_id = :lrId;