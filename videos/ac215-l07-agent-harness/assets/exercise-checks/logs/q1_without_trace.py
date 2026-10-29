# Q1 and B2: what .without("trace") keeps, and a squeezed Budget, on the Act 1 harness with the
# tutorial's scripted client (ProposalFixture "accepted", standard: one preview_order call, then a reply).
import asyncio
from collections import Counter
from acts.act1_agent import build_act1
from formaggio.agents.layers import Budget
from formaggio.fixtures.evaluation_fixture import ProposalFixture
from formaggio.operations.observability import Recorder


def events(recorder, run_id):
    return [(e["event_type"], sorted(e["payload"])) for e in recorder.timeline(run_id)]


async def run(recorder, h):
    async with ProposalFixture("accepted", "standard").client() as client:
        return await h.run(recorder, api_client=client)   # no progress printer: quiet


async def main():
    harness = build_act1(scenario="standard", execution_mode="fixture")
    lite = harness.without("trace")
    print("harness layers:", [l.name for l in harness.layers])
    print("lite layers:   ", [l.name for l in lite.layers])
    print("same object?", lite is harness)
    with Recorder("outputs/exercises.sqlite") as recorder:
        for name, h in (("lite", lite), ("harness", harness)):
            result = await run(recorder, h)
            print(f"\n--- {name}: model_calls={result['model_calls']} tool_calls={result['tool_calls']} "
                  f"cart_check_status={result['cart_check_status']}")
            for event_type, keys in events(recorder, result["run_id"]):
                print(f"  {event_type:22s} {keys}")
            spans = recorder.query("SELECT name FROM spans WHERE run_id=?", (result["run_id"],))
            print("  spans:", Counter(s["name"] for s in spans).most_common())
        try:
            harness.without("cartcheck")
        except ValueError as exc:
            print("\nharness.without('cartcheck') ->", type(exc).__name__ + ":", exc)
        try:
            Budget(model_calls=0)
        except ValueError as exc:
            print("Budget(model_calls=0) ->", type(exc).__name__ + ":", exc)
        squeezed = harness.without("budget").add(Budget(model_calls=1, tool_calls=20, seconds=120))
        print("\nsqueezed layers:", [l.name for l in squeezed.layers])
        try:
            async with ProposalFixture("accepted", "standard").client() as client:
                await squeezed.run(recorder, api_client=client, progress=print)
        except Exception as exc:
            print("\nsqueezed run raised", type(exc).__name__ + ":", exc)
        row = recorder.query("SELECT run_id,status,error FROM runs ORDER BY started_at DESC LIMIT 1")[0]
        print("last run:", dict(row))
        print("events:", [e for e, _ in events(recorder, row["run_id"])])

asyncio.run(main())
