import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from .config import active_config
from .extensions import db

# Folder root proyek (satu level di atas folder app/)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app() -> Flask:
    """Application factory — buat dan konfigurasi instance Flask."""
    app = Flask(__name__, static_folder=os.path.join(ROOT_DIR, "static"))
    app.config.from_object(active_config)

    # Pastikan DATABASE_URI menggunakan path absolut agar SQLite bisa ditemukan
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if db_uri.startswith("sqlite:///") and not db_uri.startswith("sqlite:////"):
        relative_path = db_uri[len("sqlite:///"):]
        abs_path = os.path.join(ROOT_DIR, relative_path)
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{abs_path}"

    # Extensions
    CORS(app)
    db.init_app(app)

    # Buat tabel jika belum ada
    with app.app_context():
        os.makedirs(os.path.join(ROOT_DIR, "db"), exist_ok=True)
        from .models import OpenerRequest, Opener # noqa: F401
        db.create_all()

    # Daftarkan blueprint
    from .routes.motivation_routes import bp as openers_bp
    app.register_blueprint(openers_bp)

    # Serve index.html di root
    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    return app
