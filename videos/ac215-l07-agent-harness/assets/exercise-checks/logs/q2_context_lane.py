# Q2 and B3: where the enriched packet goes, and whether it stops Comté. Act 2 enriched, standard request (PA),
# the tutorial's scripted client proposing the raw-milk cart (comte 350 / bucheron 350 / epoisses 300).
import asyncio
from acts.act2_context import build_act2
from formaggio.fixtures.evaluation_fixture import ProposalFixture
from formaggio.operations.observability import Recorder


async def main():
    harness = build_act2(scenario="standard", mode="enriched", execution_mode="fixture")
    with Recorder("outputs/exercises.sqlite") as recorder:
        async with ProposalFixture("accepted", "pa-shipping").client() as client:
            result = await harness.run(recorder, api_client=client)
        print("excluded in the packet:", [(p["product_id"], p.get("reasons") or p) for p in result["context"]["excluded_products"]])
        first = next(e for e in recorder.timeline(result["run_id"]) if e["event_type"] == "model.request")
        print("model call 1 options:", sorted(first["payload"]["options"]))
        print("instructions start:", first["payload"]["options"].get("instructions", "")[:60].replace("\n", " "), "…")
        for i, m in enumerate(first["payload"]["messages"], 1):
            text = next((c["text"] for c in m["contents"] if c["type"] == "text"), "")
            print(f"message {i}: role={m['role']}: {text[:75]!r}")
        report = result["report"]
        print("cart:", [(i.product, i.grams) for i in report.items], "ok:", report.ok)
        print("violations:", [(v.rule, v.product_id, v.detail) for v in report.violations])
        print("cart_check_status:", result["cart_check_status"], "| order placed: never in Acts 1-2")

asyncio.run(main())
