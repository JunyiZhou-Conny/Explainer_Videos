available_golden_cases = golden_cases(EVAL_ACT)
if type(EVAL_N) is not int or not 1 <= EVAL_N <= len(available_golden_cases):
    raise ValueError(f"For Act {EVAL_ACT}, choose EVAL_N from 1 to {len(available_golden_cases)}.")
if type(EVAL_M) is not int or not 1 <= EVAL_M <= 20:
    raise ValueError("Choose EVAL_M from 1 to 20; use at least 2 to explore repeatability.")
if EVAL_ACT == 2 and EVAL_CONTEXT not in {"basic", "enriched"}:
    raise ValueError("For this lab, choose one context mode: basic or enriched.")

selected_golden_cases = available_golden_cases[:EVAL_N]
for index, case in enumerate(available_golden_cases, 1):
    print(f"\n{'✅ Selected' if index <= EVAL_N else '◻️ Available'} · {index}. {case['case_id']}")
    print("👤 Request:", case["request"])
    print("🎯 Expected:", case["expected"])
    print(f"Review decision if requested: {case['review_decision']}; vendor document: {case['document']}")

print(f"\nScheduled: {EVAL_N} requests × {EVAL_M} repeats = {EVAL_N * EVAL_M} runs")
print("Mode:", "SCRIPTED — tests the evaluation machinery" if EVAL_FIXTURES else "LIVE — measures model behavior")

evaluation_selection = (EVAL_ACT, EVAL_N, EVAL_M, EVAL_CONTEXT)
