from sqlalchemy import text, Engine

def LoanRecord(engine: Engine, reader_id, books_location_id):
  with engine.connect() as conn:
    result = conn.execute(text(
      """
      INSERT INTO loan_records     
      VALUES (1+COUNT(*), :rid, :blid, CURDATE(), CURDATE() + INTERVAL 14 DAY, NULL);
      """
    ),{"rid":reader_id}, {"blid":books_location_id})
    
    return result.all()