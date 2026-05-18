"""Local FastAPI proof service for retrieval and safety eval workflows."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent_safety_eval import run_eval
from rag_proof_retriever import run_query


SERVICE_VERSION = "0.1.0"


class HealthResponse(BaseModel):
    status: str
    version: str


class RetrieveRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class SearchHitResponse(BaseModel):
    document_id: str
    title: str
    url: str
    chunk_index: int
    score: float
    snippet: str


class RetrieveResponse(BaseModel):
    query: str
    claim_boundary: str
    hits: list[SearchHitResponse]


class EvalRequest(BaseModel):
    files: list[str] = Field(min_length=1)
    allow_frameworks: list[str] = Field(default_factory=lambda: ["LangGraph"])


class EvalResponse(BaseModel):
    passed: bool
    scanned_files: int
    summary: dict[str, int]
    findings: list[dict[str, Any]]


app = FastAPI(
    title="Agent Framework Proof Service",
    version=SERVICE_VERSION,
    description="Local public-safe API proof for retrieval and artifact safety evals.",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=SERVICE_VERSION)


@app.post("/retrieve", response_model=RetrieveResponse)
def retrieve(request: RetrieveRequest) -> dict:
    return run_query(query=request.query, top_k=request.top_k)


@app.post("/eval", response_model=EvalResponse)
def eval_artifacts(request: EvalRequest) -> EvalResponse:
    result = run_eval(request.files, request.allow_frameworks)
    return EvalResponse(
        passed=result["passed"],
        scanned_files=len(result["scanned_files"]),
        summary=result["summary"],
        findings=result["findings"],
    )
