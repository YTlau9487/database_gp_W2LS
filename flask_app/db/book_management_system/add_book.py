from datetime import date
from sqlalchemy import text
from typing import Optional

from flask_app.utils.database import SessionLocal


def add_book(
    session_factory: Optional[SessionLocal] = None,
    input_isbn: str = "",
    input_title: str = "",
    input_category_id: Optional[int] = None,
    input_publisher_id: Optional[int] = None,
    input_loc_id: Optional[int] = None,
    input_create_date: Optional[str] = None,
    conn: Optional[object] = None,
) -> int:
    """
    Add a book and a books_location record using the same logic as `addBook.sql`.

    Steps:
      1. Check if a book with the same ISBN exists. If so, use its book_id.
      2. Otherwise insert into `books` and obtain the new book_id.
      3. Insert a record into `books_location` with status 'O' (on shelf).

    Returns the `book_id` for the book that was used/inserted.
    """

    # default create date to today if not provided
    if input_create_date is None:
        input_create_date = date.today().isoformat()

    # If a connection is provided (from an existing transaction), reuse it
    if conn is not None:
        # use provided connection (assumed to be an SQLAlchemy Connection)
        # 1) Check existing book by ISBN
        row = conn.execute(text("SELECT book_id FROM books WHERE isbn_no = :isbn_no"), {"isbn_no": input_isbn}).first()
        if row:
            book_id = int(row[0])
        else:
            conn.execute(
                text(
                    "INSERT INTO books (isbn_no, book_title, category_id, publisher_id) "
                    "VALUES (:isbn_no, :title, :category_id, :publisher_id)"
                ),
                {
                    "isbn_no": input_isbn,
                    "title": input_title,
                    "category_id": input_category_id,
                    "publisher_id": input_publisher_id,
                },
            )
            book_id = int(conn.execute(text("SELECT LAST_INSERT_ID()")).scalar_one())

        conn.execute(
            text(
                "INSERT INTO books_location (book_id, loc_id, create_date, book_status) "
                "VALUES (:book_id, :loc_id, :create_date, 'O')"
            ),
            {"book_id": book_id, "loc_id": input_loc_id, "create_date": input_create_date},
        )
        return book_id

    # Otherwise, operate with our own session (backward compatible)
    if session_factory is None:
        session_factory = SessionLocal

    session = session_factory()
    try:
        with session.begin():
            # 1) Check existing book by ISBN
            row = session.execute(text("SELECT book_id FROM books WHERE isbn_no = :isbn_no"), {"isbn_no": input_isbn}).first()

            if row:
                book_id = int(row[0])
            else:
                # 2) Insert new book
                session.execute(
                    text(
                        "INSERT INTO books (isbn_no, book_title, category_id, publisher_id) "
                        "VALUES (:isbn_no, :title, :category_id, :publisher_id)"
                    ),
                    {
                        "isbn_no": input_isbn,
                        "title": input_title,
                        "category_id": input_category_id,
                        "publisher_id": input_publisher_id,
                    },
                )
                # Use MySQL LAST_INSERT_ID() to get the autoincrement value
                book_id = int(session.execute(text("SELECT LAST_INSERT_ID()")).scalar_one())

            # 3) Insert into books_location with status 'O'
            session.execute(
                text(
                    "INSERT INTO books_location (book_id, loc_id, create_date, book_status) "
                    "VALUES (:book_id, :loc_id, :create_date, 'O')"
                ),
                {"book_id": book_id, "loc_id": input_loc_id, "create_date": input_create_date},
            )

        # transaction commits here
        return book_id
    finally:
        session.close()