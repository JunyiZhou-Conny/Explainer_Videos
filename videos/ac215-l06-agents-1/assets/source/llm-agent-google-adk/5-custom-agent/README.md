# Tutorial 5: Custom Agents - Advanced Patterns

Learn how to build custom agents by extending `BaseAgent` for complex, multi-stage workflows.

## Overview

In this tutorial, you'll learn:
- How to extend `BaseAgent` for custom orchestration
- Implementing `_run_async_impl` for execution logic
- Using `LoopAgent` for iterative workflows
- Managing state with `InvocationContext`
- Event handling and escalation
- Conditional logic and branching
- Pydantic integration for agent configuration

## Prerequisites

- Completed Tutorials 1-4
- Understanding of async/await in Python
- Familiarity with Pydantic
- Python 3.10+

## Concepts

### Why Custom Agents?

Built-in agents (`SequentialAgent`, `ParallelAgent`, `LoopAgent`) handle common patterns, but custom agents enable:

- **Complex orchestration**: Multi-stage workflows with conditional logic
- **State machines**: Advanced state management and transitions
- **Domain-specific logic**: Business rules and validation
- **Event handling**: Custom event processing and escalation
- **Reusable patterns**: Package complex workflows as single agents

### BaseAgent Extension

```python
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator

class MyCustomAgent(BaseAgent):
    """Custom agent with specific orchestration logic."""

    # Pydantic field declarations
    sub_agent_1: LlmAgent
    sub_agent_2: LlmAgent

    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, name: str, sub_agent_1: LlmAgent, sub_agent_2: LlmAgent):
        # Initialize sub-agents before calling super().__init__
        super().__init__(
            name=name,
            sub_agent_1=sub_agent_1,
            sub_agent_2=sub_agent_2,
            sub_agents=[sub_agent_1, sub_agent_2]
        )

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Implement custom orchestration logic."""

        # Run first agent
        async for event in self.sub_agent_1.run_async(ctx):
            yield event

        # Conditional logic based on state
        if ctx.session.state.get("condition"):
            async for event in self.sub_agent_2.run_async(ctx):
                yield event
```

### Key Components

**InvocationContext**
- Access to session state: `ctx.session.state`
- Conversation history: `ctx.history`
- User info: `ctx.user_id`, `ctx.session_id`

**Event Management**
- Yield events from sub-agents
- Create custom events
- Use `escalate=True` to stop loops

**State Management**
- Read/write shared state
- Pass data between agents
- Implement state machines

## Setup

```bash
uv sync
cp .env.example .env
# Add your GOOGLE_API_KEY
```

## File Structure

```
5-custom-agent/
├── README.md                    # This tutorial
├── .env.example                # Environment template
├── pyproject.toml              # Dependencies
├── agent.py                    # Simple custom agent for adk web
├── simple_custom_agent.py      # Standalone example with session setup
└── conditional_agent.py        # Advanced: Dynamic routing example
```

## Running the Examples

### Option 1: Using `adk web` (Quickest)

From the **repository root**:

```bash
uv run adk
```

Open http://localhost:8000 and interact with the simple custom agent that adds a 🤖 prefix to responses.

### Option 2: Simple Custom Agent

Demonstrates BaseAgent extension with a prefix agent:

```bash
cd 5-custom-agent
uv run python simple_custom_agent.py
```

**What it does:**
- Extends BaseAgent with custom behavior
- Adds emoji prefix to all responses
- Shows proper session management setup

### Option 3: Conditional Workflow Agent

Advanced example with dynamic routing:

```bash
cd 5-custom-agent
uv run python conditional_agent.py
```

**What it does:**
1. Classifies query complexity (simple/complex/ambiguous)
2. Routes to appropriate handler agent
3. Tests multiple query types automatically

**Logic**: Route based on query complexity to different processing paths

## Code Walkthrough

### Simple Custom Agent (agent.py)

The minimal example for `adk web`:

```python
from google.adk.agents import BaseAgent, LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator

class CustomAgent(BaseAgent):
    """Custom agent that adds a prefix to responses"""

    llm_agent: LlmAgent

    def __init__(self):
        llm_agent = LlmAgent(
            model="gemini-2.0-flash",
            name="assistant",
            instruction="You are a helpful assistant."
        )

        super().__init__(
            name="CustomAgent",
            llm_agent=llm_agent,
            sub_agents=[llm_agent]
        )

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Add custom prefix to responses"""
        async for event in self.llm_agent.run_async(ctx):
            if event.is_final_response():
                original = event.content.parts[0].text
                event.content.parts[0].text = f"🤖 {original}"
            yield event

root_agent = CustomAgent()
```

### Conditional Routing Agent (conditional_agent.py)

Advanced pattern showing dynamic agent selection (see full implementation in the file):

```python
class ConditionalAgent(BaseAgent):
    """Routes queries to different handlers based on complexity."""

    # Pydantic field declarations
    classifier: LlmAgent
    simple_handler: LlmAgent
    complex_handler: LlmAgent
    clarification_handler: LlmAgent

    model_config = {"arbitrary_types_allowed": True}

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        # Step 1: Classify the query
        async for event in self.classifier.run_async(ctx):
            yield event

        # Get classification result
        complexity = ctx.session.state.get("query_complexity", "simple")

        # Step 2: Route based on complexity
        if complexity == "simple":
            async for event in self.simple_handler.run_async(ctx):
                yield event
        elif complexity == "complex":
            async for event in self.complex_handler.run_async(ctx):
                yield event
        else:  # ambiguous
            async for event in self.clarification_handler.run_async(ctx):
                yield event
```

### Using LoopAgent with Escalation

```python
from google.adk.agents import LoopAgent, BaseAgent
from google.adk.events import Event, EventActions

class CheckCondition(BaseAgent):
    """Agent that checks a condition and escalates when done."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        status = ctx.session.state.get("status", "pending")
        is_done = (status == "completed")

        # Escalate to break the loop
        yield Event(
            author=self.name,
            actions=EventActions(escalate=is_done)
        )

# Use in a loop
poller = LoopAgent(
    name="StatusPoller",
    max_iterations=10,
    sub_agents=[process_step, CheckCondition(name="Checker")]
)
```

### State Management Patterns

```python
async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
    # Read from state
    previous_result = ctx.session.state.get("key", "default")

    # Write to state
    ctx.session.state["new_key"] = "value"

    # Conditional routing based on state
    if ctx.session.state.get("needs_validation"):
        async for event in self.validator.run_async(ctx):
            yield event

    # Pass all state to sub-agent (via output_key)
    async for event in self.processor.run_async(ctx):
        yield event
```

## Advanced Patterns

### Pattern 1: Dynamic Sub-Agent Selection

```python
async def _run_async_impl(self, ctx: InvocationContext):
    # Choose agent based on input
    query_length = len(ctx.history[-1].parts[0].text)

    if query_length > 100:
        agent = self.complex_handler
    else:
        agent = self.simple_handler

    async for event in agent.run_async(ctx):
        yield event
```

### Pattern 2: Error Recovery

```python
async def _run_async_impl(self, ctx: InvocationContext):
    try:
        async for event in self.primary_agent.run_async(ctx):
            yield event
    except Exception as e:
        logger.error(f"Primary agent failed: {e}")

        # Fallback agent
        async for event in self.fallback_agent.run_async(ctx):
            yield event
```

### Pattern 3: Parallel with Conditional Merge

```python
async def _run_async_impl(self, ctx: InvocationContext):
    # Run parallel agents
    async for event in self.parallel_group.run_async(ctx):
        yield event

    # Conditional merge based on results
    if all([
        ctx.session.state.get("result1"),
        ctx.session.state.get("result2"),
        ctx.session.state.get("result3")
    ]):
        async for event in self.merger.run_async(ctx):
            yield event
    else:
        # Handle partial results
        async for event in self.partial_merger.run_async(ctx):
            yield event
```

## Exercise

Build a research agent that:
1. Validates the research topic
2. Generates research questions (3-5 questions)
3. For each question: Research → Verify → Refine (loop)
4. Synthesizes all findings
5. Generates citations

Hints:
- Extend `BaseAgent`
- Use `LoopAgent` for question processing
- Use `ParallelAgent` for multiple questions
- Manage state for each research step
- Implement conditional logic for verification

## Key Takeaways

- Custom agents enable complex orchestration logic
- Extend `BaseAgent` and implement `_run_async_impl`
- Use Pydantic for agent configuration
- Manage state via `InvocationContext`
- Yield events from sub-agents
- Escalate to control loops
- Combine built-in agents for powerful patterns

## Troubleshooting

**Error: "Field not declared in model"**
- Add Pydantic field declarations at class level
- Use type hints for all fields
- Set `model_config = {"arbitrary_types_allowed": True}`

**State not persisting**
- Ensure you're using the same session_id
- Check that state is written to `ctx.session.state`
- Verify session service is configured correctly

**Loop never stops**
- Ensure escalate condition is reachable
- Check `max_iterations` is set
- Verify escalate event is yielded correctly

**Sub-agents not executing**
- Make sure to `yield` events from sub-agents
- Use `async for` when calling sub-agents
- Pass `ctx` to `run_async()`

## Best Practices

1. **Always declare Pydantic fields** for type safety
2. **Initialize sub-agents before super().__init__()**
3. **Use descriptive names** for clarity
4. **Add logging** for debugging workflows
5. **Handle errors gracefully** with try/except
6. **Document complex logic** with comments
7. **Test each sub-agent separately** before integrating

## Congratulations!

You've completed all 5 tutorials! You now know:

✓ Sequential and parallel orchestration
✓ Multi-model support with LiteLLM
✓ Tool integration via MCP
✓ Production deployment with FastAPI
✓ Custom agents with advanced patterns

## Next Steps

**Build something amazing:**
- Personal assistant agent
- Research automation tool
- Content generation pipeline
- Customer service bot
- Code review system

**Explore more:**
- [ADK Examples](https://github.com/google/adk-samples)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Community Projects](https://github.com/topics/google-adk)

**Share your work:**
- Contribute to adk-samples
- Write about your experience
- Help others learn ADK

Happy building! 🚀
