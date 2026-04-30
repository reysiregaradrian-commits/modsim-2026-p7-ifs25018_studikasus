from datetime import datetime, timezone
from app.extensions import db


class Opener(db.Model):
    """
    Model untuk menyimpan setiap kalimat pembuka hasil generate.
    Sesuai spesifikasi modul: id, content, request_id, created_at
    """
    __tablename__ = "openers"

    id         = db.Column(db.Integer, primary_key=True)
    content    = db.Column(db.Text, nullable=False)
    request_id = db.Column(
        db.Integer,
        db.ForeignKey("opener_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self) -> dict:
        return {
            "id":         self.id,
            "content":    self.content,
            "request_id": self.request_id,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Opener id={self.id} request_id={self.request_id}>"
