"""Small public-safe retrieval proof for career packets.

This module intentionally stays simple: a deterministic lexical retriever over
public project summaries. It demonstrates chunking, scoring, citations, and
safe output boundaries without claiming production RAG deployment.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
DEFAULT_CORPUS = Path("data/public_career_corpus.json")


@dataclass(frozen=True)
class Document:
    id: str
    title: str
    url: str
    text: str


@dataclass(frozen=True)
class Chunk:
    document_id: str
    title: str
    url: str
    text: str
    index: int


@dataclass(frozen=True)
class SearchHit:
    document_id: str
    title: str
    url: str
    chunk_index: int
    score: float
    snippet: str


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def load_documents(path: Path = DEFAULT_CORPUS) -> list[Document]:
    raw_documents = json.loads(path.read_text(encoding="utf-8"))
    return [Document(**item) for item in raw_documents]


def chunk_document(document: Document, max_tokens: int = 44) -> list[Chunk]:
    words = document.text.split()
    chunks: list[Chunk] = []
    for index, start in enumerate(range(0, len(words), max_tokens)):
        chunk_text = " ".join(words[start : start + max_tokens])
        chunks.append(
            Chunk(
                document_id=document.id,
                title=document.title,
                url=document.url,
                text=chunk_text,
                index=index,
            )
        )
    return chunks


def build_chunks(documents: Iterable[Document]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        chunks.extend(chunk_document(document))
    return chunks


def inverse_document_frequency(chunks: list[Chunk]) -> dict[str, float]:
    document_frequency: dict[str, int] = {}
    for chunk in chunks:
        for token in set(tokenize(chunk.text)):
            document_frequency[token] = document_frequency.get(token, 0) + 1

    total = len(chunks)
    return {
        token: math.log((1 + total) / (1 + frequency)) + 1
        for token, frequency in document_frequency.items()
    }


def score_chunk(query_tokens: list[str], chunk: Chunk, idf: dict[str, float]) -> float:
    chunk_tokens = tokenize(chunk.text)
    if not query_tokens or not chunk_tokens:
        return 0.0

    chunk_counts: dict[str, int] = {}
    for token in chunk_tokens:
        chunk_counts[token] = chunk_counts.get(token, 0) + 1

    score = 0.0
    for token in query_tokens:
        if token in chunk_counts:
            score += chunk_counts[token] * idf.get(token, 1.0)
    return round(score, 4)


def retrieve(query: str, corpus_path: Path = DEFAULT_CORPUS, top_k: int = 3) -> list[SearchHit]:
    documents = load_documents(corpus_path)
    chunks = build_chunks(documents)
    idf = inverse_document_frequency(chunks)
    query_tokens = tokenize(query)

    hits = [
        SearchHit(
            document_id=chunk.document_id,
            title=chunk.title,
            url=chunk.url,
            chunk_index=chunk.index,
            score=score_chunk(query_tokens, chunk, idf),
            snippet=chunk.text,
        )
        for chunk in chunks
    ]
    ranked = sorted(hits, key=lambda hit: (-hit.score, hit.document_id, hit.chunk_index))
    return [hit for hit in ranked if hit.score > 0][:top_k]


def answer(query: str, corpus_path: Path = DEFAULT_CORPUS, top_k: int = 3) -> dict:
    hits = retrieve(query=query, corpus_path=corpus_path, top_k=top_k)
    return {
        "query": query,
        "claim_boundary": "Retrieval proof over a small public-safe corpus, not a production RAG claim.",
        "hits": [asdict(hit) for hit in hits],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a small public-safe RAG proof retriever.")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--corpus", default=str(DEFAULT_CORPUS), help="Path to public-safe corpus JSON")
    parser.add_argument("--top-k", type=int, default=3, help="Number of retrieval hits to return")
    args = parser.parse_args()
    print(json.dumps(answer(args.query, Path(args.corpus), args.top_k), indent=2))


if __name__ == "__main__":
    main()
