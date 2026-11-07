#!/usr/bin/env python3
"""Capture-only helper, not part of the tutorial.

Turns ONE job of the tutorial's `.github/workflows/ci.yml` into a bash script of `gstep` calls
for runner_job.sh, so that the local stand-in runner executes the workflow's own `run:` scripts,
verbatim, in the workflow's order. GitHub substitutes `${{ ... }}` expressions into a `run:`
script before bash sees it; this does the same for the expressions the file uses:
  github.sha, github.workspace     the commit under test, the runner's workspace path
  needs.<job>.result               the results of the stand-in jobs (passed as --needs)
  secrets.SLACK_WEBHOOK_URL        not set here, so "" (what GitHub substitutes for a missing secret)
`uses:` steps cannot run without GitHub; runner_job.sh records a stand-in for each (see ASSETS.md).
Usage: ci_plan.py <ci.yml> <job-id> <sha> <workspace> [--needs job=result ...]
"""
import re
import shlex
import sys

import yaml


def main(argv):
    path, job_id, sha, ws = argv[1:5]
    needs = {}
    rest = argv[5:]
    if rest and rest[0] == "--needs":
        for kv in rest[1:]:
            k, v = kv.split("=", 1)
            needs[k] = v
    wf = yaml.safe_load(open(path, encoding="utf-8"))
    job = wf["jobs"][job_id]

    def subst(text):
        def one(m):
            expr = m.group(1).strip()
            if expr == "github.sha":
                return sha
            if expr == "github.workspace":
                return ws
            mm = re.fullmatch(r"needs\.([\w-]+)\.result", expr)
            if mm:
                return needs.get(mm.group(1), "")
            if expr.startswith("secrets."):
                return ""
            raise SystemExit(f"unsupported expression in a run: script: {expr}")
        return re.sub(r"\$\{\{(.*?)\}\}", one, text)

    print(f"job_begin {shlex.quote(job_id)} {shlex.quote(job.get('name', job_id))}")
    for i, st in enumerate(job["steps"], 1):
        name = st.get("name", "")
        cond = str(st.get("if", ""))
        coe = "true" if st.get("continue-on-error") is True else "false"
        sid = st.get("id", "")
        if "uses" in st:
            kind, body = "uses", st["uses"]
        else:
            kind, body = "run", subst(st["run"]).rstrip("\n")
        print(" ".join(shlex.quote(x) for x in
                       ["gstep", f"{i:02d}", name, kind, cond, coe, sid, body]))
    print("job_end")


if __name__ == "__main__":
    main(sys.argv)
