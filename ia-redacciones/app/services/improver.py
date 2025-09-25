import re
from typing import Dict, List
from .spellcheck import correct_text
from .tokenize import sentences

_spaces_re = re.compile(r'\s+')
_space_punct = [
    (re.compile(r'\s+,\s*'), ', '),
    (re.compile(r'\s+;\s*'), '; '),
    (re.compile(r'\s+:\s*'), ': '),
    (re.compile(r'\s+\.\s*'), '. '),
    (re.compile(r'\s+\?\s*'), '? '),
    (re.compile(r'\s+!\s*'), '! ')
]
_double_space = re.compile(r' {2,}')

_passive_re = re.compile(r'\b(es|son|fue|fueron|será|serán)\s+[a-záéíóúüñ]+(ado|ada|ados|adas|ido|ida|idos|idas)\b', re.IGNORECASE)

def improve(text: str, language: str = "es") -> Dict[str, object]:
    suggestions: List[Dict[str, str]] = []

    # 1) Normalizar espacios
    t = text.replace('\u00A0', ' ')
    t = _double_space.sub(' ', t)

    # 2) Espacios alrededor de puntuación
    for patt, repl in _space_punct:
        t2 = patt.sub(repl, t)
        if t2 != t:
            suggestions.append({"rule": "punctuation_spacing", "before": t, "after": t2})
            t = t2

    # 3) Dividir oraciones muy largas (>25 palabras)
    sents = sentences(t)
    new_sents: List[str] = []
    for s in sents:
        wc = len(s.split())
        if wc > 25:
            # Heurística: divide por ';' o ','
            parts = re.split(r'(;|,)', s)
            rebuilt = []
            acc = ""
            for p in parts:
                if p in {',',';'}:
                    acc += p
                    continue
                if not acc:
                    acc = p.strip()
                else:
                    acc = (acc + " " + p.strip()).strip()
                if len(acc.split()) >= 18:
                    rebuilt.append(acc.strip().rstrip(',;'))
                    acc = ""
            if acc.strip():
                rebuilt.append(acc.strip().rstrip(',;'))
            if rebuilt:
                suggestions.append({"rule":"split_long_sentence","original": s, "result": " ".join(x + "." for x in rebuilt)})
                new_sents.extend(x.strip().rstrip('.') for x in rebuilt)
            else:
                new_sents.append(s)
        else:
            new_sents.append(s)
    t = " ".join(s.strip().rstrip('.') + "." for s in new_sents) if new_sents else t

    # 4) Voz pasiva (sugerencia)
    if _passive_re.search(t):
        suggestions.append({"rule":"avoid_passive_voice","message":"Considera reescribir construcciones pasivas ('ser' + participio) a voz activa."})

    # 5) Corrección ortográfica al final
    corr = correct_text(t, language=language)
    if corr.get("corrections"):
        suggestions.append({"rule":"spelling", "count": str(len(corr["corrections"]))})
    t = corr["corrected_text"]

    # 6) Consolidar espacios finales
    t = _spaces_re.sub(lambda m: ' ' if '\n' not in m.group(0) else m.group(0), t).strip()
    return {"improved_text": t, "suggestions": suggestions}
