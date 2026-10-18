"""
Baseline Agent - Travel Planner (Sequential Pipeline)

Demonstrates a sequential itinerary planning workflow.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import SequentialAgent, LlmAgent

load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

validator = LlmAgent(
    name="ItineraryValidator",
    model=GEMINI_MODEL,
    instruction="You validate trip requests. Extract traveler count, origin, destinations, dates, budget, and constraints from the input.",
    output_key="itinerary_validation"
)

processor = LlmAgent(
    name="TravelPlanner",
    model=GEMINI_MODEL,
    instruction="Using {itinerary_validation}, design a realistic multi-day travel plan with routing, daily schedule, estimated costs, and key booking recommendations.",
    output_key="travel_plan"
)

summarizer = LlmAgent(
    name="TripSummarizer",
    model=GEMINI_MODEL,
    instruction="Provide a concise, traveler-friendly summary based on {travel_plan}. Include total estimated cost and a highlights list.",
    output_key="trip_summary"
)

root_agent = SequentialAgent(
    name="TravelPlannerPipeline",
    sub_agents=[validator, processor, summarizer],
    description="Sequential itinerary planning pipeline"
)
