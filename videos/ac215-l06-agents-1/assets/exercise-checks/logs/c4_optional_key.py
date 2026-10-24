# c4_optional_key.py: the planner alone again (as in q4_whiteboard.py), once with the placeholder made optional:
# {itinerary_validation?}. What instruction reaches the model?
import asyncio, sys
from adk_standin import StandIn, run
sys.path.insert(0, "/home/student/AC215/llm-agent-google-adk")
from baseline.agent import processor
from google.adk.agents import LlmAgent
instruction = processor.instruction.replace("{itinerary_validation}", "{itinerary_validation?}")
alone = LlmAgent(name="TravelPlanner", model=StandIn(answer=lambda si, c: "(stand-in reply)"),
                 instruction=instruction, output_key="travel_plan")
print("instruction as written:", instruction[:60] + "…")
asyncio.run(run(alone, "2 adults, Boston to Montreal", app_name="alone"))
