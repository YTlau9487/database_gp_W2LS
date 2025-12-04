from sqlalchemy import text, Engine

def ReaderName(engine: Engine, reader_id):
  with engine.connect() as conn:
    result = conn.execute(text(
      """
      SELECT reader_name AS UserName
      FROM reader_info
      WHERE reader_id = :rId;
      """
    ), {"rid":reader_id})
    
    return result.all()