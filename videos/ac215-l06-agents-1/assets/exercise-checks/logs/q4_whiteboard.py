# q4_whiteboard.py: the video's baseline agent (1-baseline renamed to baseline, unchanged code), each LlmAgent's
# model swapped for the stand-in. One trip request: what does each agent receive, what lands in the state?
# Then a second session (empty state), and the planner alone in a fresh session (no validator before it).
import asyncio, sys

from adk_standin import StandIn, run
sys.path.insert(0, "/home/student/AC215/llm-agent-google-adk")
from baseline.agent import root_agent, validator, processor, summarizer
from google.adk.agents import LlmAgent

def label(name):
    return lambda si, contents: f"(stand-in reply written for {name})"

for a in (validator, processor, summarizer):
    print(f"{a.name}: model={a.model!r} -> stand-in; output_key={a.output_key!r}; instruction={a.instruction[:60]!r}…")
    a.model = StandIn(answer=label(a.name))

async def main():
    msg = "2 adults, Boston to Montreal, Oct 30 - Nov 2, 1500 dollars, train preferred"
    print("\n== session 1: one trip request through", root_agent.name)
    runner, s1 = await run(root_agent, msg, app_name="baseline")
    print("state after the run:", s1.state)
    print("events in the session:", len(s1.events), [e.author for e in s1.events])
    print("\n== session 2 (same runner, new session): state before any message")
    s2 = await runner.session_service.create_session(app_name="baseline", user_id="student")
    print("state:", s2.state, "events:", len(s2.events))
    print("\n== the planner alone, in a fresh session (nothing has written itinerary_validation)")
    alone = LlmAgent(name="TravelPlanner", model=StandIn(answer=label("TravelPlanner")), instruction=processor.instruction,
                     output_key="travel_plan")
    try:
        await run(alone, msg, app_name="alone")
    except Exception as e:
        print(f"  {type(e).__name__}: {e}")

asyncio.run(main())
