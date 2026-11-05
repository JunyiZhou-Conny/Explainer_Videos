"""Capture-only helper for the L15 recording, NOT part of the tutorial.

Builds the SageMaker Pipeline that ml-workflow-aws/src/workflow/cli.py's own pipeline() defines and
prints its JSON definition (the DAG SageMaker would receive), WITHOUT an AWS account: the account
lookups answer with the placeholder account 000000000000, the default bucket and the Lambda
function ARN are placeholders, and Pipeline.upsert() prints the definition instead of sending it,
then stops (nothing is created, nothing is started).
Usage (inside the tutorial's workflow image, /app = src/workflow): python pipeline_offline.py
"""
import json
import sys

sys.path.insert(0, "/app")
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


def upsert(self, role_arn=None, **kwargs):
    print(json.dumps(json.loads(self.definition()), indent=2))
    raise SystemExit("[capture stub] Pipeline.upsert() and start() NOT sent: no AWS account in this recording")


Pipeline.upsert = upsert
import cli  # noqa: E402

cli.pipeline()
