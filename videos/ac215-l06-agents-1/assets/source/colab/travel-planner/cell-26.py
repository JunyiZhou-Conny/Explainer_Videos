# Turn 3: select every catalog item and ask for the exact proposal.
reply = await run_turn(agent, """
I choose outbound flight SEA-SFO-20261106-1, return flight
SFO-SEA-20261110-1, hotel SFO-BAY, and attractions SFO-BRIDGE and
SFO-MUSEUM.
""", session, context, invoke_agent)
assert reply.kind == "clarification"
assert context.pending_proposal is not None
