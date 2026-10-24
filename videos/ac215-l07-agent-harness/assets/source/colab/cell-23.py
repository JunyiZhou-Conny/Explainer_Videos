# Agent + Harness

act1 = (
    Harness(build_agent, model=MODEL, scenario=SCENARIO)
    .add(Trace())
    .add(Budget(model_calls=8, tool_calls=20, seconds=120))
    .add(Context("basic"))
    .add(CartCheck())
)

with Recorder(DB_PATH) as recorder:
    act1_result = await act1.run(recorder, progress=print)

print_agent_result(act1_result)
