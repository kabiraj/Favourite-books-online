import bcrypt

class Person:
    def __init__(self, name, email, password, is_hashed=False):
        self.id = None
        self.name = name
        self.email = email
        self.password = None
        if is_hashed:
            self.password = password
        else:
            self.hash_password(password)

    def hash_password(self, password):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def check_password(self, password):
        stored = self.password
        if isinstance(stored, str):
            stored = stored.encode("utf-8")
        return bcrypt.checkpw(password.encode(), stored)
    

