act5_tasting = build_act5(
    scenario="tasting-plan", model=MODEL, fixture=USE_FIXTURES,
    memory_path=MEMORY_PATH, output_root=OUTPUT_ROOT,
)
with Recorder(DB_PATH) as recorder:
    act5_tasting_result = await act5_tasting.run(recorder, reviewer=review_email, progress=print)
print_harness_result(act5_tasting_result)
show_chat(DB_PATH, act5_tasting_result["run_id"], title="Act 5 · tasting-plan")
