from sqlalchemy import text, Engine

def UpdateState(engine: Engine, book_id) -> bool:
  with engine.begin() as conn:
    try:
      result = conn.execute(text(
        """
        UPDATE books_location
        SET book_status = 'L'
        WHERE book_id = :bid;
        """
      ), {"bid":book_id})

      return True
    except:
      return False