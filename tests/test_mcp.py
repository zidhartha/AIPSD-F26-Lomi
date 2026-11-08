"""The MCP door: same contract, read-only annotation, no identity field, in-memory client."""
import asyncio

from mcp import Client

from src import tools
from src.mcp_server import mcp


def run(coro):
    return asyncio.run(coro)


async def listed():
    async with Client(mcp) as client:
        return {tool.name: tool for tool in (await client.list_tools()).tools}


async def call(name, args):
    async with Client(mcp) as client:
        return await client.call_tool(name, args)


def strip(schema):
    return {key: {item: value for item, value in spec.items() if item != "title"}
            for key, spec in schema["properties"].items()}


def test_same_tools_through_both_doors():
    assert set(run(listed())) == set(tools.TOOLS)


def test_both_doors_describe_the_arguments_identically():
    mcp_schema = run(listed())["lookup_handbook"].input_schema
    fc_schema = tools.TOOLS["lookup_handbook"].schema()["function"]["parameters"]
    assert strip(mcp_schema) == strip(fc_schema)
    assert set(mcp_schema.get("required", [])) == set(fc_schema.get("required", []))


def test_the_tool_is_marked_read_only():
    listed_tools = run(listed())
    assert listed_tools["lookup_handbook"].annotations.read_only_hint is True
    assert listed_tools["lookup_handbook"].annotations.destructive_hint is False


def test_bad_arguments_are_rejected_by_the_sdk():
    result = run(call("lookup_handbook", {"question": "../../.env"}))
    assert result.is_error


def test_a_missing_rule_reaches_the_model_as_text():
    result = run(call("lookup_handbook", {"question": "What is the guest cafeteria menu on Friday?"}))
    assert result.is_error
    assert "not in the company documents" in result.content[0].text


def test_the_model_cannot_name_the_caller():
    schema = run(listed())["lookup_handbook"].input_schema
    assert "user_id" not in schema["properties"]
    assert "student" not in schema["properties"]
    assert "account" not in schema["properties"]
