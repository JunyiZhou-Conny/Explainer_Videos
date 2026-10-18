# @title Finalize Plan Tool

def finalize_plan(travel_context: TravelContext, outbound_id: str,
                       return_id: str, hotel_id: str, travelers: int,
                       budget_usd: int, daily_food_usd: int,
                       local_transport_usd: int, pet_friendly: bool,
                       attraction_ids: list[str]) -> dict:
    """Check the chosen round trip and budget before presenting a final itinerary.

    Use the user's budget and traveler count, and explicitly agreed allowances.
    Food is USD per person per calendar day; transport is USD for the whole trip.
    Pass daily_food_usd exactly as the per-person amount the user stated. For
    example, 50 per person for two travelers means daily_food_usd=50, never 100.
    Python multiplies by travelers and days; do not multiply tool arguments.
    Flights, hotel, and attractions must use IDs returned by the search tools.
    This checks prices and compatibility; it does not book anything.
    """
    log_tool("finalize_plan", "validating selections and calculating costs")
    result = check_itinerary(outbound_id, return_id, hotel_id, travelers, budget_usd,
                             daily_food_usd, local_transport_usd, pet_friendly, attraction_ids)
    proposal = {
        "outbound_id": outbound_id,
        "return_id": return_id,
        "hotel_id": hotel_id,
        "travelers": travelers,
        "budget_usd": budget_usd,
        "daily_food_usd": daily_food_usd,
        "local_transport_usd": local_transport_usd,
        "pet_friendly": pet_friendly,
        "attraction_ids": sorted(attraction_ids),
    }

    # A model tool call can propose a plan, but only a later human turn can
    # approve that exact proposal. This prevents the model from silently
    # inventing requirements or treating its own suggestion as confirmation.
    if proposal != travel_context.approved_proposal:
        travel_context.pending_proposal = proposal
        return {
            "status": "needs_confirmation",
            "requirements": proposal,
            "message": "Stop and wait for the user's next chat reply.",
        }

    travel_context.pending_proposal = None
    travel_context.budget_report = result
    travel_context.validated_this_turn = True
    if result["status"] == "within_budget":
        travel_context.checked_plan = result
        travel_context.finalized_this_turn = True
    return result
