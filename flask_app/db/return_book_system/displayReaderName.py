from sqlalchemy import text, Engine

def displayReaderName(engine: Engine, reader_id):
  with engine.connect() as conn:
    name = conn.execute(text(
      """
      SELECT
        reader_name
      FROM
        reader_info
      WHERE
        reader_id = :rId;
      """
    ),{"rId":reader_id})
    
    return name.scalar()