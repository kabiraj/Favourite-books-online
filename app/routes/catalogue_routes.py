from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.models.catalogue import Catalogue

catalogue_bp = Blueprint("catalogue", __name__)


@catalogue_bp.route("/browse")
def browse():
    if not session.get("customer_logged_in"):
        flash("Please log in to browse books.", "error")
        return redirect(url_for("auth.login"))

    query = request.args.get("q", "").strip()
    books = Catalogue.search_books(query) if query else Catalogue.get_all_books()

    return render_template(
        "browse.html",
        books=books,
        search_query=query,
    )
