from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import text
from ..utils.database import engine, SessionLocal
from datetime import date

addBook_bp = Blueprint("addBook", __name__)

@addBook_bp.route("/addBook", methods=["GET", "POST"])
def add_book():
    # load categories for select
    with engine.connect() as conn:
        categories = [r[0] for r in conn.execute(text("SELECT category_name FROM category ORDER BY category_name")).fetchall()]

    if request.method == "GET":
        added = request.args.get("added")
        # if redirected after success, show the added book
        book = None
        if added:
            with engine.connect() as conn:
                book = conn.execute(text("SELECT * FROM search_book WHERE book_id = :id"), {"id": added}).fetchone()
        return render_template("addBook.html", categories=categories, book=book, message=request.args.get("message"))

    form = request.form
    title = (form.get("book_title") or "").strip()
    author = (form.get("author_name") or "").strip()
    isbn = (form.get("isbn_no") or "").strip()
    # category: existing or new
    category = (form.get("category_new") or "").strip() if form.get("category") == "__new__" else (form.get("category") or "").strip()
    publisher = (form.get("publisher") or "").strip()
    loc_district = (form.get("loc_district") or "").strip()
    book_shelf = (form.get("book_shelf") or "").strip()
    shelf_level = (form.get("shelf_level") or "").strip()
    book_status = (form.get("book_status") or "L").strip()

    # validate mandatory fields (all required)
    required = {
        "Title": title,
        "Author": author,
        "ISBN": isbn,
        "Category": category,
        "Publisher": publisher,
        "Location district": loc_district,
        "Shelf": book_shelf,
        "Shelf level": shelf_level,
        "Status": book_status,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        return render_template("addBook.html", error=f"Missing: {', '.join(missing)}", form=form, categories=categories)

    # convert shelf level
    try:
        shelf_level_int = int(shelf_level)
    except ValueError:
        return render_template("addBook.html", error="Shelf level must be an integer.", form=form, categories=categories)

    try:
        with engine.begin() as conn:
            def get_or_create(table, idcol, namecol, value):
                r = conn.execute(text(f"SELECT {idcol} FROM {table} WHERE {namecol} = :v"), {"v": value}).fetchone()
                if r:
                    return r[0]
                conn.execute(text(f"INSERT INTO {table} ({namecol}) VALUES (:v)"), {"v": value})
                return conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()

            # find existing book by ISBN first, else by title+author
            book_id = None
            if isbn:
                r = conn.execute(text("SELECT book_id FROM books WHERE isbn_no = :isbn"), {"isbn": isbn}).fetchone()
                if r:
                    book_id = r[0]

            if not book_id:
                r = conn.execute(text(
                    "SELECT b.book_id FROM books b "
                    "JOIN book_authors ba ON b.book_id = ba.book_id "
                    "JOIN author_info a ON ba.author_id = a.author_id "
                    "WHERE b.book_title = :t AND a.author_name = :a LIMIT 1"
                ), {"t": title, "a": author}).fetchone()
                if r:
                    book_id = r[0]

            # ensure location exists (get or create)
            loc = conn.execute(text(
                "SELECT loc_id FROM locations WHERE loc_district = :ld AND book_shelf = :bs AND shelf_level = :sl"
            ), {"ld": loc_district, "bs": book_shelf, "sl": shelf_level_int}).fetchone()
            if loc:
                loc_id = loc[0]
            else:
                conn.execute(text(
                    "INSERT INTO locations (loc_district, book_shelf, shelf_level) VALUES (:ld, :bs, :sl)"
                ), {"ld": loc_district, "bs": book_shelf, "sl": shelf_level_int})
                loc_id = conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()

            # if book exists -> add a books_location row (if not already present)
            if book_id:
                exists_bl = conn.execute(text(
                    "SELECT books_location_id FROM books_location WHERE book_id = :bid AND loc_id = :lid"
                ), {"bid": book_id, "lid": loc_id}).fetchone()
                if not exists_bl:
                    conn.execute(text(
                        "INSERT INTO books_location (book_id, loc_id, create_date, book_status) VALUES (:bid,:lid,:cd,:bs)"
                    ), {"bid": book_id, "lid": loc_id, "cd": date.today(), "bs": book_status})
                # redirect to GET (PRG) to clear form
                return redirect(url_for("addBook.add_book", added=book_id, message="Added an additional copy."))

            # not exists -> create book + relations + books_location
            category_id = get_or_create("category", "category_id", "category_name", category)
            publisher_id = get_or_create("publisher", "publisher_id", "publisher_name", publisher)

            # Use the helper that encapsulates the book + books_location insertion
            from ..db.book_management_system.add_book import add_book as add_book_helper
            # add_book_helper will create the book if needed and insert books_location
            # pass the current `conn` so the whole flow uses the same transaction/connection
            book_id = add_book_helper(
                input_isbn=isbn,
                input_title=title,
                input_category_id=int(category_id),
                input_publisher_id=int(publisher_id),
                input_loc_id=int(loc_id),
                input_create_date=date.today(),
                conn=conn,
            )

            # ensure author exists and insert book_authors
            author_id = get_or_create("author_info", "author_id", "author_name", author)
            if author_id:
                conn.execute(text("INSERT INTO book_authors (book_id, author_id) VALUES (:bid, :aid)"),
                             {"bid": book_id, "aid": author_id})

        # PRG: redirect to GET so form is cleared and user sees result
        return redirect(url_for("addBook.add_book", added=book_id, message="Book created."))
    except Exception as e:
        return render_template("addBook.html", error=f"Database error: {e}", form=form, categories=categories)