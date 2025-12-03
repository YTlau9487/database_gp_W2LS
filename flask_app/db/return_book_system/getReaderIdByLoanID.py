from sqlalchemy import text, Engine

def getReaderIdByLoanID(engine: Engine, loan_record_id) -> int:
  with engine.connect() as conn:
    result = conn.execute(text(
      """
      SELECT
        reader_id
      FROM
        loan_records
      WHERE
        loan_records_id = :lrId
      """
    ), {"lrId": loan_record_id})
  return result.scalar()
