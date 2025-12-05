# routes/__init__.py
from flask import Flask, Blueprint

def init_routes(app: Flask):
    from .rootPage import root_bp
    from .search import search_bp
    from .returnBook import return_book_bp
    from .loan import BooksLoan_bp
    from .loanV2 import BooksLoan_bp1, BooksLoan_bp2, BooksLoan_bp3
    # from .book_management import book_bp
    from .addBook import addBook_bp
    from .deleteBook import deleteBook_bp

    app.register_blueprint(root_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(return_book_bp)
    app.register_blueprint(BooksLoan_bp)
    app.register_blueprint(BooksLoan_bp1)
    app.register_blueprint(BooksLoan_bp2)
    app.register_blueprint(BooksLoan_bp3)
    # app.register_blueprint(book_bp)
    app.register_blueprint(addBook_bp)
    app.register_blueprint(deleteBook_bp)
