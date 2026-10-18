"""
Conditional Workflow Agent

Demonstrates conditional routing and dynamic agent selection based on input analysis.
Shows how to implement branching logic in custom agents.
"""

import asyncio
import os
import logging
from typing import AsyncGenerator
from dotenv import load_dotenv

from google.adk.agents import BaseAgent, LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.runners import InMemoryRunner
from google.genai import types

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model configuration
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


class ConditionalAgent(BaseAgent):
    """
    Custom agent that routes queries to different handlers based on complexity.

    Routes:
    - Simple queries → Fast handler
    - Complex queries → Detailed handler
    - Ambiguous queries → Clarification handler
    """

    # Pydantic field declarations
    classifier: LlmAgent
    simple_handler: LlmAgent
    complex_handler: LlmAgent
    clarification_handler: LlmAgent

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        name: str,
        classifier: LlmAgent,
        simple_handler: LlmAgent,
        complex_handler: LlmAgent,
        clarification_handler: LlmAgent
    ):
        """Initialize the conditional agent."""
        super().__init__(
            name=name,
            classifier=classifier,
            simple_handler=simple_handler,
            complex_handler=complex_handler,
            clarification_handler=clarification_handler,
            sub_agents=[
                classifier,
                simple_handler,
                complex_handler,
                clarification_handler
            ]
        )

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Execute conditional routing logic."""

        logger.info(f"[{self.name}] Starting conditional workflow")

        # Step 1: Classify the query
        logger.info("  Step 1: Classifying query complexity...")
        async for event in self.classifier.run_async(ctx):
            yield event

        # Get classification result
        complexity = ctx.session.state.get("query_complexity", "simple")
        logger.info(f"  Classification: {complexity}")

        # Step 2: Route based on complexity
        if complexity == "simple":
            logger.info("  Step 2: Routing to simple handler...")
            async for event in self.simple_handler.run_async(ctx):
                yield event

        elif complexity == "complex":
            logger.info("  Step 2: Routing to complex handler...")
            async for event in self.complex_handler.run_async(ctx):
                yield event

        else:  # ambiguous
            logger.info("  Step 2: Routing to clarification handler...")
            async for event in self.clarification_handler.run_async(ctx):
                yield event

        logger.info(f"[{self.name}] Conditional workflow completed")


async def test_query(agent, runner, query: str, session_service):
    """Test a single query through the conditional agent."""
    import uuid

    print("\n" + "=" * 70)
    print(f"Query: {query}")
    print("=" * 70)

    session_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    await session_service.create_session(
        app_name="conditional_demo",
        user_id=user_id,
        session_id=session_id,
        state={}
    )

    message = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )

    route_taken = None
    final_response = None

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message
    ):
        if hasattr(event, 'author') and event.author:
            if "Handler" in event.author or "Clarification" in event.author:
                route_taken = event.author
                print(f"\n→ Routed to: {route_taken}")

        if event.is_final_response():
            final_response = event.content.parts[0].text

    print(f"\nResponse:\n{final_response}")
    print("-" * 70)


async def main():
    print("=" * 70)
    print("Conditional Workflow Agent Demo")
    print("=" * 70)

    # Create agents
    print("\n1. Creating workflow agents...")

    classifier = LlmAgent(
        name="QueryClassifier",
        model=GEMINI_MODEL,
        instruction="""You are a query classifier.
Analyze the user's query and classify its complexity:
- 'simple': Basic questions, facts, definitions
- 'complex': Multi-step reasoning, analysis, comparisons
- 'ambiguous': Unclear or needs clarification

Output ONLY one word: simple, complex, or ambiguous
Save to state key 'query_complexity'.
""",
        description="Classifies query complexity",
        output_key="query_complexity"
    )

    simple_handler = LlmAgent(
        name="SimpleHandler",
        model=GEMINI_MODEL,
        instruction="""You handle simple queries.
Provide a concise, direct answer (1-2 sentences).
Be friendly and helpful.
""",
        description="Handles simple queries"
    )

    complex_handler = LlmAgent(
        name="ComplexHandler",
        model=GEMINI_MODEL,
        instruction="""You handle complex queries.
Provide a detailed, well-structured answer with:
- Clear explanation
- Multiple perspectives if relevant
- Examples
- Summary

Take your time to be thorough.
""",
        description="Handles complex queries"
    )

    clarification_handler = LlmAgent(
        name="ClarificationHandler",
        model=GEMINI_MODEL,
        instruction="""You handle ambiguous queries.
Ask clarifying questions to understand what the user wants.
Be helpful and guide them to rephrase their question.
""",
        description="Handles ambiguous queries"
    )

    print("   ✓ All agents created")

    # Create conditional agent
    print("\n2. Creating Conditional Agent...")

    conditional_agent = ConditionalAgent(
        name="ConditionalRouter",
        classifier=classifier,
        simple_handler=simple_handler,
        complex_handler=complex_handler,
        clarification_handler=clarification_handler
    )

    print(f"   ✓ {conditional_agent.name} created")

    # Set up runner
    print("\n3. Setting up execution environment...")

    from google.adk.sessions import InMemorySessionService
    from google.adk.runners import Runner

    session_service = InMemorySessionService()

    runner = Runner(
        agent=conditional_agent,
        app_name="conditional_demo",
        session_service=session_service
    )

    print("   ✓ Runner ready")

    # Test with different types of queries
    print("\n4. Testing different query types...")

    test_queries = [
        "What is Python?",  # Simple
        "Compare and contrast object-oriented vs functional programming paradigms",  # Complex
        "Tell me about that thing",  # Ambiguous
    ]

    for query in test_queries:
        await test_query(conditional_agent, runner, query, session_service)

    print("\n" + "=" * 70)
    print("✓ Conditional Agent demo completed!")
    print("=" * 70)

    print("\n💡 Key Observations:")
    print("  • Classifier determined query complexity")
    print("  • Routing logic selected appropriate handler")
    print("  • Different handlers provided appropriate responses")
    print("  • Custom agent enabled flexible workflow control")


if __name__ == "__main__":
    print("\nConditional Workflow Agent Example")
    print("Demonstrates dynamic routing based on input analysis\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\nError: {e}")
        logger.error("Error in main", exc_info=True)
