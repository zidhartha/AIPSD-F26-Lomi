"""route_notice through the MCP door: same contract, read-only, no identity, in-memory client."""
import asyncio

from mcp import Client

from src import tools
from src.mcp_notice import mcp
from src.notice_contracts import RouteNotice
from src.notice_tool import route_notice

CLEAN = {
    "title": {"value": "Time off", "evidence": "Time off", "confidence": 0.95},
    "action": {"value": "File a request in the HR form", "evidence": "File a request in the HR form", "confidence": 0.95},
    "timing": {"value": "at least 5 working days ahead", "evidence": "at least 5 working days ahead", "confidence": 0.95},
    "contact": {"value": "your manager", "evidence": "your manager", "confidence": 0.95},
}


def run(coro):
    return asyncio.run(coro)


async def listed():
    async with Client(mcp) as client:
        return {tool.name: tool for tool in (await client.list_tools()).tools}


async def call(args):
    async with Client(mcp) as client:
        return await client.call_tool("route_notice", args)


def untitled(value):
    if isinstance(value, dict):
        return {key: untitled(item) for key, item in value.items() if key != "title" or not isinstance(item, str)}
    if isinstance(value, list):
        return [untitled(item) for item in value]
    return value


def test_the_mcp_server_serves_route_notice():
    assert "route_notice" in run(listed())


def test_both_doors_describe_the_arguments_identically():
    mcp_schema = run(listed())["route_notice"].input_schema
    fc_schema = tools.TOOLS["route_notice"].schema()["function"]["parameters"]
    assert untitled(mcp_schema["properties"]) == untitled(fc_schema["properties"])
    assert untitled(mcp_schema["$defs"]["ReadField"]) == untitled(fc_schema["$defs"]["ReadField"])
    assert set(mcp_schema["required"]) == set(fc_schema["required"])


def test_the_tool_is_marked_read_only():
    annotations = run(listed())["route_notice"].annotations
    assert annotations.read_only_hint is True
    assert annotations.destructive_hint is False


def test_both_doors_return_the_same_route():
    via_mcp = run(call(CLEAN))
    direct = route_notice(RouteNotice.model_validate(CLEAN)).model_dump(mode="json")
    assert not via_mcp.is_error
    assert via_mcp.structured_content == direct


def test_bad_arguments_are_rejected_by_the_mcp_door():
    bad = {**CLEAN, "title": {"value": "Time off", "evidence": "Time off", "confidence": 1.7}}
    assert run(call(bad)).is_error


def test_the_model_cannot_name_the_caller():
    properties = run(listed())["route_notice"].input_schema["properties"]
    assert not {"user_id", "student", "account"} & set(properties)
