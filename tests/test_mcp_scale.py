"""scale_notice through the MCP door: same contract, read-only, no identity, in-memory client."""
import asyncio

from mcp import Client

from src import tools
from src.mcp_scale import mcp
from src.scale_contracts import ScaleNotice
from src.scale_tool import scale_notice

CLEAN = {"width": 2000, "height": 1000, "label": "Time off poster"}


def run(coro):
    return asyncio.run(coro)


async def listed():
    async with Client(mcp) as client:
        return {tool.name: tool for tool in (await client.list_tools()).tools}


async def call(args):
    async with Client(mcp) as client:
        return await client.call_tool("scale_notice", args)


def untitled(value):
    if isinstance(value, dict):
        return {key: untitled(item) for key, item in value.items() if key != "title"}
    if isinstance(value, list):
        return [untitled(item) for item in value]
    return value


def test_the_mcp_server_serves_scale_notice():
    assert "scale_notice" in run(listed())


def test_both_doors_describe_the_arguments_identically():
    mcp_schema = run(listed())["scale_notice"].input_schema
    fc_schema = tools.TOOLS["scale_notice"].schema()["function"]["parameters"]
    assert untitled(mcp_schema["properties"]) == untitled(fc_schema["properties"])
    assert set(mcp_schema["required"]) == set(fc_schema["required"])
    assert fc_schema["additionalProperties"] is False


def test_the_tool_is_marked_read_only():
    annotations = run(listed())["scale_notice"].annotations
    assert annotations.read_only_hint is True
    assert annotations.destructive_hint is False


def test_both_doors_return_the_same_size():
    via_mcp = run(call(CLEAN))
    direct = scale_notice(ScaleNotice.model_validate(CLEAN)).model_dump(mode="json")
    assert not via_mcp.is_error
    assert via_mcp.structured_content == direct


def test_bad_arguments_are_rejected_by_the_mcp_door():
    assert run(call({**CLEAN, "width": 0})).is_error


def test_the_model_cannot_name_the_caller():
    properties = run(listed())["scale_notice"].input_schema["properties"]
    assert not {"user_id", "student", "account"} & set(properties)
