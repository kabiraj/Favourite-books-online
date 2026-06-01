from app.models.person import Person
class Admin(Person):
    def __init__(self, name, email, password, is_hashed=False):
        super().__init__(name, email, password, is_hashed)

    def add_book(self):
        pass

    def edit_book(self):
        pass

    def remove_book(self):
        pass

    @staticmethod
    def login(username, password):
        return username == "admin" and password == "admin123"