from sqlalchemy import text, Engine

def LoanRecord(engine: Engine, reader_id, books_location_id):
    with engine.connect() as conn:
        sql = text("""
            INSERT INTO loan_records (reader_id, books_location_id, loan_date, due_date, ret_date)
            VALUES (:rid, :blid, CURDATE(), CURDATE() + INTERVAL 14 DAY, NULL)
        """)
        conn.execute(sql, {"rid": reader_id, "blid": books_location_id})
        conn.commit()  # 别忘了提交事务
    return True