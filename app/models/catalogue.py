from app.models.database import Database
from app.models.book import Book

class Catalogue:
    @classmethod
    def get_all_books(cls):
        db = Database.get_db()
        books_data = db.books.find()
        books = []
        for book in books_data:
            books.append(Book.from_dict(book))
        return books

    @classmethod
    def search_books(cls, query):
        db = Database.get_db()
        books_data = db.books.find({
            "$or" : [
                {"title": {"$regex": query, "$options": "i"}},
                {"author": {"$regex": query, "$options": "i"}},
                {"isbn": {"$regex": query, "$options": "i"}}
            ]
        })
        books = []
        for book in books_data:
            books.append(Book.from_dict(book))
        return books
