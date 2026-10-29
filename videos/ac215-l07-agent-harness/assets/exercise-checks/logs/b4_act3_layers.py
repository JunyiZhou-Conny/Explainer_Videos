# B4: Act 3's removable layers on the scripted out-of-stock repair (fixture proposals, no model).
import asyncio
from acts.act3_workflow import build_act3
from formaggio.agents.layers import Trace
from formaggio.operations.observability import Recorder
from cli import print_workflow_result


async def main():
    lesson = build_act3(fixture=True, scenario="out-of-stock")
    bare = lesson.without("trace").without("budget")
    print("lesson layers:", [l.name for l in lesson.layers], "| bare layers:", [l.name for l in bare.layers])
    with Recorder("outputs/exercises.sqlite") as recorder:
        result = await bare.run(recorder, progress=print)
        print_workflow_result(result)
        kinds = [e["event_type"] for e in recorder.timeline(result["run_id"])]
        print("validation events:", kinds.count("cart.validated"), "| policy decisions:", kinds.count("policy.decision"),
              "| order.placed:", kinds.count("order.placed"))
    for attempt in (lambda: lesson.without("validation"), lambda: lesson.add(Trace())):
        try:
            attempt()
        except (ValueError, TypeError) as exc:
            print(type(exc).__name__ + ":", exc)

asyncio.run(main())
