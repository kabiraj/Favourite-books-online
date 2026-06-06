class OrderItem:
    def __init__(self, book_title, price, quantity):
        self.book_title = book_title
        self.price = float(price)
        self.quantity = int(quantity)

    def subtotal(self):
        return self.price * self.quantity