from __future__ import annotations

from rag_proof_retriever import answer, retrieve, tokenize


def test_tokenize_lowercases_and_strips_punctuation() -> None:
    assert tokenize("LangGraph, RAG, and CI!") == ["langgraph", "rag", "and", "ci"]


def test_retrieve_langgraph_ci_finds_agent_framework_repo() -> None:
    hits = retrieve("LangGraph safety eval CI", top_k=2)

    assert hits
    assert hits[0].document_id == "agent-framework-proof"
    assert hits[0].score > 0


def test_retrieve_aml_regtech_finds_aml_engine() -> None:
    hits = retrieve("AML RegTech transaction risk", top_k=2)

    assert hits
    assert hits[0].document_id == "aml-detection-engine"


def test_answer_includes_claim_boundary_and_citations() -> None:
    result = answer("portfolio proof for AI finance projects", top_k=3)

    assert "not a production RAG claim" in result["claim_boundary"]
    assert result["hits"]
    assert all(hit["url"].startswith("https://github.com/hash02/") for hit in result["hits"])
