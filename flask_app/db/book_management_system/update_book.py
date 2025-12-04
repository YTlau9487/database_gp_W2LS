from sqlalchemy import text
from typing import Optional

from flask_app.utils.database import SessionLocal


def update_book(
    book_id: int,
    input_isbn: str = "",
    input_title: str = "",
    input_category_id: Optional[int] = None,
    input_publisher_id: Optional[int] = None,
    conn: Optional[object] = None,
    session_factory: Optional[SessionLocal] = None,
) -> int:
    """
    Update a book record using the same logic as `updateBook.sql`.

    Updates the book with the given book_id, setting isbn_no, book_title, 
    category_id, and publisher_id.

    Returns the number of rows updated (should be 1 if successful).
    """

    # If a connection is provided (from an existing transaction), reuse it
    if conn is not None:
        result = conn.execute(
            text(
                "UPDATE books SET isbn_no = :isbn, book_title = :title, "
                "category_id = :category_id, publisher_id = :publisher_id "
                "WHERE book_id = :book_id"
            ),
            {
                "isbn": input_isbn,
                "title": input_title,
                "category_id": input_category_id,
                "publisher_id": input_publisher_id,
                "book_id": book_id,
            },
        )
        return result.rowcount

    # Otherwise, operate with our own session (backward compatible)
    if session_factory is None:
        session_factory = SessionLocal

    session = session_factory()
    try:
        with session.begin():
            result = session.execute(
                text(
                    "UPDATE books SET isbn_no = :isbn, book_title = :title, "
                    "category_id = :category_id, publisher_id = :publisher_id "
                    "WHERE book_id = :book_id"
                ),
                {
                    "isbn": input_isbn,
                    "title": input_title,
                    "category_id": input_category_id,
                    "publisher_id": input_publisher_id,
                    "book_id": book_id,
                },
            )
        return result.rowcount
    finally:
        session.close()
