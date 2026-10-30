# Rerun the selection cell after changing the evaluation settings.
if evaluation_selection != (EVAL_ACT, EVAL_N, EVAL_M, EVAL_CONTEXT):
    raise ValueError("Evaluation settings changed; rerun the golden-case selection cell first.")
evaluation_label = f"colab-act{EVAL_ACT}-{uuid4().hex[:12]}"


def evaluation_progress(message):
    # Full model/tool traces are saved; keep the notebook's progress output short.
    if message.startswith(("FIXTURE", "LIVE", "Case ")):
        print(message)


with Recorder(DB_PATH) as recorder:
    evaluation_report = await run_live_suite(
        recorder,
        evaluation_label,
        act=EVAL_ACT,
        case_ids=[case["case_id"] for case in selected_golden_cases],
        repeats=EVAL_M,
        context=EVAL_CONTEXT if EVAL_ACT == 2 else None,
        model=MODEL,
        fixture=EVAL_FIXTURES,
        output_root=OUTPUT_ROOT,
        progress=evaluation_progress,
    )
    evaluation_export = {
        "report": evaluation_report,
        "traces": {run["run_id"]: recorder.timeline(run["run_id"])
                   for run in evaluation_report["runs"]},
    }

evaluation_json = OUTPUT_ROOT / f"{evaluation_label}.json"
evaluation_json.write_text(json.dumps(evaluation_export, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nSaved complete results and recorded events: {evaluation_json}")
print(f"Experiment: {evaluation_label} · database: {DB_PATH}")
