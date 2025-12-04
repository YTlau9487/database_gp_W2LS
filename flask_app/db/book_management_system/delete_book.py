from typing import Optional, Dict
from sqlalchemy import text
from flask_app.utils.database import SessionLocal


def delete_book(book_id: int, conn: Optional[object] = None, session_factory: Optional[SessionLocal] = None) -> Dict[str, int]:
    """
    Implements the logic from `deleteBook.sql`:

    1) Count active loans for the given book_id (ret_date IS NULL).
    2) Mark all books_location rows for the book as deleted ('D') where status <> 'L'.

    If `conn` (an SQLAlchemy Connection) is provided it will be used; otherwise a session
    created from `session_factory` (or default `SessionLocal`) will be used.

    Returns a dict: {"active_loans": int, "rows_updated": int}
    """

    sql_count = text(
        "SELECT COUNT(*) FROM loan_records lr "
        "JOIN books_location bl ON lr.books_location_id = bl.books_location_id "
        "WHERE bl.book_id = :book_id AND lr.ret_date IS NULL"
    )

    sql_update = text(
        "UPDATE books_location SET book_status = 'D' "
        "WHERE book_id = :book_id AND book_status <> 'L'"
    )

    if conn is not None:
        # Using provided connection (likely inside a transaction)
        active_loans = int(conn.execute(sql_count, {"book_id": book_id}).scalar_one())
        result = conn.execute(sql_update, {"book_id": book_id})
        try:
            rows_updated = int(result.rowcount)
        except Exception:
            # Fallback when rowcount is not available
            rows_updated = 0
        return {"active_loans": active_loans, "rows_updated": rows_updated}

    # Use our own session/transaction
    if session_factory is None:
        session_factory = SessionLocal

    session = session_factory()
    try:
        with session.begin():
            active_loans = int(session.execute(sql_count, {"book_id": book_id}).scalar_one())
            result = session.execute(sql_update, {"book_id": book_id})
            try:
                rows_updated = int(result.rowcount)
            except Exception:
                rows_updated = 0

        return {"active_loans": active_loans, "rows_updated": rows_updated}
    finally:
        session.close()


if __name__ == "__main__":
    import os
    import sys

    if len(sys.argv) < 2:
        print("Usage: python delete_book.py <book_id>")
        raise SystemExit(1)

    bid = int(sys.argv[1])
    res = delete_book(bid)
    print(res)
