from datetime import datetime, timezone
from app.extensions import db


class OpenerRequest(db.Model):
    """
    Model untuk menyimpan permintaan generate kalimat pembuka.
    Sesuai spesifikasi modul: id, letter_type, recipient, context, tone, created_at
    """
    __tablename__ = "opener_requests"

    id         = db.Column(db.Integer, primary_key=True)
    letter_type = db.Column(db.String(50), nullable=False, index=True)
    # Nilai: lamaran | undangan | keluhan | penawaran
    recipient  = db.Column(db.String(150), nullable=False)
    context    = db.Column(db.Text, nullable=False)
    tone       = db.Column(db.String(50), nullable=False)
    # Nilai: formal | semi-formal | casual | persuasif
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relasi one-to-many ke Opener
    openers = db.relationship(
        "Opener",
        backref="request",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def to_dict(self, include_openers: bool = False) -> dict:
        data = {
            "id":          self.id,
            "letter_type": self.letter_type,
            "recipient":   self.recipient,
            "context":     self.context,
            "tone":        self.tone,
            "created_at":  self.created_at.isoformat(),
        }
        if include_openers:
            data["openers"] = [o.to_dict() for o in self.openers]
        return data

    def __repr__(self):
        return f"<OpenerRequest id={self.id} type={self.letter_type}>"
