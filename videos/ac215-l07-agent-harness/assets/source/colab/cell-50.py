act6 = build_act6(
    scenario="standard",
    model=MODEL,
    fixture=USE_FIXTURES,
)

with Recorder(DB_PATH) as recorder:
    act6_result = await act6.run(
        recorder,
        manager=review_order,
        progress=print,
    )
    act6_events = recorder.timeline(act6_result["run_id"])

print_composition_result(act6_result)

print("\n🔍 Was the requested tasting plan delivered?")
delivery_checks = [
    event["payload"] for event in act6_events
    if event["event_type"] == "delivery.checked"
]
if delivery_checks:
    for check in delivery_checks:
        print("Ready:", check["ready"])
        for error in check.get("errors", []):
            print("-", error)
else:
    print("No delivery check was recorded. Inspect the run status above.")
