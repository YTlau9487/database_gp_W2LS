from sqlalchemy import text, Engine

def returnBookByLoanID(engine: Engine, loan_id = 0) -> bool:
  with engine.begin() as conn:
    try:
      conn.execute(text(
      """
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
      """
      ),{"lrId":loan_id})

      return True
    except Exception:
      return False