"""Check-only helper (NOT part of the tutorial). C8: run ml-workflow-aws/src/workflow/
deploy_model_lambda.py's own lambda_handler with the event the DeployModel step sends
(cli.py:308-313), against a recording stand-in for the SageMaker client. The stand-in's
list_endpoints(NameContains=...) keeps the endpoints whose name CONTAINS the string (the documented
meaning of NameContains); update_endpoint on a name that does not exist raises a ClientError whose
message is the stand-in's own, not AWS's. Nothing calls AWS."""
import importlib.util

import boto3
from botocore.exceptions import ClientError

existing = set()


class StandIn:
    def create_endpoint_config(self, **kw):
        print(f"  create_endpoint_config(EndpointConfigName={kw['EndpointConfigName'][:27]}<time>, "
              f"ModelName={kw['ProductionVariants'][0]['ModelName']!r}, "
              f"InstanceType={kw['ProductionVariants'][0]['InstanceType']!r})")
        return {}

    def list_endpoints(self, NameContains, **kw):
        hits = sorted(e for e in existing if NameContains in e)
        print(f"  list_endpoints(NameContains={NameContains!r}) -> {hits}")
        return {"Endpoints": [{"EndpointName": e} for e in hits]}

    def update_endpoint(self, EndpointName, EndpointConfigName):
        print(f"  update_endpoint(EndpointName={EndpointName!r})")
        if EndpointName not in existing:
            raise ClientError({"Error": {"Code": "ValidationException",
                                         "Message": f"[stand-in] no endpoint named {EndpointName}"}}, "UpdateEndpoint")
        return {}

    def create_endpoint(self, EndpointName, EndpointConfigName):
        print(f"  create_endpoint(EndpointName={EndpointName!r})")
        existing.add(EndpointName)
        return {}


boto3.client = lambda service, *a, **k: StandIn()
spec = importlib.util.spec_from_file_location("deploy_model_lambda", "/wf/deploy_model_lambda.py")
lam = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lam)
lam.print = lambda *a, **k: None  # the handler's own response dumps are noise here
event = {"model_name": "pipelines-placeholder-CreateModel", "endpoint_instance_type": "ml.m5.large",
         "endpoint_config_name": "cheese-app-endpoint-config", "endpoint_name": "cheese-app-endpoint"}
for case in ([], ["cheese-app-endpoint"], ["cheese-app-endpoint-ab12cd34"]):
    existing.clear()
    existing.update(case)
    print(f"existing endpoints: {case or 'none'}")
    try:
        r = lam.lambda_handler(event, None)
        print("  -> returned", r["body"])
    except ClientError as e:
        print("  -> ClientError:", e.response["Error"]["Code"], "-", e.response["Error"]["Message"])
