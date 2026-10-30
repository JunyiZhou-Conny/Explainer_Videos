act3_before = build_act3(scenario="pa-shipping-blocked", model=MODEL, fixture=USE_FIXTURES)
with Recorder(DB_PATH) as recorder:
    act3_before_result = await act3_before.run(recorder, manager=review_order, progress=print)
print_workflow_result(act3_before_result)
show_chat(DB_PATH, act3_before_result["run_id"], title="Act 3 · before")
