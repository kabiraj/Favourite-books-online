from app.models.cart import Cart
from app.models.order import Order


class Book:
    def __init__(self, book_id, title, price):
        self.book_id = book_id
        self.title = title
        self.price = price


book1 = Book(1, "Clean Code", 45.00)
book2 = Book(2, "Design Patterns", 60.00)

cart = Cart()

cart.add_item(book1, 2)
cart.add_item(book2, 1)

print("Cart items:")
for item in cart.items:
    print(item.book.title, item.quantity, item.subtotal())

print("Cart total:", cart.total())

cart.update_quantity(1, 3)
print("Updated Clean Code quantity to 3")
print("New cart total:", cart.total())

cart.remove_item(2)
print("Removed Design Patterns")
print("New cart total:", cart.total())

order = Order(
    customer_name="Lasith Perera",
    email="lasith@example.com",
    address="Melbourne, Australia",
    phone="0400000000",
    cart=cart,
    payment_method="Card"
)

print("\nOrder created successfully")
print("Order ID:", order.order_id)
print("Customer:", order.customer_name)
print("Payment:", order.payment_status)
print("Invoice:", order.invoice.invoice_number)
print("Total:", order.total_amount)

print("\nOrder items:")
for item in order.items:
    print(item.book_title, item.quantity, item.subtotal())