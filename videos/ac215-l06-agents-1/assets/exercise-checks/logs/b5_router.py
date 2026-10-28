# b5_router.py <module> <labels>: runs main() of custom_agent/<module>.py (its three test queries, its Runner and
# its ConditionalAgent, unchanged) with every LlmAgent's model swapped for the stand-in. The classifier's
# "answer" for each query comes from <labels>, a JSON object; the handlers answer with their own name.
import asyncio, importlib, json, logging, sys
from adk_standin import StandIn
sys.path.insert(0, "/home/student/AC215/llm-agent-google-adk")
mod = importlib.import_module("custom_agent." + sys.argv[1])
labels = json.loads(sys.argv[2])
logging.getLogger("google_adk").setLevel(logging.WARNING)

def answer(si, contents):
    if "query classifier" in si:
        query = next(p.text for c in contents if c.role == "user" for p in c.parts if p.text)
        print(f"  [stand-in classifier] for {query!r} answers {labels[query]!r}")
        return labels[query]
    return "(stand-in reply of the handler: " + si.split(".")[0] + ")"

mod.GEMINI_MODEL = StandIn(answer=answer, quiet=True)
asyncio.run(mod.main())
