from sqlalchemy import text, Engine

def InsertLoanRecord(engine: Engine, reader_id, books_location_id) -> bool:
  with engine.begin() as conn:
    try:
      result = conn.execute(text(
        """
        INSERT INTO loan_records (reader_id, books_location_id, loan_date, due_date, ret_date) 
        VALUES (:rid, :blid, CURDATE(), CURDATE() + INTERVAL 14 DAY, NULL);
        """
      ),[{"rid":reader_id,"blid":books_location_id}])
      
      return True
    except:
      return False