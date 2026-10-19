"""
LiteLLM Configuration Module

Sets up LiteLLM to work with multiple LLM providers.
Provides examples for connecting to OpenAI and Anthropic.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def configure_litellm():
    """
    Configure LiteLLM with different providers.

    Examples included for:
    - OpenAI (standard API)
    - Anthropic Claude

    Uncomment the provider you want to use and set the appropriate API key in .env
    """

    # Option 1: OpenAI
    # Set OPENAI_API_KEY in your .env file
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
        print("✓ OpenAI configured")
        print("  Available models: gpt-4, gpt-4-turbo, gpt-3.5-turbo")

    # Option 2: Anthropic Claude
    # Set ANTHROPIC_API_KEY in your .env file
    # anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    # if anthropic_key:
    #     os.environ["ANTHROPIC_API_KEY"] = anthropic_key
    #     print("✓ Anthropic configured")
    #     print("  Available models: claude-3-5-sonnet-20241022, claude-3-opus-20240229")


def get_available_models() -> dict:
    """
    Returns available models based on configured API keys.

    Returns:
        dict: Model identifiers
    """
    models = {}

    # OpenAI models
    if os.getenv("OPENAI_API_KEY"):
        models["gpt-4"] = "gpt-4"

    # Anthropic models
    # if os.getenv("ANTHROPIC_API_KEY"):
    #     models["claude"] = "claude-3-5-sonnet-20241022"

    # Fallback to Gemini (requires GOOGLE_API_KEY)
    if not models and os.getenv("GOOGLE_API_KEY"):
        models["gemini"] = "gemini-2.0-flash"

    return models
