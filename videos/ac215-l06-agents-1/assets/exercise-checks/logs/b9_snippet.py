# b9_snippet.py: exercise B9's new cell, exactly as printed in exercises.md, after the notebook's cells up to
# "Travel Agent" (9, 12, 14, 15, 18, 20, 21; the key cell 10 is skipped: nothing here calls OpenAI).
from notebook import run_cells
ns = run_cells("travel-planner", ["09", "12", "14", "15", "18", "20", "21"])
exec('''
ctx = TravelContext()
plan = dict(outbound_id="SEA-SFO-20261106-1", return_id="SFO-SEA-20261110-1", hotel_id="SFO-BAY",
            travelers=2, budget_usd=6000, daily_food_usd=60, local_transport_usd=150,
            pet_friendly=True, attraction_ids=["SFO-BRIDGE", "SFO-MUSEUM"])
print(finalize_plan(ctx, **plan)["status"]); print(finalize_plan(ctx, **plan)["status"])
apply_confirmation("Yes!", ctx)
print(finalize_plan(ctx, **plan)["total_usd"])
''', ns)
