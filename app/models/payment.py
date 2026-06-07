class Payment:
    def __init__(self, payment_method, amount, order_id):
        self.payment_method = payment_method
        self.amount = float(amount)
        self.transaction_ref = f"TXN-{order_id:04d}"
        self.status = "Processed"

    def process_payment(self):
        return (
            f"Payment processed successfully using {self.payment_method}. "
            f"Transaction reference: {self.transaction_ref}."
        )
