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


def validate_checkout(
    customer_name,
    email,
    address,
    phone,
    payment_method,
    card_name="",
    card_number="",
    expiry_date="",
    cvv="",
):
    errors = {}
    customer_name = (customer_name or "").strip()
    email = (email or "").strip()
    address = (address or "").strip()
    phone = (phone or "").strip()
    payment_method = (payment_method or "").strip()

    if not customer_name:
        errors["customer_name"] = "Customer name is required."
    elif len(customer_name) <= 3:
        errors["customer_name"] = "Customer name must be more than 3 characters."

    if not email:
        errors["email"] = "Email is required."
    elif not EMAIL_PATTERN.match(email):
        errors["email"] = "Enter a valid email address."

    if not address:
        errors["address"] = "Delivery address is required."
    elif len(address) < 10:
        errors["address"] = "Address must be at least 10 characters."
    elif not ADDRESS_PATTERN.match(address):
        errors["address"] = "Enter a valid delivery address (letters, numbers, commas)."

    phone_digits = re.sub(r"\D", "", phone)
    if not phone:
        errors["phone"] = "Phone number is required."
    elif len(phone_digits) < 10 or len(phone_digits) > 15:
        errors["phone"] = "Phone number must be 10 to 15 digits."

    if not payment_method:
        errors["payment_method"] = "Payment method is required."
    elif payment_method != "Card":
        errors["payment_method"] = "Only card payment is supported."

    if payment_method == "Card":
        errors.update(
            validate_card(card_name, card_number, expiry_date, cvv)
        )

    return errors


def validate_card(card_name, card_number, expiry_date, cvv):
    errors = {}
    card_name = (card_name or "").strip()
    card_number = re.sub(r"\s+", "", card_number or "")
    expiry_date = (expiry_date or "").strip()
    cvv = (cvv or "").strip()

    if not card_name:
        errors["card_name"] = "Name on card is required."
    elif len(card_name) < 2:
        errors["card_name"] = "Name on card must be at least 2 characters."

    if not card_number:
        errors["card_number"] = "Card number is required."
    elif not card_number.isdigit() or len(card_number) != 16:
        errors["card_number"] = "Card number must be 16 digits."

    if not expiry_date:
        errors["expiry_date"] = "Expiry date is required."
    elif not re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", expiry_date):
        errors["expiry_date"] = "Expiry date must be MM/YY (e.g. 12/28)."

    if not cvv:
        errors["cvv"] = "CVV is required."
    elif not re.match(r"^\d{3}$", cvv):
        errors["cvv"] = "CVV must be 3 digits."

    return errors
