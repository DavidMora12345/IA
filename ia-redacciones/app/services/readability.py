import re
from typing import Dict
from .tokenize import sentences, words

_vowels = set("aeiouáéíóúü")
_vowel_groups = re.compile(r'[aeiouáéíóúü]+', re.IGNORECASE)

def _normalize_word(w: str) -> str:
    return re.sub(r'[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ]', '', w, flags=re.UNICODE).lower()

def syllables_in_word(word: str) -> int:
    """
    Conteo aproximado de sílabas en español:
    - Cuenta grupos de vocales como 1 sílaba.
    - Ajuste para 'qu' y 'gu(e/i)' (u muda) sin diéresis.
    - Mínimo 1.
    """
    w = _normalize_word(word)
    if not w:
        return 0
    # 'qu' -> trata la 'u' como muda
    w = w.replace('que', 'qe').replace('qui', 'qi')
    # 'gue/gui' sin diéresis -> u muda
    w = w.replace('gue', 'ge').replace('gui', 'gi')
    # con diéresis 'güe/güi' la u suena, se mantiene
    groups = _vowel_groups.findall(w)
    count = len(groups)
    return max(1, count)

def syllables_in_text(text: str) -> int:
    return sum(syllables_in_word(w) for w in words(text))

def metrics(text: str) -> Dict[str, float]:
    sents = sentences(text)
    n_sent = max(1, len(sents))
    n_words = max(1, len(words(text)))
    n_syll = max(1, syllables_in_text(text))

    # Szigriszt-Pazos (adaptación Flesch para español)
    szp = 206.835 - 62.3 * (n_syll / n_words) - (n_words / n_sent)
    # Fernández-Huerta: 206.84 - 0.60 * sílabas/100palabras - 1.02 * (palabras/oración)
    syl_per_100 = (n_syll / n_words) * 100.0
    fh = 206.84 - 0.60 * syl_per_100 - 1.02 * (n_words / n_sent)

    return {
        "sentences": float(n_sent),
        "words": float(n_words),
        "syllables": float(n_syll),
        "szigriszt_pazos": round(szp, 2),
        "fernandez_huerta": round(fh, 2),
        "avg_sentence_length": round(n_words / n_sent, 2),
        "avg_syllables_per_word": round(n_syll / n_words, 3),
    }
