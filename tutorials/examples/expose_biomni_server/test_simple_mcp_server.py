#!/usr/bin/env python3
import asyncio
import json
import os
import sys

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

# ---------- CONFIGURE THESE ----------
# Use the Python from the env where rcsb-api is installed
PY_EXE = r"C:\Users\vlad8\miniconda3\envs\mcp310\python.exe"

# Start your MCP server module
SERVER_CMD = [PY_EXE, "-m", "biomni.tool.mcp_tools.rcsb_mcp"]

TOOL_TO_TEST = "rcsb_text_search"
TEST_ARGS = {"search_string": "insulin", "max_results": 3}
# -------------------------------------


async def test_single_tool():
    env = os.environ.copy()
    params = StdioServerParameters(command=SERVER_CMD[0], args=SERVER_CMD[1:], env=env)

    try:
        print("🔌 Connecting to MCP server...")
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await session.initialize()
                print("✅ Connected to MCP server")

                # List tools
                resp = await session.list_tools()
                tools = resp.tools
                print(f"✅ Found {len(tools)} tools: {[t.name for t in tools]}")

                # Find the tool
                names = [t.name for t in tools]
                if TOOL_TO_TEST not in names:
                    print(f"❌ Tool '{TOOL_TO_TEST}' not found!")
                    return False

                # Show schema (helpful for arg mismatches)
                target = next(t for t in tools if t.name == TOOL_TO_TEST)
                print(f"\n🔍 Testing tool: {target.name}")
                print(f"📝 Description: {target.description or 'No description'}")
                print(f"📋 Input Schema: {target.inputSchema}")

                print(f"\n🧪 Testing with arguments: {TEST_ARGS}")
                result = await session.call_tool(TOOL_TO_TEST, TEST_ARGS)
                print("✅ Tool call successful!")

                text = result.content[0].text
                try:
                    print(json.dumps(json.loads(text), indent=2))
                except Exception:
                    print(text[:1000])
                return True

    except Exception as e:
        print(f"❌ Failed to connect/call: {e}")
        return False


if __name__ == "__main__":
    print(f"🧪 Testing single tool: {TOOL_TO_TEST}")
    print(f"📋 Test arguments: {TEST_ARGS}")
    print("-" * 50)

    ok = asyncio.run(test_single_tool())
    print("\n✅ Test completed successfully!" if ok else "\n❌ Test failed!")
    sys.exit(0 if ok else 1)
