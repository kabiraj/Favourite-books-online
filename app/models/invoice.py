class Invoice:
    def __init__(self, order):
        self.order = order
        self.invoice_number = f"INV-{order.order_id}"

    def get_total(self):
        return self.order.total_amount

    def get_invoice_summary(self):
        return {
            "invoice_number": self.invoice_number,
            "customer_name": self.order.customer_name,
            "total": self.order.total_amount,
            "payment_status": self.order.payment_status
        }