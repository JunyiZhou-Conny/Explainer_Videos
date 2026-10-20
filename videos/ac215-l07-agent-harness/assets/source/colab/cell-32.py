with Recorder(DB_PATH) as recorder:
    comparison_results = await run_act2(
        recorder, scenario=CONTEXT_SCENARIO, mode="both", model=MODEL,
        on_result=print_agent_result,
    )
    context_events = {result["run_id"]: recorder.timeline(result["run_id"])
                      for result in comparison_results}
context_results = {result["context"]["mode"]: result for result in comparison_results}
print_context_comparison(comparison_results, context_events)
for mode, result in context_results.items():
    show_chat(DB_PATH, result["run_id"], title=f"Act 2 · comparison · {mode}")
