"""
Simple Custom Agent Example

Shows how to create a custom agent by extending BaseAgent.
This agent adds a simple prefix to all responses.
"""

import os
import uuid
from typing import AsyncGenerator
from dotenv import load_dotenv
from google.adk.agents import BaseAgent, LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.runners import InMemoryRunner
from google.genai import types

load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


class PrefixAgent(BaseAgent):
    """Custom agent that adds a prefix to responses"""

    llm_agent: LlmAgent
    prefix: str

    def __init__(self, name: str, prefix: str = "🤖"):
        llm_agent = LlmAgent(
            model=GEMINI_MODEL,
            name=f"{name}_llm",
            instruction="You are a helpful assistant."
        )

        super().__init__(
            name=name,
            llm_agent=llm_agent,
            prefix=prefix,
            sub_agents=[llm_agent]
        )

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        """Run the LLM and add prefix to response"""

        # Run the underlying LLM agent
        async for event in self.llm_agent.run_async(ctx):
            # Modify final response to add prefix
            if event.is_final_response():
                original_text = event.content.parts[0].text
                event.content.parts[0].text = f"{self.prefix} {original_text}"

            yield event


async def main():
    agent = PrefixAgent(name="PrefixBot", prefix="🤖 [Bot]:")

    # Create runner with session management
    from google.adk.sessions import InMemorySessionService
    from google.adk.runners import Runner

    session_service = InMemorySessionService()
    session_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())

    await session_service.create_session(
        app_name="custom-agent-demo",
        user_id=user_id,
        session_id=session_id,
        state={}
    )

    runner = Runner(
        app_name="custom-agent-demo",
        agent=agent,
        session_service=session_service
    )

    message = types.Content(
        role="user",
        parts=[types.Part(text="Hello! What can you do?")]
    )

    print("Custom Agent Demo\n")
    print("User: Hello! What can you do?\n")
    print("Agent: ", end="", flush=True)

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
