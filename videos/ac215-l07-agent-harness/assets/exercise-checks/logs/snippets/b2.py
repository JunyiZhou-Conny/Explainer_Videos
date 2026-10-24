import asyncio
from acts.act1_agent import build_act1
from formaggio.agents.layers import Budget
from formaggio.fixtures.evaluation_fixture import ProposalFixture
from formaggio.operations.observability import Recorder


async def main():
    squeezed = (build_act1(execution_mode="fixture")
                .without("budget").add(Budget(model_calls=1, tool_calls=20, seconds=120)))
    with Recorder("outputs/exercises.sqlite") as recorder:
        try:
            async with ProposalFixture("accepted", "standard").client() as client:
                await squeezed.run(recorder, api_client=client, progress=print)
        except Exception as exc:
            print(type(exc).__name__ + ":", exc)
        print(recorder.query("SELECT status, error FROM runs ORDER BY started_at DESC LIMIT 1"))

asyncio.run(main())
