from sqlalchemy import text, Engine

def FindLocation(engine: Engine, BID):
  with engine.connect() as conn:
    result = conn.execute(text(
      """
      SELECT books_location_id
      FROM books_location 
      WHERE book_id = :bid;
      """
    ), {"bid":BID})
    
    return result.scalar()