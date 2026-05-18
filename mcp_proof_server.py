"""Local MCP-style proof server for recruiter-safe agent tools.

This is a protocol-shape proof only. It mirrors MCP's core idea of tool
discovery plus structured tool calls without opening a socket, making network
calls, or requiring credentials.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from mcp_tools.proof_lookup import proof_lookup
from mcp_tools.safety_summary import safety_summary


BOUNDARY = (
    "Local MCP-style tool server proof only; no live MCP connection, network "
    "call, credential requirement, or production deployment."
)


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: dict
    handler: Callable[[dict], dict]


def _proof_lookup_handler(params: dict) -> dict:
    return proof_lookup(str(params.get("query", "")))


def _safety_summary_handler(params: dict) -> dict:
    return safety_summary(str(params.get("text", "")))


TOOL_REGISTRY = {
    "proof_lookup": ToolDefinition(
        name="proof_lookup",
        description="Return public-safe project proof references for a query.",
        input_schema={
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
        handler=_proof_lookup_handler,
    ),
    "safety_summary": ToolDefinition(
        name="safety_summary",
        description="Summarize whether text stays inside local-proof boundaries.",
        input_schema={
            "type": "object",
            "properties": {"text": {"type": "string"}},
            "required": ["text"],
        },
        handler=_safety_summary_handler,
    ),
}


def list_tools() -> list[dict]:
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.input_schema,
        }
        for tool in TOOL_REGISTRY.values()
    ]


def call_tool(tool_name: str, params: dict) -> dict:
    tool = TOOL_REGISTRY.get(tool_name)
    if tool is None:
        return {
            "tool": tool_name,
            "params": params,
            "result": {},
            "boundary": BOUNDARY,
            "error": f"Tool not registered: {tool_name}",
        }
    try:
        result = tool.handler(params)
        error = None
    except Exception as exc:  # pragma: no cover - defensive protocol boundary
        result = {}
        error = f"Tool failed: {type(exc).__name__}"
    return {
        "tool": tool_name,
        "params": params,
        "result": result,
        "boundary": BOUNDARY,
        "error": error,
    }


def sample_run() -> dict:
    return {
        "boundary": BOUNDARY,
        "tools": list_tools(),
        "calls": [
            call_tool("proof_lookup", {"query": "agent framework proof"}),
            call_tool("safety_summary", {"text": "local proof artifact only"}),
            call_tool("missing_tool", {"query": "demo error response"}),
        ],
    }


def save_sample(output_path: Path) -> dict:
    payload = sample_run()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local MCP-style proof server sample.")
    parser.add_argument(
        "--output",
        default="runs/mcp-proof-server-output-2026-05-18.json",
        help="Where to save the MCP-style sample output.",
    )
    args = parser.parse_args()
    output_path = Path(args.output)
    payload = save_sample(output_path)
    print(json.dumps({"output": str(output_path), **payload}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
