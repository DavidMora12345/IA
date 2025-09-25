import re
from typing import List

_sent_split = re.compile(r'(?<=[\.\?\!…;:])\s+')
_word_re = re.compile(r"""[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:'[A-Za-z]+)?|\d+""", re.UNICODE)

def sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    parts = _sent_split.split(text)
    # Limpia espacios extra
    return [p.strip() for p in parts if p.strip()]

def words(text: str) -> List[str]:
    return _word_re.findall(text)

def is_capitalized(word: str) -> bool:
    return len(word) > 0 and word[0].isupper()
