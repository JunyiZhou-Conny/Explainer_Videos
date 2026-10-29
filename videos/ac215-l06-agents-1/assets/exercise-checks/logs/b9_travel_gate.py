# b9_travel_gate.py: the Travel Planner's own Python (cells 9, 12, 14, 15, 18, 20, 21: imports, catalog, tools,
# the gate, business logic, the agent's definition), with no model: the tool function and the turn logic are
# called directly, as exercise B9 does in a new notebook cell. invoke_agent is replaced by stand-ins for D/C.
import asyncio, json
from notebook import run_cells
nb = run_cells("travel-planner", ["09", "12", "14", "15", "18", "20", "21"])
TravelContext, finalize_plan, apply_confirmation = nb["TravelContext"], nb["finalize_plan"], nb["apply_confirmation"]
turn3 = dict(outbound_id="SEA-SFO-20261106-1", return_id="SFO-SEA-20261110-1", hotel_id="SFO-BAY", travelers=2,
             budget_usd=6000, daily_food_usd=60, local_transport_usd=150, pet_friendly=True,
             attraction_ids=["SFO-BRIDGE", "SFO-MUSEUM"])
def brief(r):
    return {k: r[k] for k in ("status", "total_usd", "remaining_usd", "costs_usd") if k in r}

print("== 1. the model calls finalize twice in turn 3")
ctx = TravelContext()
for i in (1, 2):
    r = finalize_plan(ctx, **turn3)
    print(f"call {i}: status={r['status']!r}; approved_proposal={ctx.approved_proposal}")
print("\n== 2. which replies approve the pending proposal? (apply_confirmation, cell 18 lines 55-65)")
for reply in ["Yes!", "yes please", "Yes, please.", "y", "Confirm.", "OK", "sure", "yes, confirm", "Yes go ahead"]:
    c = TravelContext(pending_proposal={"x": 1})
    apply_confirmation(reply, c)
    print(f"  {reply!r:16} -> {'APPROVED' if c.approved_proposal else 'not approved'}")
print("\n== 3. the human types yes, then finalize runs again")
apply_confirmation("yes", ctx)
r = finalize_plan(ctx, **turn3)
print("status after yes:", brief(r), "| finalized_this_turn:", ctx.finalized_this_turn)
print("\n== 4. variants (check_itinerary directly)")
ci = nb["check_itinerary"]
print("15:00 outbound (-2):", brief(ci(**{**turn3, "outbound_id": "SEA-SFO-20261106-2"})))
try:
    ci(**{**turn3, "hotel_id": "SFO-GATE"})
except ValueError as e:
    print("SFO-GATE, pet_friendly=True: ValueError:", e)
print("SFO-GATE, pet_friendly=False:", brief(ci(**{**turn3, "hotel_id": "SFO-GATE", "pet_friendly": False})))
r = finalize_plan(ctx, **{**turn3, "hotel_id": "SFO-GATE", "pet_friendly": False})
print("finalize with that changed plan, after the earlier yes:", r["status"])

print("\n== 5. run_turn's guardrails with stand-in agents (invoke_agent replaced; no model)")
PlannerReply, run_turn = nb["PlannerReply"], nb["run_turn"]
async def claims_itinerary(agent, prompt, session, context):
    print("  [stand-in agent] returns kind='itinerary' without calling finalize")
    return PlannerReply(kind="itinerary", message="Your trip is all set!")
async def repeats_money(agent, prompt, session, context):
    return PlannerReply(kind="options", message="Flight 1 is $220 per person.")
async def turn3_model(agent, prompt, session, context):
    finalize_plan(context, **turn3); finalize_plan(context, **turn3)
    return PlannerReply(kind="clarification", message="Please confirm.")
async def turn4_model(agent, prompt, session, context):
    finalize_plan(context, **turn3)
    return PlannerReply(kind="itinerary", message="Here is your trip.")
async def main():
    try:
        await run_turn(None, "Book it.", None, TravelContext(), claims_itinerary)
    except RuntimeError as e:
        print("  RuntimeError:", e)
    await run_turn(None, "Show me flights.", None, TravelContext(), repeats_money)
    c = TravelContext()
    print("  -- turn 3 (stand-in calls finalize twice):")
    await run_turn(None, "I choose ...", None, c, turn3_model)
    print("  -- turn 4, the human types 'yes':")
    await run_turn(None, "yes", None, c, turn4_model)
asyncio.run(main())

print("\n== 6. the Agents SDK of cell 8 (openai-agents 0.3.2)")
import inspect, agents, agents.run
from agents import SQLiteSession
print("DEFAULT_MAX_TURNS =", agents.run.DEFAULT_MAX_TURNS, "| MaxTurnsExceeded:", agents.MaxTurnsExceeded.__mro__[1].__name__)
print("SQLiteSession", inspect.signature(SQLiteSession.__init__))
