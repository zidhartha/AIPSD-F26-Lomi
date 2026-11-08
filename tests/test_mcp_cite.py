"""check_citations through the MCP door: same contract, read-only, no identity, in-memory client."""
import asyncio

from mcp import Client

from src import tools
from src.cite_contracts import CheckCitations
from src.cite_tool import check_citations
from src.mcp_cite import mcp

CLEAN = {
    "answer": "File a request in the HR form [1].",
    "citations": [1],
    "n_sources": 2,
}


def run(coro):
    return asyncio.run(coro)


async def listed():
    async with Client(mcp) as client:
        return {tool.name: tool for tool in (await client.list_tools()).tools}


async def call(args):
    async with Client(mcp) as client:
        return await client.call_tool("check_citations", args)


def untitled(value):
    if isinstance(value, dict):
        return {key: untitled(item) for key, item in value.items() if key != "title" or not isinstance(item, str)}
    if isinstance(value, list):
        return [untitled(item) for item in value]
    return value


def test_the_mcp_server_serves_check_citations():
    assert "check_citations" in run(listed())


def test_both_doors_describe_the_arguments_identically():
    mcp_schema = run(listed())["check_citations"].input_schema
    fc_schema = tools.TOOLS["check_citations"].schema()["function"]["parameters"]
    assert untitled(mcp_schema["properties"]) == untitled(fc_schema["properties"])
    assert set(mcp_schema["required"]) == set(fc_schema["required"])


def test_the_tool_is_marked_read_only():
    annotations = run(listed())["check_citations"].annotations
    assert annotations.read_only_hint is True
    assert annotations.destructive_hint is False


def test_both_doors_return_the_same_verdict():
    via_mcp = run(call(CLEAN))
    direct = check_citations(CheckCitations.model_validate(CLEAN)).model_dump(mode="json")
    assert not via_mcp.is_error
    assert via_mcp.structured_content == direct


def test_bad_arguments_are_rejected_by_the_mcp_door():
    assert run(call({**CLEAN, "n_sources": 0})).is_error


def test_the_model_cannot_name_the_caller():
    properties = run(listed())["check_citations"].input_schema["properties"]
    assert not {"user_id", "student", "account"} & set(properties)
