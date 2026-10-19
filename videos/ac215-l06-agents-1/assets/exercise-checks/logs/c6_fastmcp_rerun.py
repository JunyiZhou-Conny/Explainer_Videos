# c6_fastmcp_rerun.py: the Cheese Quiz's own MCP server (cells 11, 48, 57) in one Python process, as in one Colab
# runtime, with today's unpinned packages (cell 10). No model: a FastMCP client lists and calls the tool directly.
# Then the tool is edited and cell 57 is run again in the same runtime.
import asyncio, sys, time, types, importlib.util, json
for name in ("IPython", "IPython.display"):                    # Colab has these; the check venv does not
    sys.modules[name] = types.ModuleType(name)
sys.modules["IPython.display"].HTML = sys.modules["IPython.display"].Markdown = str
from notebook import run_cells
import fastmcp, agents
print("fastmcp", fastmcp.__version__, "| openai-agents", importlib.metadata.version("openai-agents"))
nb = run_cells("cheese-quiz", ["11", "48", "57"])
time.sleep(3)
async def ask():
    async with fastmcp.Client("http://127.0.0.1:8001/mcp") as c:
        tools = await c.list_tools()
        r = await c.call_tool("pavlos_fun_fact_mcp", {})
        return [t.name for t in tools], r.data if hasattr(r, "data") and r.data else r.content[0].text
print("client: tools and one call ->", asyncio.run(ask()))

print("\n== edit the tool (it should now return a fixed text) and run cell 57 again in the same runtime")
src = open("/cells/cheese-quiz/cell-57.py").read()
src = src.replace('    return pavlos_fun_fact()', '    return {"fact": "EDITED TOOL", "generated_at": 0}')
assert "EDITED TOOL" in src
exec(compile(src, "cell-57 (edited, second run)", "exec"), nb)
time.sleep(3)
print("Server thread alive (checked again, 3 s later):", nb["thread"].is_alive())
print("client: tools and one call ->", asyncio.run(ask()))
