import json

from vector_retriever import retrieve


def test_deterministic_mode_returns_results_with_citations():
    result = retrieve("AI finance agent framework", mode="deterministic")

    assert result["mode"] == "deterministic"
    assert result["query"] == "AI finance agent framework"
    assert isinstance(result["chroma_available"], bool)
    assert result["results"]
    assert all("chunk" in item for item in result["results"])
    assert all("score" in item for item in result["results"])
    assert all("citation" in item for item in result["results"])


def test_chroma_mode_returns_or_falls_back_cleanly():
    result = retrieve("governed agent workflow proof", mode="chroma")

    assert result["mode"] in {"chroma", "deterministic_fallback"}
    assert isinstance(result["chroma_available"], bool)
    assert result["results"]
    assert all(item["citation"].startswith("https://github.com/hash02/") for item in result["results"])


def test_unknown_mode_uses_deterministic_fallback():
    result = retrieve("AML risk retrieval", mode="unknown")

    assert result["mode"] == "deterministic_fallback"
    assert result["results"]


def test_serialized_result_has_no_private_markers():
    payload = json.dumps(retrieve("portfolio retrieval proof", mode="chroma"), sort_keys=True)
    forbidden_markers = [
        "C:",
        "Users",
        "100.",
        "private " + "key",
        "wallet " + "secret",
        "client data",
    ]

    assert not any(marker in payload for marker in forbidden_markers)
