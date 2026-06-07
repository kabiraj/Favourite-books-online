class OrderItem:
    def __init__(self, book_title, price, quantity, isbn=""):
        self.book_title = book_title
        self.price = float(price)
        self.quantity = int(quantity)
        self.isbn = isbn

    def subtotal(self):
        return self.price * self.quantity
