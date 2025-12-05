from sqlalchemy import text, Engine

def FindID(engine: Engine, Name):
  with engine.connect() as conn:
    result = conn.execute(text(
      """
      SELECT reader_id
      FROM reader_info 
      WHERE reader_name = :name;
      """
    ), {"name":Name})
    
    return result.scalar()