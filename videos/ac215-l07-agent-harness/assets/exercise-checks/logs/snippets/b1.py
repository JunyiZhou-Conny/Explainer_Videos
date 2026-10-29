import asyncio
from acts.act1_agent import build_act1
from formaggio.fixtures.evaluation_fixture import ProposalFixture
from formaggio.operations.observability import Recorder
from cli import print_agent_result


async def main():
    harness = build_act1(scenario="pa-shipping", execution_mode="fixture")
    with Recorder("outputs/exercises.sqlite") as recorder:
        for h in (harness, harness.without("cart_check")):
            async with ProposalFixture("accepted", "pa-shipping").client() as client:
                print_agent_result(await h.run(recorder, api_client=client, progress=print))

asyncio.run(main())
