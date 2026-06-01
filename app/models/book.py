from tkinter import NO


class Book:
    def __init__(self, title, author, isbn, price, stock, genre, id=None):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
        self.stock = stock
        self.genre = genre

    def to_dict(self):
        return {
            ""
        }