# Exercise checks · ac215-l15-vertex-ml-workflows (2026-11-05, 07:00–07:10 UTC)

What was run to verify [`exercises.md`](../../exercises.md), beyond the captures in `assets/terminal/`, which the
answers cite directly (`laptop/NN`, `expected/…`; provenance in [`ASSETS.md`](../../ASSETS.md)). Logs and the check
scripts are in [`logs/`](logs/). Every step in a log starts with its command (`$ …`) and ends with `[exit N]`, as in
`assets/terminal/run_steps.sh`. Where a step pipes into `grep`, `[exit N]` is the last command's status; steps that
matter print the real status themselves (`exit status: N`).

There was **no AWS account, no access key and no SageMaker**, as in the captures. Nothing here created a cloud
resource or called an AWS API: every check that runs tutorial code ran with `--network none`, with the AWS clients
replaced by a placeholder or a recording stand-in that prints what it was asked. The only network use was pip
(through the session proxy) in `setup.sh` and in B2's `--dry-run`. No log contains a person's name, a key, a real
account id or a real bucket: the values are the READMEs' placeholders, the capture's
`PLACEHOLDER_NOT_A_REAL_…` keys and the placeholder account `000000000000`.

## Setup (disposable; nothing from the repos ran on the host)

- Docker Engine 29.8.2 on the session machine. The tutorial files are the copies in `assets/source/` (unchanged at
  `model-deployment-aws` `077f4db` and `ml-workflow-aws` `f165c6e`, both re-checked with `git ls-remote` that day),
  mounted read-only. Two sample photos (`data/brie-1.jpg`, `data/gouda-2.jpeg`) were taken from a clone with
  `git show 077f4db:data/<name>` into the session scratchpad and mounted read-only; they are not in this repository.
- [`setup.sh`](logs/setup.sh) ([`setup.log`](logs/setup.log)) built two virtual environments in the session
  scratchpad, inside `python:3.11-slim` (Python 3.11.18, the workflow and training images' Python):
  `venv-sdk` with `sagemaker<3` → **sagemaker 2.257.7**, boto3 1.43.124 (what the workflow image installs after the
  `<3` fix, `laptop/90:35`), and `venv-tf` with **tensorflow-cpu 2.20.0 + keras 3.11.2** (the training image's
  TensorFlow and Keras, `laptop/73:28-30`) and pillow 13.0.0 (see Cleanup).
- [`lib.sh`](logs/lib.sh): the `step` function. [`stubs.py`](logs/stubs.py): lets a tutorial `cli.py` be imported
  without packages the check does not use (TensorFlow, Pillow, dask, scikit-learn): an absent one becomes an empty
  stand-in module; an installed one is used as is.
- [`sdk-run.sh`](logs/sdk-run.sh) → [`sdk.sh`](logs/sdk.sh) ([`sdk.log`](logs/sdk.log)): `python:3.11-slim`,
  `--network none`, `venv-sdk`.
  [`tf-run.sh`](logs/tf-run.sh) → [`tf.sh`](logs/tf.sh) ([`tf.log`](logs/tf.log)): the same with `venv-tf`.
  [`shell-run.sh`](logs/shell-run.sh) → [`shell-in.sh`](logs/shell-in.sh) ([`shell.log`](logs/shell.log)): C3 with
  the host's Docker CLI (`debian:12` running `env`), then `debian:12` (`sh` is dash), then B2 in `python:3.9-slim`.

## Checks

| exercise | what was run | result |
| --- | --- | --- |
| B1, Q3, D4 | [`req_size.py`](logs/req_size.py) ([`tf.log`](logs/tf.log)): `cli.py`'s own lines 221–225 on two sample photos, serialized as the SDK's `JSONSerializer` does (`json.dumps`, checked in `sagemaker/base_serializers.py`) | `(224, 224, 3) float32, 150,528 numbers`; JSON body **3,126,999** bytes (brie-1, 20.8 bytes per number) and 3,082,201 bytes (gouda-2); the JPEGs are 5,244 and 5,217 bytes (base64: 6,992 and 6,956): about 590 times smaller |
| B2, Q5 | `shell-run.sh`, last two steps: `pip install --dry-run --no-deps` on Python 3.9.25 | `sagemaker -> ['3.13.1']`; `sagemaker<3 -> ['2.257.7']` (the full resolve with dependencies is the capture `laptop/22`) |
| B4 | [`flags.py`](logs/flags.py) ([`sdk.log`](logs/sdk.log)): each CLI imported with its work functions replaced by prints, then its own `if __name__ == "__main__":` block | Part A `--prepare --deploy`: `Prepare model and save model to GCS Bucket`, only `prepare()`; Part A `--test`: no output at all; workflow `--data_collector --data_processor`: `CLI Arguments: Namespace(data_collector=True, data_processor=True, …)`, then both functions |
| B5, C6, D6 | [`labels.py`](logs/labels.py) ([`tf.log`](logs/tf.log)): `tfrecords.py`'s own `data_details` (read with `ast`); TensorFlow 2.20.0's `tf.one_hot` and Keras 3.11.2's `categorical_crossentropy` | `'gouda cheese' -> label 3`; `'cheddar cheese'` and `'Brie cheese'` → `KeyError`; `num_classes = 3`: one-hot of label 3 = `[0, 0, 0]`, its cross-entropy `0.0000`; with 4: `[0, 0, 0, 1]`, `0.9163` for the made-up prediction |
| B6, Q4 | [`pipe_variants.py`](logs/pipe_variants.py) ([`sdk.log`](logs/sdk.log)): `workflow/cli.py`'s own `pipeline()` built offline with sagemaker 2.257.7 (the capture helper's method), as written and in three edited copies | as written and with `steps=[…]` **reversed**: the same five references and the same run order (waves `DataCollector` → `DataProcessor` → `ModelTraining` → `CreateModel-CreateModel` → `DeployModel`), only the list order in the JSON changes; with a **literal** `f"s3://{S3_BUCKET_NAME}/tfrecords"`: `ModelTraining references: -`, wave 1 = `['DataCollector', 'ModelTraining']`; literal **+ `depends_on=[step_process]`**: `DependsOn: ['DataProcessor']`, the five waves again |
| B7, Q2, D2 | [`delete_sim.py`](logs/delete_sim.py) ([`sdk.log`](logs/sdk.log)): `cli.py`'s own `delete()` after two deploys (placeholder timestamps), AWS clients replaced by a recording stand-in | one `delete_endpoint` (the name in `endpoint_config.json`), both endpoint configurations deleted (their names contain the model name), the model, the tarball; **after: the older endpoint is still there**, `endpoint_config.json` removed. The SDK names each endpoint configuration after its endpoint (`session.py:6359`) |
| C3 | `shell-run.sh`, first step: Option 2's exports, then `docker-shell.sh`'s three `-e` flags | inside: `AWS_REGION`, `S3_MODELS_BUCKET_NAME`, `SAGEMAKER_ROLE`, and no key; with `-e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY` added, both keys arrive |
| C4 | [`shell-in.sh`](logs/shell-in.sh) ([`shell.log`](logs/shell.log)) | `export: '[YOUR': not a valid identifier`, `export: 'REGION]': …`, `export exit status: 1`, but `REGION=us-east-1`; an empty account id gives `ECR URI: .dkr.ecr.us-east-1.amazonaws.com/…`; `false \|\| true` → exit status 0 |
| C5 | same | `syntax error near unexpected token 'newline'`, exit status 2, before any program runs (as `laptop/31`) |
| C7 | same: `src/data-collector/docker-shell.sh` with no keys configured, `aws` and `docker` replaced by stand-in scripts, under `sh` (dash) and `bash` | dash: `docker-shell.sh: 18: [[: not found`, then the `docker build` and `docker run … -e AWS_ACCESS_KEY_ID= …` lines (the check is skipped), exit status 0; bash: `AWS not configured. Run: aws configure`, exit status 1 |
| C8 | [`lambda_sim.py`](logs/lambda_sim.py) ([`sdk.log`](logs/sdk.log)): `deploy_model_lambda.py`'s own handler with the event `DeployModel` sends, SageMaker client replaced by a recording stand-in (`NameContains` = substring, its documented meaning) | no endpoint → `create_endpoint('cheese-app-endpoint')`; `cheese-app-endpoint` exists → `update_endpoint`; only `cheese-app-endpoint-ab12cd34` exists → `list_endpoints` returns it, the handler calls `update_endpoint('cheese-app-endpoint')`, which does not exist (the stand-in's error, not AWS's wording) |
| C9 | `sdk.sh` step 2: `inspect.signature(Lambda.__init__)` in sagemaker 2.257.7 | `Lambda(...) runtime default: python3.8` |
| D4 | [`skew.py`](logs/skew.py) ([`tf.log`](logs/tf.log)): one JPEG through three of the repos' own preprocessing paths | training records vs the serving signature: max difference **0.0039** (= 1/255, the uint8 cast), 0 % beyond it; Part A's Pillow client vs the serving signature: max **0.0701** (brie-1) / 0.0588 (gouda-2), about 42–45 % of values more than 1/255 apart |

## Not run (and why)

- **Everything that needs an AWS account**: buckets, uploads, `--deploy`, `--predict` against an endpoint, the
  delete calls, ECR, Processing and Training jobs, the Lambda, `upsert`/`start` and the pipeline run. Answers about
  them cite the READMEs, the code at the pinned commits, the SDK source (sagemaker 2.257.7), the captures' honest
  errors and the README's own recording (`expected/md-predict-readme.txt`), and say so. The stand-ins in B7 and C8
  run the repos' own functions; what AWS itself would answer is not shown.
- **AWS's behaviour beyond the code**: that SageMaker runs steps without dependencies in parallel (B6, Q4), how step
  caching decides a hit (D3), whether a new `python3.8` Lambda can still be created in an account (C9), the
  InvokeEndpoint payload limit (B1), and that deleting an endpoint configuration or model leaves a running endpoint
  running (B7). These are taken from AWS's documentation and marked "per AWS's documentation, not checked here".
- **B3 (the signature, the tarball)**: needs the 4 GB `model-deployment-cli-aws` image and the downloaded release;
  the captures `laptop/42` and `laptop/43` answer it.
- **C1, C2, C5's AWS line, C6 (`PermissionError`)**: the captures `laptop/20`, `23`, `86`, `32`, `73` show them; not
  repeated. The trainer's save after the fix was not captured (ASSETS.md) and was not re-run here.

## Cleanup

Every check container ran with `--rm`. The two sample photos in the session scratchpad were deleted afterwards,
each by its path, and the images `python:3.11-slim` and `python:3.9-slim`, pulled for these checks, were removed
(`debian:12` was already on the machine and was kept). The two virtual environments (`venv-sdk`, `venv-tf`) stayed
in the session scratchpad for the coordinator to remove (the session's rules allow no whole-directory deletes by an
agent); `setup.sh` rebuilds them. Nothing was written outside the containers, the scratchpad and this folder.
