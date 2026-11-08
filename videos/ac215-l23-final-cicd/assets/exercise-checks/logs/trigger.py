# Q5, Ponder 3, B7: the two conditions of ci_cd_aws.yml, read from the file at 5950118, applied to
# commit messages with the rule GitHub documents for contains() on strings ("case-insensitive
# substring"). This is a model of that documented rule, not GitHub: no Actions run was possible here.
import re, sys
wf = open(sys.argv[1]).read().split("\n")
job = re.search(r"contains\(github\.event\.head_commit\.message, '([^']+)'\)", wf[8]).group(1)    # line 9
step = re.search(r"contains\(github\.event\.head_commit\.message, '([^']+)'\)", wf[99]).group(1)  # line 100
print(f"line 9:   job runs if the message contains {job!r}")
print(f"line 100: last step runs if it also contains {step!r}\n")
def contains(s, sub): return sub.lower() in s.lower()
msgs = ["update readme", "fix typo /run-tests", "/run-deploy-app", "/RUN-DEPLOY-APP",
        "\\run-deploy-app", "deploy /run-deploy", "redeploy: /run-deploy-app-now"]
print(f"{'head_commit.message':32} {'job (build+push)':17} {'deploy step'}")
for m in msgs:
    j = contains(m, job); d = j and contains(m, step)
    print(f"{m:32} {'runs' if j else 'skipped':17} {'runs' if d else ('skipped' if j else '-')}")
