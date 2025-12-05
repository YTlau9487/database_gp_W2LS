from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..utils.database import engine
from ..db.Books_Loan.FindBook import FindBook
from ..db.Books_Loan.InsertLoanRecord import InsertLoanRecord
from ..db.Books_Loan.ReaderName import ReaderName
from ..db.Books_Loan.UpdateState import UpdateState
from ..db.Books_Loan.FindLocation import FindLocation
from ..db.Books_Loan.FindLocationIDByBookId import FindLocationIDByBookId

BooksLoan_bp = Blueprint("booksLoan", __name__)

@BooksLoan_bp.route("/loan-book", methods=["GET", "POST"])
def BookLoan():
    if request.method == "GET":
        return render_template("booksLoan.html")

    elif request.method == "POST":
        # Step 1: Check Reader ID
        reader_id = request.form.get("reader_id")
        if reader_id:
            try:
                reader_id = int(reader_id)
                reader_name = ReaderName(engine, reader_id)
                if not reader_name:
                    flash("Reader ID not found.", "error")
                    return render_template("booksLoan.html", reader_name=None)

                session['reader_id'] = reader_id
                session['reader_name'] = reader_name
                return render_template("booksLoan.html", reader_name=reader_name)

            except ValueError:
                flash("Invalid Reader ID.", "error")
                return render_template("booksLoan.html")

        # Step 2: Check ISBN
        ISBN = request.form.get("ISBN")
        if ISBN:
            results = FindBook(engine, ISBN)
            if not results:
                flash("No book found with the provided ISBN.", "error")
                return render_template("booksLoan.html", reader_name=session.get("reader_name"))

            # If book exists, get location
            location = FindLocation(engine, ISBN)
            if location:
                row = location[0]
                session['location_id'] = row[0]
                session['book_id'] = row[1]
                return render_template("booksLoan.html", datail=results, reader_name=session.get("reader_name"))
            else:
                flash("Book location not found.", "error")
                return render_template("booksLoan.html", reader_name=session.get("reader_name"))

        # If no valid form data, reload page
        return render_template("booksLoan.html", reader_name=session.get("reader_name"))

@BooksLoan_bp.route("/loan-book/confirm", methods=["POST"])
def confirm_loan():
    reader_id = session.get("reader_id")
    book_id = request.form.get("book_id")

    if not reader_id or not book_id:
        flash("Missing reader or book information, please try again.", "error")
        return redirect(url_for("booksLoan.BookLoan"))

    book_location_id = FindLocationIDByBookId(engine, book_id)
    if not book_location_id:
        flash("Cannot find book location record.", "error")
        return redirect(url_for("booksLoan.BookLoan"))

    try:
        insertStatus = InsertLoanRecord(engine, reader_id, book_location_id)
        updateStatus = UpdateState(engine, book_id)

        if insertStatus and updateStatus:
            flash("Successfully borrowed the book.", "success")
        else:
            flash("Failed to loan the book, please try again.", "error")

    except Exception:
        flash("Failed to loan the book, please try again.", "error")

    return redirect(url_for("booksLoan.BookLoan"))
