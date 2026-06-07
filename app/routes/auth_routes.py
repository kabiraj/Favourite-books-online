from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.customer import Customer
from app.models.database import Database
from app.validation import validate_signup, validate_login

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        address = request.form.get("address", "")
        form = {
            "name": name.strip(),
            "email": email.strip(),
            "address": address.strip(),
        }

        errors = validate_signup(name, email, password, address)
        if errors:
            return render_template(
                "register.html", errors=errors, form=form
            ), 400

        db = Database.get_db()
        existing_customer = db.customers.find_one({"email": form["email"]})

        if existing_customer:
            flash("Email already exists. Please login.", "error")
            return redirect(url_for("auth.register"))

        customer = Customer(
            form["name"], form["email"], password, form["address"]
        )
        db.customers.insert_one(customer.to_dict())
        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("customer_logged_in"):
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        form = {"email": email.strip()}

        errors = validate_login(email, password)
        if errors:
            return render_template("login.html", errors=errors, form=form), 400

        db = Database.get_db()
        customer_data = db.customers.find_one({"email": form["email"]})

        if not customer_data:
            flash("No account found with this email.", "error")
            errors = {"email": "No account found with this email."}
            return render_template("login.html", errors=errors, form=form), 401

        customer = Customer.from_dict(customer_data)
        if not customer.check_password(password):
            flash("Incorrect password.", "error")
            errors = {"password": "Incorrect password."}
            return render_template("login.html", errors=errors, form=form), 401

        # Session keys used across browse, cart, checkout, and order history.
        session["customer_logged_in"] = True
        session["customer_email"] = customer.email
        session["customer_name"] = customer.name
        session["customer_id"] = str(customer.id)

        return redirect(url_for("home"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("customer_logged_in", None)
    session.pop("customer_email", None)
    session.pop("customer_name", None)
    session.pop("customer_id", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
