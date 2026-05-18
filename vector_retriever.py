"""Optional vector retrieval proof with deterministic fallback.

The Chroma path is intentionally optional so CI and local runs stay reliable.
If Chroma is unavailable or fails at runtime, retrieval falls back to the
existing deterministic public-safe retriever.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rag_proof_retriever import DEFAULT_CORPUS, build_chunks, load_documents, retrieve as deterministic_retrieve, tokenize


try:  # pragma: no cover - availability depends on local environment
    import chromadb  # type: ignore

    _CHROMA_AVAILABLE = True
except ImportError:  # pragma: no cover - exercised through fallback tests
    chromadb = None
    _CHROMA_AVAILABLE = False


BOUNDARY = (
    "Optional Chroma vector retrieval proof with deterministic fallback; local "
    "public-safe corpus only, not production RAG or hosted vector search."
)


def _format_deterministic_results(query: str, top_k: int, mode: str) -> dict:
    hits = deterministic_retrieve(query, top_k=top_k)
    return {
        "mode": mode,
        "query": query,
        "results": [
            {
                "chunk": hit.snippet,
                "score": hit.score,
                "citation": hit.url,
            }
            for hit in hits
        ],
        "chroma_available": _CHROMA_AVAILABLE,
        "boundary": BOUNDARY,
    }


def _vocabulary(chunks: list) -> list[str]:
    tokens: set[str] = set()
    for chunk in chunks:
        tokens.update(tokenize(chunk.text))
    return sorted(tokens)


def _embedding(text: str, vocabulary: list[str]) -> list[float]:
    tokens = tokenize(text)
    counts = {token: tokens.count(token) for token in set(tokens)}
    return [float(counts.get(token, 0)) for token in vocabulary]


def _retrieve_with_chroma(query: str, top_k: int, corpus_path: Path) -> dict:
    if chromadb is None:
        raise RuntimeError("Chroma unavailable")

    documents = load_documents(corpus_path)
    chunks = build_chunks(documents)
    vocabulary = _vocabulary(chunks)
    client = chromadb.Client()
    collection = client.create_collection("career_proof_vector_retriever")
    collection.add(
        ids=[f"{chunk.document_id}-{chunk.index}" for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        embeddings=[_embedding(chunk.text, vocabulary) for chunk in chunks],
        metadatas=[
            {
                "citation": chunk.url,
                "title": chunk.title,
                "document_id": chunk.document_id,
            }
            for chunk in chunks
        ],
    )
    response = collection.query(
        query_embeddings=[_embedding(query, vocabulary)],
        n_results=top_k,
        include=["documents", "distances", "metadatas"],
    )
    documents_result = response.get("documents", [[]])[0]
    distances = response.get("distances", [[]])[0]
    metadatas = response.get("metadatas", [[]])[0]
    results = []
    for chunk_text, distance, metadata in zip(documents_result, distances, metadatas):
        results.append(
            {
                "chunk": chunk_text,
                "score": round(1 / (1 + float(distance)), 4),
                "citation": metadata["citation"],
            }
        )
    return {
        "mode": "chroma",
        "query": query,
        "results": results,
        "chroma_available": _CHROMA_AVAILABLE,
        "boundary": BOUNDARY,
    }


def retrieve(query: str, mode: str = "deterministic", top_k: int = 3, corpus_path: Path = DEFAULT_CORPUS) -> dict:
    if mode == "deterministic":
        return _format_deterministic_results(query, top_k, "deterministic")
    if mode == "chroma" and _CHROMA_AVAILABLE:
        try:
            return _retrieve_with_chroma(query, top_k, corpus_path)
        except Exception:
            return _format_deterministic_results(query, top_k, "deterministic_fallback")
    return _format_deterministic_results(query, top_k, "deterministic_fallback")


def save_result(result: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run optional vector retriever proof.")
    parser.add_argument("query", nargs="?", default="agent framework proof with citations")
    parser.add_argument("--mode", default="chroma", choices=["deterministic", "chroma"])
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument(
        "--output",
        default="runs/vector-retriever-output-2026-05-18.json",
        help="Where to save the vector retriever result.",
    )
    args = parser.parse_args()
    result = retrieve(args.query, mode=args.mode, top_k=args.top_k)
    save_result(result, Path(args.output))
    print(json.dumps({"output": args.output, **result}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
