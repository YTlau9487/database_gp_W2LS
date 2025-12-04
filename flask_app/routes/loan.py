from flask import Blueprint, render_template, request, Flask, session
from ..utils.database import engine
from ..db.Books_Loan.FindBook import FindBook
from ..db.Books_Loan.LoanRecord import LoanRecord
from ..db.Books_Loan.ReaderName import ReaderName
from ..db.Books_Loan.UpdateState import UpdateState
from ..db.Books_Loan.FindLocation import FindLocation

BooksLoan_bp = Blueprint("booksLoan", __name__)
app = Flask(__name__)
app.secret_key = "you_guess"

@BooksLoan_bp.route("/loan-book", methods=["GET", "POST"])
def BookLoan():
    if request.method == "GET":
        # original page load
        return render_template("booksLoan.html")

    elif request.method == "POST":
        # check Reader ID(1)
        reader_id = request.form.get("reader_id")
        if reader_id:
            try:
                reader_id = int(reader_id)
            except:
                return render_template("booksLoan.html", LoginFail="Invalid reader ID")

            reader_name = ReaderName(engine, reader_id)
            if not reader_name:
                return render_template("booksLoan.html", LoginFail="Reader ID not found")
            else:
                return render_template("booksLoan.html", reader_name=reader_name)

        # check Loan (2)
        Loan = request.form.get("Loan")
        if session.get("location_id") and Loan:
            location = session['location_id']
            book = session['book_id']
            reader = request.form.get("reader_name")

            # insert loan record and update book state
            LoanRecord(engine, reader, location)
            UpdateState(engine, book)

            # null session
            session["location_id"] = None
            session["book_id"] = None

            # show success message
            return render_template("booksLoan.html", reader_name=reader, LoanSuccess="You loan a book")

        # check ISBN
        ISBN = request.form.get("ISBN")
        reader_name = request.form.get("reader_name")  # keep reader name
        if ISBN:
            results = FindBook(engine, ISBN)  # find book by ISBN
            if not results:
                return render_template(
                    "booksLoan.html",
                    NoFind="No book found with the provided ISBN",
                    reader_name=reader_name
                )

            save = FindLocation(engine, ISBN)
            if save:
                session['location_id'] = save[0]
                session['book_id'] = save[1]

            return render_template(
                "booksLoan.html",
                datail=results,
                reader_name=reader_name
            )

        # If ISBN is null but has reader_name
        if reader_name:
            return render_template(
                "booksLoan.html",
                reader_name=reader_name,
                NoFind="Please input ISBN"
            )

        # if no valid form data, reload page
        return render_template("booksLoan.html")