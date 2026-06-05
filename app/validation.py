import re

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$"
)
ADDRESS_PATTERN = re.compile(r"^[A-Za-z0-9\s,.\-#/]{10,}$")


def validate_signup(name, email, password, address):
    errors = {}
    name = (name or "").strip()
    email = (email or "").strip()
    password = password or ""
    address = (address or "").strip()

    if not name:
        errors["name"] = "Name is required."
    elif len(name) <= 3:
        errors["name"] = "Name must be more than 3 characters."

    if not email:
        errors["email"] = "Email is required."
    elif not EMAIL_PATTERN.match(email):
        errors["email"] = "Enter a valid email address."

    if not password:
        errors["password"] = "Password is required."
    elif not PASSWORD_PATTERN.match(password):
        errors["password"] = (
            "Password must be at least 8 characters and include uppercase, "
            "lowercase, a number, and a special character."
        )

    if not address:
        errors["address"] = "Address is required."
    elif len(address) < 10:
        errors["address"] = "Address must be at least 10 characters."
    elif not ADDRESS_PATTERN.match(address):
        errors["address"] = "Enter a valid shipping address (letters, numbers, commas)."

    return errors


def validate_login(email, password):
    errors = {}
    email = (email or "").strip()
    password = password or ""

    if not email:
        errors["email"] = "Email is required."
    elif not EMAIL_PATTERN.match(email):
        errors["email"] = "Enter a valid email address."

    if not password:
        errors["password"] = "Password is required."

    return errors
