from langchain_core.tools import BaseTool

from langchain_tool_caller import (
    build_tools,
    route_request,
    run_tool_call,
    run_tool_workflow,
)


def test_build_tools_returns_named_langchain_tools():
    tools = build_tools()
    names = {tool.name for tool in tools}

    assert all(isinstance(tool, BaseTool) for tool in tools)
    assert names == {"retrieve_project_proof", "evaluate_artifact_safety"}


def test_route_request_selects_retrieval_tool():
    decision = route_request("Find proof for LangGraph RAG Docker")

    assert decision.tool_name == "retrieve_project_proof"
    assert decision.arguments["query"] == "Find proof for LangGraph RAG Docker"
    assert decision.reason == "query_requested_project_evidence"


def test_route_request_selects_eval_tool():
    decision = route_request("Evaluate README.md before sharing it")

    assert decision.tool_name == "evaluate_artifact_safety"
    assert decision.arguments["paths"] == ["README.md"]
    assert decision.reason == "query_requested_safety_eval"


def test_run_tool_call_returns_retrieval_result():
    tools = {tool.name: tool for tool in build_tools()}
    decision = route_request("Find proof for FastAPI Docker CI")

    result = run_tool_call(tools, decision)

    assert result["tool_name"] == "retrieve_project_proof"
    assert result["result"]["claim_boundary"]
    assert result["result"]["hits"]


def test_run_tool_workflow_includes_boundary_and_tool_result():
    result = run_tool_workflow("Find proof for RAG retrieval")

    assert result["boundary"] == (
        "LangChain tool-calling proof over local deterministic tools; "
        "no paid model call and no external action."
    )
    assert result["decision"]["tool_name"] == "retrieve_project_proof"
    assert result["tool_result"]["result"]["hits"]
