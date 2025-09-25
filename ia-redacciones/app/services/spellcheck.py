from typing import Dict, List
from ..core.config import settings
from ..engines.ollama import OllamaEngine

def correct_text(text: str, language: str = "es") -> Dict[str, object]:
    """
    Corrección ortográfica y de puntuación usando Ollama.
    Mantiene el estilo, no reescribe en profundidad.
    """
    if not settings.ollama_base_url or settings.engine != "ollama":
        # Sin Ollama, no hacemos nada (no usamos pyspellchecker)
        return {
            "corrected_text": text,
            "corrections": [],
            "language": language,
            "note": "Ollama no configurado: ENGINE=ollama y OLLAMA_BASE_URL requeridos"
        }

    engine = OllamaEngine(settings.ollama_base_url, settings.ollama_model)
    prompt = f"""Actúa como corrector ortográfico y de puntuación en {language}.
Corrige tildes, mayúsculas, ortografía y puntuación mínima; NO cambies el estilo ni el significado.
Respeta nombres propios, URLs, cifras y saltos de línea.
Devuelve SOLO el texto corregido, sin comillas ni explicaciones.

TEXTO:
{text}
"""
    try:
        corrected = engine.generate(prompt).strip()
        # No calculamos diff palabra a palabra; devolvemos lista vacía.
        return {"corrected_text": corrected, "corrections": [], "language": language}
    except Exception as e:
        return {"corrected_text": text, "corrections": [], "language": language, "error": str(e)}
