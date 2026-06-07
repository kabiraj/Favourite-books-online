from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.models.book import Book
from app.models.cart import Cart
from app.models.customer import Customer
from app.models.database import Database
from app.models.order import Order
from app.validation import validate_checkout

# Cart, checkout, and customer order routes (Blueprint name "customer" for url_for).
cart_bp = Blueprint("customer", __name__)


class CartBook:
    """Lightweight book representation stored in the session cart."""

    def __init__(self, isbn, title, price):
        self.isbn = isbn
        self.title = title
        self.price = float(price)


def customer_login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("customer_logged_in"):
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def _get_book_by_isbn(isbn):
    data = Database.get_db().books.find_one({"isbn": isbn})
    return Book.from_dict(data) if data else None


def _next_order_id(db):
    # Auto-increment order_id from the highest existing order in MongoDB.
    latest = db.orders.find_one(sort=[("order_id", -1)])
    return (latest["order_id"] + 1) if latest else 1


def get_cart():
    # Rebuild Cart from Flask session (stored as plain dicts, not Book objects).
    cart_data = session.get("cart", [])
    cart = Cart()

    for item in cart_data:
        book = CartBook(
            isbn=item["isbn"],
            title=item["title"],
            price=item["price"],
        )
        cart.add_item(book, item["quantity"])

    return cart


def save_cart(cart):
    # Write cart back to session in a JSON-serializable format.
    session["cart"] = [
        {
            "isbn": item.book.isbn,
            "title": item.book.title,
            "price": item.book.price,
            "quantity": item.quantity,
        }
        for item in cart.items
    ]


def _reduce_stock(cart):
    # Check all stock first, then decrement — avoids partial updates on failure.
    db = Database.get_db()
    for item in cart.items:
        book = db.books.find_one({"isbn": item.book.isbn})
        if not book:
            raise ValueError(f"Book '{item.book.title}' is no longer available.")
        if book["stock"] < item.quantity:
            raise ValueError(
                f"Not enough stock for '{item.book.title}'. "
                f"Only {book['stock']} left."
            )

    for item in cart.items:
        db.books.update_one(
            {"isbn": item.book.isbn},
            {"$inc": {"stock": -item.quantity}},
        )


@cart_bp.route("/cart")
@customer_login_required
def view_cart():
    cart = get_cart()
    return render_template(
        "cart.html",
        cart_items=cart.items,
        total=cart.total(),
    )


@cart_bp.route("/cart/add", methods=["POST"])
@customer_login_required
def add_to_cart():
    isbn = (request.form.get("isbn") or "").strip()
    quantity = request.form.get("quantity", 1)

    book = _get_book_by_isbn(isbn)
    if not book:
        flash("Book not found.", "error")
        return redirect(url_for("catalogue.browse"))

    if book.stock < 1:
        flash("This book is out of stock.", "error")
        return redirect(url_for("catalogue.browse"))

    try:
        qty = int(quantity)
        cart = get_cart()
        existing = next((i for i in cart.items if i.book.isbn == isbn), None)
        current_qty = existing.quantity if existing else 0

        if current_qty + qty > book.stock:
            flash(f"Only {book.stock} copy/copies available in stock.", "error")
            return redirect(url_for("catalogue.browse"))

        cart_book = CartBook(book.isbn, book.title, book.price)
        cart.add_item(cart_book, qty)
        save_cart(cart)
        flash(f"'{book.title}' added to cart.", "success")
    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("catalogue.browse"))


@cart_bp.route("/update-cart/<isbn>", methods=["POST"])
@customer_login_required
def update_cart(isbn):
    quantity = request.form.get("quantity")

    try:
        book = _get_book_by_isbn(isbn)
        if not book:
            raise ValueError("Book not found.")

        qty = int(quantity)
        if qty > book.stock:
            raise ValueError(f"Only {book.stock} copy/copies available in stock.")

        cart = get_cart()
        cart.update_quantity(isbn, qty)
        save_cart(cart)
        flash("Cart updated.", "success")
    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("customer.view_cart"))


@cart_bp.route("/remove-from-cart/<isbn>", methods=["POST"])
@customer_login_required
def remove_from_cart(isbn):
    cart = get_cart()
    cart.remove_item(isbn)
    save_cart(cart)
    flash("Book removed from cart.", "error")
    return redirect(url_for("customer.view_cart"))


@cart_bp.route("/checkout")
@customer_login_required
def checkout():
    cart = get_cart()
    if cart.is_empty():
        flash("Your cart is empty. Please add books before checkout.", "error")
        return redirect(url_for("customer.view_cart"))

    customer = None
    customer_id = session.get("customer_id")
    if customer_id:
        from bson.objectid import ObjectId

        try:
            data = Database.get_db().customers.find_one({"_id": ObjectId(customer_id)})
            if data:
                customer = Customer.from_dict(data)
        except Exception:
            pass

    return render_template(
        "checkout.html",
        customer=customer,
        total=cart.total(),
        form=session.pop("checkout_form", {}),
        errors=session.pop("checkout_errors", {}),
    )


@cart_bp.route("/place-order", methods=["POST"])
@customer_login_required
def place_order():
    cart = get_cart()

    customer_name = request.form.get("customer_name", "").strip()
    email = request.form.get("email", "").strip()
    address = request.form.get("address", "").strip()
    phone = request.form.get("phone", "").strip()
    payment_method = request.form.get("payment_method", "").strip()

    errors = validate_checkout(
        customer_name,
        email,
        address,
        phone,
        payment_method,
        request.form.get("card_name"),
        request.form.get("card_number"),
        request.form.get("expiry_date"),
        request.form.get("cvv"),
    )
    if errors:
        # Keep form values in session so checkout page can repopulate after errors.
        session["checkout_form"] = {
            key: request.form.get(key, "")
            for key in (
                "customer_name",
                "email",
                "address",
                "phone",
                "payment_method",
                "card_name",
                "card_number",
                "expiry_date",
            )
        }
        session["checkout_errors"] = errors
        return redirect(url_for("customer.checkout"))

    try:
        _reduce_stock(cart)
        db = Database.get_db()
        order_id = _next_order_id(db)

        order = Order(
            order_id=order_id,
            customer_name=customer_name,
            email=email,
            address=address,
            phone=phone,
            cart=cart,
            payment_method=payment_method,
        )

        db.orders.insert_one(order.to_dict())
        session["cart"] = []

        return render_template("order_confirmation.html", order=order)

    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("customer.checkout"))


@cart_bp.route("/orders")
@customer_login_required
def my_orders():
    # List all orders placed by the logged-in customer (matched by email).
    email = session.get("customer_email")
    orders = list(
        Database.get_db().orders.find({"email": email}).sort("order_id", -1)
    )
    return render_template("orders.html", orders=orders)
