from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.models.cart import Cart
from app.models.order import Order
from app.models.database import Database
from app.models.book import Book


cart_bp = Blueprint("customer", __name__)


class CartBook:
    """
    Small wrapper class used only for cart storage.
    Wali's Book objects may not have book_id, so we use the list index as book_id.
    """
    def __init__(self, book_id, title, price):
        self.book_id = int(book_id)
        self.title = title
        self.price = float(price)


def get_cart():
    """
    Rebuilds a Cart object from Flask session data.
    """
    cart_data = session.get("cart", [])
    cart = Cart()

    for item in cart_data:
        book = CartBook(
            book_id=item["book_id"],
            title=item["title"],
            price=item["price"]
        )

        cart.add_item(book, item["quantity"])

    return cart


def save_cart(cart):
    """
    Saves cart items into Flask session.
    Session stores simple dictionary data, not full objects.
    """
    cart_data = []

    for item in cart.items:
        cart_data.append({
            "book_id": item.book.book_id,
            "title": item.book.title,
            "price": item.book.price,
            "quantity": item.quantity
        })

    session["cart"] = cart_data


@cart_bp.route("/cart")
def view_cart():
    """
    Displays all items currently in the shopping cart.
    """
    cart = get_cart()

    return render_template(
        "cart.html",
        cart_items=cart.items,
        total=cart.total()
    )


@cart_bp.route("/add-to-cart/<int:index>", methods=["POST"])
def add_to_cart(index):
    db = Database.get_db()
    books = list(db.books.find())

    if index < 0 or index >= len(books):
        flash("Book not found.")
        return redirect(url_for("catalogue.browse"))

    selected_book = Book.from_dict(books[index])
    quantity = request.form.get("quantity", 1)

    try:
        book = CartBook(
            book_id=index,
            title=selected_book.title,
            price=selected_book.price
        )

        cart = get_cart()
        cart.add_item(book, quantity)
        save_cart(cart)

        flash("Book added to cart successfully.")

    except ValueError as error:
        flash(str(error))

    return redirect(url_for("customer.view_cart"))


@cart_bp.route("/update-cart/<int:book_id>", methods=["POST"])
def update_cart(book_id):
    """
    Updates the quantity of a selected cart item.
    """
    quantity = request.form.get("quantity")

    try:
        cart = get_cart()
        cart.update_quantity(book_id, quantity)
        save_cart(cart)

        flash("Cart updated successfully.")

    except ValueError as error:
        flash(str(error))

    return redirect(url_for("customer.view_cart"))


@cart_bp.route("/remove-from-cart/<int:book_id>", methods=["POST"])
def remove_from_cart(book_id):
    """
    Removes a selected book from the cart.
    """
    cart = get_cart()
    cart.remove_item(book_id)
    save_cart(cart)

    flash("Book removed from cart.")
    return redirect(url_for("customer.view_cart"))


@cart_bp.route("/checkout")
def checkout():
    """
    Displays checkout page if the cart is not empty.
    """
    cart = get_cart()

    if cart.is_empty():
        flash("Your cart is empty. Please add books before checkout.")
        return redirect(url_for("customer.view_cart"))

    return render_template("checkout.html")


@cart_bp.route("/place-order", methods=["POST"])
def place_order():
    """
    Creates an order from cart items and displays order confirmation.
    Payment is simplified as a confirmation message.
    """
    cart = get_cart()

    customer_name = request.form.get("customer_name", "").strip()
    email = request.form.get("email", "").strip()
    address = request.form.get("address", "").strip()
    phone = request.form.get("phone", "").strip()
    payment_method = request.form.get("payment_method", "").strip()

    try:
        order = Order(
            customer_name=customer_name,
            email=email,
            address=address,
            phone=phone,
            cart=cart,
            payment_method=payment_method
        )

        session["cart"] = []

        return render_template(
            "order_confirmation.html",
            order=order
        )

    except ValueError as error:
        flash(str(error))
        return redirect(url_for("customer.checkout"))