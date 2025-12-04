from flask import Blueprint, render_template, request, Flask, session
from sqlalchemy import text
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
    session["location_id"] = None
    session["book_id"] = None

    if request.method == "GET":
        reader_id = request.args.get("reader_id")

        if not reader_id:
          return render_template("BooksLoan.html")
        
        else:
          try:
              reader_id = int(reader_id)
          except:
              return render_template("BooksLoan.html", LoginFail="Invalid reader ID")

          reader_name = ReaderName(engine, reader_id)
          if not reader_name:
            return render_template("BooksLoan.html", LoginFail="Reader ID not found")
          else:
            return render_template("BooksLoan.html", reader_name = reader_name)
            
        

    elif request.method == "POST":

      Loan = request.form.get("Loan")
      if (session["location_id"] & Loan):
        location = session['location_id']
        book = session['book_id']
        reader = request.args.get("reader_id")
        LoanRecord(engine, reader, location)
        UpdateState(engine, book)

        session["location_id"] = None
        session["book_id"] = None



      ISBN = request.form.get("ISBN")
      session["location_id"] = None
      session["book_id"] = None

      if not ISBN:
        return render_template( "BooksLoan.html", NullFind="Please enter a ISBN number",)

      else:  
        results = FindBook(engine, ISBN)
        if not results:
          return render_template( "BooksLoan.html", NoFind= "No book found with the provided ISBN")
        
        else: 
          save = FindLocation(engine, ISBN)
          session['location_id'] = save[0]
          session['book_id'] = save[1]
          return render_template("BooksLoan.html", datail = results)
        
    



