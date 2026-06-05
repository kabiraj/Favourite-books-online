class Book:
    def __init__(
        self,
        title,
        author,
        isbn,
        price,
        stock,
        genre,
        image_url="",
        description="",
        id=None,
    ):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
        self.stock = stock
        self.genre = genre
        self.image_url = image_url
        self.description = description

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "price": self.price,
            "stock": self.stock,
            "genre": self.genre,
            "image_url": self.image_url,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(
            id=data.get("_id"),
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            price=data["price"],
            stock=data["stock"],
            genre=data.get("genre", ""),
            image_url=data.get("image_url", ""),
            description=data.get("description", ""),
        )
        return book