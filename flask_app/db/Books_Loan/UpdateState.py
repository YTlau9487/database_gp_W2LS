from sqlalchemy import text, Engine

def UpdateState(engine: Engine, book_id):
  with engine.connect() as conn:
    result = conn.execute(text(
      """
      UPDATE books_location
      SET book_status = 'L'
      WHERE book_id = :bid;
      """
    ), {"bid":book_id})
    
    return True