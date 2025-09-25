from typing import Dict, List, Tuple
import re
from .tokenize import words, is_capitalized

class SpellResult(dict):
    corrected_text: str
    corrections: List[Dict[str, str]]

def correct_text(text: str, language: str = "es") -> Dict[str, object]:
    try:
        from spellchecker import SpellChecker
    except Exception:
        # Sin dependencia -> devuelve original
        return {"corrected_text": text, "corrections": [], "language": language, "note":"pyspellchecker no disponible"}
    sp = SpellChecker(language=language)
    tokens = re.findall(r"""[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+|\W+""", text, flags=re.UNICODE)
    out: List[str] = []
    corrections: List[Dict[str, str]] = []
    for t in tokens:
        if re.fullmatch(r'[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+', t):
            lower = t.lower()
            if lower in sp:
                out.append(t)
                continue
            # Evita cambiar nombres propios claros
            if is_capitalized(t):
                out.append(t)
                continue
            cand = sp.correction(lower)
            if cand and cand != lower:
                corrections.append({"from": t, "to": cand})
                out.append(cand if t.islower() else cand.capitalize())
            else:
                out.append(t)
        else:
            out.append(t)
    return {"corrected_text": "".join(out), "corrections": corrections, "language": language}
