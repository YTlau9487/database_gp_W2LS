from sqlalchemy import text, Engine

def FindBook(engine: Engine, ISBN):
  with engine.connect() as conn:
    result = conn.execute(text(
      """
      SELECT b.book_id, b.isbn, b.book_title,
      a.author_name, 
      c.category_name, 
      p.publisher_name,
      l.loc_district, l.book_shelf, l.shelf_level 

      FROM books b

      JOIN publisher p ON b.publisher_id = p.publisher_id
      JOIN catagory c ON c.catagory_id = b.catagory_id  
      JOIN books_location bl ON b.book_id = bl.book_id
      JOIN location l ON bl.loc_id = l.loc_id
      JOIN book_author ba ON b.book_id = ba.book_id
      JOIN author_info a ON b.author_id = a.author_id

      WHERE b.isbn = :isbn 
      AND bl.book_status = 'O';
      """
    ),{"isbn":ISBN})
    
    return result.all()