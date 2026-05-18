"""LangChain tool-calling proof over local public-safe functions.

This module intentionally avoids paid model calls. It demonstrates the shape of
tool registration, deterministic routing, invocation, and auditable output while
calling the repo's existing local proof functions.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from typing import Any

from langchain_core.tools import BaseTool, tool

from agent_safety_eval import run_eval
from rag_proof_retriever import run_query


BOUNDARY = (
    "LangChain tool-calling proof over local deterministic tools; "
    "no paid model call and no external action."
)


@dataclass(frozen=True)
class ToolDecision:
    tool_name: str
    arguments: dict[str, Any]
    reason: str


@tool
def retrieve_project_proof(query: str, top_k: int = 3) -> dict:
    """Retrieve public-safe project proof snippets with citations."""
    return run_query(query=query, top_k=top_k)


@tool
def evaluate_artifact_safety(paths: list[str], allow_frameworks: list[str] | None = None) -> dict:
    """Evaluate local artifacts for private data, unsafe actions, and framework overclaims."""
    frameworks = allow_frameworks or ["LangGraph", "LangChain"]
    return run_eval(paths, frameworks)


def build_tools() -> list[BaseTool]:
    return [retrieve_project_proof, evaluate_artifact_safety]


def route_request(request: str) -> ToolDecision:
    normalized = request.lower()
    eval_intent = re.search(r"\b(eval|evaluate|scan|safety|safe)\b", normalized)
    if eval_intent:
        paths = extract_paths(request)
        return ToolDecision(
            tool_name="evaluate_artifact_safety",
            arguments={"paths": paths or ["README.md"], "allow_frameworks": ["LangGraph", "LangChain"]},
            reason="query_requested_safety_eval",
        )
    return ToolDecision(
        tool_name="retrieve_project_proof",
        arguments={"query": request, "top_k": 3},
        reason="query_requested_project_evidence",
    )


def extract_paths(request: str) -> list[str]:
    candidates = re.findall(r"[\w./\\-]+\.(?:md|json|txt|py)", request)
    return candidates


def run_tool_call(tools: dict[str, BaseTool], decision: ToolDecision) -> dict:
    selected_tool = tools[decision.tool_name]
    result = selected_tool.invoke(decision.arguments)
    return {
        "tool_name": decision.tool_name,
        "reason": decision.reason,
        "arguments": decision.arguments,
        "result": result,
    }


def run_tool_workflow(request: str) -> dict:
    tools = {tool_item.name: tool_item for tool_item in build_tools()}
    decision = route_request(request)
    tool_result = run_tool_call(tools, decision)
    return {
        "boundary": BOUNDARY,
        "decision": asdict(decision),
        "tool_result": tool_result,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a local LangChain tool-calling proof.")
    parser.add_argument("request", help="Natural language request for retrieval or artifact safety eval")
    args = parser.parse_args()
    print(json.dumps(run_tool_workflow(args.request), indent=2))


if __name__ == "__main__":
    main()
