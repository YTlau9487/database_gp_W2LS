from flask import Blueprint, render_template, request, Flask, session
from ..utils.database import engine
from ..db.Books_Loan.FindBook import FindBook
from ..db.Books_Loan.LoanRecord import LoanRecord
from ..db.Books_Loan.ReaderName import ReaderName
from ..db.Books_Loan.UpdateState import UpdateState
from ..db.Books_Loan.FindLocation import FindLocation

BooksLoan_bp = Blueprint("BooksLoan", __name__)
app = Flask(__name__)
app.secret_key = "you_guess"

@BooksLoan_bp.route("/loan", methods=["GET", "POST"])
def BookLoan():
    results = None
    reader_name = None

    if request.method == "GET":
        # 初始页面
        return render_template("BooksLoan.html")

    elif request.method == "POST":
        # 先检查 Reader ID
        reader_id = request.form.get("reader_id")
        if reader_id:
            try:
                reader_id = int(reader_id)
            except:
                return render_template("BooksLoan.html", LoginFail="Invalid reader ID")

            reader_name = ReaderName(engine, reader_id)
            if not reader_name:
                return render_template("BooksLoan.html", LoginFail="Reader ID not found")
            else:
                return render_template("BooksLoan.html", reader_name=reader_name)

        # 再检查 Loan
        Loan = request.form.get("Loan")
        if session.get("location_id") and Loan:
            location = session['location_id']
            book = session['book_id']
            reader = request.form.get("reader_name")
            LoanRecord(engine, reader, location)
            UpdateState(engine, book)
            session["location_id"] = None
            session["book_id"] = None
            return render_template("BooksLoan.html", reader_name=reader)

        # 最后检查 ISBN
        ISBN = request.form.get("ISBN")
        if ISBN:
            results = FindBook(engine, ISBN)
            if not results:
                return render_template("BooksLoan.html", NoFind="No book found with the provided ISBN")

            save = FindLocation(engine, ISBN)
            session['location_id'] = save[0]
            session['book_id'] = save[1]
            return render_template("BooksLoan.html", datail=results, reader_name=request.form.get("reader_name"))

        # 如果没有任何字段
        return render_template("BooksLoan.html")