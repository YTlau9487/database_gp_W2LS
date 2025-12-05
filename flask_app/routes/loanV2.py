from flask import Blueprint, render_template, request, Flask, redirect, url_for
from ..utils.database import engine
from ..db.Books_Loan.FindBook import FindBook
from ..db.Books_Loan.LoanRecord import LoanRecord
from ..db.Books_Loan.ReaderName import ReaderName
from ..db.Books_Loan.UpdateState import UpdateState
from ..db.Books_Loan.FindLocation import FindLocation
from ..db.Books_Loan.FindID import FindID

BooksLoan_bp1 = Blueprint("booksLoan1", __name__)
BooksLoan_bp2 = Blueprint("booksLoan2", __name__)
BooksLoan_bp3 = Blueprint("booksLoan3", __name__)

@BooksLoan_bp1.route("/loan-book/login", methods=["GET", "POST"])
def BookID():
  if request.method == "GET":
    return render_template("booksLoan1.html")

  elif request.method == "POST":
    reader_id = request.form.get("reader_id")

    if not reader_id:
      return render_template("booksLoan1.html", LoginFail = "Please enter a reader ID")
    
    else:
      try:
        reader_id = int(reader_id)
      except:
        return render_template("booksLoan1.html", LoginFail = "Invalid reader ID")

      try:
        reader_name = ReaderName(engine, reader_id)
      except:
        return render_template("booksLoan1.html", LoginFail = "Error retrieving reader name")
      
      if not reader_name:
        return render_template("booksLoan1.html", LoginFail = "Reader ID not found")
      else:
        return redirect(url_for("booksLoan2.BookLoan", name = reader_name))
      


@BooksLoan_bp2.route("/loan-book/loan", methods=["GET", "POST"])
def BookLoan():
  try:
      ReaderName = request.args.get("name") or request.form.get("name")
  except:
      ReaderName = "fail"

  if request.method == "GET":
    if not ReaderName:
      return render_template("booksLoan1.html")
    
    else:
      return render_template("booksLoan2.html", name = ReaderName)
    
  elif request.method == "POST":
    if not ReaderName:
      return render_template("booksLoan2.html", SearchFail = "Reader name missing")
    ISBN = request.form.get("ISBN")
    if not ISBN:
      return render_template("booksLoan2.html", name = ReaderName, SearchFail = "Please enter an ISBN")

    else:
      book_info = FindBook(engine, ISBN)
      if not book_info:
        return render_template("booksLoan2.html", name = ReaderName, SearchFail = "Book not found or not available")
      
      else:
        return render_template("booksLoan2.html", name = ReaderName, book_info = book_info)
      


@BooksLoan_bp3.route("/loan-book/finish", methods=["POST"])
def ConfirmLoan():
  reader_name = request.form.get("name")
  book_id = request.form.get("book_id")
  reader_id = FindID(engine, reader_name)
  location_id = FindLocation(engine, book_id)
  LoanRecord(engine, reader_id, location_id)
  UpdateState(engine, book_id)
  return render_template("booksLoan3.html")
  


  
