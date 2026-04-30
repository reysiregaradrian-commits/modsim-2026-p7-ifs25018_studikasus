import anthropic
from flask import current_app


LETTER_TYPE_LABELS = {
    "lamaran":   "surat lamaran pekerjaan",
    "undangan":  "surat undangan resmi",
    "keluhan":   "surat keluhan / pengaduan",
    "penawaran": "surat penawaran bisnis atau produk",
}

TONE_LABELS = {
    "formal":      "sangat formal dan profesional",
    "semi-formal": "semi-formal, ramah namun tetap sopan",
    "casual":      "santai namun tetap menghormati penerima",
    "persuasif":   "persuasif, meyakinkan, dan antusias",
}


def build_prompt(letter_type: str, recipient: str, context: str, tone: str, count: int = 5) -> str:
    jenis = LETTER_TYPE_LABELS.get(letter_type, letter_type)
    nada  = TONE_LABELS.get(tone, tone)

    return f"""Kamu adalah ahli penulisan surat dan email profesional berbahasa Indonesia.

Tugasmu: Buat TEPAT {count} variasi kalimat pembuka untuk {jenis}.

Detail konteks:
- Nama / jabatan penerima : {recipient}
- Tujuan / konteks surat  : {context}
- Gaya bahasa             : {nada}

Aturan ketat:
1. Setiap kalimat harus UNIK — berbeda struktur, pilihan kata, maupun pendekatan.
2. Kalimat harus lengkap, natural, dan langsung bisa dipakai tanpa editan.
3. Jangan tambahkan nomor, bullet, penjelasan, atau kalimat lain di luar {count} kalimat itu.
4. Balas HANYA dengan {count} kalimat, masing-masing pada baris terpisah."""


def call_llm(letter_type: str, recipient: str, context: str, tone: str) -> str:
    """
    Memanggil Anthropic API dan mengembalikan raw text response.
    Raise exception jika API key tidak ada atau request gagal.
    """
    api_key = current_app.config.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY belum dikonfigurasi di .env")

    model      = current_app.config.get("LLM_MODEL", "claude-3-5-haiku-20241022")
    max_tokens = current_app.config.get("LLM_MAX_TOKENS", 1024)
    count      = current_app.config.get("OPENER_COUNT", 5)

    client  = anthropic.Anthropic(api_key=api_key)
    prompt  = build_prompt(letter_type, recipient, context, tone, count)

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
