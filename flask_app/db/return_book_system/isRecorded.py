from sqlalchemy import text, Engine

def isRecorded(engine: Engine, reader_id = 0) -> int:
  with engine.connect() as conn:
    result = conn.execute(text(
      """
      SELECT EXISTS (
        SELECT 1
        FROM
          reader_info
        WHERE
          reader_id = :rId
        ) AS is_recorded;
      """
      ),{"rId":reader_id})
    
  return int(result.scalar())