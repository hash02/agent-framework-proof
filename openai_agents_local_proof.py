"""Local OpenAI Agents SDK-shaped proof for governed tool workflows.

This module mirrors the small abstractions recruiters expect to see around an
agent SDK: Agent, Tool, and a runner. It intentionally avoids network calls and
credential requirements. If a real SDK is added later, this file can become the
adapter boundary while the tests keep the public-safe behavior stable.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


BOUNDARY = (
    "OpenAI Agents SDK-shaped local proof only; safe mocked tools, no live API "
    "call, no credential requirement, and not production agent deployment."
)

BLOCKED_TERMS = {
    "external_action_token",
    "profile_change_token",
    "live_site_change_token",
}


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    handler: Callable[[str], dict]


@dataclass(frozen=True)
class Agent:
    name: str
    instructions: str
    tools: list[Tool]


def lookup_proof_artifact(query: str) -> dict:
    return {
        "artifact": "agent-framework-proof/README.md",
        "match_summary": "Local agent framework proof includes tool calling, queue states, RBAC, retrieval, trace events, and tests.",
        "evidence_refs": [
            "agent-framework-proof/README.md",
            "agent-framework-proof/runs/queue-sim-output-2026-05-18.json",
        ],
        "query": query,
    }


def run_safety_check(text: str) -> dict:
    lowered = text.lower()
    blocked = any(term in lowered for term in BLOCKED_TERMS)
    if blocked:
        return {
            "status": "blocked",
            "reason": "Requested external action remains blocked for human review.",
        }
    return {"status": "pass", "reason": "Local artifact workflow only."}


def build_demo_agent() -> Agent:
    return Agent(
        name="career-proof-local-agent",
        instructions=(
            "Use local mocked tools to prepare recruiter-safe proof summaries. "
            "Block external actions and keep output public-safe."
        ),
        tools=[
            Tool(
                name="lookup_proof_artifact",
                description="Return canned public-safe proof references for local portfolio artifacts.",
                handler=lookup_proof_artifact,
            ),
            Tool(
                name="run_safety_check",
                description="Check whether an input requests an external or irreversible action.",
                handler=run_safety_check,
            ),
        ],
    )


def _tool_by_name(agent: Agent, name: str) -> Tool:
    for tool in agent.tools:
        if tool.name == name:
            return tool
    raise ValueError(f"Tool not registered: {name}")


def run_agent(agent: Agent, input_text: str) -> dict:
    safety_tool = _tool_by_name(agent, "run_safety_check")
    safety_result = safety_tool.handler(input_text)
    tools_called = [safety_tool.name]

    if safety_result["status"] == "blocked":
        return {
            "agent_name": agent.name,
            "input": input_text,
            "tools_called": tools_called,
            "output_summary": "Blocked because the request asked for an external action.",
            "safety_status": "blocked",
            "evidence_refs": ["agent-framework-proof/agent_safety_eval.py"],
            "boundary": BOUNDARY,
        }

    lookup_tool = _tool_by_name(agent, "lookup_proof_artifact")
    lookup_result = lookup_tool.handler(input_text)
    tools_called.append(lookup_tool.name)
    return {
        "agent_name": agent.name,
        "input": input_text,
        "tools_called": tools_called,
        "output_summary": lookup_result["match_summary"],
        "safety_status": "pass",
        "evidence_refs": lookup_result["evidence_refs"],
        "boundary": BOUNDARY,
    }


def serialize_result(result: dict) -> str:
    return json.dumps(result, indent=2, sort_keys=True)


def public_agent_metadata(agent: Agent) -> dict:
    return {
        "name": agent.name,
        "instructions": agent.instructions,
        "tools": [
            {"name": tool.name, "description": tool.description}
            for tool in agent.tools
        ],
    }


def save_result(result: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(serialize_result(result), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local OpenAI Agents SDK-shaped proof.")
    parser.add_argument(
        "input",
        nargs="?",
        default="Prepare local proof summary for recruiter packet.",
        help="Public-safe local prompt for the demo runner.",
    )
    parser.add_argument(
        "--output",
        default="runs/openai-agents-local-proof-output-2026-05-18.json",
        help="Where to save the structured run result.",
    )
    args = parser.parse_args()
    agent = build_demo_agent()
    result = run_agent(agent, args.input)
    output_path = Path(args.output)
    save_result(result, output_path)
    print(
        serialize_result(
            {"agent": public_agent_metadata(agent), "result": result, "output": str(output_path)}
        )
    )


if __name__ == "__main__":
    main()
