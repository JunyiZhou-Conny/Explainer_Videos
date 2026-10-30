act5_sourcing = build_act5(
    scenario="event-shortage", model=MODEL, fixture=USE_FIXTURES,
    memory_path=MEMORY_PATH, output_root=OUTPUT_ROOT,
)
with Recorder(DB_PATH) as recorder:
    act5_sourcing_result = await act5_sourcing.run(recorder, reviewer=review_email, progress=print)
print_harness_result(act5_sourcing_result)
show_chat(DB_PATH, act5_sourcing_result["run_id"], title="Act 5 · event-shortage")
