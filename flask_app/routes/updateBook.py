from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import text
from ..utils.database import engine
from ..db.book_management_system.update_book import update_book as update_book_helper

updateBook_bp = Blueprint("updateBook", __name__)


@updateBook_bp.route("/update-book", methods=["GET", "POST"])
def update_book():
    # load categories, publishers for selects
    with engine.connect() as conn:
        categories = [r[0] for r in conn.execute(text("SELECT category_name FROM category ORDER BY category_name")).fetchall()]
        publishers = [r[0] for r in conn.execute(text("SELECT publisher_name FROM publisher ORDER BY publisher_name")).fetchall()]

    if request.method == "GET":
        # show search form or edit form if book_id provided
        book_id = request.args.get("book_id")
        book = None
        location = None
        if book_id:
            with engine.connect() as conn:
                book = conn.execute(
                    text(
                        "SELECT b.book_id, b.isbn_no, b.book_title, b.category_id, b.publisher_id, "
                        "c.category_name, p.publisher_name FROM books b "
                        "LEFT JOIN category c ON b.category_id = c.category_id "
                        "LEFT JOIN publisher p ON b.publisher_id = p.publisher_id "
                        "WHERE b.book_id = :id"
                    ),
                    {"id": book_id},
                ).fetchone()
                # fetch location from books_location joined with locations
                if book:
                    location = conn.execute(
                        text(
                            "SELECT l.loc_id, l.loc_district, l.book_shelf, l.shelf_level FROM locations l "
                            "JOIN books_location bl ON l.loc_id = bl.loc_id "
                            "WHERE bl.book_id = :id LIMIT 1"
                        ),
                        {"id": book_id},
                    ).fetchone()
        return render_template(
            "updateBook.html",
            categories=categories,
            publishers=publishers,
            book=book,
            location=location,
            form={},
            message=request.args.get("message"),
        )

    # POST: handle search or update
    form = request.form
    action = form.get("action", "search").strip()

    # Search action: find book by ID
    if action == "search":
        search_book_id = (form.get("search_book_id") or "").strip()
        if not search_book_id:
            return render_template(
                "updateBook.html",
                error="Please enter a Book ID to search.",
                categories=categories,
                publishers=publishers,
                form=form,
            )

        try:
            search_book_id_int = int(search_book_id)
        except ValueError:
            return render_template(
                "updateBook.html",
                error="Book ID must be an integer.",
                categories=categories,
                publishers=publishers,
                form=form,
            )

        with engine.connect() as conn:
            book = conn.execute(
                text(
                    "SELECT b.book_id, b.isbn_no, b.book_title, b.category_id, b.publisher_id, "
                    "c.category_name, p.publisher_name FROM books b "
                    "LEFT JOIN category c ON b.category_id = c.category_id "
                    "LEFT JOIN publisher p ON b.publisher_id = p.publisher_id "
                    "WHERE b.book_id = :id"
                ),
                {"id": search_book_id_int},
            ).fetchone()

            location = None
            if book:
                location = conn.execute(
                    text(
                        "SELECT l.loc_id, l.loc_district, l.book_shelf, l.shelf_level FROM locations l "
                        "JOIN books_location bl ON l.loc_id = bl.loc_id "
                        "WHERE bl.book_id = :id LIMIT 1"
                    ),
                    {"id": search_book_id_int},
                ).fetchone()

        if not book:
            return render_template(
                "updateBook.html",
                error=f"Book with ID {search_book_id_int} not found.",
                categories=categories,
                publishers=publishers,
                form=form,
            )

        return render_template(
            "updateBook.html",
            categories=categories,
            publishers=publishers,
            book=book,
            location=location,
            form={},
            message=f"Book found: ID {search_book_id_int}",
        )

    # POST: Update action
    update_book_id = (form.get("book_id") or "").strip()
    isbn = (form.get("isbn_no") or "").strip()
    title = (form.get("book_title") or "").strip()
    category = (form.get("category") or "").strip()
    publisher = (form.get("publisher") or "").strip()
    loc_district = (form.get("loc_district") or "").strip()
    book_shelf = (form.get("book_shelf") or "").strip()
    shelf_level = (form.get("shelf_level") or "").strip()

    # validate mandatory fields
    required = {
        "Book ID": update_book_id,
        "ISBN": isbn,
        "Title": title,
        "Category": category,
        "Publisher": publisher,
        "Location District": loc_district,
        "Shelf": book_shelf,
        "Shelf Level": shelf_level,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        return render_template(
            "updateBook.html",
            error=f"Missing: {', '.join(missing)}",
            form=form,
            categories=categories,
            publishers=publishers,
        )

    # convert book_id and shelf_level
    try:
        book_id_int = int(update_book_id)
        shelf_level_int = int(shelf_level)
    except ValueError:
        return render_template(
            "updateBook.html",
            error="Book ID and Shelf Level must be integers.",
            form=form,
            categories=categories,
            publishers=publishers,
        )

    try:
        with engine.begin() as conn:
            # helper to get or create lookup rows (category/publisher)
            def get_or_create(table, idcol, namecol, value):
                r = conn.execute(text(f"SELECT {idcol} FROM {table} WHERE {namecol} = :v"), {"v": value}).fetchone()
                if r:
                    return r[0]
                conn.execute(text(f"INSERT INTO {table} ({namecol}) VALUES (:v)"), {"v": value})
                return conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()

            # ensure category and publisher exist (create if necessary)
            category_id = get_or_create("category", "category_id", "category_name", category)
            publisher_id = get_or_create("publisher", "publisher_id", "publisher_name", publisher)

            # Update books table
            rows_updated = update_book_helper(
                book_id=book_id_int,
                input_isbn=isbn,
                input_title=title,
                input_category_id=category_id,
                input_publisher_id=publisher_id,
                conn=conn,
            )

            # Update or create location
            loc_row = conn.execute(
                text(
                    "SELECT loc_id FROM locations "
                    "WHERE loc_district = :ld AND book_shelf = :bs AND shelf_level = :sl"
                ),
                {"ld": loc_district, "bs": book_shelf, "sl": shelf_level_int},
            ).fetchone()

            if loc_row:
                loc_id = loc_row[0]
            else:
                # Insert new location
                conn.execute(
                    text(
                        "INSERT INTO locations (loc_district, book_shelf, shelf_level) "
                        "VALUES (:ld, :bs, :sl)"
                    ),
                    {"ld": loc_district, "bs": book_shelf, "sl": shelf_level_int},
                )
                loc_id = conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()

            # Update books_location with new location (update first matching record)
            conn.execute(
                text(
                    "UPDATE books_location SET loc_id = :loc_id "
                    "WHERE book_id = :book_id"
                ),
                {"loc_id": loc_id, "book_id": book_id_int},
            )

        if rows_updated > 0:
            return redirect(
                url_for(
                    "updateBook.update_book",
                    book_id=book_id_int,
                    message="Book updated successfully.",
                )
            )
        else:
            return render_template(
                "updateBook.html",
                error="Book not found or no changes made.",
                form=form,
                categories=categories,
                publishers=publishers,
            )
    except Exception as e:
        return render_template(
            "updateBook.html",
            error=f"Database error: {e}",
            form=form,
            categories=categories,
            publishers=publishers,
        )
