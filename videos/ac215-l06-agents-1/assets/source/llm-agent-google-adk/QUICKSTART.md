# Quick Start Guide

Get started with Google ADK tutorials in 3 minutes!

## Setup (One Time)

```bash
# 1. Clone repository
git clone <repository-url>
cd google-adk-tutorial

# 2. Install dependencies
uv sync

# 3. Configure API key
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key_here
```

## Run Agents with `adk web`

### Tutorial 1: Sequential & Parallel Agents
```bash
uv run adk web 1-baseline/agent.py
```
**What you'll see:** Data processing pipeline (Validator → Processor → Summarizer)

---

### Tutorial 2: Multi-Model with LiteLLM
```bash
uv run adk web 2-litellm/agent.py
```
**What you'll see:** Agent using AWS OpenAI (GPT-4) or Gemini, auto-selected based on your API keys

**Tip:** Add `AWS_OPENAI_API_KEY` to `.env` to test with GPT-4

---

### Tutorial 3: MCP Filesystem Tools
```bash
uv run adk web 3-mcp-connections/agent.py
```
**What you'll see:** Agent that can list and read files in the tutorial folder

**Try asking:**
- "List files in this directory"
- "Read the README.md file"
- "What Python files are here?"

**Note:** Requires Node.js/npm installed

---

### Tutorial 5: Custom Story Agent
```bash
uv run adk web 5-custom-agent/agent.py
```
**What you'll see:** Multi-stage story generation with critique, revision, and tone analysis

**Try asking:** "Write a short story about a robot learning to paint"

---

## Alternative: Run Python Scripts

### Tutorial 1
```bash
cd 1-baseline
uv run python sequential_example.py   # Sequential demo
uv run python parallel_example.py     # Parallel demo
uv run python main.py                 # Interactive CLI
```

### Tutorial 2
```bash
cd 2-litellm
uv run python litellm_config.py       # Test configuration
uv run python main.py                 # Interactive model testing
```

### Tutorial 3
```bash
cd 3-mcp-connections
uv run python filesystem_agent.py     # Interactive filesystem agent
```

### Tutorial 5
```bash
cd 5-custom-agent
uv run python story_flow_agent.py     # Story generation workflow
uv run python state_machine_agent.py  # State machine example
uv run python conditional_agent.py    # Conditional routing
```

---

## Troubleshooting

**Error: "No module named 'google.adk'"**
```bash
# Run from repository root:
uv sync
```

**Error: "No root_agent found"**
- Make sure you're using `agent.py` files (not example scripts)
- Example: `uv run adk web 1-baseline/agent.py` ✅
- Not: `uv run adk web 1-baseline/sequential_example.py` ❌

**Error: "Invalid API key"**
- Check `.env` file has `GOOGLE_API_KEY=your_key_here`
- Get key from: https://aistudio.google.com/app/apikey

**Error: "npx command not found" (Tutorial 3)**
- Install Node.js: `brew install node` (macOS)
- Or visit: https://nodejs.org/

---

## Next Steps

1. **Start with Tutorial 1** to learn the basics
2. **Read the READMEs** in each folder for detailed explanations
3. **Modify the agents** to experiment and learn
4. **Build your own agent** using the patterns you've learned!

Happy learning! 🚀
