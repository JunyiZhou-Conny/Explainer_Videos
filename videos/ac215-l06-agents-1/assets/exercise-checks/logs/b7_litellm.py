# b7_litellm.py: module 2 under google-adk 2.12.0, without an OpenAI key and without internet.
import asyncio, os, sys, logging
sys.path.insert(0, os.getcwd())
logging.disable(logging.WARNING)
from google.adk.models.registry import LLMRegistry
for name in ("gpt-4", "openai/gpt-5.6-luna"):
    cls = LLMRegistry.resolve(name)
    print(f"model={name!r:32} -> {cls.__module__}.{cls.__name__}")
from google.adk.cli.utils.agent_loader import AgentLoader
loader = AgentLoader(os.getcwd())
print("agents listed:", loader.list_agents())
for app in ("2-litellm", "litellm", "litellm_agent"):
    try:
        a = loader.load_agent(app)
        print(f"load_agent({app!r}) -> {type(a).__name__} {a.name!r}, model {a.model!r}")
    except Exception as e:
        print(f"load_agent({app!r}) -> {type(e).__name__}: {str(e)[:200]}")
from adk_standin import run
a = loader.load_agent("litellm_agent")
print("OPENAI_API_KEY set:", "OPENAI_API_KEY" in os.environ)
try:
    asyncio.run(run(a, "Hello!", app_name="litellm_agent"))
except Exception as e:
    print(f"first message -> {type(e).__name__}: {str(e)[:300]}")
