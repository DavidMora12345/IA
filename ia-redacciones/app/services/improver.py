import re
from typing import Dict, List
from ..core.config import settings
from ..engines.ollama import OllamaEngine

def _ollama_improve(text: str, language: str = "es") -> str:
    """
    Reescritura completa con Ollama: ortografía, gramática, puntuación y claridad.
    Devuelve SOLO el texto reescrito.
    """
    if not settings.ollama_base_url or settings.engine != "ollama":
        raise RuntimeError("Ollama no está configurado: ENGINE=ollama y OLLAMA_BASE_URL requeridos")
    engine = OllamaEngine(settings.ollama_base_url, settings.ollama_model)
    prompt = f"""Eres un corrector y editor experto en {language}.
Reescribe el siguiente texto manteniendo el sentido y mejorando:
- ortografía y gramática
- puntuación y espacios
- claridad y fluidez (divide oraciones largas si conviene)
- evita voz pasiva cuando sea natural
- respeta nombres propios, URLs, cifras y formato (conserva saltos de línea)
- NO añadas ni inventes información

Devuelve SOLO el texto reescrito, sin comillas ni explicaciones.

TEXTO:
{text}
"""
    return engine.generate(prompt).strip()

def improve(text: str, language: str = "es") -> Dict[str, object]:
    """
    Modo SOLO OLLAMA: no aplica reglas locales ni pyspellchecker.
    """
    try:
        improved = _ollama_improve(text, language=language)
        return {
            "improved_text": improved,
            "suggestions": [
                {"rule": "ollama_rewrite", "model": settings.ollama_model}
            ]
        }
    except Exception as e:
        # Fallback blando: devolvemos el original con aviso (sin reglas locales)
        return {
            "improved_text": text,
            "suggestions": [
                {"rule": "ollama_error", "message": str(e)}
            ]
        }
