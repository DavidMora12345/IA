from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any

from .services.readability import metrics
from .services.summarizer import summarize
from .services.spellcheck import correct_text
from .services.improver import improve
from .services.drafter import draft

app = FastAPI(title="IA Redacciones API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

class DraftIn(BaseModel):
    topic: str = Field(..., description="Tema o consigna")
    tone: Literal["neutral","formal","informal","entusiasta","persuasivo"] = "neutral"
    length: Literal["corto","medio","largo"] = "medio"
    language: Literal["es","en"] = "es"

class ImproveIn(BaseModel):
    text: str
    language: Literal["es","en"] = "es"

class CorrectIn(BaseModel):
    text: str
    language: Literal["es","en"] = "es"

class SummarizeIn(BaseModel):
    text: str
    max_sentences: int = 3
    language: Literal["es","en"] = "es"

class ReadabilityIn(BaseModel):
    text: str
    language: Literal["es","en"] = "es"

@app.get("/health")
def health() -> dict:
    return {"status":"ok"}

@app.post("/v1/draft")
def api_draft(body: DraftIn) -> dict:
    text = draft(body.topic, body.tone, body.length, body.language)
    return {"draft": text, "engine": "rules_or_ollama"}

@app.post("/v1/improve")
def api_improve(body: ImproveIn) -> dict:
    res = improve(body.text, language=body.language)
    return res

@app.post("/v1/correct")
def api_correct(body: CorrectIn) -> dict:
    return correct_text(body.text, language=body.language)

@app.post("/v1/summarize")
def api_summarize(body: SummarizeIn) -> dict:
    text = summarize(body.text, max_sentences=body.max_sentences)
    return {"summary": text, "sentences": body.max_sentences}

@app.post("/v1/readability")
def api_readability(body: ReadabilityIn) -> dict:
    return metrics(body.text)
