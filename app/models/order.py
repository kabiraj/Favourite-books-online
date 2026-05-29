from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.invoice import Invoice


class Order:
    order_counter = 1

    def __init__(self, customer_name, email, address, phone, cart, payment_method):
        if not customer_name.strip():
            raise ValueError("Customer name cannot be blank")
        if not email.strip():
            raise ValueError("Email cannot be blank")
        if not address.strip():
            raise ValueError("Address cannot be blank")
        if not phone.strip():
            raise ValueError("Phone number cannot be blank")
        if cart.is_empty():
            raise ValueError("Cart cannot be empty")

        self.order_id = Order.order_counter
        Order.order_counter += 1

        self.customer_name = customer_name
        self.email = email
        self.address = address
        self.phone = phone
        self.items = []

        for cart_item in cart.items:
            order_item = OrderItem(
                cart_item.book.title,
                cart_item.book.price,
                cart_item.quantity
            )
            self.items.append(order_item)

        self.total_amount = sum(item.subtotal() for item in self.items)

        payment = Payment(payment_method, self.total_amount)
        self.payment_status = payment.process_payment()

        self.invoice = Invoice(self)