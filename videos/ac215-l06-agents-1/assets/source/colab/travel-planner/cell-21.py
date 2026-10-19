# @title Travel Agent

@function_tool(description_override=finalize_plan.__doc__)
def finalize_itinerary(travel_context: RunContextWrapper[TravelContext], outbound_id: str,
                       return_id: str, hotel_id: str, travelers: int,
                       budget_usd: int, daily_food_usd: int,
                       local_transport_usd: int, pet_friendly: bool,
                       attraction_ids: list[str]) -> dict:
    # Finalize plan
    return finalize_plan(travel_context.context, outbound_id, return_id, hotel_id, travelers, budget_usd, daily_food_usd, local_transport_usd, pet_friendly, attraction_ids)

async def invoke_agent(agent: Agent, prompt: str, session: SQLiteSession, context: TravelContext) -> PlannerReply:
    """Run one agent invocation and obtain its Pydantic response value."""

    # Run agent
    result = await Runner.run(
        agent, prompt, session=session, context=context, max_turns=12
    )
    if isinstance(result.final_output, PlannerReply):
        return result.final_output
    raise RuntimeError("Agent returned a response that did not match PlannerReply.")

def build_agent():
    # LLM
    MODEL_NAME = "gpt-5.6-luna"

    # Tools
    tools = [
        function_tool(city_search),
        function_tool(flight_search),
        function_tool(hotel_search),
        function_tool(restaurant_search),
        function_tool(attraction_search),finalize_itinerary
    ]

    # Session & Context
    session = SQLiteSession("travel-planner")
    context = TravelContext()

    # Agent
    agent = Agent(
        name="Travel Planner",
        model=MODEL_NAME,
        instructions=TRAVEL_AGENT_INSTRUCTIONS,
        tools=tools,
        output_type=PlannerReply,
    )

    return agent, session, context
