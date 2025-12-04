from sqlalchemy import text, Engine

def FindLocation(engine: Engine, ISBN):
  with engine.connect() as conn:
    result = conn.execute(text(
      """
      SELECT books_location_id, b.book_id
      FROM books_location bl, books b
      WHERE bl.book_id = (SELECT b.book_id FROM books b WHERE b.isbn_no = :isbn);
      """
    ), {"isbn":ISBN})
    
    return result.all()