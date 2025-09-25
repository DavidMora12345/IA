from typing import Literal, Optional
from datetime import date
from ..core.config import settings
from ..engines.ollama import OllamaEngine

Tone = Literal["neutral","formal","informal","entusiasta","persuasivo"]
Length = Literal["corto","medio","largo"]

def _rules_template(topic: str, tone: Tone, length: Length, language: str = "es") -> str:
    n_bullets = {"corto":3, "medio":5, "largo":7}.get(length, 5)
    intro = {
        "neutral":"Aquí tienes un borrador claro y directo.",
        "formal":"A continuación, se presenta un borrador con estilo formal y preciso.",
        "informal":"Te dejo un borrador sencillo y cercano.",
        "entusiasta":"¡Vamos a por un borrador inspirador y enérgico!",
        "persuasivo":"Propuesta enfocada en beneficios y llamado a la acción."
    }[tone]
    lines = [f"# {topic}", "", intro, ""]
    lines.append("Puntos clave:")
    for i in range(1, n_bullets+1):
        lines.append(f"- Punto {i}: detalle breve y accionable.")
    lines += ["", "Conclusión:", "Cierre con una idea principal y, si aplica, llamada a la acción."]
    return "\n".join(lines)

def draft(topic: str, tone: Tone = "neutral", length: Length = "medio", language: str = "es") -> str:
    if settings.engine == "ollama" and settings.ollama_base_url:
        try:
            engine = OllamaEngine(settings.ollama_base_url, settings.ollama_model)
            prompt = f"""Eres un redactor en {language}. Escribe un borrador sobre: '{topic}'.
            Tono: {tone}. Longitud: {length}. Estructura con título, introducción, viñetas y cierre claro."""
            return engine.generate(prompt)
        except Exception:
            # Fallback
            return _rules_template(topic, tone, length, language)
    else:
        return _rules_template(topic, tone, length, language)
