# Turn 4: only this later human turn approves the displayed proposal.
reply = await run_turn(agent, "yes", session, context, invoke_agent)
assert reply.kind == "itinerary"
assert context.finalized_this_turn
assert context.checked_plan is not None
assert context.checked_plan["total_usd"] == 2690.0
