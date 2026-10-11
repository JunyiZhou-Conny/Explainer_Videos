"""Replay Marco's current model-free feedback planner on the 40 saved first-search results (offline).
Usage: python -I replay_planner.py <marco_repo> <out.json>"""
import collections, json, sys
from pathlib import Path
repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "services/retrieve"))
from careonex_retrieve.feedback_expansion import plan_feedback_queries
from careonex_retrieve.retriever import Passage, PROGRAM_LABELS
d = json.loads((repo / "evaluation/universal_homecare_v2_full_prior.json").read_text(encoding="utf-8"))
reasons, rows = collections.Counter(), []
for case in d["cases"]:
    ps = [Passage(text=p["text"], heading_path=p.get("heading_path"), title=p.get("title"), program=p.get("program"),
                  source_url=p.get("source_url"), effective_date=None, score=None, s3_key=p.get("s3_key"))
          for p in case["runs"]["baseline_child"]["passages"]]
    plan = plan_feedback_queries(case["query"], ps, known_program_aliases=tuple(PROGRAM_LABELS))
    reasons[plan.reason] += 1
    rows.append({"id": case["id"], "query": case["query"], "reason": plan.reason, "extra_searches": plan.queries[1:],
                 "saved_run_queries": case["runs"]["feedback_child"]["queries_used"][1:]})
print(dict(reasons))
print("extra searches:", collections.Counter(len(r["extra_searches"]) for r in rows))
json.dump({"reasons": reasons, "cases": rows}, open(sys.argv[2], "w"), indent=1)
for r in rows[:8]:
    print(r["id"], "|", r["reason"], "|", r["extra_searches"][:1])
