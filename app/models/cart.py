from app.models.cart_item import CartItem


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, book, quantity=1):
        quantity = int(quantity)

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        for item in self.items:
            if item.book.isbn == book.isbn:
                item.update_quantity(item.quantity + quantity)
                return

        self.items.append(CartItem(book, quantity))

    def remove_item(self, isbn):
        self.items = [item for item in self.items if item.book.isbn != isbn]

    def update_quantity(self, isbn, quantity):
        quantity = int(quantity)

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        for item in self.items:
            if item.book.isbn == isbn:
                item.update_quantity(quantity)
                return

        raise ValueError("Book not found in cart")

    def total(self):
        return sum(item.subtotal() for item in self.items)

    def is_empty(self):
        return len(self.items) == 0

    def clear(self):
        self.items = []
