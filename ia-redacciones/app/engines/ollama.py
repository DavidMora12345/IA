import json
from typing import Optional
from .base import TextEngine

try:
    from urllib.request import Request, urlopen
except Exception as e:
    Request = None
    urlopen = None

class OllamaEngine(TextEngine):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str) -> str:
        if not Request or not urlopen:
            raise RuntimeError("urllib no disponible en el entorno.")
        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        data = json.dumps(payload).encode("utf-8")
        req = Request(endpoint, data=data, headers={"Content-Type":"application/json"}, method="POST")
        with urlopen(req, timeout=120) as resp:
            raw = resp.read()
            obj = json.loads(raw.decode("utf-8"))
            return obj.get("response", "").strip()
