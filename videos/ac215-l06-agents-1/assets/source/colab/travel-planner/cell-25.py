# Turn 2: resolve the city and state both allowances with exact units.
reply = await run_turn(agent, """
San Francisco. Food allowance of $60 per person per day
and $150 total for local transportation for the whole trip.
""", session, context, invoke_agent)
assert reply.kind == "options"
