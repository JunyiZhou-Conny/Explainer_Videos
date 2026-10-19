# c1_mcp_env.py: with a module .env inside mcp_tools/ (the module README's `cp .env.example .env`), can the agent's
# filesystem tools read it? The module's own MCPToolset, no model.
import asyncio, importlib.util, logging, warnings
warnings.filterwarnings("ignore"); logging.disable(logging.WARNING)
spec = importlib.util.spec_from_file_location("agent_under_test", "mcp_tools/agent.py")
agent = importlib.util.module_from_spec(spec); spec.loader.exec_module(agent)
async def main():
    session = await agent.toolset._mcp_session_manager.create_session()
    r = await session.call_tool("list_directory", {"path": agent.ALLOWED_PATH})
    print("list_directory ->", " | ".join(r.content[0].text.splitlines()))
    r = await session.call_tool("read_file", {"path": agent.ALLOWED_PATH + "/.env"})
    print("read_file mcp_tools/.env -> is_error", r.is_error)
    print(r.content[0].text)
    await agent.toolset.close()
asyncio.run(main())
