from sqlalchemy import text, Engine

def FindBook(engine: Engine, ISBN):
  with engine.connect() as conn:
    result = conn.execute(text(
      """
      SELECT b.book_id, b.isbn_no, b.book_title,
      a.author_name, 
      c.category_name, 
      p.publisher_name,
      l.loc_district, l.book_shelf, l.shelf_level 

      FROM books b

      JOIN publisher p ON b.publisher_id = p.publisher_id
      JOIN category c ON c.category_id = b.category_id  
      JOIN books_location bl ON b.book_id = bl.book_id
      JOIN locations l ON bl.loc_id = l.loc_id
      JOIN book_authors ba ON b.book_id = ba.book_id
      JOIN author_info a ON ba.author_id = a.author_id

      WHERE b.isbn_no = :isbn 
      AND bl.book_status = 'O';
      """
    ),{"isbn":ISBN})
    
    return result.scalar()