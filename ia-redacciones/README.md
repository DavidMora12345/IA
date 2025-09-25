# IA de Redacciones (API REST)

API REST **sin dependencias de pago** para tareas de:
- Generación de borradores (`/v1/draft`)
- Mejora/edición de estilo (`/v1/improve`)
- Corrección ortográfica básica (`/v1/correct`)
- Resumen extractivo (`/v1/summarize`)
- Métricas de legibilidad en español (`/v1/readability`)
- Salud (`/health`)

## Requisitos
- Windows 10/11
- Python 3.13 (probado con `py --version`)
- Sin GPU ni servicios externos obligatorios. **Recomendado:** Ollama local para la generación.

## Instalación rápida en Windows (CMD)
```bat
C:
mkdir C:\ia-redacciones
cd C:\ia-redacciones
REM Copia aquí el contenido de este proyecto (o descomprime el ZIP)
py -3.13 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
REM Arranca Ollama en otro terminal: `ollama serve`
set OLLAMA_BASE_URL=http://localhost:11434
set ENGINE=ollama
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O usa `runserver.bat`:
```bat
C:
cd C:\ia-redacciones
runserver.bat
```

## .env (opcional)
Crea `C:\ia-redacciones\.env` copiando desde `.env.example` y ajusta:
```
ENGINE=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
```

## Endpoints (cURL)

**Borrador**
```bat
curl -X POST "http://127.0.0.1:8000/v1/draft" ^
     -H "Content-Type: application/json" ^
     -d "{"topic":"Eficiencia energética en casa","tone":"neutral","length":"medio","language":"es"}"
```

**Mejora**
```bat
curl -X POST "http://127.0.0.1:8000/v1/improve" ^
     -H "Content-Type: application/json" ^
     -d "{"text":"Este es un texto   con  errores ,  y frases muy largas que deberian dividirse para facilitar la lectura","language":"es"}"
```

**Corrección ortográfica**
```bat
curl -X POST "http://127.0.0.1:8000/v1/correct" ^
     -H "Content-Type: application/json" ^
     -d "{"text":"Hize una prueba con ortgrafia.","language":"es"}"
```

**Resumen**
```bat
curl -X POST "http://127.0.0.1:8000/v1/summarize" ^
     -H "Content-Type: application/json" ^
     -d "{"text":"<pega un texto largo>","max_sentences":3,"language":"es"}"
```

**Legibilidad**
```bat
curl -X POST "http://127.0.0.1:8000/v1/readability" ^
     -H "Content-Type: application/json" ^
     -d "{"text":"<tu texto>","language":"es"}"
```

## Arquitectura
```
app/
  core/config.py          # Config (.env), selección de motor
  engines/base.py         # Interfaz de motor
  engines/ollama.py       # Cliente opcional para Ollama
  services/tokenize.py    # Tokenización simple ES
  services/readability.py # Métricas y sílabas ES
  services/summarizer.py  # Resumen extractivo básico
  services/spellcheck.py  # Corrección con pyspellchecker
  services/improver.py    # Reglas de estilo/sugerencias
  services/drafter.py     # Borradores (rules / ollama)
  main.py                 # FastAPI app y rutas
```

## Notas
- La corrección ortográfica usa un diccionario general: revisa nombres propios.
- Las métricas y la división de oraciones son aproximadas.
- Con la configuración por defecto (`ENGINE=ollama`), el endpoint `/v1/draft` usa el modelo definido en `OLLAMA_MODEL` (por defecto `llama3.1:8b`).
- Si prefieres las plantillas internas sin IA, cambia `ENGINE=rules`.
