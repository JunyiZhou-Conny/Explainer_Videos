import asyncio
from acts.act3_workflow import build_act3
from formaggio.agents.layers import Trace
from formaggio.operations.observability import Recorder
from cli import print_workflow_result


async def main():
    lesson = build_act3(fixture=True, scenario="out-of-stock")
    with Recorder("outputs/exercises.sqlite") as recorder:
        print_workflow_result(await lesson.without("trace").without("budget").run(recorder))
    for attempt in (lambda: lesson.without("validation"), lambda: lesson.add(Trace())):
        try:
            attempt()
        except Exception as exc:
            print(type(exc).__name__ + ":", exc)

asyncio.run(main())
