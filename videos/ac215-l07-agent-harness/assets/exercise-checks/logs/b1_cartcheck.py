# B1 (and Q1): the Act 1 harness offline, with the tutorial's own scripted client (ProposalFixture, the one
# `--evaluate core --fixture` uses). The script "proposes" the customer's raw-milk cart for PA.
import asyncio
from acts.act1_agent import build_act1
from formaggio.fixtures.evaluation_fixture import ProposalFixture
from formaggio.operations.observability import Recorder
from cli import print_agent_result


async def main():
    harness = build_act1(scenario="pa-shipping", execution_mode="fixture")
    with Recorder("outputs/exercises.sqlite") as recorder:
        for h in (harness, harness.without("cart_check")):
            print("=== layers:", [layer.name for layer in h.layers])
            async with ProposalFixture("accepted", "pa-shipping").client() as client:
                result = await h.run(recorder, api_client=client, progress=print)
            print_agent_result(result)
            print("cart_check_status:", result["cart_check_status"])

asyncio.run(main())
