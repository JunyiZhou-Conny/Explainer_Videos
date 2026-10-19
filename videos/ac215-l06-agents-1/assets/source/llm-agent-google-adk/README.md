# Google Agent Development Kit (ADK) Tutorial

A comprehensive, hands-on tutorial series for learning Google's Agent Development Kit (ADK). This tutorial progressively builds your knowledge from basic agent orchestration to production-ready deployments.

![Demo](demo.gif)

## What is Google ADK?

The Agent Development Kit (ADK) is an open-source, code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents. It's optimized for Gemini and the Google ecosystem, offering:

- **Flexible orchestration**: Sequential, parallel, and loop-based agent execution
- **Multi-agent architecture**: Build complex workflows with specialized sub-agents
- **Rich tool ecosystem**: MCP integration, custom tools, and built-in utilities
- **Production-ready**: Deploy to Cloud Run, Vertex AI Agent Engine, or any Python environment

## Additional Resources

- [Official ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python Repository](https://github.com/google/adk-python)
- [ADK Samples](https://github.com/google/adk-samples)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## Tutorial Structure

This tutorial is organized into 6 progressive modules:

### [1. Baseline - Agent Orchestration](./1-baseline/)

**Learn**: Core ADK concepts, sequential and parallel agent patterns
**Build**: Simple multi-agent workflows with state sharing

### [2. LiteLLM - Multi-Model Support](./2-litellm/)

**Learn**: Using multiple LLM providers beyond Gemini
**Build**: Agents with model fallbacks and cost optimization

### [3. MCP Tools - Tool Integration](./3-mcp-tools/)

**Learn**: Model Context Protocol for external tool access
**Build**: Agents with filesystem, web, and custom MCP tools

### [4. Production Ready - Deployment](./4-production-ready/)

**Learn**: FastAPI integration, async patterns, cloud deployment
**Build**: Production-grade agent API with authentication and monitoring

### [5. Custom Agents - Advanced Patterns](./5-custom-agent/)

**Learn**: Extending BaseAgent for complex workflows
**Build**: Custom agents with conditional logic and state machines

### [6. RAG - Retrieval-Augmented Generation](./6-rag/)

**Learn**: RAG concepts, vector databases, embeddings, and document retrieval
**Build**: Two RAG implementations - Vertex AI RAG Engine and custom ChromaDB solution

## Prerequisites

### Required

- **Python 3.10+** installed on your system
- **uv** package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Google Cloud account** with billing enabled (free tier works for learning)
- **Git** for cloning this repository

### Recommended

- Basic Python async/await knowledge
- Familiarity with REST APIs
- Understanding of LLM concepts (prompts, tokens, etc.)

## Getting Started

### 1. Clone this repository

```bash
git clone <repository-url>
cd google-adk-tutorial
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 3. Set up Google Cloud credentials

**Option A: Google AI Studio (Easiest for learning)**

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create an API key
3. Copy it for use in `.env` files

### 4. Install dependencies

```bash
# From repository root
uv sync
```

This creates a virtual environment with all dependencies for all tutorials.

### 5. Start learning!

See "Running Agents" below for different ways to interact with the tutorials.

## Running Agents

### Option 1: Using `adk web` (Recommended - Interactive UI)

From the **repository root**, start the ADK web UI:

```bash
uv run adk web
```

Then open **http://localhost:8000** in your browser. In the UI, select the agents or tutorial folders you want to run.

## Learning Path

We recommend following the tutorials in order:

```
1-baseline → 2-litellm → 3-mcp-tools → 4-production-ready → 5-custom-agent → 6-rag
```

However, if you have specific interests:

- **Just want to deploy agents?** → Start with 1-baseline, then jump to 4-production-ready
- **Focus on tool integration?** → 1-baseline → 3-mcp-tools
- **Advanced orchestration?** → 1-baseline → 5-custom-agent
- **Knowledge-grounded agents?** → 1-baseline → 6-rag

## Key Concepts: Session, Memory, Runner

- **Session**: The unique interaction context for a single conversation/run. Use a consistent `session_id` so events, memory, and traces align. If you encounter "Session not found", verify the `session_id` exists and matches what the runner/UI created.

- **Memory**: Structured state tied to a `session_id` and available across steps/turns. Store relevant facts, tool outputs, and user preferences. Separate sessions do not share memory.

- **Runner**: The orchestrator that executes agents/workflows and streams step events. It manages lifecycle, sessions, and tracing. Run via the web UI (`uv run adk web <path>`) or programmatically.

Tip: When running scripts directly, either let the runner manage sessions or reuse the same `session_id` throughout a single conversation.

## Sequential Agent Data Flow

- **output_key**: Each sub-agent writes its result to an `output_key` in shared state.
- **Referencing prior outputs**: Use curly braces to reference keys, e.g., `{validation_result}`.
- **Do NOT use quotes**: Avoid `'validation_result'` in instructions. Write `Using {validation_result}, ...` not `Using 'validation_result', ...`.

Example flow:

1. `Validator` → `output_key="validation_result"`
2. `Planner` reads `{validation_result}` and writes `output_key="travel_plan"`
3. `Summarizer` reads `{travel_plan}` to produce the final summary

## Getting Help

- **Documentation Issues**: Check the [official ADK docs](https://google.github.io/adk-docs/)
- **Code Examples**: Review [adk-samples](https://github.com/google/adk-samples)
- **Community**: Join discussions on GitHub

## License

This tutorial is licensed under the Apache License 2.0, consistent with Google ADK.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve these tutorials.

---

**Ready to build AI agents?** Start with [Tutorial 1: Baseline](./1-baseline/) →
