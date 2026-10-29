# B5 (ponder 3 by hand): approve the manager-approval cart, but let another order take Mimolette while the
# manager is "thinking". One shared Checkout, as Act 6 uses; fixture proposals, no model.
import asyncio
from acts.act3_workflow import build_act3
from formaggio.shop.checkout import Checkout
from formaggio.operations.observability import Recorder
from cli import print_workflow_result


async def main():
    checkout = Checkout()

    async def manager(ticket):
        print(f"manager sees ticket {ticket.ticket_id[:8]}…, fingerprint {ticket.fingerprint[:16]}…")
        checkout.store.inventory["mimolette"] -= 2000          # another order ships 2,000 g meanwhile
        print("mimolette left:", checkout.store.inventory["mimolette"], "g; manager answers: approve")
        return "approve"

    with Recorder("outputs/exercises.sqlite") as recorder:
        result = await build_act3(fixture=True, scenario="manager-approval").run(
            recorder, manager=manager, checkout=checkout, progress=print)
        print_workflow_result(result)
        for e in recorder.timeline(result["run_id"]):
            if e["event_type"] in {"approval.requested", "approval.decided", "policy.decision", "order.placed"}:
                p = e["payload"]
                print(e["event_type"], {k: (str(v)[:16] + "…" if k == "fingerprint" else v) for k, v in p.items()
                                        if k in {"fingerprint", "decision", "source", "action", "outcome", "reason"}})

asyncio.run(main())
