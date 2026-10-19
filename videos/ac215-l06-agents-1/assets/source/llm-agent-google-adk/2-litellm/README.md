# Tutorial 2: LiteLLM - Multi-Model Support

Learn how to use multiple LLM providers with Google ADK and LiteLLM, including AWS-hosted OpenAI.

## Overview

In this tutorial, you'll learn:

- How to configure LiteLLM with AWS OpenAI endpoints
- Using different LLM providers (OpenAI, Anthropic, Google)
- Model selection and fallback strategies
- Running agents with `adk web`
- Programmatic model testing

## Prerequisites

- Completed Tutorial 1 (Baseline)
- Python 3.10+
- uv package manager
- At least one API key (Google AI or AWS OpenAI)

## Setup

### 1. Install dependencies (from root)

```bash
# From repository root
uv sync
```

### 2. Configure environment

```bash
# Copy from root or tutorial folder
cp .env.example .env
```

Edit `.env`:

```bash
# Required: At least one of these
GOOGLE_API_KEY=your_google_ai_key
AWS_OPENAI_API_KEY=your_aws_openai_key

# Optional: Other providers
# ANTHROPIC_API_KEY=your_anthropic_key
# OPENAI_API_KEY=your_openai_key
```

**Getting AWS OpenAI API Key:**

- If using AWS Bedrock/SageMaker with OpenAI models
- Or standard OpenAI API from AWS infrastructure
- Or just use standard `OPENAI_API_KEY` from https://platform.openai.com/api-keys

## File Structure

```
2-litellm/
├── README.md              # This file
├── .env.example          # Environment template
├── pyproject.toml        # Dependencies
├── litellm_config.py     # LiteLLM setup & AWS OpenAI config
└── agent.py              # Root agent for `adk web`
```

## Running the Examples

### Option 1: Using `adk web` (Recommended)

From the **repository root**:

```bash
uv run adk
```

Then open http://localhost:8000 in your browser and chat with the agent!

You can modify `agent.py` to switch between different models (GPT-4, Claude, Gemini) by uncommenting the desired model configuration.

### Option 2: Test LiteLLM Configuration

```bash
cd 2-litellm
uv run python litellm_config.py
```

Tests which models are accessible with your current API keys.

## Code Walkthrough

### Using Different Models

```python
from google.adk.agents import LlmAgent

# Google Gemini (fastest, cheapest)
gemini_agent = LlmAgent(
    name="GeminiAgent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant."
)

# OpenAI GPT-4 (high quality)
gpt4_agent = LlmAgent(
    name="GPT4Agent",
    model="gpt-4",
    instruction="You are a helpful assistant."
)

# Anthropic Claude (balanced)
claude_agent = LlmAgent(
    name="ClaudeAgent",
    model="claude-3-5-sonnet-20241022",
    instruction="You are a helpful assistant."
)
```

### Model Fallback Pattern

```python
from google.adk.agents import LlmAgent

async def run_with_fallback(query: str):
    """Try primary model, fallback to secondary."""

    primary = LlmAgent(model="gpt-4", ...)
    fallback = LlmAgent(model="gemini-2.0-flash", ...)

    try:
        # Try primary
        result = await run_agent(primary, query)
        return result
    except Exception as e:
        print(f"Primary failed: {e}, using fallback...")
        # Use fallback
        result = await run_agent(fallback, query)
        return result
```

### Environment-Based Model Selection

```python
import os

# Use different models per environment
model_name = os.getenv(
    "LLM_MODEL",
    "gemini-2.0-flash"  # Default
)

agent = LlmAgent(
    model=model_name,
    ...
)
```

## Model Selection Guide

### Speed Priority

- **Best**: `gemini-2.0-flash`
- **Alternative**: `gpt-3.5-turbo`, `claude-3-5-haiku-20241022`

### Quality Priority

- **Best**: `gpt-4`, `claude-3-5-sonnet-20241022`
- **Alternative**: `gemini-2.0-pro`

### Cost Priority

- **Best**: `gemini-2.0-flash` (free tier available)
- **Alternative**: `gpt-3.5-turbo`

### Balanced

- **Best**: `gemini-2.0-flash`, `claude-3-5-sonnet-20241022`

## Exercise

Create an agent routing system that:

1. Uses `gemini-2.0-flash` for simple queries
2. Uses `gpt-4` for complex reasoning
3. Has a fallback to `claude-3-5-sonnet-20241022`

Hints:

- Analyze query complexity (length, keywords)
- Create separate agents per model
- Implement conditional routing logic

## Key Takeaways

- ADK supports LiteLLM model names natively
- Different models have different strengths
- Fallback strategies improve reliability
- Environment variables enable flexible configuration
- Cost/performance tradeoffs matter in production

## Troubleshooting

**Error: "Invalid API key"**

- Check your `.env` file for the correct key
- Ensure the key is for the right provider (OPENAI_API_KEY for OpenAI, etc.)
- Verify the key is active in the provider's dashboard

**Error: "Model not found"**

- Check the model name spelling
- Some models require specific API access (e.g., GPT-4 may need approval)
- Refer to LiteLLM's model list: https://docs.litellm.ai/docs/providers

**Slow responses**

- Different models have different speeds
- GPT-4 is typically slower than GPT-3.5 or Gemini Flash
- Consider using faster models for latency-sensitive apps

**Cost concerns**

- Use environment variables to switch models per deployment
- Gemini has generous free tier limits
- Monitor usage in provider dashboards

## Best Practices

1. **Use environment variables** for model selection
2. **Implement fallbacks** for production reliability
3. **Monitor costs** across providers
4. **Test different models** for your use case
5. **Cache results** when appropriate
6. **Set timeouts** to prevent hanging requests

## Next Steps

**Continue learning**: Move to [Tutorial 3: MCP Connections](../3-mcp-connections/) to add external tools.

**Experiment more**:

- Try other models (Mistral, Llama, etc.)
- Implement cost tracking
- Build a model router based on query type

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [LiteLLM Supported Models](https://docs.litellm.ai/docs/providers)
- [ADK Model Configuration](https://google.github.io/adk-docs/agents/models/)
- [OpenAI Pricing](https://openai.com/pricing)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [Google AI Pricing](https://ai.google.dev/pricing)
