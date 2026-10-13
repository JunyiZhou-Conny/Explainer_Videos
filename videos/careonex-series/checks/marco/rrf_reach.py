"""Can a passage found ONLY by the extra search reach the top 5 under today's merge?
Uses Marco's own reciprocal_rank_fusion with the weights retrieve() passes ([1.5, 1.0]).
Usage: python -I rrf_reach.py <marco_repo>"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "services/retrieve"))
from careonex_retrieve.retriever import CANDIDATE_MULTIPLIER, MIN_CANDIDATES, Passage, reciprocal_rank_fusion


def P(name):
    return Passage(text=name, heading_path=None, title=None, program=None, source_url=None, effective_date=None,
                   score=None, s3_key=f"chunks/{name}.md")


top_k = 5
n = max(top_k * CANDIDATE_MULTIPLIER, MIN_CANDIDATES)
print("candidates per search:", n)
for first_len in (n, 5, 4, 3):
    first = [P(f"first{i}") for i in range(1, first_len + 1)]
    extra = [P(f"new{i}") for i in range(1, n + 1)]          # every extra hit is new (and admitted)
    merged = reciprocal_rank_fusion([first, extra], weights=[1.5, 1.0])[:top_k]
    print(f"first search returned {first_len:>2}: top 5 = {[p.text for p in merged]}")
print("best score of a new-only passage: 1/61 =", round(1 / 61, 5), "; 10th passage of the first search: 1.5/70 =", round(1.5 / 70, 5))
