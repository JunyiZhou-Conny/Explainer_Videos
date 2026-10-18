# Tutorial 1: Baseline - Travel Planner (Sequential & Parallel)

Learn the fundamentals of Google ADK by building sequential and parallel agent workflows. The baseline example implements a simple travel planner pipeline.

## Overview

In this tutorial, you'll learn:

- How to create basic LLM agents with the ADK
- Sequential agent execution (pipeline pattern)
- Parallel agent execution (concurrent pattern)
- State sharing between agents
- Session management and runners

## Prerequisites

- Python 3.10+
- uv package manager installed
- Google AI API key or Vertex AI access

## Concepts

### Sequential Agents

`SequentialAgent` executes sub-agents **one after another** in order. Each agent can:

- Read state from previous agents
- Write results to shared state via `output_key` and reference them with curly braces in prompts (e.g., `{travel_plan}`)
- Access the full conversation history

**Use cases**: Data pipelines, multi-step workflows, validation chains

### Parallel Agents

`ParallelAgent` executes sub-agents **concurrently**. Each agent:

- Runs simultaneously with others
- Has isolated context (`branch`)
- Shares the same session state
- Reduces total execution time

**Use cases**: Web research, data gathering, independent computations

### Runners

`InMemoryRunner` provides the execution environment for agents:

- Manages sessions and state
- Handles message routing
- Streams events from agents

## Setup

### 1. Install dependencies

```bash
uv sync
```

This installs all required packages defined in `pyproject.toml`.

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

**Option A: Google AI Studio (Easiest)**

```bash
GOOGLE_API_KEY=your_api_key_here
```

## Running the Examples

### Web UI (Recommended)

Launch the ADK web UI from the repository root:

```bash
uv run adk web
```

Then open http://localhost:8000 and select this tutorial folder (`1-baseline`) to run it.

**What to observe**:

- The pipeline executes in strict order: Validator → Planner → Summarizer
- Each agent reads from state written by previous agents
- Total time = sum of individual agent times for the sequential pipeline

### Parallel Pattern (Concept)

Parallel pipelines run sub-agents concurrently. Results are merged afterward. Total time is dominated by the slowest branch, not the sum of all.

### Interactive Runner (Optional, Programmatic)

You can also run agents programmatically using `InMemoryRunner`. The web UI is recommended for this tutorial.

## Code Walkthrough

### Creating a Basic Agent

```python
from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="MyAgent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant.",
    description="Helps users with questions",
    output_key="result"  # Where to save output in state
)
```

### Sequential Orchestration (Travel Planner)

```python
from google.adk.agents import SequentialAgent

# Three-step travel planner
# 1) ItineraryValidator → output_key="itinerary_validation"
# 2) TravelPlanner reads {itinerary_validation} → output_key="travel_plan"
# 3) TripSummarizer reads {travel_plan} → output_key="trip_summary"

pipeline = SequentialAgent(
    name="TravelPlannerPipeline",
    sub_agents=[validator, processor, summarizer]
)
```

Agents execute: validator → processor → summarizer

### Parallel Orchestration

```python
from google.adk.agents import ParallelAgent

gatherer = ParallelAgent(
    name="InfoGatherer",
    sub_agents=[weather_agent, news_agent, traffic_agent]
)
```

All 3 agents execute concurrently.

### Running an Agent

```python
from google.adk.runners import InMemoryRunner
from google.genai import types

runner = InMemoryRunner(agent=pipeline, app_name="my_app")
session_service = runner.session_service

# Create a session (ensure this session_id is reused)
await session_service.create_session(
    app_name="my_app",
    user_id="user123",
    session_id="session123"
)

# Send message
message = types.Content(
    role="user",
    parts=[types.Part(text="Process this data: ...")]
)

# Get response
async for event in runner.run_async(
    user_id="user123",
    session_id="session123",
    new_message=message
):
    if event.is_final_response():
        print(event.content.parts[0].text)
```

## Exercise

Create a research assistant that:

1. **Parallel Phase**: Simultaneously gathers information from 3 sources
2. **Sequential Phase**: Validates → Summarizes → Formats the results

Hints:

- Combine `ParallelAgent` and `SequentialAgent`
- Use `output_key` for each parallel agent
- Create a merger agent that reads all parallel outputs

## Key Takeaways

- `SequentialAgent` = ordered execution, shared state
- `ParallelAgent` = concurrent execution, faster results
- `output_key` = how agents share data via state
- `InMemoryRunner` = local execution environment
- Combine patterns for complex workflows

## Troubleshooting

**Error: "API key not found"**

- Ensure `.env` file exists with `GOOGLE_API_KEY`
- Check that you ran `cp .env.example .env`

**Error: "Model not available"**

- For Vertex AI: Enable the Vertex AI API in Google Cloud Console
- Verify your `GOOGLE_CLOUD_PROJECT` is correct

**Slow execution**

- Parallel agents should be noticeably faster than sequential
- Check your internet connection
- Consider using `gemini-2.0-flash` (faster) vs `gemini-2.0-pro` (higher quality)

## Next Steps

**Ready for more?** Continue to [Tutorial 2: LiteLLM](../2-litellm/) to learn multi-model support.

**Want to explore?** Try:

- Adding more agents to the pipelines
- Creating conditional logic with custom agents (preview of Tutorial 5)
- Adding tool usage (preview of Tutorial 3)

## Resources

- [ADK Agent Orchestration Docs](https://google.github.io/adk-docs/agents/orchestration/)
- [Sequential Agent API](https://google.github.io/adk-docs/api/agents/#sequential-agent)
- [Parallel Agent API](https://google.github.io/adk-docs/api/agents/#parallel-agent)
