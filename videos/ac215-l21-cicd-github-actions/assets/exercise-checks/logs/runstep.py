#!/usr/bin/env python3
"""Check-only helper (not the tutorial's). Prints the run: script of one step of a workflow file
with the ${{ }} expressions GitHub would substitute (needs.<job>.result, secrets.<NAME>) filled in.
Usage: runstep.py <workflow.yml> <job-id> <step-id> [needs.<job>.result=<value> | secrets.<NAME>=<value> ...]"""
import re, sys, yaml
wf = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
step = next(s for s in wf["jobs"][sys.argv[2]]["steps"] if s.get("id") == sys.argv[3])
vals = dict(a.split("=", 1) for a in sys.argv[4:])
def sub(m):
    e = m.group(1).strip()
    if e in vals: return vals[e]
    if e.startswith("secrets."): return ""        # a missing secret becomes the empty string
    raise SystemExit("no value for " + e)
print(re.sub(r"\$\{\{(.*?)\}\}", sub, step["run"]), end="")
