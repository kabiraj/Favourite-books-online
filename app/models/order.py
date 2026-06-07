from datetime import datetime, timezone

from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.invoice import Invoice
from app.models.shipment import Shipment


class Order:
    def __init__(
        self,
        order_id,
        customer_name,
        email,
        address,
        phone,
        cart,
        payment_method,
    ):
        if not customer_name.strip():
            raise ValueError("Customer name cannot be blank")
        if not email.strip():
            raise ValueError("Email cannot be blank")
        if not address.strip():
            raise ValueError("Address cannot be blank")
        if not phone.strip():
            raise ValueError("Phone number cannot be blank")
        if not payment_method.strip():
            raise ValueError("Payment method cannot be blank")
        if cart.is_empty():
            raise ValueError("Cart cannot be empty")

        self.order_id = order_id
        self.customer_name = customer_name.strip()
        self.email = email.strip()
        self.address = address.strip()
        self.phone = phone.strip()
        self.payment_method = payment_method.strip()
        self.items = []
        self.created_at = datetime.now(timezone.utc)

        for cart_item in cart.items:
            self.items.append(
                OrderItem(
                    cart_item.book.title,
                    cart_item.book.price,
                    cart_item.quantity,
                    cart_item.book.isbn,
                )
            )

        self.total_amount = sum(item.subtotal() for item in self.items)

        payment = Payment(payment_method, self.total_amount, self.order_id)
        self.payment_status = payment.process_payment()
        self.transaction_ref = payment.transaction_ref
        self.invoice = Invoice(self)
        self.shipment = Shipment(
            tracking_no=f"TRK-{self.order_id:04d}",
            status="Processing",
        )

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_name": self.customer_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "transaction_ref": self.transaction_ref,
            "invoice_number": self.invoice.invoice_number,
            "tracking_no": self.shipment.tracking_no,
            "shipment_status": self.shipment.status,
            "total_amount": self.total_amount,
            "items": [
                {
                    "book_title": item.book_title,
                    "isbn": item.isbn,
                    "price": item.price,
                    "quantity": item.quantity,
                }
                for item in self.items
            ],
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        order = cls.__new__(cls)
        order.order_id = data["order_id"]
        order.customer_name = data["customer_name"]
        order.email = data["email"]
        order.address = data["address"]
        order.phone = data["phone"]
        order.payment_method = data.get("payment_method", "")
        order.payment_status = data["payment_status"]
        order.transaction_ref = data.get("transaction_ref", "")
        order.total_amount = data["total_amount"]
        order.created_at = data.get("created_at")
        order.items = [
            OrderItem(
                item["book_title"],
                item["price"],
                item["quantity"],
                item.get("isbn", ""),
            )
            for item in data.get("items", [])
        ]
        order.invoice = Invoice(order)
        order.shipment = Shipment(
            tracking_no=data.get("tracking_no", ""),
            status=data.get("shipment_status", "Processing"),
        )
        return order
