class Payment:
    def __init__(self, payment_method, amount):
        self.payment_method = payment_method
        self.amount = float(amount)
        self.status = "Pending"

    def process_payment(self):
        self.status = "Processed"
        return f"Payment processed successfully using {self.payment_method}."