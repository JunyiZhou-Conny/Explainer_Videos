# Tutorial 3: MCP & Tools - Agent Tool Integration

Learn how to equip Google ADK agents with tools - both regular Python functions and MCP-based tools (local and remote).

## Overview

In this tutorial, you'll learn:
- How to create tools from Python functions (FunctionTool)
- Using local MCP servers (stdio)
- Connecting to remote MCP servers (HTTP/SSE)
- Security best practices for tool access
- Tool discovery and filtering

## What You'll Build

1. **Basic Tools** - Python functions as agent tools
2. **Local MCP Tools** - Filesystem access via local MCP server
3. **Remote MCP Tools** - Connecting to MCP servers via URL
4. **Custom MCP Server** - Build and deploy your own MCP server

## Prerequisites

- Completed Tutorial 1-2
- Python 3.10+
- Node.js and npm (for MCP examples)
- uv package manager
- Google AI API key

## Setup

### 1. Install dependencies (from root)

```bash
uv sync
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```bash
GOOGLE_API_KEY=your_api_key_here

# Optional: For remote MCP server examples
# MCP_SERVER_URL=https://your-mcp-server.com/sse
# MCP_SERVER_TOKEN=your_auth_token
```

### 3. Install Node.js (for MCP examples)

```bash
# macOS
brew install node

# Ubuntu
sudo apt install nodejs npm

# Windows
# Download from https://nodejs.org/
```

## File Structure

```
3-mcp-tools/
├── README.md         # This file
├── .env.example     # Environment template
├── pyproject.toml   # Dependencies
└── agent.py         # MCP filesystem agent demo
```

The tutorial focuses on a working MCP filesystem agent. Code examples below demonstrate other patterns you can implement.

## Running the Demo

### Using `adk web` (Recommended)

From the **repository root**:

```bash
uv run adk
```

Then open http://localhost:8000 and try asking:
- "List files in this directory"
- "Read the README.md file"
- "What Python files are here?"
- "Search for files containing 'agent'"

The agent uses MCP filesystem tools to explore the `3-mcp-tools/` directory.

## Part 1: Basic ADK Tools (FunctionTool)

### What are FunctionTools?

The simplest way to give agents capabilities - wrap Python functions!

**Key concepts:**
- Any Python function can become a tool
- Docstrings help agents understand tool purpose
- Type hints enable parameter validation
- Tools are called automatically when needed

**Example:**
```python
from google.adk.tools import FunctionTool
from google.adk.agents import LlmAgent

def get_weather(city: str) -> dict:
    """Get weather for a city."""
    return {"city": city, "temp": "72°F"}

weather_tool = FunctionTool(func=get_weather)

agent = LlmAgent(
    model="gemini-2.0-flash",
    name="assistant",
    tools=[weather_tool]
)
```

## Part 2: Local MCP Tools (stdio)

### What is MCP?

Model Context Protocol - standardized way to connect AI agents to external tools and data sources.

**Local MCP** uses stdio (standard input/output) to communicate with MCP servers running as child processes.

**Key concepts:**
- `MCPToolset` with `StdioConnectionParams`
- Local MCP servers (like `@modelcontextprotocol/server-filesystem`)
- Tool filtering for security
- Path restrictions

**Example (see agent.py for working implementation):**
```python
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from mcp import StdioServerParameters

# Configure MCP toolset with filesystem server
toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='npx',
            args=['-y', '@modelcontextprotocol/server-filesystem', '/allowed/path']
        ),
        timeout=10
    ),
    tool_filter=['read_file', 'list_directory', 'search_files']
)

# Create agent with MCP tools
root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name='filesystem_assistant',
    instruction="You can explore and read files. Use the tools available.",
    tools=[toolset]
)
```

## Part 3: Remote MCP Tools (HTTP/SSE)

### What are Remote MCP Servers?

MCP servers hosted on URLs, accessible via HTTP with Server-Sent Events (SSE).

**Benefits:**
- Share tools across team/organization
- Managed MCP services
- Cloud-hosted tool providers
- Scalable and centralized

**Key concepts:**
- `SseConnectionParams` for remote servers
- Authentication via headers
- HTTPS for security
- Shared tool infrastructure

**Example (pattern you can implement):**
```python
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool import SseConnectionParams

# Connect to remote MCP server
toolset = MCPToolset(
    connection_params=SseConnectionParams(
        url="https://your-mcp-server.com/sse",
        headers={'Authorization': 'Bearer YOUR_TOKEN'}
    )
)

agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[toolset]
)
```

**Use cases:**
- Your own MCP server deployed on Cloud Run
- Third-party MCP service providers
- Team-shared tool servers
- Enterprise tool catalogs

## Part 4: Custom MCP Server (Advanced)

You can build your own MCP server to expose custom tools!

**Conceptual example:**
```python
# custom_mcp_server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("my-custom-server")

@app.list_tools()
async def list_tools():
    return [
        {
            "name": "calculate",
            "description": "Perform calculations",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                }
            }
        }
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "calculate":
        result = eval(arguments["expression"])  # Be careful with eval in production!
        return {"result": result}

async def main():
    async with stdio_server() as streams:
        await app.run(
            streams[0], streams[1],
            app.create_initialization_options()
        )
```

**To deploy as remote server:**
1. Use SSE transport instead of stdio
2. Deploy to Cloud Run, Kubernetes, etc.
3. Add authentication and input validation
4. Share URL with your team

## Tool Comparison

| Type | Transport | Use Case | Example |
|------|-----------|----------|---------|
| **FunctionTool** | Direct | Simple Python functions | `get_weather()` |
| **Local MCP** | stdio | Local processes, file access | Filesystem, local DB |
| **Remote MCP** | HTTP/SSE | Shared tools, cloud services | Team tools, APIs |

## Security Best Practices

### 1. Path Restrictions (Filesystem)

```python
# ✅ Good: Restricted path
allowed_path = os.path.join(os.getcwd(), "data")

# ❌ Bad: Full system access
allowed_path = "/"
```

### 2. Tool Filtering

```python
# ✅ Good: Only safe operations
tool_filter=['read_file', 'list_directory']

# ❌ Bad: All tools exposed
# No tool_filter specified
```

### 3. Authentication (Remote MCP)

```python
# ✅ Good: Authenticated
headers={'Authorization': f'Bearer {token}'}

# ❌ Bad: No authentication
headers={}
```

### 4. Input Validation

```python
def safe_tool(path: str) -> dict:
    """Tool with validation."""
    # Validate input
    if ".." in path or path.startswith("/"):
        return {"error": "Invalid path"}

    # Process safely
    return {"result": "ok"}
```

## Exercise

Create an agent that combines multiple tool types:
1. **FunctionTool**: Weather lookup
2. **Local MCP**: Read local config file
3. **Custom logic**: Combine data and make recommendations

Bonus: Deploy your own MCP server and connect to it remotely!

## Key Takeaways

- ✅ **FunctionTool** = Easiest, for Python functions
- ✅ **Local MCP** = Standardized, for local processes
- ✅ **Remote MCP** = Scalable, for shared tools
- ✅ **Always** filter tools and restrict access
- ✅ **MCP** enables tool sharing across frameworks

## Troubleshooting

**Error: "npx command not found"**
- Install Node.js: `brew install node` or visit nodejs.org

**Error: "Permission denied"**
- Check file/directory permissions
- Use absolute paths
- Verify allowed_path is accessible

**Error: "Connection timeout" (Remote MCP)**
- Check MCP_SERVER_URL is correct
- Verify server is running
- Check network/firewall settings

**Tool not working**
- Verify tool is in `tool_filter` list
- Check MCP server supports the tool
- Review tool docstring and parameters

## Best Practices

1. **Start with FunctionTool** for simple needs
2. **Use MCP for standardization** and sharing
3. **Filter tools** to minimum required set
4. **Restrict paths** for filesystem access
5. **Authenticate** remote MCP connections
6. **Log tool usage** for debugging and auditing
7. **Test tools separately** before agent integration

## Next Steps

**Continue learning**: Move to [Tutorial 4: Production Ready](../4-production-ready/) for deployment.

**Experiment more**:
- Create your own FunctionTools
- Deploy MCP server to Cloud Run
- Integrate with real APIs
- Build team-shared tool catalog

## Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [ADK Tools Documentation](https://google.github.io/adk-docs/tools/)
- [ADK MCP Integration](https://google.github.io/adk-docs/tools/mcp-tools/)
- [MCP Server Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
