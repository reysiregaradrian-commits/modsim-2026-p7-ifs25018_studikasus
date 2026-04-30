from flask_sqlalchemy import SQLAlchemy

# Instance SQLAlchemy dibuat di sini agar bisa di-import
# di seluruh modul tanpa circular import
db = SQLAlchemy()
