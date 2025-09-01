import os
from pathlib import Path

# Extra guards (harmless if ignored by your Biomni version)
os.environ["BIOMNI_USE_TOOL_RETRIEVER"] = "0"

from biomni.agent.a1 import A1

# Some repo versions don't auto-create the registry unless full bootstrap runs
try:
    from biomni.tool.tool_registry import ToolRegistry  # your tree uses this
except ImportError:
    from biomni.tool.registry import ToolRegistry       # fallback in other commits

# Resolve config path robustly from this file’s location
HERE = Path(__file__).resolve().parent
CONFIG = (HERE.parent / "add_mcp_server" / "mcp_config.yaml").resolve()

# Create a lean agent (no tool retriever => no data lake downloads)
agent = A1(use_tool_retriever=False)

if not hasattr(agent, "tool_registry") or agent.tool_registry is None:
    agent.tool_registry = ToolRegistry()

# Attach ONLY the RCSB MCP server
agent.add_mcp(config_path=str(CONFIG))

# Ask the agent to use the tool
agent.go("Use the RCSB tool to find 3 insulin-related PDB entries and show their IDs.")
