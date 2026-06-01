from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "favourite-books-secret-key"

    from app.routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)

    @app.route("/")
    def home():
        return "<h1>Favourite Books Online</h1>"

    return app