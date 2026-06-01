from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.admin import Admin

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

books = []


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

    return render_template("admin/dashboard.html", books_count=len(books))


@admin_bp.route("/catalogue")
def catalogue():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    return render_template("admin/catalogue_management.html", books=books)


@admin_bp.route("/add-book", methods=["GET", "POST"])
def add_book():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    if request.method == "POST":
        book = {
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "isbn": request.form.get("isbn"),
            "genre": request.form.get("genre"),
            "price": request.form.get("price"),
            "stock": request.form.get("stock"),
            "image_url": request.form.get("image_url"),
            "description": request.form.get("description")
        }

        books.append(book)
        return redirect(url_for("admin.catalogue"))

    return render_template("admin/add_book.html")


@admin_bp.route("/edit-book/<int:index>", methods=["GET", "POST"])
def edit_book(index):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    if index < 0 or index >= len(books):
        return redirect(url_for("admin.catalogue"))

    if request.method == "POST":
        books[index]["title"] = request.form.get("title")
        books[index]["author"] = request.form.get("author")
        books[index]["isbn"] = request.form.get("isbn")
        books[index]["genre"] = request.form.get("genre")
        books[index]["price"] = request.form.get("price")
        books[index]["stock"] = request.form.get("stock")
        books[index]["image_url"] = request.form.get("image_url")
        books[index]["description"] = request.form.get("description")

        return redirect(url_for("admin.catalogue"))

    return render_template("admin/edit_book.html", book=books[index])


@admin_bp.route("/delete-book/<int:index>")
def delete_book(index):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    if 0 <= index < len(books):
        books.pop(index)

    return redirect(url_for("admin.catalogue"))


@admin_bp.route("/orders")
def orders():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    return render_template("admin/orders.html")


@admin_bp.route("/shipments")
def shipments():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    return render_template("admin/shipments.html")


@admin_bp.route("/sales-report")
def sales_report():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    return render_template("admin/sales_report.html")


@admin_bp.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.login"))