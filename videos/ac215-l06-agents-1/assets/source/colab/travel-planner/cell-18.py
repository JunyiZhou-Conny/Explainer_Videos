# @title Business Logic

#########################
# Business Logic
#########################
def check_itinerary(outbound_id: str, return_id: str, hotel_id: str,
                    travelers: int, budget_usd: int, daily_food_usd: int,
                    local_transport_usd: int, pet_friendly: bool,
                    attraction_ids: list[str]) -> dict:
    """Validate a round trip and compute its budget from canonical catalog prices.

    This demo supports 1–2 travelers sharing one room. Food is an allowance
    per person per calendar day; transport is an allowance for the entire trip.
    Mock flight/hotel prices are all-in; no real-world fees are implied.
    """
    if travelers not in (1, 2):
        raise ValueError("This demo supports 1–2 travelers sharing one room.")
    if budget_usd <= 0 or daily_food_usd < 0 or local_transport_usd < 0:
        raise ValueError("Budget must be positive and allowances cannot be negative.")
    outbound, inbound = resolve_flight(outbound_id), resolve_flight(return_id)
    if (outbound["origin"], outbound["destination"]) != (inbound["destination"], inbound["origin"]):
        raise ValueError("Return flight must reverse the outbound route.")
    nights = (parse_date(inbound["date"]) - parse_date(outbound["date"])).days
    if nights <= 0:
        raise ValueError("Return date must be after the outbound date.")
    if hotel_id not in HOTELS:
        raise ValueError("Unknown hotel ID; use hotel_search.")
    city, hotel_name, nightly, pets = HOTELS[hotel_id]
    if city != outbound["destination"] or (pet_friendly and not pets):
        raise ValueError("Hotel does not meet the destination/pet-friendly requirements.")
    if len(set(attraction_ids)) != len(attraction_ids):
        raise ValueError("Choose each attraction at most once.")
    admission = 0
    for key in attraction_ids:
        if key not in ATTRACTIONS or ATTRACTIONS[key][0] != city:
            raise ValueError(f"Attraction {key!r} is not in the destination city.")
        admission += ATTRACTIONS[key][2] * travelers
    costs = {"round_trip_flights": (outbound["price_cents"] + inbound["price_cents"]) * travelers,
             "hotel": nightly * nights, "food_allowance": daily_food_usd * 100 * travelers * (nights + 1),
             "local_transport_allowance": local_transport_usd * 100, "attractions": admission}
    total = sum(costs.values())
    return {"status": "within_budget" if total <= budget_usd * 100 else "over_budget",
            "booking_status": "Not booked — fictional planning only",
            "origin": outbound["origin"], "destination": city,
            "start_date": outbound["date"], "end_date": inbound["date"],
            "travelers": travelers, "rooms": 1, "nights": nights,
            "pet_friendly_required": pet_friendly,
            "outbound_flight": outbound_id, "return_flight": return_id,
            "hotel": hotel_name, "attractions": [ATTRACTIONS[k][1] for k in attraction_ids],
            "costs_usd": {k: v / 100 for k, v in costs.items()},
            "total_usd": total / 100, "budget_usd": budget_usd,
            "remaining_usd": (budget_usd * 100 - total) / 100,
            "assumptions": "One shared room; food for every calendar day, including arrival/departure; transport is a whole-trip allowance."}

def apply_confirmation(prompt: str, context: TravelContext) -> None:
    """Let only a later, explicit human response approve a pending proposal."""
    if context.pending_proposal is None:
        return
    answer = prompt.strip().casefold().rstrip(".! ")
    if answer in {"y", "yes", "confirm", "confirmed", "yes, confirm", "yes please"}:
        context.approved_proposal = context.pending_proposal.copy()
    else:
        # Corrections and unrelated replies never approve the previous proposal.
        context.approved_proposal = None
    context.pending_proposal = None

def checked_itinerary_reply(plan: dict) -> PlannerReply:
    """Use canonical checked data for the final prose, without repeating prices."""
    attractions = ", ".join(plan["attractions"]) or "no paid attractions"
    return PlannerReply(
        kind="itinerary",
        message=(
            f"Your checked round trip from {plan['origin']} to {plan['destination']} "
            f"is ready for {plan['travelers']} traveler(s), with {plan['hotel']} and "
            f"{attractions}. Budget report is shown below. Nothing has been booked."
        ),
    )

def confirmation_reply(context: TravelContext) -> PlannerReply:
    """Render the exact Python-owned proposal that needs human approval."""
    return PlannerReply(
        kind="clarification",
        message=(
            "Please review this exact proposed plan and reply with 'yes' to approve it, "
            "or tell me what to change. Food is per person per calendar day; local "
            "transport is for the whole trip.\n"
            + json.dumps(context.pending_proposal, indent=2)
        ),
    )

async def run_turn(agent, prompt,session, context, invoke_agent) -> PlannerReply:
    """
    Run one conversation turn and enforce confirmation, validation, and presentation.
    The model chooses actions and produces replies, while Python decides whether the resulting state permits those replies.
    """

    # Input validations
    if not prompt.strip():
        raise ValueError("The prompt cannot be empty.")

    # State Tracking
    context.validated_this_turn = False
    context.finalized_this_turn = False

    # Human approval and state tracking
    apply_confirmation(prompt, context)

    # Run Agent
    reply = await invoke_agent(agent, prompt, session=session, context=context)

    # Postcondition checking and corrective retry
    if reply.kind == "itinerary" and not context.finalized_this_turn and context.pending_proposal is None:
        reply = await invoke_agent(
            agent,
            "Application validation: an itinerary is not final until you call "
            "finalize_itinerary in this turn. Call it now with the exact selected "
            "plan. If requirements or approval are missing, return clarification "
            "or options instead.",
            session=session, context=context
        )

    # Authoritative presentation: determines what the user actually sees from the checked state
    if context.pending_proposal is not None:
        # Human confirmation
        reply = confirmation_reply(context)
    elif context.finalized_this_turn:
        # Render the validated final itinerary
        reply = checked_itinerary_reply(context.checked_plan)
    elif reply.kind == "itinerary":
        # Hard Guardrail: an unchecked final itinerary is rejected.
        raise RuntimeError("The agent returned an itinerary without a successful same-turn check.")

    # Soft Guardrail: it detects certain monetary expressions but still displays the response.
    if MONEY_IN_PROSE.search(reply.message):
        print("  [warning] The model repeated a monetary amount in narrative output.")

    print(f"Kind: {reply.kind}")
    print(reply.message)

    # Budget Report
    if context.validated_this_turn and context.budget_report is not None:
        print("Budget report (computed by Python; fictional planning only):")
        print(json.dumps(context.budget_report, indent=2))

    return reply
