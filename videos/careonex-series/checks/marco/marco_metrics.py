"""Numbers E6 quotes from Marco's committed evaluation files (offline, no AWS).

1. A/B/C chunking: his own scorer (evaluation/chunking_retrieval_benchmark.py score) on his grades,
   plus which chunker had the best NDCG per question.
2. The saved 40-question feedback run: extra searches used, top-5 unchanged, latency, how many
   passages carry a grade.
Usage: python -I marco_metrics.py <marco_repo> <out.json>"""
import collections, json, statistics as st, sys
from pathlib import Path

repo, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo / "evaluation"))
from chunking_retrieval_benchmark import score  # noqa: E402

abc = score(repo / "evaluation/chunk_abc_prior_graded.json")
best = collections.Counter()
for case in abc["cases"]:
    nd = {v: m["ndcg_at_k"] for v, m in case["metrics"].items() if m["ndcg_at_k"] is not None}
    if not nd:
        best["no relevant passage"] += 1
        continue
    top = max(nd.values())
    winners = [v for v, x in nd.items() if abs(x - top) < 1e-9]
    best[winners[0] if len(winners) == 1 else "tie"] += 1

run = json.loads((repo / "evaluation/universal_homecare_v2_full_prior.json").read_text(encoding="utf-8"))
used = collections.Counter()
nq = collections.Counter()
same = 0
lat_b, lat_f = [], []
graded = total = 0
per_case = []
for case in run["cases"]:
    b, f = case["runs"]["baseline_child"], case["runs"]["feedback_child"]
    used[f["expansion_status"]] += 1
    nq[len(f["queries_used"])] += 1
    identical = [p["sha256"] for p in b["passages"]] == [p["sha256"] for p in f["passages"]]
    same += identical
    per_case.append({"id": case["id"], "extra_searches": len(f["queries_used"]) - 1, "top5_identical": identical,
                     "baseline_ms": b["latency_ms"], "feedback_ms": f["latency_ms"]})
    lat_b.append(b["latency_ms"])
    lat_f.append(f["latency_ms"])
    for arm in case["runs"].values():
        for p in arm["passages"]:
            total += 1
            graded += p.get("relevance") is not None


def p90(xs):
    return st.quantiles(xs, n=10)[-1]


# the grade grid E6 draws: question -> chunker -> grades of its top 5 (None = fewer than 5 returned)
abc_file = json.loads((repo / "evaluation/chunk_abc_prior_graded.json").read_text(encoding="utf-8"))
grid = {case["id"]: {v: [p["relevance"] for p in case["runs"][v]["passages"][:5]] + [None] * (5 - len(case["runs"][v]["passages"][:5]))
                     for v in ("legacy", "section", "hierarchical")} for case in abc_file["cases"]}

res = {
    "chunking": {"averages": abc["averages"], "best_ndcg_per_question": dict(best), "questions": abc["questions"],
                 "grades": grid},
    "feedback_run": {
        "kb": "hierarchical staging KB (C)", "questions": len(run["cases"]),
        "expansion_status": dict(used), "queries_per_search": dict(sorted(nq.items())),
        "top5_identical": same,
        "latency_ms": {"baseline": {"median": st.median(lat_b), "mean": round(st.mean(lat_b), 1), "p90": round(p90(lat_b), 1)},
                       "feedback": {"median": st.median(lat_f), "mean": round(st.mean(lat_f), 1), "p90": round(p90(lat_f), 1)}},
        "passages_graded": graded, "passages_total": total,
        "merge_weights": "equal (fusion scores 1/(60+rank))", "cases": per_case,
    },
}
out.write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps(res, indent=1))
