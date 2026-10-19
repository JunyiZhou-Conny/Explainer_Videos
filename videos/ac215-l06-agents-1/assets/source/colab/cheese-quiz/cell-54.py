# MCP Server
pavlos_mcp_url = "https://pavlos-fun-facts.dlops.io/mcp"

async def run_agent(query: str):
  async with AsyncExitStack() as stack:
      # Build a list of MCP servers we want to use
      mcp_servers = []

      # Connect to the Pavlos Cheese MCP server for this session
      mcp_server = await stack.enter_async_context(
          MCPServerStreamableHttp(
              name="Pavlos FastMCP",
              params={"url": pavlos_mcp_url},          # MCP endpoint
              cache_tools_list=True,                   # optional: cache tool discovery
              max_retry_attempts=3,
              client_session_timeout_seconds=180,
          )
      )
      mcp_servers.append(mcp_server)

      # Agent that uses MCP for tool use
      agent = Agent(
          name="Culinary Expert (MCP)",
          instructions=system_prompt,
          model=model,
          # IMPORTANT: add the server in mcp_servers (not tools)
          mcp_servers=mcp_servers,
          model_settings=ModelSettings(temperature=0.2, tool_choice="auto"),
      )
      result = await Runner.run(agent, input=query)
      return result.final_output

# Call it:
out = await run_agent(user_prompt)
from IPython.display import Markdown, display
display(Markdown(out))
