import json

from mcp_proof_server import BOUNDARY, call_tool, list_tools


def test_list_tools_returns_discoverable_tool_metadata():
    tools = list_tools()

    assert len(tools) >= 2
    assert {tool["name"] for tool in tools} == {"proof_lookup", "safety_summary"}
    assert all(tool["description"] for tool in tools)
    assert all("input_schema" in tool for tool in tools)


def test_call_tool_dispatches_to_proof_lookup():
    response = call_tool("proof_lookup", {"query": "agent proof stack"})

    assert response["tool"] == "proof_lookup"
    assert response["params"] == {"query": "agent proof stack"}
    assert response["error"] is None
    assert response["boundary"] == BOUNDARY
    assert response["result"]["artifact"]
    assert response["result"]["evidence_refs"]


def test_call_tool_dispatches_to_safety_summary():
    response = call_tool("safety_summary", {"text": "local proof artifact only"})

    assert response["tool"] == "safety_summary"
    assert response["error"] is None
    assert response["result"]["status"] == "pass"
    assert isinstance(response["result"]["findings"], list)


def test_unregistered_tool_returns_error_response():
    response = call_tool("missing_tool", {"query": "anything"})

    assert response["tool"] == "missing_tool"
    assert response["result"] == {}
    assert response["error"] == "Tool not registered: missing_tool"


def test_serialized_responses_do_not_expose_private_markers():
    responses = [
        {"tools": list_tools()},
        call_tool("proof_lookup", {"query": "portfolio evidence"}),
        call_tool("safety_summary", {"text": "external_action_token"}),
    ]
    payload = json.dumps(responses, sort_keys=True)
    forbidden_markers = [
        "C:",
        "Users",
        "100.",
        "private " + "key",
        "wallet " + "secret",
        "client data",
    ]

    assert not any(marker in payload for marker in forbidden_markers)
