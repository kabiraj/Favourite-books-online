from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.models.cart import Cart
from app.models.order import Order


cart_bp = Blueprint("cart", __name__)


def get_cart():
    cart_data = session.get("cart", [])
    cart = Cart()

    for item in cart_data:
        class Book:
            def __init__(self, book_id, title, price):
                self.book_id = int(book_id)
                self.title = title
                self.price = float(price)

        book = Book(item["book_id"], item["title"], item["price"])
        cart.add_item(book, item["quantity"])

    return cart


def save_cart(cart):
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
    cart = get_cart()

    return render_template(
        "cart.html",
        cart_items=cart.items,
        total=cart.total()
    )


@cart_bp.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    book_id = request.form.get("book_id")
    title = request.form.get("title")
    price = request.form.get("price")
    quantity = request.form.get("quantity", 1)

    if not book_id or not title or not price:
        flash("Book details are missing.", "error")
        return redirect(url_for("customer.catalogue"))

    class Book:
        def __init__(self, book_id, title, price):
            self.book_id = int(book_id)
            self.title = title
            self.price = float(price)

    try:
        cart = get_cart()
        book = Book(book_id, title, price)
        cart.add_item(book, quantity)
        save_cart(cart)
        flash("Book added to cart successfully.", "success")
    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/update-cart/<int:book_id>", methods=["POST"])
def update_cart(book_id):
    quantity = request.form.get("quantity")

    try:
        cart = get_cart()
        cart.update_quantity(book_id, quantity)
        save_cart(cart)
        flash("Cart updated successfully.", "success")
    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/remove-from-cart/<int:book_id>", methods=["POST"])
def remove_from_cart(book_id):
    cart = get_cart()
    cart.remove_item(book_id)
    save_cart(cart)

    flash("Book removed from cart.", "success")
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/checkout")
def checkout():
    cart = get_cart()

    if cart.is_empty():
        flash("Your cart is empty. Please add books before checkout.", "error")
        return redirect(url_for("cart.view_cart"))

    return render_template("checkout.html")


@cart_bp.route("/place-order", methods=["POST"])
def place_order():
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

        return render_template("order_confirmation.html", order=order)

    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("cart.checkout"))