# --- Define your MCP server with one tool: pavlos_fun_fact
mcp = FastMCP("Pavlos Cheese MCP Local")

# ✅ Define a Tool as MCP Server
@mcp.tool
def pavlos_fun_fact_mcp() -> dict:
    """Return one random fun fact from Pavlos about cheese. Call multiple times if you want several facts."""
    print("Pavlos Fun Fact Tool Called")
    return pavlos_fun_fact()

# 🏃‍♀️ Run the server over HTTP on port 8000 in a background thread
def run_server():
    # HTTP transport serves the MCP endpoint at /mcp
    mcp.run(transport="http", host="127.0.0.1", port=8001)

thread = threading.Thread(target=run_server, daemon=True)
thread.start()
print("FastMCP server starting on http://127.0.0.1:8001/mcp")

print("Server thread alive:", thread.is_alive())
