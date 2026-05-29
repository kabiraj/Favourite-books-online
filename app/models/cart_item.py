class CartItem:
    def __init__(self, book, quantity):
        self.book = book
        self.quantity = int(quantity)

    def subtotal(self):
        return self.book.price * self.quantity

    def update_quantity(self, quantity):
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        self.quantity = quantity