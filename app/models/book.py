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
            "title" : self.title,
            "author" : self.author,
            "isbn" : self.isbn,
            "price" : self.price,
            "stock" : self.stock,
            "genre" : self.genre
        }
    @classmethod
    def from_dict(cls, data):
        book = cls(
            id = data["_id"],
            title = data["title"],
            author = data["author"],
            isbn = data["isbn"],
            price = data["price"],
            stock = data["stock"],
            genre = data["genre"]
        )
        return book