from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from risk_service_api import app


client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}


def test_retrieve_known_query_returns_hit_and_claim_boundary() -> None:
    response = client.post("/retrieve", json={"query": "LangGraph safety eval CI"})

    assert response.status_code == 200
    body = response.json()
    assert "not a production RAG claim" in body["claim_boundary"]
    assert body["hits"]
    assert body["hits"][0]["document_id"] == "agent-framework-proof"


def test_retrieve_empty_query_returns_validation_error() -> None:
    response = client.post("/retrieve", json={"query": ""})

    assert response.status_code == 422


def test_eval_clean_file_passes(tmp_path: Path) -> None:
    clean_file = tmp_path / "clean.md"
    clean_file.write_text("Built a public-safe LangGraph proof module.", encoding="utf-8")

    response = client.post("/eval", json={"files": [str(clean_file)], "allow_frameworks": ["LangGraph"]})

    assert response.status_code == 200
    body = response.json()
    assert body["passed"] is True
    assert body["scanned_files"] == 1
    assert body["summary"]["total"] == 0
