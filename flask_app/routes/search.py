# routes/search.py
from flask import Blueprint, render_template, request
from sqlalchemy import text
from ..utils.database import engine
from ..db.search_book import search_book

search_bp = Blueprint("search", __name__)


@search_bp.route("/search", methods=["GET", "POST"])
def search_books():
    results = None

    # query = request.form.get('search_query', '').strip()
    if request.method == "GET":
        return render_template("search_book.html")

    elif request.method == "POST":
        book_title = request.form.get("book_title", "")
        author_name = request.form.get("author_name", "")
        isbn_no = request.form.get("isbn_no", "")
        print(request.form)

        if not (book_title or author_name or isbn_no):
            return render_template(
                "search_book.html",
                error="Please enter a book title or author name or ISBN number.",
            )
        results = search_book(engine, book_title, author_name)
        print("query result: ", results)

        return render_template("search_book.html", books=results)

