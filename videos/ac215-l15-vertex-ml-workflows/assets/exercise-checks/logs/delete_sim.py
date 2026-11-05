"""Check-only helper (NOT part of the tutorial). B7: run model-deployment-aws/cli.py's own delete()
after two --deploy runs. The AWS clients are replaced by a recording stand-in that holds what two
deploys would have created (SDK 2.x names each endpoint configuration after its endpoint:
sagemaker/session.py endpoint_from_production_variants) and prints every call delete() makes.
Nothing calls AWS. Endpoint names use placeholder timestamps T1 < T2."""
import importlib.util
import json
import os
import sys

sys.path.insert(0, "/checks")
import stubs  # noqa: E402

stubs.install()
MODEL = "model-mobilenetv2-train-base-True-v1"
OLD, NEW = f"{MODEL}-endpoint-20261105000001", f"{MODEL}-endpoint-20261105000002"
state = {"endpoints": {OLD, NEW}, "configs": {OLD, NEW}, "models": {MODEL},
         "s3": {"model-mobilenetv2_train_base_True.v1/model.tar.gz"}}


class Paginator:
    def __init__(self, pages):
        self.pages = pages

    def paginate(self, **kw):
        return iter(self.pages(**kw))


class StandIn:
    def __init__(self, service):
        self.service = service

    def _log(self, operation, **kw):
        print(f"  [{self.service}] {operation}({', '.join(f'{k}={v!r}' for k, v in kw.items())})")

    def delete_endpoint(self, EndpointName):
        self._log("delete_endpoint", EndpointName=EndpointName)
        state["endpoints"].discard(EndpointName)

    def delete_endpoint_config(self, EndpointConfigName):
        self._log("delete_endpoint_config", EndpointConfigName=EndpointConfigName)
        state["configs"].discard(EndpointConfigName)

    def delete_model(self, ModelName):
        self._log("delete_model", ModelName=ModelName)
        state["models"].discard(ModelName)

    def get_paginator(self, op):
        self._log("get_paginator", op=op)
        if op == "list_endpoint_configs":
            return Paginator(lambda **kw: [{"EndpointConfigs": [{"EndpointConfigName": n} for n in sorted(state["configs"])]}])
        return Paginator(lambda **kw: [{"Contents": [{"Key": k} for k in sorted(state["s3"]) if k.startswith(kw["Prefix"])]}])

    def delete_objects(self, Bucket, Delete):
        self._log("delete_objects", Bucket=Bucket, Keys=[o["Key"] for o in Delete["Objects"]])
        for o in Delete["Objects"]:
            state["s3"].discard(o["Key"])


os.environ.setdefault("S3_MODELS_BUCKET_NAME", "your-models-bucket-placeholder")
spec = importlib.util.spec_from_file_location("md_cli", "/md/cli.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)
cli.boto3.client = lambda service, **kw: StandIn(service)

os.makedirs("/tmp/md", exist_ok=True)
os.chdir("/tmp/md")
json.dump({"endpoint_name": NEW, "region": "us-east-1"}, open("endpoint_config.json", "w"))
print("before: endpoints", sorted(state["endpoints"]))
print("endpoint_config.json names:", NEW)
cli.delete()
print("after:  endpoints", sorted(state["endpoints"]) or "none")
print("        endpoint configs", sorted(state["configs"]) or "none", "| models", sorted(state["models"]) or "none",
      "| S3 objects", sorted(state["s3"]) or "none")
print("endpoint_config.json still there:", os.path.exists("endpoint_config.json"))
