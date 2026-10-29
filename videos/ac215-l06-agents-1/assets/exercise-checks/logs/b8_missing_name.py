# b8_missing_name.py: tool_filter naming a tool the server doesn't have (as 'read_file' would be if a future
# server dropped it): does anything complain? The module's toolset with another filter, no model.
import asyncio, importlib.util, logging, warnings
warnings.filterwarnings("ignore"); logging.disable(logging.WARNING)
spec = importlib.util.spec_from_file_location("agent_under_test", "mcp_tools/agent.py")
agent = importlib.util.module_from_spec(spec); spec.loader.exec_module(agent)
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
ts = MCPToolset(connection_params=agent.toolset._connection_params,
                tool_filter=["read_file_v0", "list_directory", "search_files"])
async def main():
    print("tool_filter:", ts.tool_filter)
    print("tools the agent sees:", [t.name for t in await ts.get_tools()])
    await ts.close()
asyncio.run(main())
