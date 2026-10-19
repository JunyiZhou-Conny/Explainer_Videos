"""
Custom Agent - Simple Example

Shows how to extend BaseAgent to add custom behavior.
"""

import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from google.adk.agents import BaseAgent, LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event

load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


class CustomAgent(BaseAgent):
    """Custom agent that adds a prefix to responses"""

    llm_agent: LlmAgent

    def __init__(self):
        llm_agent = LlmAgent(
            model=GEMINI_MODEL,
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
