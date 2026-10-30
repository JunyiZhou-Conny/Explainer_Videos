act2_enriched = build_act2(scenario=CONTEXT_SCENARIO, mode="enriched", model=MODEL)
with Recorder(DB_PATH) as recorder:
    act2_enriched_result = await act2_enriched.run(recorder, progress=print)
print_agent_result(act2_enriched_result)
show_chat(DB_PATH, act2_enriched_result["run_id"], title="Act 2 · enriched")
