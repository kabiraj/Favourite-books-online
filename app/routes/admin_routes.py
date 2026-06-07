from bson.objectid import ObjectId
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.models.admin import Admin
from app.models.book import Book
from app.models.catalogue import Catalogue
from app.models.database import Database

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _get_book_by_id(book_id):
    try:
        oid = ObjectId(book_id)
    except Exception:
        return None
    data = Database.get_db().books.find_one({"_id": oid})
    return Book.from_dict(data) if data else None


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if Admin.login(username, password):
            session["admin_logged_in"] = True
            return redirect(url_for("admin.dashboard"))

        flash("Invalid username or password")

    return render_template("admin/login.html")


@admin_bp.route("/dashboard")
def dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    books_count = Database.get_db().books.count_documents({})
    orders_count = Database.get_db().orders.count_documents({})
    pending_shipments_count = Database.get_db().orders.count_documents(
        {"shipment_status": {"$ne": "Delivered"}}
    )
    return render_template(
        "admin/dashboard.html",
        books_count=books_count,
        orders_count=orders_count,
        pending_shipments_count=pending_shipments_count,
    )


@admin_bp.route("/catalogue")
def catalogue():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    books = Catalogue.get_all_books()
    return render_template("admin/catalogue_management.html", books=books)


@admin_bp.route("/add-book", methods=["GET", "POST"])
def add_book():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        isbn = (request.form.get("isbn") or "").strip()
        db = Database.get_db()

        if db.books.find_one({"isbn": isbn}):
            flash("A book with this ISBN already exists.", "error")
            return render_template("admin/add_book.html"), 400

        book = Book(
            title=request.form.get("title", "").strip(),
            author=request.form.get("author", "").strip(),
            isbn=isbn,
            genre=request.form.get("genre", "").strip(),
            price=float(request.form.get("price") or 0),
            stock=int(request.form.get("stock") or 0),
            image_url=request.form.get("image_url", "").strip(),
            description=request.form.get("description", "").strip(),
        )
        db.books.insert_one(book.to_dict())
        flash("Book added to catalogue.", "success")
        return redirect(url_for("admin.catalogue"))

    return render_template("admin/add_book.html")


@admin_bp.route("/edit-book/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    book = _get_book_by_id(book_id)
    if not book:
        flash("Book not found.", "error")
        return redirect(url_for("admin.catalogue"))

    if request.method == "POST":
        isbn = (request.form.get("isbn") or "").strip()
        db = Database.get_db()
        duplicate = db.books.find_one({"isbn": isbn, "_id": {"$ne": ObjectId(book_id)}})
        if duplicate:
            flash("Another book already uses this ISBN.", "error")
            return render_template("admin/edit_book.html", book=book), 400

        updated = Book(
            title=request.form.get("title", "").strip(),
            author=request.form.get("author", "").strip(),
            isbn=isbn,
            genre=request.form.get("genre", "").strip(),
            price=float(request.form.get("price") or 0),
            stock=int(request.form.get("stock") or 0),
            image_url=request.form.get("image_url", "").strip(),
            description=request.form.get("description", "").strip(),
        )
        db.books.update_one({"_id": ObjectId(book_id)}, {"$set": updated.to_dict()})
        flash("Book updated.", "success")
        return redirect(url_for("admin.catalogue"))

    return render_template("admin/edit_book.html", book=book)


@admin_bp.route("/delete-book/<book_id>")
def delete_book(book_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    try:
        oid = ObjectId(book_id)
    except Exception:
        flash("Book not found.", "error")
        return redirect(url_for("admin.catalogue"))

    result = Database.get_db().books.delete_one({"_id": oid})
    if result.deleted_count:
        flash("Book removed.", "success")
    else:
        flash("Book not found.", "error")

    return redirect(url_for("admin.catalogue"))


@admin_bp.route("/orders")
def orders():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    order_list = list(
        Database.get_db().orders.find().sort("order_id", -1)
    )
    return render_template("admin/orders.html", orders=order_list)


@admin_bp.route("/shipments")
def shipments():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    shipment_list = list(
        Database.get_db().orders.find().sort("order_id", -1)
    )
    return render_template("admin/shipments.html", shipments=shipment_list)


@admin_bp.route("/shipments/<int:order_id>/update", methods=["POST"])
def update_shipment(order_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    new_status = (request.form.get("status") or "").strip()
    if not new_status:
        flash("Shipment status is required.", "error")
        return redirect(url_for("admin.shipments"))

    # Shipment status lives on the order document (no separate shipments collection).
    result = Database.get_db().orders.update_one(
        {"order_id": order_id},
        {"$set": {"shipment_status": new_status}},
    )
    if result.modified_count:
        flash(f"Shipment for order #{order_id} updated to '{new_status}'.", "success")
    else:
        flash("Order not found.", "error")

    return redirect(url_for("admin.shipments"))


@admin_bp.route("/sales-report")
def sales_report():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    return render_template("admin/sales_report.html")


@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.login"))
