from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import text
from ..utils.database import engine
from ..db.return_book_system.isRecorded import isRecorded
from ..db.return_book_system.displayReaderName import displayReaderName
from ..db.return_book_system.displayNotReturn import displayNotReturn
from ..db.return_book_system.returnBookByLoanID import returnBookByLoanID
from ..db.return_book_system.getReaderIdByLoanID import getReaderIdByLoanID

return_book_bp = Blueprint("returnBook", __name__)

@return_book_bp.route("/return-book", methods=["GET", "POST"])
def return_book():
    # status and reader_id_qs for the confirm_function() is finished
    status = request.args.get("status")
    reader_id_qs = request.args.get("reader_id")

    if request.method == "GET" and reader_id_qs:
        try:
            reader_id = int(reader_id_qs)
        except:
            return render_template("returnBook.html", error="Invalid reader ID")

        if isRecorded(engine, reader_id) == 1:
            reader_name = displayReaderName(engine, reader_id)
            loans_books = displayNotReturn(engine, reader_id)

            success_msg = None
            error_msg = None
            if status == "success":
                success_msg = "Book returned successfully."
            elif status == "error":
                error_msg = "Error occurred when returning book."

            return render_template(
                "returnBook.html",
                reader_name=reader_name,
                loan_books=loans_books,
                success=success_msg,
                error=error_msg,
            )
        else:
            return render_template("returnBook.html", error="Reader does not exist")

    if request.method == "GET":
        return render_template("returnBook.html")

    # Post: user search reader id
    reader_id = request.form.get("reader_id")

    try:
        reader_id = int(reader_id)
    except:
        error = "Invalid reader ID"
        return render_template("returnBook.html", error=error)

    if isRecorded(engine, reader_id) == 1:
        reader_name = displayReaderName(engine, reader_id)
        loans_books = displayNotReturn(engine, reader_id)
        return render_template(
            "returnBook.html",
            reader_name=reader_name,
            loan_books=loans_books,
        )
    else:
        error = "Reader does not exist"
        return render_template("returnBook.html", error=error)
  
# Function for doing the process of return book
@return_book_bp.route("/return-book/confirm", methods=["POST"])
def confirm_return():
  loan_record_id = request.form.get("loan_record_id")

  try:
      loan_record_id = int(loan_record_id)
  except:
      return redirect(url_for("returnBook.return_book",status="error"))

  returnStatus = returnBookByLoanID(engine, loan_record_id)

  if not returnStatus:
     return redirect(url_for("returnBook.return_book",status="error"))
  
  reader_id = getReaderIdByLoanID(engine, loan_record_id)
  return redirect(url_for("returnBook.return_book",reader_id=reader_id, status="success"))