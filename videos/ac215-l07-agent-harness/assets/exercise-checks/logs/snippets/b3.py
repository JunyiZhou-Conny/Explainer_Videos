import asyncio
from acts.act2_context import build_act2
from formaggio.fixtures.evaluation_fixture import ProposalFixture
from formaggio.operations.observability import Recorder
from cli import print_agent_result


async def main():
    harness = build_act2(scenario="standard", mode="enriched", execution_mode="fixture")
    with Recorder("outputs/exercises.sqlite") as recorder:
        async with ProposalFixture("accepted", "pa-shipping").client() as client:
            result = await harness.run(recorder, api_client=client)
        print_agent_result(result)
        call1 = next(e for e in recorder.timeline(result["run_id"]) if e["event_type"] == "model.request")
        for message in call1["payload"]["messages"]:
            print(message["role"], "|", message["contents"][0]["text"][:60].replace("\n", " "))

asyncio.run(main())
