"""Check-only helper (NOT part of the tutorial). Builds the JSON definition that
ml-workflow-aws/src/workflow/cli.py's own pipeline() would upsert, offline, for a variant of the file,
and prints what decides the run order: each step's references ("Get": "Steps.X...") and DependsOn.
Same offline method as assets/terminal/helpers/pipeline_offline.py: account lookups answer with the
placeholder 000000000000, the Lambda is not created, Pipeline.upsert() prints instead of sending.
Usage: python pipe_variants.py <variant>   (original | reversed | literal | literal+depends_on)
The variant is applied to a COPY of the tutorial file in /tmp (the mounted source stays read-only)."""
import json
import os
import shutil
import sys

variant = sys.argv[1]
src, work = "/wf", f"/tmp/wf-{variant.replace('+', '-')}"
shutil.rmtree(work, ignore_errors=True)
shutil.copytree(src, work)
path = os.path.join(work, "cli.py")
code = open(path).read()

LIST = "steps=[step_collect, step_process, step_train, step_create_model, step_deploy_lambda]"
REF = 'step_process.properties.ProcessingOutputConfig\n                .Outputs["tfrecords"].S3Output.S3Uri'
edits = []
if variant == "reversed":
    edits.append((LIST, "steps=[step_deploy_lambda, step_create_model, step_train, step_process, step_collect]"))
if variant.startswith("literal"):
    edits.append((REF, 'f"s3://{S3_BUCKET_NAME}/tfrecords"'))
if variant == "literal+depends_on":
    edits.append(('name="ModelTraining",', 'name="ModelTraining",\n        depends_on=[step_process],'))
for old, new in edits:
    assert code.count(old) == 1, old
    code = code.replace(old, new)
    print("edit:", " ".join(old.split())[:60], "->", " ".join(new.split())[:60])
open(path, "w").write(code)
sys.path.insert(0, work)
os.chdir(work)

import boto3  # noqa: E402

ACCOUNT = "000000000000"  # placeholder, not an AWS account


class PlaceholderSTS:
    def get_caller_identity(self, **kwargs):
        return {"Account": ACCOUNT, "Arn": f"arn:aws:iam::{ACCOUNT}:user/placeholder", "UserId": "PLACEHOLDER"}


_client, _session_client = boto3.client, boto3.Session.client
boto3.client = lambda name, *a, **k: PlaceholderSTS() if name == "sts" else _client(name, *a, **k)
boto3.Session.client = lambda self, name, *a, **k: PlaceholderSTS() if name == "sts" else _session_client(self, name, *a, **k)

import sagemaker  # noqa: E402
from sagemaker.lambda_helper import Lambda  # noqa: E402
from sagemaker.workflow.pipeline import Pipeline  # noqa: E402

sagemaker.session.Session.default_bucket = lambda self: f"sagemaker-us-east-1-{ACCOUNT}"
Lambda.create = lambda self: {"FunctionArn": f"arn:aws:lambda:us-east-1:{ACCOUNT}:function:{self.function_name}"}
Lambda.update = Lambda.create


def refs(node, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "Get" and isinstance(v, str) and v.startswith("Steps."):
                out.add(v.split(".")[1])
            refs(v, out)
    elif isinstance(node, list):
        for v in node:
            refs(v, out)
    return out


def upsert(self, role_arn=None, **kwargs):
    d = json.loads(self.definition())
    names = [s["Name"] for s in d["Steps"]]
    print("Steps in the definition, in list order:", names)
    deps = {}
    for s in d["Steps"]:
        r = sorted(refs(s.get("Arguments", {}), set()) | refs({k: v for k, v in s.items() if k != "Arguments"}, set()))
        deps[s["Name"]] = set(r) | set(s.get("DependsOn", []))
        print(f"  {s['Name']:<24} references: {r or '-'}  DependsOn: {s.get('DependsOn', '-')}")
    # the run order these edges allow: a step can start once every step it depends on is done
    wave, done = 1, set()
    while len(done) < len(names):
        ready = [n for n in names if n not in done and deps[n] <= done]
        print(f"  can start in wave {wave}: {sorted(ready)}")
        done |= set(ready)
        wave += 1
    raise SystemExit("[check stub] Pipeline.upsert() and start() NOT sent: no AWS account")


Pipeline.upsert = upsert
import cli  # noqa: E402

cli.pipeline()
