# routes/__init__.py
from flask import Flask, Blueprint

def init_routes(app: Flask):
    from .search import search_bp
    from .returnBook import return_book_bp
    # from .loan import loan_bp
    # from .book_management import book_bp
    from .addBook import addBook_bp
    from .deleteBook import deleteBook_bp

    app.register_blueprint(search_bp)
    app.register_blueprint(return_book_bp)
    # app.register_blueprint(loan_bp)
    # app.register_blueprint(book_bp)
    app.register_blueprint(addBook_bp)
    app.register_blueprint(deleteBook_bp)
