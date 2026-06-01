import bcrypt

class Person:
    def __init__(self, name, email, password):
        self.id = None
        self.name = name
        self.email = email
        self.password = None
        self.hash_password(password)

    "Hash password"
    def hash_password(self, password):
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password)
    

