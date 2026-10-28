# b8_mcp.py <agent file>: the module's own MCPToolset, without a model: the tools the agent sees, the server's
# description of read_file / read_text_file, then three calls a model could make (search_files twice, and
# read_file on a path outside the allowed folder).
import asyncio, importlib.util, sys, logging, warnings
warnings.filterwarnings("ignore"); logging.disable(logging.WARNING)
path = sys.argv[1]
spec = importlib.util.spec_from_file_location("agent_under_test", path)
agent = importlib.util.module_from_spec(spec); spec.loader.exec_module(agent)

async def main():
    tools = await agent.toolset.get_tools()
    print("tool_filter:", agent.toolset.tool_filter)
    print("tools the agent sees:", [t.name for t in tools])
    session = await agent.toolset._mcp_session_manager.create_session()
    listed = {t.name: t for t in (await session.list_tools()).tools}
    for name in ("read_file", "read_text_file", "search_files"):
        print(f"server's description of {name}: {listed[name].description[:230]!r}")
    for args in ({"path": agent.ALLOWED_PATH, "pattern": "agent"}, {"path": agent.ALLOWED_PATH, "pattern": "**/*agent*"}):
        r = await session.call_tool("search_files", args)
        print(f"search_files {args['pattern']!r} ->", " | ".join(c.text for c in r.content)[:300])
    r = await session.call_tool("read_file", {"path": agent.ALLOWED_PATH.rsplit("/", 1)[0] + "/.env"})
    print("read_file ../.env -> is_error", r.is_error, ":", " ".join(c.text for c in r.content)[:200])
    await agent.toolset.close()
asyncio.run(main())
