# Exercises · AC215 L15 — ML workflows: deploy one model, then automate the pipeline on SageMaker

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real: the captures of
2026-11-05 (`assets/terminal/laptop/NN`: a fresh Docker 29.8.2 engine standing in for your laptop,
AWS CLI 2.34.63, **no AWS account**, keys either missing or obviously fake placeholders), and the
extra checks run for these exercises, listed with their logs in
[`assets/exercise-checks/`](assets/exercise-checks/README.md). **README A** is
`dlops-io/model-deployment-aws` at `077f4db`, **README B** is `dlops-io/ml-workflow-aws` at
`f165c6e`; `A:NN` means README A's line NN, and code paths are relative to each repository. Nothing
here touched an AWS account: whatever only AWS can show is quoted from the README's own recording
(`expected/…`, *recorded*), from the code or the SageMaker SDK's source, or from AWS's documentation,
and the answer says which. Versions are those at the time of recording; yours may be newer.

---

## Part A · The five questions from the end of the video

**Q1. Your laptop and the SageMaker endpoint both reach S3. Which identity does each use, and why
do Option 2's exported keys never reach the Part A container?**

<details><summary>Answer</summary>

- **Your laptop (and the CLI container)** signs every request with the **IAM user's access key**:
  the `model-deployment` user of A:21-30, whose keys `aws configure` writes to
  `~/.aws/credentials` (A:75). `docker-shell.sh:24` mounts that folder into the container
  (`-v ~/.aws:/home/app/.aws`), so `--prepare`'s bucket creation and upload are signed by the user.
  With no keys, the container's own check says so: `Unable to locate credentials` (`laptop/25:32`).
- **The endpoint** acts as the **execution role** `SageMakerExecutionRole` (A:32-44): `--deploy`
  hands its ARN to SageMaker (`role=role`, `cli.py:153`, from `SAGEMAKER_ROLE`), and SageMaker uses
  the role, with its `AmazonS3FullAccess` policy, to fetch `model.tar.gz` from your bucket. Your key
  never leaves your laptop.
- **Option 2:** the three `export` lines (A:80-82) set variables in your laptop's shell. A container
  sees only the variables `docker run` passes with `-e`, and `docker-shell.sh:25-27` passes three:
  `AWS_REGION`, `S3_MODELS_BUCKET_NAME`, `SAGEMAKER_ROLE`. The keys stay outside (exercise check
  C3 shows exactly that). Fix: use Option 1, or add `-e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY`
  to the `docker run` line.
</details>

**Q2. Name the three things `--deploy` creates. Which is the address, and which bills while nobody
calls it?**

<details><summary>Answer</summary>

One `tensorflow_model.deploy(...)` call (`cli.py:168-174`) creates, in this order:

1. **a SageMaker Model**, `model-mobilenetv2-train-base-True-v1`: the tarball's S3 URI, the AWS
   TensorFlow Serving image the SDK picks from `framework_version="2.13"`, and the role
   (`cli.py:151-159`). The READMEs call this "Model Registry"; the code creates a plain Model.
2. **an endpoint configuration**: which model, on which machine (`ml.m5.xlarge`), how many (1). The
   SDK names it after the endpoint (`sagemaker/session.py:6359` in 2.257.7: `"EndpointConfigName":
   name`), with one variant `AllTraffic`.
3. **the endpoint**, `model-mobilenetv2-train-base-True-v1-endpoint-<timestamp>` (`cli.py:164-167`):
   **the address** `--predict` calls.

**The endpoint bills**: one `ml.m5.xlarge` instance runs around the clock while the endpoint
exists, with zero traffic too ("serverless" here means no server for you to manage, not scale to
zero). The Model and the configuration are descriptions; the tarball they point to bills S3
storage. That is why `--delete` (and every clean-up list) removes the endpoint first.
</details>

**Q3. Where does preprocessing sit in Part A, and where in the Part B trainer? Give the lecture's
two reasons to put it in the model.**

<details><summary>Answer</summary>

- **Part A: in the client.** `--predict` opens the photo, converts it to RGB, resizes it to
  224 × 224 and divides by 255 (`cli.py:221-223`), then sends the floats as JSON (`:225`). The
  exported model's signature confirms it takes floats: `inputs['input']` `DT_FLOAT`
  `(-1, 224, 224, 3)`, `outputs['output_0']` `(-1, 4)` (`laptop/43:13-20`). `--prepare` changes the
  *format* (SavedModel, A:115), not the signature.
- **Part B: inside the model.** At the end of training, `task.py` defines `preprocess_image`
  (decode the JPEG, convert to float32, resize to 224 × 224, lines 277-281), wraps it with the model
  in `serving_function`, whose input is a batch of JPEG strings (`tf.TensorSpec([None], tf.string)`,
  lines 284-296), and saves it as `serving_default` (lines 314-318). Raw bytes in, one score per
  class out. (README B:7 gives this job to Model Deploy; the trainer does it.)
- **The lecture's reasons (slide 13):** *client-side brittleness*, every client (web app, phone
  app, notebook) must repeat the same steps exactly, and one that forgets `÷ 255` gets confident
  nonsense; and *one copy in the model* is easier to version and roll back. A bonus you can measure
  (B1): a bytes-in request carries the JPEG, about 7 KB in base64, instead of about 3 MB of JSON.
</details>

**Q4. Which lines make `ModelTraining` wait for `DataProcessor`? What would a literal
`s3://…/tfrecords` string change?**

<details><summary>Answer</summary>

`src/workflow/cli.py:265-268`: the training input is
`step_process.properties.ProcessingOutputConfig.Outputs["tfrecords"].S3Output.S3Uri` (lines
266-267), a **property reference** to the processor's declared output. In the definition it becomes
`{"Get": "Steps.DataProcessor.ProcessingOutputConfig.Outputs['tfrecords'].S3Output.S3Uri"}`
(`laptop/92:212`), and that `Get` is the edge.

With the literal `f"s3://{S3_BUCKET_NAME}/tfrecords"` the S3 path is the same, but the edge is gone:
the offline definition shows `ModelTraining references: -`, and the order that leaves is
`DataCollector` and `ModelTraining` together first, then `DataProcessor` and `CreateModel`, then
`DeployModel` (exercise check B6). SageMaker starts steps that depend on nothing at once (AWS's
documentation; not run here), so training would run **in parallel with the collector**, on whatever
old or missing data the prefix holds. To keep a literal path, add the edge by hand:
`depends_on=[step_process]` (the check shows `DependsOn: ['DataProcessor']` and the five-step order
again).
</details>

**Q5. Which two one-line fixes did today's tutorial need, and which one would an Apple-silicon Mac
not need?**

<details><summary>Answer</summary>

1. **The plain build line.** `docker-shell.sh:19` (Part A; also `data-processor/docker-shell.sh`
   and `model-training/docker-shell.sh`) builds `--platform=linux/arm64/v8`, "M1/2 chip macs use
   this line". On an Intel/AMD machine without emulation the first `RUN` fails with
   `exec /bin/sh: exec format error` (`laptop/20:36`); Docker Desktop on Intel Macs and Windows
   emulates it, slowly. Fix: use the script's own commented line 17,
   `docker build -t $IMAGE_NAME -f Dockerfile .` (`laptop/21`). **An Apple-silicon Mac does not
   need this one**: arm64 is its native platform.
2. **`sagemaker = "<3"`.** `Pipfile:10` (and `src/workflow/Pipfile:9`) says `sagemaker = "*"`, and
   neither image uses a lock, so the build resolves the newest release: SDK **3.13.1** on Python 3.9
   at the time of recording (`laptop/22`), a rewritten package without `sagemaker.tensorflow`,
   `serializers` or `get_execution_role`, so `cli.py` fails at import (`laptop/23`). `"<3"` stops at
   2.257.7 (exercise check B2). **Everyone needs this one**, Mac or not.

Careful on the Mac: images you push to ECR for SageMaker must be **amd64**, so build those with
README B:161's `--platform=linux/amd64/v2` line, even on Apple silicon.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. How big is one request?** Inside the Part A container (after the two fixes), predict how many
numbers `--predict` sends for one photo, and roughly how many bytes that is as JSON. Then measure it
with the client's own lines:

```bash
python -c "
import json, numpy as np; from PIL import Image
with Image.open('data/brie-1.jpg') as img:
    arr = np.asarray(img.convert('RGB').resize((224, 224)), dtype=np.float32) / 255.0
print(arr.size, len(json.dumps({'instances': [arr.tolist()]})))"
ls -l data/brie-1.jpg
```

<details><summary>Answer</summary>

224 × 224 × 3 = **150,528** numbers. Python writes each float32 value as a long decimal
(`0.8666666746139526`), about 21 bytes with its comma and space, so the body is **3,126,999 bytes**
for `brie-1.jpg` and 3,082,201 for `gouda-2.jpeg`, while the JPEGs themselves are 5,244 and 5,217
bytes (6,992 and 6,956 in base64): about 590 times smaller (exercise check B1, which runs
`cli.py:221-225` itself). That is still under the 6 MB request limit AWS documents for a real-time
endpoint (not checked here), but every photo pays for it in upload time. A bytes-in signature (the
Part B trainer, Q3) would carry the JPEG itself.
</details>

**B2. Star or pin?** In any Python 3.9 environment, predict which `sagemaker` version each line
would install, then run them (nothing is installed):

```bash
pip install --dry-run --no-deps "sagemaker"
pip install --dry-run --no-deps "sagemaker<3"
```

<details><summary>Answer</summary>

`sagemaker` → **3.13.1**, `sagemaker<3` → **2.257.7** (2026-11-05, exercise check B2; newer days
may differ). 3.13.1 is the last SDK 3 release that still installs on Python 3.9; on the workflow
image's Python 3.11 the same `"*"` gave 3.29.0 (`laptop/85:10`). `"*"` is a constraint with no upper
bound, so "the newest that installs" moves under you; `"<3"` keeps the major version the code was
written for. For a fully reproducible image, commit a lock and install from it: the training image
does (`pipenv sync`, sagemaker 2.250.0, `laptop/73:29`), the workflow image has a lock but never
copies it (`Dockerfile:40-42`, `laptop/87`).
</details>

**B3. Read the model's front door.** After `python cli.py --prepare` (with keys), predict the
signature's input dtype and shape and the number of outputs, and the top folder inside the tarball.
Then run, inside the container:

```bash
saved_model_cli show --dir artifacts/model-mobilenetv2_train_base_True.v1/1 --tag_set serve --signature_def serving_default
tar tzvf artifacts/model-mobilenetv2_train_base_True.v1/model.tar.gz
```

<details><summary>Answer</summary>

`inputs['input']`: `dtype: DT_FLOAT`, `shape: (-1, 224, 224, 3)`; `outputs['output_0']`:
`shape: (-1, 4)`; `Method name is: tensorflow/serving/predict` (`laptop/43:13-22`). So: floats in
(preprocessing is the client's job), **four** probabilities out, and the batch size is free (`-1`).
The tarball holds everything under `1/`: `1/saved_model.pb`, `1/variables/…`,
`1/fingerprint.pb`, `1/assets/` (`laptop/42`), because `cli.py:102-104` exports into a folder named
`1` ("SageMaker expects version number") and `:117` archives it as `arcname="1"`: TensorFlow Serving
finds a model by name, then version. Not re-run for these exercises (it needs the 4 GB image); the
captures are the evidence.
</details>

**B4. One flag or two?** Predict what each command does, then try them inside the containers
(without keys, each stops at its first AWS call, but you can see which function starts):

```bash
python cli.py --prepare --deploy                 # Part A container
python cli.py --test                             # Part A container
python cli.py --data_collector --data_processor  # workflow container
```

<details><summary>Answer</summary>

- Part A, `--prepare --deploy`: **only `prepare()`** runs. `main()` is an `if … elif …` chain
  (`cli.py:317-331`), so the first flag wins; it prints `Prepare model and save model to GCS Bucket`
  (the leftover GCP wording) and nothing about deploy.
- Part A, `--test`: **nothing at all.** The flag exists (`:355-358`, "Test deployment to Vertex
  AI") but `main()` never looks at it.
- Workflow, `--data_collector --data_processor`: **both**, in order. Its `main()` uses separate
  `if`s (`src/workflow/cli.py:334-350`): `CLI Arguments: Namespace(data_collector=True,
  data_processor=True, …)`, then the collector job, then `Data Processor` and the processor job.
  Without keys you never get that far: the module-level account lookup (`:31-32`) fails at import,
  for every flag (`laptop/90:60`, `98`).

Checked with each file's own parser and `main()`, the work functions replaced by prints (exercise
check B4).
</details>

**B5. Labels are folder names.** In the data processor, predict which label `gouda cheese` gets,
and what `python cli.py --prepare` does if your collector run had used
`--query "cheddar cheese"` or `"Brie cheese"`. Then predict the target the trainer
(`num_classes = 3`, `task.py:68`) gives a gouda photo.

<details><summary>Answer</summary>

The processor maps folder names to labels with exact keys (`src/data-processor/tfrecords.py:11-16`):
`parmigiano cheese` → 0, `gruyere cheese` → 1, `brie cheese` → 2, **`gouda cheese` → 3**. The
collector names each folder after its query, so any other spelling (`cheddar cheese`, even
`Brie cheese`) raises `KeyError` in `create_tf_example` (`:36`) during `--prepare` (exercise check
B5). Type the four queries exactly as README B:99 writes them.

With `num_classes = 3`, `tf.one_hot(3, 3)` is `[0, 0, 0]`: a gouda photo has **no target**, its
cross-entropy is 0 whatever the model predicts, so gouda is never learned, and the model has only
three outputs (`dense_1 (Dense) … (None, 3)`, `laptop/73:119`). With `num_classes = 4` the target is
`[0, 0, 0, 1]` and the loss is real (0.9163 for a made-up prediction; exercise check B5). Fix:
`num_classes = 4`, then re-run `sh package-trainer.sh` so the tarball carries the fix.
</details>

**B6. Reverse the list.** In a copy of `src/workflow/cli.py`, reverse
`steps=[step_collect, …, step_deploy_lambda]` (line 322). Predict the run order. Then put the
original list back and replace lines 266-267 with `f"s3://{S3_BUCKET_NAME}/tfrecords"`. Predict
again. (With keys, `python cli.py --pipeline` uploads the definition; to look without running
anything, print `sm_pipeline.definition()` instead of calling `upsert`.)

<details><summary>Answer</summary>

**Reversed list: no change.** The definition lists the steps in the new order
(`['DeployModel', 'CreateModel-CreateModel', 'ModelTraining', 'DataProcessor', 'DataCollector']`),
but every step carries the same reference, so the order is still DataCollector → DataProcessor →
ModelTraining → CreateModel → DeployModel. The list is a set of steps, not a schedule.

**Literal string: the chain breaks in two.** `ModelTraining` references nothing, so it can start
with `DataCollector`; `DataProcessor` and `CreateModel` follow, then `DeployModel`. Both results come
from the definition built offline with sagemaker 2.257.7 (exercise check B6); that SageMaker starts
independent steps together is AWS's documented behaviour, not run here. See Q4 for the fix
(`depends_on`).
</details>

**B7. Deploy twice, delete once.** Read `cli.py:163-167` and `:242-312` and predict, after
`--deploy`, `--deploy`, `--delete`: which endpoints, endpoint configurations and models are left?
Then check with `aws sagemaker list-endpoints`.

<details><summary>Answer</summary>

Each `--deploy` creates a **new** endpoint with a new timestamp; `endpoint_config.json` keeps only
the last name. `--delete`:

1. deletes the endpoint named in the JSON file (the **newer** one);
2. lists endpoint configurations and deletes **every** one whose name contains the model name: both
   (the SDK names each configuration after its endpoint);
3. deletes the model (the second deploy reused it: the SDK logs `Using already existing model`),
   then the tarball, then `endpoint_config.json`.

Left: **the older endpoint, still running and billing**, while its configuration and model are
already gone (exercise check B7 runs `delete()` itself against a recording stand-in). AWS documents
that deleting an endpoint configuration does not stop an endpoint that uses it; you must delete the
endpoint (not checked here). So `aws sagemaker list-endpoints` shows one endpoint: delete it with
`aws sagemaker delete-endpoint --endpoint-name <its name>` (your name, without the angle brackets,
C5).
</details>

---

## Part C · Debugging

**C1. `exec /bin/sh: exec format error`.** `sh docker-shell.sh` in `model-deployment-aws` pulls
`ubuntu:20.04`, then stops at `[ 2/14] RUN apt-get update …` with this error and
`ERROR: failed to build`. Nothing ran yet. What happened?

<details><summary>Answer</summary>

`docker-shell.sh:19` builds for `--platform=linux/arm64/v8`, so Docker pulls the **arm64** Ubuntu,
and an Intel/AMD Linux machine without emulation cannot execute its `/bin/sh` (`laptop/20:19`,
`36`). `set -e` stops the script before `docker run`. Fix: comment line 19 and use line 17,
`docker build -t $IMAGE_NAME -f Dockerfile .` (`laptop/21`); the processor and training scripts need
the same swap (`laptop/65`/`66`, `70`/`71`). On an Apple-silicon Mac the original line is right.
</details>

**C2. `ModuleNotFoundError: No module named 'sagemaker.tensorflow'`.** The image built fine, but
`python cli.py --prepare` fails at the import on line 21. In the workflow container the same thing
says `No module named 'sagemaker.processing'`. Nobody changed the code. Why, and what are two fixes?

<details><summary>Answer</summary>

`sagemaker = "*"` let the build install **SDK 3** (3.13.1 on Python 3.9, 3.29.0 on 3.11, at the time
of recording), a namespace package whose modules are `ai_registry`, `core`, `lineage`, `mlops`,
`serve`, `train`: none of the 2.x modules the code imports (`laptop/23`, `86`). No lock protected
you: Part A's Git ignores `Pipfile.lock` (`.gitignore:68`) and builds it fresh
(`Dockerfile:52-55`); the workflow Dockerfile copies only the `Pipfile` (`Dockerfile:40-42`). Fixes:
`sagemaker = "<3"` in the Pipfile (`laptop/24`, `88`), or pin exactly (`"==2.250.0"`, what the
workflow's committed lock says), or copy the committed lock into the image and `pipenv sync` from it.
Then rebuild.
</details>

**C3. Option 2, no credentials.** You chose Option 2, typed the three `export` lines with your real
keys, ran `sh docker-shell.sh`, and the banner still says `Unable to locate credentials`. Your keys
are correct. Why?

<details><summary>Answer</summary>

A container does not inherit your shell's variables; it gets only what `docker run` passes with
`-e`. `docker-shell.sh:25-27` passes `AWS_REGION`, `S3_MODELS_BUCKET_NAME` and `SAGEMAKER_ROLE`.
Exercise check C3 reproduces it with placeholder values: inside, those three, and no key; with
`-e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY` added, both arrive. And since you skipped
`aws configure`, the mounted `~/.aws` has no credentials file either. Fix: Option 1 (`aws configure`,
the README's recommended way), or add those two `-e` flags. Never write the keys into the script
(A:56-58).
</details>

**C4. An ECR URI that starts with a dot.** You pasted README B:169-173 and B:198 as written. The
terminal shows `export: '[YOUR': not a valid identifier`, `export: 'REGION]': not a valid
identifier`, then `ECR URI: .dkr.ecr.us-east-1.amazonaws.com/cheese-app-data-collector:latest`.
Which of these is harmless, which is fatal, and why did `aws ecr create-repository … || true` then
exit 0?

<details><summary>Answer</summary>

- The two `not a valid identifier` lines are **harmless but noisy**: `export` rejects the pasted
  note `[YOUR DEVELOPMENT REGION]` word by word, yet still sets `REGION=us-east-1` (exercise check C4:
  `export exit status: 1`, `REGION=us-east-1`). Paste only the value.
- The URI starting with `.` is **fatal**: `ACCOUNT_ID=$(aws sts get-caller-identity …)` came back
  empty because the account lookup failed (`laptop/80:10`, `11`): with no valid key there is no
  account id. Every later `docker tag`/`docker push` would aim at a registry that does not exist. Fix
  your keys (`aws sts get-caller-identity` must print your account) and run the block again.
- `|| true` turns any failure into success: the `create-repository` call failed
  (`UnrecognizedClientException … The security token included in the request is invalid`) and the
  line still exits 0 (`laptop/81`). It is there so that a second run, when the repository already
  exists, does not stop you; it also hides real errors. Read the message, not the exit code.
</details>

**C5. `syntax error near unexpected token 'newline'`.** You pasted README A:161,
`aws sagemaker delete-endpoint --endpoint-name <your-endpoint-name>`. What went wrong, and how do you
find the right name?

<details><summary>Answer</summary>

The angle brackets are placeholders, but the shell reads `<` as "take input from a file" and `>` as
"write output to a file", and then finds no file name before the end of the line: a syntax error
before `aws` even starts (`laptop/31`; exercise check C5, exit status 2). Type your own name without
brackets. Find the names with `aws sagemaker list-endpoints`, `aws sagemaker list-endpoint-configs`
and `aws sagemaker list-models`, then delete in that order: endpoint, configuration, model.
</details>

**C6. `PermissionError: [Errno 13] Permission denied: '/persistent/model'`.** On a Linux laptop, local
training (README B:136) trains one epoch, prints `Change model signature and save`, then fails with
this. The training data was read from `/persistent` a minute earlier. Why can it read but not write,
and what is the fix?

<details><summary>Answer</summary>

`../../../persistent-folder` did not exist when you first ran the collector's `docker-shell.sh`, so
Docker on Linux created it, **owned by root** (`laptop/61:9`). The collector and processor run as
root and wrote `dataset/` into it; the training container runs as `app` (uid 1000), which may read
the root-owned folders (`drwxr-sr-x`) but not create `model/` in them (`task.py:310-312`,
`laptop/73:146`). Fix: exit the container, then on your laptop
`sudo chown -R $USER ../../../persistent-folder` (works when your uid is 1000: `id -u`), or create
`persistent-folder` yourself before the first `docker-shell.sh`. Docker Desktop on a Mac maps the
mount to your user and avoids this. (The successful save after the fix was not captured; the code
writes `/persistent/model/1/`.)
</details>

**C7. The key check that never fires.** On Ubuntu, a classmate with **no** AWS keys runs
`sh docker-shell.sh` in `src/data-collector`. Instead of `AWS not configured. Run: aws configure`,
they see `docker-shell.sh: 18: [[: not found`, and the image builds anyway. Why?

<details><summary>Answer</summary>

On Debian and Ubuntu, `sh` is **dash**, not bash. The script is written for bash (`#!/bin/bash`):
dash does not know `[[ … ]]` (so the test fails and the `if` simply skips its body) and reads
`&> /dev/null` as "run in the background", then an empty redirect. The check never stops the
script: it builds and runs the container with `-e AWS_ACCESS_KEY_ID=` empty (exercise check C7, with
stand-in `aws` and `docker` programs). Under bash the same script stops with the intended message and
exit status 1. On Linux, run `bash docker-shell.sh`. On a Mac, `sh` behaves like bash, which is why
the README's `sh` works there.
</details>

**C8. `DeployModel` fails on the second pipeline run.** Your first `python cli.py --pipeline`
worked. Then you tested the components (README B:245-248), including `--model_deploy`. Now a new
`--pipeline` run fails at `DeployModel`. What changed?

<details><summary>Answer</summary>

`--model_deploy` created another endpoint, `cheese-app-endpoint-<8 characters>` (`model.py:170`). The
deploy Lambda decides between create and update with
`list_endpoints(NameContains="cheese-app-endpoint")` (`deploy_model_lambda.py:40-44`), and
`NameContains` matches any name that **contains** that string, so the new endpoint counts. If
`cheese-app-endpoint` itself is gone (you deleted it) but `cheese-app-endpoint-…` exists, the handler
calls `update_endpoint` on `cheese-app-endpoint`, which does not exist, and the step fails. Exercise
check C8 runs the handler against a recording stand-in: no endpoint → `create_endpoint`; only
`cheese-app-endpoint-ab12cd34` → `update_endpoint('cheese-app-endpoint')` → error (AWS's own wording
was not checked). If `cheese-app-endpoint` still exists, the update works and both keep billing. Fix:
delete the `--model_deploy` endpoints before the next `--pipeline` (and remember they bill).
</details>

**C9. `upsert` fails while creating the Lambda.** `python cli.py --pipeline` stops in `upsert`
with a `ValueError` carrying an AWS message about the Lambda **runtime**. Where does the runtime come
from, and how would you change it?

<details><summary>Answer</summary>

`Lambda(...)` in `src/workflow/cli.py:297-303` passes no `runtime`, so the SDK's default applies:
**`python3.8`** in sagemaker 2.257.7 (exercise check C9) as in 2.250.0. The SDK creates or updates the
function from your laptop while it builds the pipeline definition (`LambdaStep.to_request` →
`Lambda.upsert`), before anything runs in the cloud. AWS has deprecated the Python 3.8 runtime for
Lambda; whether your account can still create functions on it was **not checked** (no account).
If yours cannot: add `runtime="python3.12"` to `Lambda(...)` (the handler needs only `boto3`, which
every Python runtime includes). Each run also creates a new `sagemaker-deploy-model-lambda-<8
characters>` function (`cli.py:294-295`): delete them when you clean up.
</details>

**C10. `--predict` after a deploy in another folder.** With keys and a working endpoint, `--predict`
prints `Error: endpoint_config.json not found. Please deploy the model first.` and then five times
`Make sure the endpoint 'model-mobilenetv2-train-base-True-v1-endpoint' exists and is in service`.
The endpoint is `InService`. Why does it still fail?

<details><summary>Answer</summary>

`--deploy` writes `endpoint_config.json` into the current folder (`cli.py:183`), which is your clone
mounted at `/app`. If you deploy from another copy of the repo, or `--delete` already removed the file,
`--predict` falls back to `model-mobilenetv2-train-base-True-v1-endpoint` (`cli.py:197`), a name no
deploy ever creates: the real one ends `-endpoint-<timestamp>` (`:164-167`). Same message as in
`laptop/29:53`, `63` (there because no deploy ran at all). Fix: run `--deploy` and `--predict` from
the same folder, or write the real name into `endpoint_config.json`
(`aws sagemaker list-endpoints`). Also note that `image_files:` lists the first five photos the glob
found, not the five it sends: the sample is drawn at random, with repetition (`cli.py:216`;
`laptop/29:60-73` sends `brie-2` three times).
</details>

---

## Part D · Think

**D1. Endpoint or Cloud Run?** Lecture 14 served a container on Cloud Run; today a SageMaker
endpoint served a model. For each, what keeps billing at zero traffic, and when would you pick which
(slides 16–17)?

<details><summary>Answer</summary>

Cloud Run with minimum instances 0 and request-based billing scales to zero: nothing bills while
nobody calls. The endpoint as `cli.py` creates it keeps **one `ml.m5.xlarge` running 24/7**: here
"serverless" means no server for you to manage, not scale to zero. The lecture's rule of thumb: a
model endpoint (SageMaker, or Vertex AI online prediction) to serve a trained model, with versioning,
A/B variants and monitoring available (this tutorial uses none of them: one instance, one variant,
no monitoring); a general container service when the model is one part of a larger app, where you
build those extras yourself. For a class project that is called a few times a week, the always-on
endpoint is the expensive choice: delete it the same day.
</details>

**D2. Count the meters.** You followed both READMEs in order: `--deploy` twice and `--delete` once
(Part A); then `--pipeline` once and the four component flags once each (README B:233, 245-248),
and everything succeeded. Which endpoints are running now, on what?

<details><summary>Answer</summary>

Three:

1. Part A's **older** timestamped endpoint, `ml.m5.xlarge` (B7: `--delete` removed only the newer).
2. **`cheese-app-endpoint`**, `ml.m5.large`, created by the pipeline's `DeployModel` Lambda
   (`cli.py:310-312`); it stays up after the run.
3. **`cheese-app-endpoint-<8 characters>`**, `ml.m5.large`, from `--model_deploy` (`model.py:170-175`).

All bill around the clock. `aws sagemaker list-endpoints` shows them; delete each, then their
configurations and models, then check buckets, ECR repositories, the `sagemaker-deploy-model-lambda-…`
functions, the `cheese-pipeline` pipeline, the access keys and the two domains (the video's
clean-up card). From the code; not run (no account).
</details>

**D3. Does the cache know about your fix?** You fixed `num_classes = 4`, ran
`sh package-trainer.sh` again (same S3 name, `cheese-app-trainer.tar.gz`), and started
`--pipeline` again a week later. Caching is on for 30 days (`cli.py:165`). Will `ModelTraining`
train with your fix?

<details><summary>Answer</summary>

Quite possibly not. Per AWS's documentation on step caching (not checked here), SageMaker looks for a
previous successful run of the step with the same arguments, and it compares the arguments, not the
contents of the S3 files they point to. Your training step's arguments did not change: same
`source_dir` URI, same hyperparameters, same image, same input reference. So `DataCollector`,
`DataProcessor` and `ModelTraining` can all be served from cache, and the "new" model is last week's.
Make the change visible to the pipeline: turn caching off for that run (`enable_caching=False`),
or change an argument (for example upload the tarball under a new name and point `source_dir` at
it). Caching saves time and money only when "same arguments" really means "same work".
</details>

**D4. Same photo, same numbers?** Part 2's training data is made by the processor
(`tfrecords.py:26-33`: decode, resize, cast to uint8, later ÷ 255 in `task.py`); its serving
signature decodes, converts to float and resizes (`task.py:277-281`); Part A's client uses Pillow.
Predict which two agree, and how closely.

<details><summary>Answer</summary>

The **training records and the serving signature** agree to within **1/255** (max difference 0.0039,
from the uint8 cast in the processor): both use TensorFlow's decoder and resizer. **Pillow's resize**
differs noticeably: up to 0.07 on one photo, with about 42–45 % of values more than 1/255 apart
(exercise check D4, two sample photos). That is the lecture's client-side brittleness in numbers:
two correct-looking preprocessing paths give a model slightly different inputs. Putting
preprocessing in the model's signature means every client gets the same numbers, and the only
copy to keep in step with training is the one in the trainer, next to the code that made the
training data.
</details>

**D5. Keys, roles and least privilege.** Why does the README tell you never to put the access keys in
`docker-shell.sh` or an image, and what does the cloud side use instead? Part A's user also gets
`IAMFullAccess`; does `cli.py` need it?

<details><summary>Answer</summary>

A key in a script or an image travels with it: into Git history, onto Docker Hub or ECR, into every
copy, and anyone holding it acts as you until you deactivate it. The tutorial keeps the key in
`~/.aws` on your laptop (mounted at run time) and gives the cloud **roles**: the endpoint, the jobs
and the pipeline act as `SageMakerExecutionRole` / `CheeseAppSageMakerExecutionRole`, the Lambda as
`CheeseAppLambdaExecutionRole`, with short-lived credentials that never leave AWS. `cli.py` never
creates a role: it receives one (`SAGEMAKER_ROLE`), and what it needs from IAM is permission to hand
that role to SageMaker (`iam:PassRole`). `IAMFullAccess` lets the user create users and keys and
change any policy: far broader than the code needs. A narrower policy grants `iam:PassRole` on that
one role. (Which IAM actions the AWS-managed SageMaker policy already includes was not checked here:
look in the IAM console.)
</details>

**D6. What if the arrows were missing?** In the pipeline, delete the `outputs=[…]` list of the
collector step and the processor's `inputs=[…]`. Does the processor still get its data, and does it
still wait for the collector?

<details><summary>Answer</summary>

It may still find data, but it no longer waits. Inside a job, the collector writes
`/persistent/dataset/raw` and uploads `raw.zip` to the **bucket root** by a fixed name
(`src/data-collector/cli.py:55-65`); it never writes into the declared folder
`/opt/ml/processing/output`. The processor, finding no local `raw` folder, downloads `raw.zip` from
the bucket root itself (`src/data-processor/cli.py:41-49`). So the files travel **by name**, and the
declared input/output was mainly what drew the edge (B6). Without it, the processor can start at
the same time as the collector and read last run's `raw.zip`, or none (then `download_file` fails);
restore the order with `depends_on=[step_collect]`. As the video says, how the training step finds
its data on SageMaker was not verified without an account.
</details>
