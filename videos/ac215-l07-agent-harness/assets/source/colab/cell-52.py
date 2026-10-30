act6_approve = build_act6(
    scenario="manager-approval", model=MODEL, fixture=USE_FIXTURES,
    decision_source="test_option",
)
with Recorder(DB_PATH) as recorder:
    act6_approve_result = await act6_approve.run(recorder, manager=approve_review, progress=print)
print_composition_result(act6_approve_result)
show_chat(DB_PATH, act6_approve_result["run_id"], title="Act 6 · manager · approve")
