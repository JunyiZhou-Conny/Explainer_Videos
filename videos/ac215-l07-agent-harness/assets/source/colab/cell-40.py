act4_interactive = build_act4(
    scenario="event-shortage", model=MODEL, fixture=USE_FIXTURES,
    memory_path=MEMORY_PATH, output_root=OUTPUT_ROOT,
    decision_source="human",
)
with Recorder(DB_PATH) as recorder:
    act4_interactive_result = await act4_interactive.run(recorder, reviewer=review_email, progress=print)
print_harness_result(act4_interactive_result)
show_chat(DB_PATH, act4_interactive_result["run_id"], title="Act 4 · interactive")
