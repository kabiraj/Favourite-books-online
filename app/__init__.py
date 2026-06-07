from flask import Flask, render_template, session

def create_app():
    app = Flask(__name__)
    app.secret_key = "favourite-books-secret-key"

    # Dev-only: prevent browser from caching static assets,
    # so CSS/HTML changes reflect immediately on refresh.
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    from app.routes.admin_routes import admin_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.catalogue_routes import catalogue_bp
    from app.routes.cart_routes import cart_bp


    app.register_blueprint(cart_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(catalogue_bp)

    @app.route("/")
    def home():
        return render_template(
            "home.html",
            customer_logged_in=session.get("customer_logged_in"),
        )

    return app