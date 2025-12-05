from sqlalchemy import text, Engine

def FindLocationIDByBookId(engine: Engine, book_id) -> int:
  with engine.connect() as conn:
    result = conn.execute(text(
      """
      SELECT bl.books_location_id
      FROM locations l
      JOIN books_location bl
      ON (l.loc_id = bl.loc_id)
      JOIN books b
      ON (b.book_id = bl.book_id)
      WHERE b.book_id = :bId;
      """
    ), {"bId":book_id})
    
    return result.scalar()