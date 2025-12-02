from flask import Blueprint, render_template, request
from sqlalchemy import text
from ..utils.database import engine
from ..db.return_book_system.isRecorded import isRecorded
from ..db.return_book_system.displayReaderName import displayReaderName
from ..db.return_book_system.displayNotReturn import displayNotReturn

return_book_bp = Blueprint("returnBook", __name__)

@return_book_bp.route("/return-book", methods=["GET","POST"])
def return_book():
  if request.method == "GET":
    return render_template("returnBook.html")
  
  reader_id = request.form.get("reader_id")
  
  try:
    reader_id = int(reader_id)
  except:
    error = "Invalid reader ID"
    return render_template("returnBook.html",error=error)
  
  if isRecorded(engine, reader_id) == 1:
     reader_name = displayReaderName(engine, reader_id)
     loans_books = displayNotReturn(engine, reader_id)
     return render_template("returnBook.html", reader_name=reader_name, loan_books=loans_books)
  else:
    error = "Reader does not exist"
    return render_template("returnBook.html",error=error)