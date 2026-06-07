class Shipment:
    def __init__(self, tracking_no, status):
        self.tracking_no = tracking_no
        self.status = status
    def update_status(self, status):
        self.status = status
