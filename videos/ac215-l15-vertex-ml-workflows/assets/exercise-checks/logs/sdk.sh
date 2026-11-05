# SDK checks (B4, B6, B7, C8, C9), run inside python:3.11-slim with --network none, using the venv
# setup.sh built (sagemaker 2.257.7, the version the fixed workflow image installs). Mounted read-only:
# /md = model-deployment-aws and /wf = ml-workflow-aws/src/workflow, both at the pinned commits
# (assets/source/). Placeholder keys only, and no network: nothing can reach AWS.
. /checks/lib.sh
export PATH=/venv/bin:$PATH PYTHONDONTWRITEBYTECODE=1 SAGEMAKER_SUPPRESS_V2_WARNING=1
export AWS_ACCESS_KEY_ID=PLACEHOLDER_NOT_A_REAL_ACCESS_KEY AWS_SECRET_ACCESS_KEY=PLACEHOLDER_NOT_A_REAL_SECRET_KEY_000000000000
export AWS_REGION=us-east-1 AWS_DEFAULT_REGION=us-east-1 S3_BUCKET_NAME=cheese-app-ml-workflow-demo S3_PACKAGE_URI=s3://cheese-app-ml-workflow-demo
export S3_MODELS_BUCKET_NAME=your-models-bucket-placeholder
cd /tmp
step 'python --version; python -m pip list 2>/dev/null | grep -i -E "^(sagemaker|boto3|botocore) "'
# C9: the runtime Lambda(...) gets when cli.py:297-303 passes none
step 'python -c "import inspect; from sagemaker.lambda_helper import Lambda; print(\"Lambda(...) runtime default:\", inspect.signature(Lambda.__init__).parameters[\"runtime\"].default)"'
# Q2/B7: what deploy(endpoint_name=...) names the endpoint configuration (SDK source, endpoint_from_production_variants)
step 'grep -n "config_options = {\"EndpointConfigName\": name" /venv/lib/python3.11/site-packages/sagemaker/session.py; grep -n "variant_name=\"AllTraffic\"" /venv/lib/python3.11/site-packages/sagemaker/session.py | head -1'
# B6 / Q4 / D3: the pipeline definition, as written and in three variants
for v in original reversed literal literal+depends_on; do
  step "cd /tmp && python /checks/pipe_variants.py $v 2>&1 | grep -v -E 'INFO|Warning|warn|migration|deprecat|^ *$|PipelineSession|Popping out|Using derived'"
done
# B4: one flag or several? Both CLIs, their own parser and main(), the work functions replaced by prints
step 'cd /tmp && python /checks/flags.py'
# B7: --delete after two --deploy runs (cli.py delete(), AWS clients replaced by a recording stand-in)
step 'cd /tmp && python /checks/delete_sim.py'
# C8: the deploy Lambda (deploy_model_lambda.py) with three sets of existing endpoints (recording stand-in)
step 'cd /tmp && python /checks/lambda_sim.py'
