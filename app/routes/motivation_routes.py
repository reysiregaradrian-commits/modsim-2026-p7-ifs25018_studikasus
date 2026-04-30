from flask import Blueprint, request, jsonify
from app.services.motivation_service import generate_openers, get_all_openers

bp = Blueprint("openers", __name__, url_prefix="/openers")


# ── POST /openers/generate ───────────────────────────────
@bp.route("/generate", methods=["POST"])
def generate():
    """
    Generate 3–5 kalimat pembuka berdasarkan input pengguna.

    Body JSON:
        letter_type : lamaran | undangan | keluhan | penawaran
        recipient   : nama / jabatan penerima
        context     : konteks singkat tujuan surat
        tone        : formal | semi-formal | casual | persuasif
    """
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Request body harus berupa JSON"}), 400

    letter_type = body.get("letter_type", "").strip().lower()
    recipient   = body.get("recipient", "").strip()
    context     = body.get("context", "").strip()
    tone        = body.get("tone", "formal").strip().lower()

    try:
        req, openers = generate_openers(letter_type, recipient, context, tone)
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500

    return jsonify({
        "message": "Kalimat pembuka berhasil di-generate",
        "request": req.to_dict(),
        "openers": [o.to_dict() for o in openers],
    }), 201


# ── GET /openers ─────────────────────────────────────────
# ── GET /openers?type=lamaran ────────────────────────────
@bp.route("", methods=["GET"])
def list_openers():
    """
    Ambil semua hasil generate.
    Query param opsional: ?type=lamaran|undangan|keluhan|penawaran
    """
    letter_type = request.args.get("type", "").strip().lower() or None
    results     = get_all_openers(letter_type)
    return jsonify({
        "count":   len(results),
        "filter":  letter_type,
        "results": results,
    }), 200
