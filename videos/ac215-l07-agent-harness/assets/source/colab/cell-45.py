act5_stock = build_act5(
    scenario="stock-question", model=MODEL, fixture=USE_FIXTURES,
    memory_path=MEMORY_PATH, output_root=OUTPUT_ROOT,
)
with Recorder(DB_PATH) as recorder:
    act5_stock_result = await act5_stock.run(recorder, reviewer=review_email, progress=print)
print_harness_result(act5_stock_result)
show_chat(DB_PATH, act5_stock_result["run_id"], title="Act 5 · stock-question")
