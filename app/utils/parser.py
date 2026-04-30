import re
from typing import List


def parse_openers(raw_text: str) -> List[str]:
    """
    Mem-parse raw text dari LLM menjadi list kalimat pembuka bersih.

    Strategi:
    1. Split per baris.
    2. Buang baris kosong.
    3. Buang awalan nomor / bullet (1. | 1) | - | * | •).
    4. Strip spasi berlebih.
    5. Kembalikan hanya baris yang punya isi bermakna (>= 10 karakter).
    """
    lines = raw_text.strip().splitlines()

    cleaned: List[str] = []
    # Pola awalan: "1.", "1)", "-", "*", "•", "–"
    prefix_pattern = re.compile(r"^\s*(?:\d+[.)]\s*|[-*•–]\s*)")

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Hapus awalan nomor / bullet
        line = prefix_pattern.sub("", line).strip()
        # Buang baris terlalu pendek (kemungkinan header/noise)
        if len(line) >= 10:
            cleaned.append(line)

    return cleaned
