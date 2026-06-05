from app.models.person import Person

class Customer(Person):
    def __init__(self, name, email, password, address, is_hashed=False, id=None):
        super().__init__(name, email, password, is_hashed)
        self.address = address
        self.id = id

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password.decode("utf-8"),
            "address": self.address
        }
    @classmethod
    def from_dict(cls, data):
        customer = cls(
            name = data["name"],
            email = data["email"],
            password = data["password"],
            address = data["address"],
            is_hashed = True,
            id = data["_id"]
        )
        return customer

