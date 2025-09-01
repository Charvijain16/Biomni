import sys
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

from rcsbapi.search import TextQuery, AttributeQuery
from rcsbapi.data import DataQuery as Query

mcp = FastMCP("rcsb-mcp")

class EntryId(BaseModel):
    """A single RCSB PDB entry identifier."""
    id: str = Field(..., description="PDB ID (e.g., '6M0J')")

class EntryList(BaseModel):
    results: list[EntryId]

@mcp.tool()
def rcsb_text_search(search_string: str, max_results: int = 10) -> EntryList:
    tq = TextQuery(value=search_string)
    hits = list(tq())
    return EntryList(results=[EntryId(id=str(h)) for h in hits[:max_results]])


if __name__ == "__main__":
    print("RCSB MCP server starting...", file=sys.stderr, flush=True)
    mcp.run(transport="stdio")