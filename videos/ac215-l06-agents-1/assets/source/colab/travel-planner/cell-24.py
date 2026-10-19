# Build the Agent
agent, session, context = build_agent()

# Turn 1: core requirements, with one deliberate city ambiguity.
reply = await run_turn(agent, """
Plan a round trip from Seattle to California from November 6 to 10, 2026.
There are two adults sharing one room, our total budget is $6000, and the
hotel must be pet-friendly.
""", session, context, invoke_agent)
assert reply.kind == "clarification"
