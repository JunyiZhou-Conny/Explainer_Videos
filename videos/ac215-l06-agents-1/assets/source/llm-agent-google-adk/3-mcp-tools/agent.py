"""
MCP Tools Agent

Demonstrates MCP filesystem tools with Google ADK.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

DEFAULT_ALLOWED_PATH = os.path.dirname(os.path.abspath(__file__))
ALLOWED_PATH = os.getenv("MCP_ALLOWED_PATH", DEFAULT_ALLOWED_PATH)

toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='npx',
            args=['-y', '@modelcontextprotocol/server-filesystem', ALLOWED_PATH]
        ),
        timeout=10
    ),
    tool_filter=['read_file', 'list_directory', 'search_files']
)

root_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='filesystem_assistant',
    instruction=f"You can explore and read files in {ALLOWED_PATH}. Use list_directory, read_file, and search_files tools.",
    tools=[toolset]
)
