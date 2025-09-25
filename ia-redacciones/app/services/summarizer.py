import re
from typing import List
from collections import Counter
from .tokenize import sentences, words

# Lista resumida de stopwords en español
_STOP = {
    "a","acá","ahí","al","algo","algunas","algunos","allá","allí","ante","antes","aquel","aquella","aquellas","aquellos",
    "aqui","aquí","así","aun","aún","bajo","bien","cada","casi","como","con","contra","cual","cuales","cualquier",
    "cuan","cuándo","cuando","cuanto","cuántos","de","del","desde","donde","dónde","dos","el","él","ella","ellas",
    "ellos","en","entre","era","erais","eran","eras","eres","es","esa","esas","ese","eso","esos","esta","estaba",
    "estaban","estado","estamos","estar","estará","estas","este","esto","estos","estoy","fin","fue","fueron","gran",
    "ha","había","habían","habrá","hace","hacen","hacer","hacia","han","hasta","hay","la","las","le","les","lo","los",
    "más","me","mi","mis","mismo","mucho","muy","nada","ni","no","nos","nosotros","nuestra","nuestras","nuestro",
    "nuestros","o","os","otra","otras","otro","otros","para","pero","poco","por","porque","que","qué","quien","quienes",
    "se","sea","según","ser","si","sí","sido","siempre","sin","sobre","sois","solamente","solo","son","su","sus","tal",
    "también","tampoco","tan","tanto","te","tenemos","tengo","ti","tiene","tienen","todo","todos","tu","tus","un","una",
    "unas","uno","unos","usted","ustedes","va","vais","valor","vamos","van","varias","varios","vosotras","vosotros","y","ya"
}

def _word_scores(text: str) -> Counter:
    toks = [w.lower() for w in words(text)]
    toks = [t for t in toks if t not in _STOP and len(t) > 2]
    return Counter(toks)

def summarize(text: str, max_sentences: int = 3) -> str:
    sents = sentences(text)
    if not sents:
        return ""
    freq = _word_scores(text)
    scores: List[float] = []
    for s in sents:
        ws = [w.lower() for w in words(s)]
        sc = sum(freq.get(w, 0) for w in ws)
        scores.append(sc)
    # Seleccionar las mejores oraciones manteniendo el orden original
    top_idx = sorted(range(len(sents)), key=lambda i: scores[i], reverse=True)[:max_sentences]
    top_idx = sorted(top_idx)
    return " ".join(sents[i] for i in top_idx)
