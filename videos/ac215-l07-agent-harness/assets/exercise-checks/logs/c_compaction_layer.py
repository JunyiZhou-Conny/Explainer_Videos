# C5: the compaction demo without the Compaction layer (notebook form).
import asyncio
from acts.act4_harness import build_act4
from formaggio.operations.observability import Recorder


async def main():
    lesson = build_act4(fixture=True, demo_compaction=True, decision_source="fixture")
    print("layers:", [l.name for l in lesson.layers])
    async def review(_):
        return "decline"
    with Recorder("outputs/exercises.sqlite") as recorder:
        try:
            await lesson.without("compaction").run(recorder, reviewer=review)
        except ValueError as exc:
            print("ValueError:", exc)
        print("runs recorded:", recorder.query("SELECT COUNT(*) AS n FROM runs")[0]["n"])

asyncio.run(main())
