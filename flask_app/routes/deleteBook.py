from flask import Blueprint, render_template, request, url_for
from ..utils.database import engine
from ..db.book_management_system.delete_book import delete_book

deleteBook_bp = Blueprint("deleteBook", __name__)


@deleteBook_bp.route("/delete-book", methods=["GET", "POST"])
def delete_book_view():
    action = url_for("deleteBook.delete_book_view")
    if request.method == "GET":
        return render_template("deleteBook.html", actionUrl=action)

    form = request.form
    book_id = (form.get("book_id") or "").strip()
    if not book_id:
        return render_template("deleteBook.html", actionUrl=action, error="Missing book_id")
    try:
        bid = int(book_id)
    except ValueError:
        return render_template("deleteBook.html", actionUrl=action, error="book_id must be an integer")

    try:
        with engine.begin() as conn:
            result = delete_book(bid, conn=conn)
        msg = f"Active loans: {result.get('active_loans', 0)}. Locations updated: {result.get('rows_updated', 0)}."
        return render_template("deleteBook.html", actionUrl=action, message=msg)
    except Exception as e:
        return render_template("deleteBook.html", actionUrl=action, error=f"Database error: {e}")
