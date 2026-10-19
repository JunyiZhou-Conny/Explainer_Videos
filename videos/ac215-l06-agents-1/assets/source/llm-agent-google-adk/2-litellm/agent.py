"""
Multi-Model Agent using LiteLLM

Example showing how to use different LLM providers through LiteLLM.
Uncomment the model you want to test with `adk web`.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

# Add current directory to path for litellm_config import
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from litellm_config import configure_litellm

load_dotenv()
configure_litellm()

# Option 1: OpenAI GPT-4
root_agent = LlmAgent(
    model="gpt-4",
    name="assistant",
    instruction="You are a helpful AI assistant."
)

# Option 2: Anthropic Claude (uncomment to use)
# root_agent = LlmAgent(
#     model="claude-3-5-sonnet-20241022",
#     name="assistant",
#     instruction="You are a helpful AI assistant."
# )
