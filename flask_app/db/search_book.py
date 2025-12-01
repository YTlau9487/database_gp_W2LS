from sqlalchemy import text, Engine


def search_book(engine: Engine, book_title="", author_name=""):
    with engine.connect() as conn:
        result = []
        rows = conn.execute(
            text(
                """SELECT 
                    book_id, 
                    isbn_no, 
                    book_title, 
                    author_name, 
                    category_name, 
                    publisher_name, 
                    loc_district, 
                    book_shelf, 
                    shelf_level
                FROM 
                    search_book
                WHERE
                    (book_title LIKE CONCAT("%", (:book_title), "%") OR (:book_title) = "")
                    AND 
                    (author_name LIKE CONCAT("%", (:author_name), "%") OR (:author_name) = "")
                    AND 
                    book_status = 'O'
                """
            ),
            [{"book_title": book_title, "author_name": author_name}],
        )

        # return 
        return rows.all()
