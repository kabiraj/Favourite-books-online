class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def login(username, password):
        return username == "admin" and password == "admin123"