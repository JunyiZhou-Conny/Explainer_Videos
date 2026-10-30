act2_basic = build_act2(scenario=CONTEXT_SCENARIO, mode="basic", model=MODEL)
with Recorder(DB_PATH) as recorder:
    act2_basic_result = await act2_basic.run(recorder, progress=print)
print_agent_result(act2_basic_result)
show_chat(DB_PATH, act2_basic_result["run_id"], title="Act 2 · basic")
