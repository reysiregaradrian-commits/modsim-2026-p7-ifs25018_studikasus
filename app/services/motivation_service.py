from typing import List, Optional, Tuple
from app.extensions import db
from app.models.opener_request import OpenerRequest
from app.models.opener import Opener
from app.services.llm_service import call_llm
from app.utils.parser import parse_openers


VALID_LETTER_TYPES = {"lamaran", "undangan", "keluhan", "penawaran"}
VALID_TONES        = {"formal", "semi-formal", "casual", "persuasif"}


def validate_input(letter_type: str, recipient: str, context: str, tone: str) -> Optional[str]:
    """Return pesan error jika validasi gagal, None jika lolos."""
    if letter_type not in VALID_LETTER_TYPES:
        return f"letter_type tidak valid. Pilihan: {', '.join(sorted(VALID_LETTER_TYPES))}"
    if not recipient or not recipient.strip():
        return "recipient tidak boleh kosong"
    if not context or len(context.strip()) < 5:
        return "context minimal 5 karakter"
    if tone not in VALID_TONES:
        return f"tone tidak valid. Pilihan: {', '.join(sorted(VALID_TONES))}"
    return None


def generate_openers(
    letter_type: str,
    recipient: str,
    context: str,
    tone: str,
) -> Tuple[OpenerRequest, List[Opener]]:
    """
    1. Validasi input.
    2. Simpan OpenerRequest ke DB.
    3. Panggil LLM.
    4. Parse hasil → simpan tiap Opener ke DB.
    5. Return (request, list_opener).
    """
    error = validate_input(letter_type, recipient, context, tone)
    if error:
        raise ValueError(error)

    # Simpan request log
    req = OpenerRequest(
        letter_type=letter_type,
        recipient=recipient.strip(),
        context=context.strip(),
        tone=tone,
    )
    db.session.add(req)
    db.session.flush()  # dapat req.id sebelum commit

    # Panggil LLM
    raw_text = call_llm(letter_type, recipient, context, tone)
    sentences = parse_openers(raw_text)

    if not sentences:
        db.session.rollback()
        raise RuntimeError("LLM tidak menghasilkan kalimat pembuka yang valid")

    # Simpan setiap kalimat pembuka
    openers: List[Opener] = []
    for sentence in sentences:
        opener = Opener(content=sentence, request_id=req.id)
        db.session.add(opener)
        openers.append(opener)

    db.session.commit()
    return req, openers


def get_all_openers(letter_type: Optional[str] = None) -> List[dict]:
    """
    Ambil semua OpenerRequest beserta opener-nya.
    Jika letter_type diisi, filter berdasarkan jenis surat.
    """
    query = OpenerRequest.query.order_by(OpenerRequest.created_at.desc())
    if letter_type:
        query = query.filter_by(letter_type=letter_type)

    results = []
    for req in query.all():
        data = req.to_dict()
        data["openers"] = [o.to_dict() for o in req.openers.order_by(Opener.id)]
        results.append(data)
    return results
