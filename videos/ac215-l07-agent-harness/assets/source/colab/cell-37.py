act3_after = build_act3(scenario="pa-shipping", model=MODEL, fixture=USE_FIXTURES)
with Recorder(DB_PATH) as recorder:
    act3_after_result = await act3_after.run(recorder, manager=review_order, progress=print)
print_workflow_result(act3_after_result)
show_chat(DB_PATH, act3_after_result["run_id"], title="Act 3 · after")
