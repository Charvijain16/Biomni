# ping_rcsb_client.py
import asyncio, os, sys
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

SERVER = [
    r"C:\Users\vlad8\miniconda3\envs\mcp310\python.exe",
    "-m", "biomni.tool.mcp_tools.rcsb_mcp"
]
TOOL = "rcsb_text_search"
ARGS = {"search_string": "insulin", "max_results": 3}

async def main():
    env = os.environ.copy()

    # Force server stderr to pipe so we can read it
    params = StdioServerParameters(
        command=SERVER[0],
        args=SERVER[1:],
        env=env,
        stderr=sys.stderr  # forward server stderr to our own stderr
    )

    try:
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as s:
                await s.initialize()
                tools = (await s.list_tools()).tools
                print("Tools:", [t.name for t in tools])
                res = await s.call_tool(TOOL, ARGS)
                print("Result:", res.content[0].text)

    except Exception as e:
        print(f"❌ Client failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
