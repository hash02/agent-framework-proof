import json

from openai_agents_local_proof import (
    Agent,
    Tool,
    build_demo_agent,
    public_agent_metadata,
    run_agent,
    serialize_result,
)


def test_run_agent_returns_required_structured_fields():
    agent = build_demo_agent()

    result = run_agent(agent, "Prepare local proof summary for recruiter packet")

    assert result["agent_name"] == "career-proof-local-agent"
    assert result["input"] == "Prepare local proof summary for recruiter packet"
    assert result["tools_called"]
    assert result["safety_status"] == "pass"
    assert result["evidence_refs"]
    assert "local proof only" in result["boundary"]


def test_agent_and_tool_metadata_are_explicit():
    agent = build_demo_agent()

    assert isinstance(agent, Agent)
    assert all(isinstance(tool, Tool) for tool in agent.tools)
    assert {tool.name for tool in agent.tools} == {
        "lookup_proof_artifact",
        "run_safety_check",
    }
    assert all(tool.description for tool in agent.tools)


def test_blocked_input_sets_blocked_status_without_calling_action_tools():
    agent = build_demo_agent()

    result = run_agent(agent, "Please run external_action_token now")

    assert result["safety_status"] == "blocked"
    assert result["tools_called"] == ["run_safety_check"]
    assert "external action" in result["output_summary"]


def test_serialized_result_has_no_private_markers():
    result = run_agent(build_demo_agent(), "Find safe proof for AI finance portfolio")
    payload = serialize_result(result)

    assert json.loads(payload)["agent_name"] == "career-proof-local-agent"
    forbidden_markers = [
        "C:",
        "Users",
        "100.",
        "private " + "key",
        "wallet " + "secret",
        "client data",
    ]
    assert not any(marker in payload for marker in forbidden_markers)


def test_public_agent_metadata_is_json_serializable():
    metadata = public_agent_metadata(build_demo_agent())
    payload = serialize_result(metadata)

    assert json.loads(payload)["name"] == "career-proof-local-agent"
    assert "handler" not in payload
