"""
ADK Agent Definition
"""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

load_dotenv()

agent = LlmAgent(
    model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
    name="assistant",
    instruction="You are a helpful AI assistant."
)
