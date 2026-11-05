# L15 · ML Workflows (Vertex AI lecture, AWS tutorials) — tutorial digest

- **Ed lesson:** https://edstem.org/us/courses/97373/lessons/166040/ (not opened; the lecture side is `SLIDES.md`).
- **Series decision (Conny):** L15 follows the **AWS** tutorials, not the GCP repos the course map lists. The lecture slides speak Vertex AI; they decide the *concepts*. The two AWS READMEs and our captures decide what the video *shows*. Section 7 maps one vocabulary onto the other.
- **Repo 1:** `dlops-io/model-deployment-aws`, branch `main`, commit `077f4dbc7b13ccef208c65a8e29489331261029e`, committed 2025-08-25 17:13:00 -0300 ("Merge pull request #1 from dlops-io/itamar/aws-initial-commit").
  - Re-checked with `git ls-remote` on 2026-11-05: `main` and `HEAD` = `077f4db`. Other refs: `itamar/aws-initial-commit` @ `1e34bff` and `itamar/new-trained-mobile-net` @ `00a4f08`, both already merged into `main`; tag `v1.0` @ `6ecc50b` (2025-08-21, "Initial commit: Add basic README for main branch").
  - The model weights come from that tag's GitHub **release** asset `mobilenetv2_train_base_True.zip` (`model-deployment-aws/cli.py:84-88`). Downloaded 2026-11-05 for inspection only: 18,090,351 bytes, five files (`.keras`, `.weights.h5`, `.json`, `_train_history.json`, `_model_metrics.json`). The `.keras` was saved by Keras 3.10.0. Its graph is MobileNetV2 → GlobalAveragePooling2D → Dense(128, relu) → Dense(**4**, softmax), input `[None,224,224,3]`, **no rescaling layer** (so the client's `/255` at `cli.py:223` is needed). `model_metrics.json` reports accuracy 0.724.
- **Repo 2:** `dlops-io/ml-workflow-aws`, branch `main`, commit `f165c6e17895d3d6c33a150d349f4b2649c807db`, committed 2025-08-19 08:50:13 -0400 ("Migrate ml-workflow from GCP to AWS"). `git ls-remote` on 2026-11-05: `main` = `HEAD` = `f165c6e`; no other branches, no tags. Same commit as the exam edition (`videos/ac215-l15-exam/`).
- **README sections covered (both READMEs, top to bottom)**
  - model-deployment-aws: Setup Environments (Clone, AWS Services to Enable, AWS Credentials → Create AWS IAM User, Create SageMaker Execution Role), Create S3 Bucket, Run Container (Security warning, Configure AWS Credentials Option 1/2, Update Configuration, Quick Start Commands, Prepare Model for Deployment, Upload & Deploy Model to SageMaker, Test Predictions), Clean Up Resources (Console, AWS CLI, CLI Script), Troubleshooting, Additional Resources.
  - ml-workflow-aws: Setup Environments (Clone, AWS Services, Create S3 Bucket, Setup AWS Credentials → Create IAM User, Create Access Keys, Install AWS CLI, Configure AWS CLI, Test Configuration, Create IAM Roles), Run Data Collector Container & Test CLI, Run Data Processor Container & Test CLI, Run Model Training Container & Test CLI (Local Training, Remote Training, Monitor), Build & Push Images (Docker Hub, Amazon ECR), Automate Running Data Collector Container, Cheese App: SageMaker Pipelines (Entire Pipeline, Test Specific Components).
- **Colab notebooks:** none for L15.
- **Third-party code read to check SDK behaviour** (downloaded from PyPI into the scratchpad, read only, never run): `sagemaker==2.250.0` (the version in `ml-workflow-aws/src/model-training/Pipfile.lock` and `src/workflow/Pipfile.lock`), `sagemaker==3.28.0` and its four sub-packages (the latest on PyPI on 2026-11-05), `botocore==1.40.11`, `difPy==4.2.1`. SDK paths below are prefixed `sagemaker-2.250.0/`.
- **What this sandbox cannot do:** there is no AWS account and no credentials. Every local step can be captured; every cloud step is shown up to its first real error, or from what the README documents (`expected`), or as a labelled illustration. Section 4 says which, step by step.

Paths are written from the folder that holds your clones. `ml-workflow-aws/src/workflow/cli.py:219` means line 219 of `src/workflow/cli.py` inside your `ml-workflow-aws` clone.

**Masking rule for every frame and file.** `model-deployment-aws/docker-shell.sh:8` hard-codes the tutorial author's own role ARN with a real-looking 12-digit account id. Never show that line unmasked: show `arn:aws:iam::<ACCOUNT_ID>:role/<ROLE_NAME>`. The README's own example (`model-deployment-aws/README.md:43`, `cli.py:143`) uses AWS's documentation placeholder account `123456789012`; for consistency show `<ACCOUNT_ID>` there too. Access keys, account ids and ARNs in any output are always placeholders.

---

## 1. What you build

The lecture has two parts, and so does the tutorial.

**Part A (model-deployment-aws).** You take an image classifier that was already trained (MobileNetV2, four cheeses, shipped as a `.keras` file in a GitHub release) and serve it from **Amazon SageMaker**:
- `python cli.py --prepare` creates your S3 bucket if needed, downloads the model, re-exports it as a TensorFlow **SavedModel** under a version folder `1/`, packs that folder into `model.tar.gz`, and uploads it to `s3://<bucket>/model-mobilenetv2_train_base_True.v1/model.tar.gz` (`model-deployment-aws/cli.py:66-123`).
- `python cli.py --deploy` creates a SageMaker **Model** (the S3 artifact plus AWS's prebuilt TensorFlow Serving 2.13 container), an **endpoint configuration** and an **endpoint** on one `ml.m5.xlarge` instance, and writes the endpoint's name to `endpoint_config.json` (`cli.py:126-185`).
- `python cli.py --predict` resizes and normalises five random sample images **on your laptop**, sends each as a JSON array of 224×224×3 floats (`{"instances": [...]}`), and prints the four probabilities and the label (`cli.py:188-239`).
- `python cli.py --delete` deletes the endpoint, its configuration, the model and the S3 artifact (`cli.py:242-312`).

Unlike the lecture's slide 13–14 and unlike the GCP repo, Part A does **not** move preprocessing into the model: the exported signature takes floats, and the client does the resizing. The tutorial's other repo does add the bytes-in signature (in the trainer, Part B).

**Part B (ml-workflow-aws).** You take the Cheese App's four stages (collect images from Bing, clean and convert them to TFRecords, train, deploy) and run them first by hand, each in its own container, then as one **SageMaker Pipeline** of five steps: `DataCollector` → `DataProcessor` → `ModelTraining` → `CreateModel` → `DeployModel` (`ml-workflow-aws/src/workflow/cli.py:157-328`).
- The two data steps are **Processing jobs** that run *your* images from *your* Amazon ECR registry.
- Training is a native SageMaker **Training job** that runs the trainer package from S3 inside AWS's TensorFlow 2.13 training container.
- `CreateModel` registers the trained artifact as a SageMaker Model; `DeployModel` is a **Lambda** function that creates or updates the endpoint `cheese-app-endpoint`.
- Your laptop only *defines* the pipeline (Python), *upserts* its definition to SageMaker and *starts* an execution. AWS-managed machines run every step.

The pipeline's edges come from **property references** (a step's input names another step's output property). But the code itself moves the data with `boto3` uploads to the bucket root (`raw.zip`, `clean.zip`, `tfrecords.zip`), not through the folders the steps declare (section 3.7 and section 10).

```
PART A — model-deployment-aws (every call goes out from your laptop; no ports are published)

 your laptop / Docker
 +---------------------------------------------+
 | container "model-deployment-cli-aws"         |  (1) HTTP GET .zip    +-------------------------------------+
 | ubuntu:20.04, python3.9 + pipenv,            | <-------------------- | github.com/dlops-io/model-deployment|
 | tensorflow 2.18.0, boto3, sagemaker (2.x)    |                       |  -aws releases/download/v1.0/       |
 | user app (uid 1000)                          |                       |  mobilenetv2_train_base_True.zip    |
 | volumes: ./ -> /app, ~/.aws -> /home/app/.aws|                       +-------------------------------------+
 | env: AWS_REGION, S3_MODELS_BUCKET_NAME,      |  (2) model.export -> artifacts/<BEST_MODEL>/1/ -> model.tar.gz
 |      SAGEMAKER_ROLE                          |  (3) s3.upload_file  +-------------------------------------+
 | $ python cli.py --prepare                    | -------------------> | S3 s3://<bucket>/model-mobilenetv2_ |
 | $ python cli.py --deploy                     |                      |  train_base_True.v1/model.tar.gz    |
 | $ python cli.py --predict                    |                      +------------------+------------------+
 | $ python cli.py --delete                     |  (4) TensorFlowModel(...).deploy        | model_data
 |                                              | -------------------> +------------------v------------------+
 |                                              |                      | SageMaker Model  (+ TF Serving 2.13 |
 |                                              |                      |  inference image, role)             |
 |                                              |                      | Endpoint config (same name as ep.)  |
 |                                              |  (5) predictor.predict JSON floats     v                   |
 |                                              | -------------------> | Endpoint  1 x ml.m5.xlarge, 24/7 $$ |
 |                                              | <------------------- |  {"predictions": [[p0,p1,p2,p3]]}   |
 +---------------------------------------------+                      +-------------------------------------+

PART B — ml-workflow-aws

 your laptop
 +---------------------------------------------------------------+
 | container "cheese-app-workflow" (python:3.11-slim, AWS CLI v2, |
 |  pipenv install: sagemaker + boto3, UNLOCKED)                  |
 |  volumes: ./ -> /app, docker.sock, ../data-collector,          |
 |  ../data-processor      env: AWS keys, AWS_REGION, S3_*        |
 | $ python cli.py --pipeline                                     |
 |   a) build 5 step objects; properties are placeholders         |
 |   b) Lambda(...) is created/updated in your account on upsert  |
 |   c) Pipeline("cheese-pipeline").upsert(role_arn) ; .start()   |----+ definition (JSON)
 +---------------------------------------------------------------+    |
                                                                       v
 SageMaker Pipelines (AWS-managed; identity = CheeseAppSageMakerExecutionRole; cache 30 days)
  +--------------------------------------------+
  | DataCollector  (Processing, ml.t3.medium)  |  image <ACCOUNT_ID>.dkr.ecr.<region>.amazonaws.com/
  |  python3 /app/cli.py --search --nums 50 ...|        cheese-app-data-collector:latest
  |  scrapes Bing -> boto3 -> s3://<b>/raw.zip |  declared output /opt/ml/processing/output -> s3://<b>/raw
  +----------------------+---------------------+
                         | property ref: Outputs["raw-data"].S3Output.S3Uri
  +----------------------v---------------------+
  | DataProcessor (Processing, ml.t3.medium)   |  image .../cheese-app-data-processor:latest
  |  --clean --prepare : raw.zip -> difPy ->   |  boto3 -> s3://<b>/clean.zip, s3://<b>/tfrecords.zip
  |  JPEG check -> TFRecords                   |  declared outputs .../output/clean, .../output/tfrecords
  +----------------------+---------------------+
                         | property ref: Outputs["tfrecords"].S3Output.S3Uri  (= s3://<b>/tfrecords)
  +----------------------v---------------------+
  | ModelTraining (Training, ml.m5.xlarge)     |  AWS tensorflow-training 2.13 py310 image
  |  package/trainer/task.py from              |  source_dir s3://<b>/cheese-app-trainer.tar.gz
  |  15 epochs, batch 16, bytes-in signature   |  output s3://<b>/model-output/<job>/output/model.tar.gz
  +----------------------+---------------------+
                         | property ref: ModelArtifacts.S3ModelArtifacts
  +----------------------v---------------------+
  | CreateModel (ModelStep)                    |  SageMaker Model + tensorflow-inference 2.13 image
  +----------------------+---------------------+
                         | property ref: ModelName
  +----------------------v---------------------+
  | DeployModel (LambdaStep)                   |  Lambda sagemaker-deploy-model-lambda-<8 chars>
  |  create endpoint config <name>-<MM-DD-HH-MM-SS> ; create or update endpoint "cheese-app-endpoint"
  |  (1 x ml.m5.large, 24/7 $$)                |  identity = CheeseAppLambdaExecutionRole
  +--------------------------------------------+

 Local "test each stage by hand" containers, run before the pipeline (README order):
  data-collector / data-processor / model-training images, each mounting
  ../../../persistent-folder -> /persistent and getting your access keys as env vars
```

## 2. Prerequisites and costs

**Accounts and local installs**
- An AWS account with billing. Both READMEs use region `us-east-1` (`model-deployment-aws/README.md:72`, `ml-workflow-aws/README.md:62`).
- Docker (Desktop or Engine), `git`.
- **The AWS CLI on your host** for Part B: every ml-workflow-aws `docker-shell.sh` runs `aws configure get ...` on the host before it builds (`ml-workflow-aws/src/data-collector/docker-shell.sh:13-26`). The README says how to install it (`ml-workflow-aws/README.md:51-53`). Part A only needs `aws configure` on the host for its recommended Option 1 (`model-deployment-aws/README.md:64-75`).
- No local Python is needed; everything else runs in containers.
- A Docker Hub account only if you build the step images yourself (`ml-workflow-aws/README.md:155-162`). The images must end up in **your own ECR** either way (see Build & Push below).
- W&B: `WANDB_KEY` is passed into the model-training and workflow containers (`ml-workflow-aws/src/model-training/docker-shell.sh:44`, `src/workflow/docker-shell.sh:43`) but no code reads it; `wandb==0.15.11` appears only in `src/model-training/package/setup.py:5`.

**AWS services the READMEs name**
- Part A: S3, SageMaker, IAM (`model-deployment-aws/README.md:12-16`).
- Part B: SageMaker AI ("Set up for single user (Quick setup)"), SageMaker Unified Studio ("Create domain"), S3, ECR, Lambda (`ml-workflow-aws/README.md:18-24`). The Unified Studio domain is only for *viewing* the pipeline (`README.md:234`); the code does not need it.

**Identities to create**

| What | README | Policies | Used by |
|---|---|---|---|
| IAM user `model-deployment` + access key | `model-deployment-aws/README.md:21-30` | `AmazonS3FullAccess`, `AmazonSageMakerFullAccess`, `IAMFullAccess` | your laptop, via `~/.aws` mounted into the container |
| Role `SageMakerExecutionRole` (trusted entity SageMaker) | `model-deployment-aws/README.md:32-44` | `AmazonSageMakerFullAccess`, `AmazonS3FullAccess` | the endpoint, through `SAGEMAKER_ROLE` (`docker-shell.sh:8`, `cli.py:131-132`) |
| IAM user `ml-workflow-user` + access key (CLI use case, download the .csv) | `ml-workflow-aws/README.md:35-49` | `AmazonS3FullAccess`, `AmazonSageMakerFullAccess`, `AmazonEC2ContainerRegistryFullAccess`, `AWSLambda_FullAccess` | your laptop, via `aws configure` + env vars |
| Role `CheeseAppSageMakerExecutionRole` (SageMaker - Execution) | `ml-workflow-aws/README.md:72-76` | `AmazonSageMakerFullAccess`, `AmazonS3FullAccess`, `AmazonEC2ContainerRegistryFullAccess` | every Processing/Training job and the pipeline itself; the **name is hard-coded** (`src/workflow/model.py:28`, `src/model-training/cli.py:33`) |
| Role `CheeseAppLambdaExecutionRole` (trusted entity Lambda) | `ml-workflow-aws/README.md:78-81` | `AWSLambda_FullAccess`, `AmazonSageMakerFullAccess` | the deploy Lambda; name hard-coded (`src/workflow/model.py:42`) |

Notes:
- The role **names** in ml-workflow-aws must be exactly as written: the code builds `arn:aws:iam::<account>:role/CheeseAppSageMakerExecutionRole` from your account id (`src/workflow/model.py:26-30`).
- In Part A the README names the role `SageMakerExecutionRole`, while `docker-shell.sh:8` ships a different role name (`model-deployment-sagemaker`) in the tutorial author's own account. Either name works if `SAGEMAKER_ROLE` holds *your* role's ARN.
- `IAMFullAccess` (`model-deployment-aws/README.md:28`) is not needed by the code: `cli.py` never creates a role; it only passes the ARN you give it. Least privilege says leave it off; the video can say so kindly.

**Values to edit before running**

Every `docker-shell.sh` hard-codes the tutorial's bucket. S3 bucket names are global (`model-deployment-aws/README.md:52`), so you **must** change them.

| File:lines | Variables |
|---|---|
| `model-deployment-aws/docker-shell.sh:7-9` | `S3_MODELS_BUCKET_NAME`, `SAGEMAKER_ROLE` (your role ARN), `AWS_REGION` (README `:85-90`) |
| `ml-workflow-aws/src/data-collector/docker-shell.sh:10` | `S3_BUCKET_NAME` |
| `ml-workflow-aws/src/data-processor/docker-shell.sh:10` | `S3_BUCKET_NAME` |
| `ml-workflow-aws/src/model-training/docker-shell.sh:9-10` | `S3_BUCKET_NAME`, `S3_PACKAGE_URI` (includes `s3://`) |
| `ml-workflow-aws/src/workflow/docker-shell.sh:8-9` | `S3_BUCKET_NAME`, `S3_PACKAGE_URI` |

The ml-workflow-aws README never says to edit these files; it only says "[REPLACE WITH YOUR BUCKET NAME]" (`README.md:30`). The local-training command also names the bucket on the command line (`README.md:136`).

**Buckets.** Part A: one models bucket (`README.md:46-52`; `--prepare` also tries to create it, `cli.py:71-82`). Part B: one bucket for everything — `raw.zip`, `clean.zip`, `tfrecords.zip`, `cheese-app-trainer.tar.gz`, `model-output/`, and the pipeline's declared `raw/`, `clean/`, `tfrecords/` prefixes.

**What costs money, and how to stop it**

| Resource | Created by | How it bills | Shut down |
|---|---|---|---|
| Endpoint, Part A | `model-deployment-aws/cli.py:168-174`: 1 × `ml.m5.xlarge`; a **new, timestamped endpoint on every `--deploy`** (`:164-167`) | per instance-hour, **24/7, even with zero traffic** | `python cli.py --delete` (only the endpoint named in `endpoint_config.json`), or the console / CLI commands in `README.md:154-164` |
| Endpoint `cheese-app-endpoint`, Part B | the pipeline's Lambda (`src/workflow/deploy_model_lambda.py:25-58`): 1 × `ml.m5.large`; later runs **update** it | 24/7 | `aws sagemaker delete-endpoint ...` (no delete command in ml-workflow-aws) |
| Endpoint `cheese-app-endpoint-<8 chars>` | every `python cli.py --model_deploy` (`src/workflow/model.py:170-175`): 1 × `ml.m5.large`, a **new endpoint each call** | 24/7 | same |
| Training jobs | `--train`, `--model_training`, the pipeline: 1 × `ml.m5.xlarge`, 15 epochs (`src/model-training/cli.py:53-68`, `src/workflow/cli.py:242-260`) | per second while running | end by themselves |
| Processing jobs | `--data_collector`, `--data_processor`, the pipeline: 1 × `ml.t3.medium` each | per second while running | end by themselves |
| Lambda functions | each `--pipeline` creates `sagemaker-deploy-model-lambda-<8 chars>` (`src/workflow/cli.py:294-303`), never deleted | per invocation (tiny); clutter | `aws lambda delete-function --function-name <name>` |
| S3, ECR | buckets, two ECR repositories | GB-month; small | empty and delete |

Cleanup commands from the README (`model-deployment-aws/README.md:160-164`), placeholders as written there:

```bash
aws sagemaker delete-endpoint --endpoint-name <your-endpoint-name>
aws sagemaker delete-endpoint-config --endpoint-config-name <your-endpoint-config-name>
aws sagemaker delete-model --model-name <your-model-name>
```

For Part B the same three commands apply; `aws sagemaker list-endpoints` lists what is running (not in either README). In Part A the endpoint configuration has the **same name as the endpoint**: the SDK names the config after the endpoint (`sagemaker-2.250.0/session.py`, `endpoint_from_production_variants`: `config_options = {"EndpointConfigName": name, ...}`).

## 3. Concepts this tutorial teaches

Concepts marked **[ANIMATE]** deserve a 3Blue1Brown-style mechanism animation. Each says which lecture slides it stands on (`SLIDES.md`).

### 3.1 SavedModel and its serving signature: where does preprocessing live? **[ANIMATE]** (slides 12–14)
- **Explanation.** A serving container does not run "a Keras model"; it runs a **SavedModel**: a graph, weights and named entry points (signatures). TF Serving calls the `serving_default` signature.
  - **Part A** loads the `.keras` model and calls Keras 3's `prediction_model.export(model_export_path)` (`model-deployment-aws/cli.py:107-109`). That exports the model *as is*: its signature takes a float tensor `[N,224,224,3]` in [0,1]. The client therefore resizes each image to 224×224, divides by 255 and sends the floats (`cli.py:221-225`). Preprocessing lives on the **client**.
  - **Part B's trainer** does what the lecture recommends. After training it defines `preprocess_image` (decode JPEG, convert to float32 in [0,1], resize to 224×224), maps it over a batch of strings in `preprocess_function`, chains it into the model call in `serving_function`, and saves the model with `signatures={"serving_default": serving_function}` (`ml-workflow-aws/src/model-training/package/trainer/task.py:276-318`). That artifact is "JPEG bytes in, probabilities out". Preprocessing lives on the **server**.
- **Version folder.** TF Serving expects `<model>/<version>/saved_model.pb`. Part A writes into `artifacts/<BEST_MODEL>/1` (`cli.py:102-104`) and tars it with `arcname="1"` (`:115-117`); the trainer writes `$SM_MODEL_DIR/1` (`task.py:304-307`), and SageMaker tars `/opt/ml/model` into `model.tar.gz` itself.
- **Mental model.** A SavedModel is a program with a front door. Part A's door says "send me pixels"; the trainer's door says "send me a photo".
- **Misconception.** "Re-saving the model in SavedModel format changes its signature." It doesn't; only an explicit `signatures=` (or a custom export) does. Part A's README step "Prepare the model in TensorFlow SavedModel format" (`README.md:115`) is a *format* change, not the lecture's *signature* change.
- **Visual.** Two pipes side by side. Left (Part A): JPEG → laptop gears (resize, ÷255) → a 224×224×3 cube of floats travels the wire → model. Right (trainer): JPEG bytes travel the wire → gears inside the model box → cube → model. Four bars come out of both.

### 3.2 SageMaker Model vs endpoint configuration vs endpoint **[ANIMATE]** (slides 11–12, 16–17)
- **Explanation.** Three separate API objects:
  - **Model**: where the artifact is (`model_data`, an S3 URI to `model.tar.gz`), which container serves it (the SDK resolves `framework_version="2.13"` to AWS's `tensorflow-inference` 2.13 image, `sagemaker-2.250.0/image_uri_config/tensorflow.json`), and which role reads it (`cli.py:151-159`). No machine runs yet.
  - **Endpoint configuration**: a list of *production variants* — which model, which instance type, how many instances, what weight. The Lambda writes one by hand: `"VariantName": "AllTraffic"`, `"InitialVariantWeight": 1`, `"InitialInstanceCount": 1`, `"InstanceType": endpoint_instance_type` (`src/workflow/deploy_model_lambda.py:25-36`).
  - **Endpoint**: the live HTTPS service, built from one configuration. `TensorFlowModel.deploy(...)` creates all three in one call (`cli.py:168-174`).
- **Updating.** To roll out a new model, create a *new* endpoint configuration and call `update_endpoint` on the existing endpoint (`deploy_model_lambda.py:47-52`). The endpoint name stays the same; SageMaker swaps the instances behind it. Several variants with different weights in one configuration are how A/B tests work (slide 16's "model versioning and A/B testing").
- **Mental model.** Model = recipe card; endpoint configuration = the staffing plan (which recipe, how many cooks, which kitchen size); endpoint = the restaurant's address with the kitchen running.
- **Misconception 1.** "Creating the model makes it callable." Only an endpoint is callable.
- **Misconception 2.** "This is the Model Registry." Both READMEs say "Model Registry" (`model-deployment-aws/README.md:7`, `ml-workflow-aws/README.md:7`), but neither repo registers a *model package* in SageMaker Model Registry; they create plain SageMaker Models (listed with the account's other models, not in a registry group). The lecture's registry box (slide 12) maps onto this step; the video can say kindly that the AWS code uses a plain Model.
- **Misconception 3.** "Deleting the model stops the bill." The endpoint is what bills; delete the endpoint (then the config and model).

### 3.3 The online prediction request **[ANIMATE]** (slide 13)
- **Explanation.** `sagemaker.Predictor(..., serializer=JSONSerializer(), deserializer=JSONDeserializer())` (`cli.py:200-205`) turns the Python dict into JSON and POSTs it to the endpoint's `invocations` URL; AWS's TF Serving container passes it to TensorFlow Serving's REST API. The body is `{"instances": [arr.tolist()]}` (`cli.py:225`): one instance = one 224×224×3 nested list of floats. The answer is `{"predictions": [[p0, p1, p2, p3]]}`; the code takes the argmax (`cli.py:231-232`) and maps it with a hard-coded dict (`cli.py:41-42`): `0 parmigiano, 1 gruyere, 2 brie, 3 gouda`.
- **Size.** One image is 224·224·3 = 150,528 numbers. Printed by Python's `json` as full-precision floats, that is a few megabytes of text per request. That is the "client-side brittleness" and cost the lecture warns about (slide 13), and the reason the trainer's bytes-in signature exists.
- **The other format (not exercised by the repos).** For a signature whose input is a string tensor (the trainer's `bytes_inputs`), TF Serving's REST convention wraps binary data as `{"b64": "<base64>"}`. Neither AWS repo calls the pipeline's endpoint, so no repo code shows this request. Say so if the video mentions it.
- **Misconception.** "Predictions come back with label names." You get floats; the label map is yours, and it must match the training order (section 10: the trainer's `num_classes = 3`).

### 3.4 Prebuilt framework containers: the runtime half of a model
- **Explanation.** SageMaker never runs a bare model; it runs a container image that loads it. The code never writes an image URI for TF: the SDK picks it from `framework_version` and `py_version`.
  - Serving: `TensorFlowModel(..., framework_version="2.13")` → `tensorflow-inference:2.13` (`model-deployment-aws/cli.py:154`, `src/workflow/cli.py:279`, `src/workflow/model.py:165`).
  - Training: `TensorFlow(..., framework_version="2.13", py_version="py310")` → `tensorflow-training:2.13` with Python 3.10 (`src/model-training/cli.py:59-60`, `src/workflow/cli.py:255-256`, `src/workflow/model.py:87-88`).
  - Processing: `Processor(image_uri=...)` runs *your* image from ECR (`src/workflow/cli.py:52-59`).
- **Version skew.** Part A exports with TensorFlow 2.18 / Keras 3 (`model-deployment-aws/Pipfile:12`) and serves with TF Serving 2.13. Newer TF writing, older TF reading is not guaranteed to work. The trainer avoids this on SageMaker (trains in the 2.13 container), but local training uses TF 2.20 (`src/model-training/Pipfile:12`). See section 10.
- **Mental model.** The artifact is a cartridge; the container is the console. The console must be new enough for the cartridge.

### 3.5 Pipeline steps: four kinds (slides 28, 34–37)
- **Explanation.** SageMaker Pipelines has typed steps. This pipeline uses four:
  - **ProcessingStep** with a `Processor(image_uri=..., entrypoint=["python3", "/app/cli.py"])` (`src/workflow/cli.py:170-197`): run *your* container with arguments. This is the KFP *container component* of the slides.
  - **TrainingStep** with a `TensorFlow` estimator (`:249-270`): a managed training job. There is no launcher step here: SageMaker Pipelines starts the training job *as* the step, so a failed job fails the step.
  - **ModelStep** with `model.create(instance_type="ml.m5.large")` (`:276-288`): creates the SageMaker Model. The console shows it as `CreateModel-CreateModel` (README image `images/sagemaker-pipeline-2.png`).
  - **LambdaStep** (`:297-315`): call a Lambda function with inputs. Here it does the deployment.
- **"Make the container callable" (slides 35–36).** The data-collector and data-processor images have exactly the lecture's two-mode entrypoint: no arguments → interactive bash; arguments → `exec "$@"` (`src/data-collector/docker-entrypoint.sh:4-8`). Note that SageMaker does not use it: `Processor(entrypoint=[...])` replaces the image's ENTRYPOINT with `python3 /app/cli.py`, and the job arguments are appended.
- **Misconception.** "Every step is a container I build." Only the two Processing steps run your images; training and serving use AWS's framework images plus your code and artifact.

### 3.6 The DAG comes from property references **[ANIMATE]** (slides 29–30, 34, 40)
- **Explanation.** While `pipeline()` runs on your laptop, nothing executes in the cloud. `step_collect.properties.ProcessingOutputConfig.Outputs["raw-data"].S3Output.S3Uri` (`src/workflow/cli.py:219-220`) is a **placeholder** for a value that will exist only after the collector's job runs. Using it as the processor's input creates the edge collector → processor. The same holds for `step_process.properties...Outputs["tfrecords"]...` into training (`:266-267`), `step_train.properties.ModelArtifacts.S3ModelArtifacts` into the model (`:277`), and `step_create_model.properties.ModelName` into the Lambda (`:309`).
- **Order.** `Pipeline(steps=[...])` (`:320-324`) is a set, not a schedule: SageMaker derives the order from the references (agrees with the exam edition, S07). An explicit `depends_on=[...]` would add an ordering-only edge; this repo does not use it.
- **Definition and run.** `sm_pipeline.upsert(role_arn=role)` (`:326`) sends the pipeline definition (JSON) to SageMaker, creating or updating the pipeline `cheese-pipeline`; `sm_pipeline.start()` (`:327`) starts an execution and returns at once; `:328` prints its ARN. Your terminal does not wait. This is the AWS counterpart of the slides' compile-to-YAML plus `PipelineJob.run()` (slides 29, 33).
- **Caching.** Every step has `CacheConfig(enable_caching=True, expire_after="30d")` (`:165`). A step whose arguments did not change reuses its previous result for 30 days. The collector's arguments never change, so a second run within 30 days does not scrape again.
- **Analogy.** A recipe where step 3 says "take the bowl from step 2": the reference is the arrow.
- **Misconception.** "The list order is the run order" — no; "the property is a string I can print" — no, it is a reference resolved at run time.

### 3.7 Where the data really flows **[ANIMATE]** (slides 20–21, 37)
- **Explanation.** Each step runs on a fresh machine; S3 is the shared state. The steps *declare* folders:
  - collector output `/opt/ml/processing/output` → `s3://<b>/raw` (`src/workflow/cli.py:189-195`);
  - processor input `.../raw` → `/opt/ml/processing/input`, outputs `/opt/ml/processing/output/clean` → `s3://<b>/clean` and `/opt/ml/processing/output/tfrecords` → `s3://<b>/tfrecords` (`:216-235`).

  But the step code never touches those folders. The collector writes `/persistent/dataset/raw.zip` and uploads it with `s3_client.upload_file(zip_file, S3_BUCKET_NAME, "raw.zip")` (`src/data-collector/cli.py:56-65`); the processor downloads `raw.zip` itself if `/persistent/dataset/raw` is missing and uploads `clean.zip` and `tfrecords.zip` to the bucket root (`src/data-processor/cli.py:41-49`, `:68`, `:95`). The declared folders stay empty; the real handoff is by **file name convention** in the bucket root.
- **Training input.** The training step's channel is the processor's declared `s3://<b>/tfrecords` (`:266-267`). The trainer looks for `/opt/ml/input/data/training/tfrecords.zip` and otherwise reads `train*`/`val*` files directly (`task.py:71-86`, `:147-148`). How the README's successful run (`images/sagemaker-pipeline-2.png`) found its data is not provable from the code alone: an S3 key prefix `tfrecords` also matches the key `tfrecords.zip` (SageMaker's `S3Prefix` is a key-name prefix), but where SageMaker places such a file inside the channel was not verified. Section 10 lists this as open.
- **Mental model.** The pipeline draws arrows between boxes; the boxes pass notes through a shared drawer (the bucket) by agreed file names.
- **Misconception.** "Declaring an output uploads my data." SageMaker uploads only what the code writes into the declared local folder.

### 3.8 Two identities: access keys on your laptop, roles in the cloud
- **Explanation.**
  - **Locally**, containers get the IAM *user's* access key: Part A through the mounted `~/.aws` (`model-deployment-aws/docker-shell.sh:24`); Part B through `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` read from your `aws configure` and passed with `-e` (`src/data-collector/docker-shell.sh:14-16`, `:37-39`). boto3 finds them automatically.
  - **In the cloud**, jobs run as an IAM *role*: the pipeline and its jobs as `CheeseAppSageMakerExecutionRole`, the Lambda as `CheeseAppLambdaExecutionRole`, the Part A endpoint as your `SAGEMAKER_ROLE`. The same `boto3.client('s3')` call inside the collector (`src/data-collector/cli.py:30`) then uses the role's temporary credentials. No key travels into an image.
  - `_resolve_role()` first tries `sagemaker.get_execution_role()`, which only returns a role when the caller already *is* a role (on a SageMaker notebook); on your laptop it fails and the code builds the ARN from your account id (`src/workflow/model.py:19-34`).
- **Misconception.** "Bake my key into the step image." Never; the role does that job. Also: the README's security warning (`model-deployment-aws/README.md:56-58`) applies to `docker-shell.sh` itself — it ships an ARN, not a key, but your edited copy must not gain one.

## 4. Step-by-step walkthrough

Conventions:
- `$` lines run on your **host**, in the folder given. `#` lines run in the shell `docker-shell.sh` opens.
- Commands are verbatim from the README. *(not in README)* marks our extra checks.
- **Capture plan** says what this sandbox can record: `live` (runs fully here), `live→error` (runs here up to its first real error, which is the honest frame), `expected` (README text), `illustration` (console clicks, drawn schematically).

### Part A — model-deployment-aws (README order)

**A1. Clone.** "Clone or download from here" (`README.md:9-10`) → `git clone https://github.com/dlops-io/model-deployment-aws` *(the README links the repo; the exact command is ours)*. Capture: live.

**A2. AWS services, IAM user, execution role, bucket** (`README.md:12-52`). Console only. Create user `model-deployment` with the three policies and an access key; create role `SageMakerExecutionRole` (trusted entity SageMaker, two policies) and copy its ARN; create a bucket with a unique name. Capture: illustration (field values from the README; ARN as `arn:aws:iam::<ACCOUNT_ID>:role/SageMakerExecutionRole`).

**A3. Credentials** (`README.md:60-83`).
- Option 1 (recommended): `aws configure` on the host (`:66-68`): Access Key ID, Secret Access Key, region (e.g. `us-east-1`), output `json`. This writes `~/.aws/credentials` and `~/.aws/config`, which the container mounts (`:75`, `docker-shell.sh:24`).
- Option 2: `export AWS_ACCESS_KEY_ID=...`, `export AWS_SECRET_ACCESS_KEY=...`, `export AWS_REGION=us-east-1` (`:80-82`). **Erratum:** `docker-shell.sh:22-28` does not pass `AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY` into the container (only `AWS_REGION`, `S3_MODELS_BUCKET_NAME`, `SAGEMAKER_ROLE`), so Option 2 alone leaves the container without credentials. Fix: use Option 1, or add `-e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY` to the `docker run`.
- Capture: `aws configure` is interactive and needs a real key → show the prompts with placeholder answers as illustration; the env-var lines can be typed live with placeholder values.

**A4. Update configuration** (`README.md:85-90`): edit `docker-shell.sh` — `S3_MODELS_BUCKET_NAME`, `SAGEMAKER_ROLE`, `AWS_REGION` (`docker-shell.sh:7-9`).
- **Platform** (not in README): line 19 builds `--platform=linux/arm64/v8` ("M1/2 chip macs use this line", `:18`). On an Intel/AMD machine, use the commented line 17 instead, or every `RUN` needs QEMU emulation (slow) or fails with `exec format error` where no emulator is installed.
- Capture: live (show the three lines with placeholders).

**A5. Build and run the container** (`README.md:96-99`): `chmod +x docker-shell.sh` then `sh docker-shell.sh`.
- **Under the hood:** `docker build` (`Dockerfile`): Ubuntu 20.04; AWS CLI v2 chosen by architecture (`Dockerfile:15-23`); docker-ce (`:26-35`, unused by this tutorial); `python3.9 python3-pip` and `pip install pipenv` (`:38-40`); user `app` uid 1000 (`:42-45`); `pipenv lock && pipenv sync` (`:55`). There is **no committed lock** (`Pipfile.lock` is git-ignored, `.gitignore:68`), so the versions are resolved at build time: `boto3`, `sagemaker`, `pillow`, `numpy`, `requests` unpinned, `tensorflow==2.18.0`, Python 3.9 (`Pipfile:8-17`). sagemaker 3.x needs Python ≥ 3.10 (PyPI metadata, 3.28.0), so on 3.9 the resolver can only pick a 2.x release. `docker run --rm -ti` mounts the repo on `/app` and `~/.aws` on `/home/app/.aws` (`docker-shell.sh:22-28`). No `-p`: nothing listens locally.
- **Entrypoint** (`docker-entrypoint.sh`): prints `Container is running!!!`, `Testing AWS connectivity...`, runs `aws sts get-caller-identity`, then `pipenv shell`. There is no `set -e`, so a failed identity check does not stop the shell.
- **You should see** (with credentials): your account's identity JSON (`UserId`, `Account`, `Arn` → mask), then a pipenv shell. Without credentials (this sandbox): the AWS CLI's "Unable to locate credentials" error, then the shell anyway.
- Capture: live→error (build with a capture-only Dockerfile copy that adds the proxy CA; say so in ASSETS.md).

**A6. Prepare** (`README.md:110-117`): `python cli.py --prepare`. README lists four actions: download from GitHub, SavedModel, `model.tar.gz`, upload.
- **Under the hood** (`cli.py:66-123`), in this order:
  1. `s3_client.create_bucket(Bucket=S3_MODELS_BUCKET_NAME)` (`:71-82`) — **before** anything else. This is not in the README's list. Only `BucketAlreadyExists` and `BucketAlreadyOwnedByYou` are caught; any other error (no credentials, access denied) stops the command here.
  2. Download and unzip the release asset into `./artifacts/` (`:84-88`; `artifacts/` is git-ignored, `.gitignore:33`).
  3. `tf.keras.models.load_model("./artifacts/mobilenetv2_train_base_True.keras")` (`:90-95`).
  4. `prediction_model.export(model_export_path)` into `./artifacts/model-mobilenetv2_train_base_True.v1/1` (`:98-112`; prints `Using Keras 3 export()`).
  5. Tar `1/` into `model.tar.gz` (`:115-117`), upload to `<BEST_MODEL>/model.tar.gz` (`:120-123`).
- **You should see:** `Prepare model and save model to GCS Bucket` (`cli.py:318`, a leftover from the GCP version), `Using Keras 3 export()`, TF's export messages, `Uploading model to s3://<bucket>/model-mobilenetv2_train_base_True.v1/model.tar.gz`, `Model uploaded successfully to S3`.
- **Check** *(not in README)*: `aws s3 ls s3://<bucket>/model-mobilenetv2_train_base_True.v1/`.
- Capture: live→error at step 1 (`create_bucket` without credentials). Steps 2–5 can be captured as an *extra* by calling the same code path without the bucket call — label it `extra`, never as the README command's output.

**A7. Deploy** (`README.md:119-129`): `python cli.py --deploy`. "typically 5-10 minutes" (`:127`).
- **Under the hood** (`cli.py:126-185`): `sagemaker.Session()`; role from `SAGEMAKER_ROLE` (else `get_execution_role()`, which fails on a laptop and prints the example ARN, `:135-145`); `TensorFlowModel(model_data=..., framework_version="2.13", name="model-mobilenetv2-train-base-True-v1")` (`:151-159`); endpoint name `model-mobilenetv2-train-base-True-v1-endpoint-<YYYYmmddHHMMSS>` in UTC (`:164-167`); `.deploy(initial_instance_count=1, instance_type="ml.m5.xlarge", ...)` (`:168-174`) waits until the endpoint is in service; writes `endpoint_config.json` (`:181-185`, git-ignored, `.gitignore:41`).
- **You should see:** `Deploy model`, `Deploying model to SageMaker endpoint...`, the SDK's progress dashes, `Model deployed successfully!`, `Endpoint name: ...`, `Endpoint configuration saved to endpoint_config.json`.
- Capture: live→error (no credentials/region). The success lines are `expected` from `cli.py` prints; the README shows no sample output for this step.

**A8. Predict** (`README.md:131-148`): `python cli.py --predict`.
- **Under the hood** (`cli.py:188-239`): read `endpoint_config.json` (if missing, print an error and fall back to a name without timestamp that never exists, `:194-197`); glob `data/*.jpg` then `data/*.jpeg` (all 8 samples); pick `min(5, 8) = 5` indices **with replacement** (`np.random.randint`, unseeded, `:216`), so repeats are normal; per image: RGB, resize 224×224, `/255.0`, send `{"instances": [arr.tolist()]}`, print result, argmax, label.
- **README sample output** (`README.md:136-148`) is **stale**: it shows *three* probabilities per image, while the deployed model has four outputs. Its labels also do not follow the code's map (index 0 is printed as `gouda`; in `cli.py:42` index 0 is `parmigiano`). Expect four numbers and labels from `parmigiano, gruyere, brie, gouda`. The model's own metrics say accuracy 0.724, so some labels will be wrong.
- Capture: live→error (the code catches the invoke error per image and prints `Error invoking endpoint: ...` and `Make sure the endpoint '...' exists and is in service`, `:237-239`).

**A9. Clean up** (`README.md:150-176`): console (SageMaker → Endpoints → Delete), the three `aws sagemaker delete-*` commands, or `python cli.py --delete`. The script deletes the endpoint from `endpoint_config.json`, every endpoint config whose name contains `model-mobilenetv2-train-base-True-v1`, the model, every S3 object under `model-mobilenetv2_train_base_True.v1/`, and the local `endpoint_config.json` (`cli.py:242-312`). It does **not** delete the bucket, and it only knows the *last* deploy's endpoint: earlier `--deploy` runs left other endpoints running. Capture: live→error. Troubleshooting (`README.md:178-197`): text only.

### Part B — ml-workflow-aws (README order)

**B1. Clone, services, bucket** (`README.md:15-30`). Bucket `cheese-app-ml-workflow-demo` → yours. Capture: illustration.

**B2. IAM user, access key, AWS CLI, configure** (`README.md:33-63`). User `ml-workflow-user` with four policies; access key for the CLI use case; download the .csv; install the AWS CLI (`brew install awscli` / `sudo snap install aws-cli --classic`); `aws configure` with region `us-east-1` and output `json`. Capture: illustration for the console; `aws --version` live *(not in README)*.

**B3. Test configuration** (`README.md:65-69`): `aws sts get-caller-identity` and `aws s3 ls`. Capture: live→error ("Unable to locate credentials").

**B4. IAM roles** (`README.md:71-81`): `CheeseAppSageMakerExecutionRole` (SageMaker - Execution; three policies) and `CheeseAppLambdaExecutionRole` (Lambda; two policies). The names must match the code exactly (section 2). Capture: illustration.

**B5. Data collector** (`README.md:88-100`): in `src/data-collector`, `sh docker-shell.sh`, then `python cli.py --search --nums 10 --query "brie cheese" "gouda cheese" "gruyere cheese" "parmigiano cheese"`; check the bucket for `raw.zip`.
- **docker-shell.sh** (`src/data-collector/docker-shell.sh`): reads your key and region from the host's AWS CLI (`:13-26`), builds `cheese-app-data-collector` with `--platform=linux/amd64` (`:31`), runs it with the repo on `/app`, `../../../persistent-folder/` on `/persistent` (a folder *next to your clone*, `:9`) and the three AWS variables plus `S3_BUCKET_NAME` (`:34-41`).
- **Image** (`Dockerfile`): `python:3.11-slim`, `pipenv install --system --deploy` from the committed `Pipfile.lock` (`:37-39`); entrypoint with two modes → bash.
- **cli.py** (`src/data-collector/cli.py`): for each query, `downloader.download_bing_images(...)` scrapes Bing's `images/async` page with a regex (`downloader.py:112-130`) and saves `Image_<n>.<ext>` under `/persistent/dataset/raw/<query>/`; then zips `raw/*/*` into `/persistent/dataset/raw.zip` with paths like `brie cheese/Image_1.jpg` (`cli.py:55-61`) and uploads it as `raw.zip` (`:65`).
- **You should see:** `CLI Arguments: Namespace(...)`, `S3_BUCKET_NAME: ...`, per query `Searching for: brie cheese`, `[%] Downloading Images to /persistent/dataset/raw/brie cheese`, `[!!]Indexing page: 1`, `[%] Indexed N Images on Page 1.`, `[%] Downloading Image #k from <url>`, `[%] File Downloaded !` (or `[!] Issue getting: ...`), `[%] Done. Downloaded 10 images.`, then `uploading file /persistent/dataset/raw.zip`.
- Capture: live→error. The scraping and zipping run here (through the proxy); the upload fails without credentials. Record how many links Bing returned on 2026-11-05.

**B6. Data processor** (`README.md:107-120`): in `src/data-processor`, `sh docker-shell.sh`, then `python cli.py --clean` (check `clean.zip`) and `python cli.py --prepare` (check `tfrecords.zip`).
- **Image:** `python:3.11-slim`; **no committed lock**: `pipenv lock && pipenv install --system --deploy` (`Dockerfile:27-29`) resolves `pandas`, `difpy`, `dask`, `boto3`, `scikit-learn` at build time with `tensorflow==2.13.1` (`Pipfile:8-14`). `docker-shell.sh:31` builds for `linux/arm64/v8` (the amd64 line is commented at `:32`).
- **--clean** (`src/data-processor/cli.py:37-68`): if `/persistent/dataset/raw` does **not** exist locally, download `raw.zip` from the bucket and unzip; otherwise use the local folder (which B5 already filled, since both containers mount the same `persistent-folder`). `cleanser.remove_duplicates` copies raw → clean and runs `difPy.build` + `difPy.search` per label, deleting lower-quality duplicates (`cleanser.py:7-32`); `verify_images` deletes files `tf.image.decode_jpeg` cannot decode (`cleanser.py:35-51`). Zip `clean/*/*` → `clean.zip`, upload.
- **--prepare** (`cli.py:69-95`): `tfrecords.create_tfrecords(clean, tfrecords)` — label from the folder name via `label_folders` (`tfrecords.py:11-16`: parmigiano 0, gruyere 1, brie 2, gouda 3), random 80/20 split (`:102-104`, unseeded), shards `train_000<n>.tfrecords` / `val_000<n>.tfrecords` built in parallel with dask (`:50-64`, `:108-130`); each record is the raw 224×224×3 `uint8` bytes plus an int64 label (`:26-47`). Zip as `tfrecords/<file>` → `tfrecords.zip`, upload.
- **You should see:** `S3_BUCKET_NAME: ...`, `Cleaning dataset`, `Labels: [...]`, `Processing label: ...`, difPy's progress and `Search Results:`, `Lower Quality Files:`, `uploading file /persistent/dataset/clean.zip`; then `Prepare dataset for training`, `Label Directories: [...]`, `Full size of the dataset: ...`, `train_xy count: ...`, `Creating shard: 0 ...`, `Total shards created: 1`, `uploading file /persistent/dataset/tfrecords.zip`.
- Capture: live→error (both commands run locally on B5's images; each fails at its upload).

**B7. Model training** (`README.md:126-145`): in `src/model-training`, `sh docker-shell.sh`; local training `python -m package.trainer.task --epochs=1 --batch_size=4 --bucket_name=cheese-app-ml-workflow-demo`; remote training `sh package-trainer.sh` then `python cli.py --train`; monitor under Training → Training jobs (job names start with `cheese-`).
- **Image:** `python:3.11-slim`, `pip install pipenv awscli` (AWS CLI **v1**, `Dockerfile:13`), user `app`, `pipenv sync` from the committed lock (`:26-28`: tensorflow 2.20.0, keras 3.11.2, sagemaker 2.250.0, boto3 1.40.11, numpy 1.26.4). Entrypoint prints `Container is running!!!` and runs `pipenv shell`. `docker-shell.sh:32` builds for arm64; `:8` defines `SECRETS_DIR` but never mounts it.
- **Local training** (`task.py`): not on SageMaker (`/opt/ml` absent, `:71`), so it uses `/persistent/dataset/tfrecords` (filled by B6) and downloads `tfrecords.zip` from `--bucket_name` only if that folder is missing (`:87-111`). It builds MobileNetV2 (ImageNet weights downloaded from the internet) + Dense(128) + Dense(`num_classes`) and trains with SGD (`:177-269`), then saves the bytes-in SavedModel to `/persistent/model/1` (`:308-318`). **`num_classes = 3`** (`:68`) while labels go up to 3 — see section 10.
- **Remote training:** `package-trainer.sh` tars `package/` into `trainer.tar.gz` and copies it to `$S3_PACKAGE_URI/cheese-app-trainer.tar.gz` (`package-trainer.sh:1-4`). `cli.py --train` builds a `TensorFlow` estimator (entry point `package/trainer/task.py` inside that tarball, `ml.m5.xlarge`, TF 2.13, py310, epochs 15, batch 16) and calls `fit(inputs="s3://<b>/tfrecords.zip", job_name="cheese-<8 chars>", wait=False)` (`cli.py:53-74`): it returns as soon as the job is submitted.
- **You should see (local):** `tensorflow version 2.20.0`, `Number of replicas: 1`, `TFRecords found at /persistent/dataset/tfrecords`, the model summary, one epoch of progress, `Training execution time (mins) ...`, `Change model signature and save`, `Model saved to: /persistent/model/1`, `Training Job Complete`.
- Capture: local training **live** (the one cloud-free success of Part B — or its real error; see section 10 on `tensorflow.python.keras`); `package-trainer.sh` live→error (tar lines, then the S3 copy fails); `cli.py --train` live→error.

**B8. Build & push images** (`README.md:152-203`). "This step has already been done for this tutorial" (`:153`) — but see the erratum: the pipeline pulls from **your** ECR (`src/workflow/cli.py:35-36`), so you must push both images to your own account.
- Docker Hub (`:155-162`): `docker login -u <USER NAME> -p <ACCESS TOKEN>`; `docker build -t <USER NAME>/<IMAGE_NAME> -f Dockerfile .`; on M1/2 Macs `docker build -t <USER NAME>/<IMAGE_NAME> --platform=linux/amd64/v2 -f Dockerfile .`; `docker push <USER NAME>/<IMAGE_NAME>`.
- ECR (`:167-199`): set `REGION`, `ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)`, `REPO`, `TAG=latest`, `ECR_URI`; then (1) `docker pull <YOUR_DOCKER_HUB_USERNAME>/$REPO:$TAG`, (2) `aws ecr create-repository ... || true`, (3) `aws ecr get-login-password ... | docker login --username AWS --password-stdin ...`, (4) `docker tag`, (5) `docker push "$ECR_URI"`, (6) `aws ecr list-images ... --output table`, (7) `echo "ECR URI: $ECR_URI"`. Repeat for both images (`:201-203`).
- **Literal paste trap:** `export REGION=us-east-1 [YOUR DEVELOPMENT REGION]` (`:169`) in bash prints ``export: `[YOUR': not a valid identifier`` and ``export: `REGION]': not a valid identifier`` and returns 1, though `REGION` is still set (tested in bash, 2026-11-05). Type `export REGION=us-east-1`.
- The images SageMaker runs must be **amd64**: build without the arm64 line, or with `--platform=linux/amd64`.
- Capture: `docker build` live; the `export` lines live (including the bracket error as a kind erratum); `ACCOUNT_ID=$(aws sts ...)` live→error (empty `ACCOUNT_ID`); create-repository, login, push: live→error or command only.

**B9. Workflow container and a standalone Processing job** (`README.md:210-224`): in `src/workflow`, `sh docker-shell.sh`, then `python cli.py --data_collector`; inspect under SageMaker AI → Processing → Processing jobs.
- **docker-shell.sh** (`src/workflow/docker-shell.sh`): builds `cheese-app-workflow` for amd64 (`:29`); mounts the Docker socket, the repo, and the two sibling stage folders (`:33-37`); passes the key, `AWS_REGION`, `S3_BUCKET_NAME`, `S3_PACKAGE_URI`, `WANDB_KEY` (`:38-43`).
- **Image** (`Dockerfile`): `python:3.11-slim`, AWS CLI v2 **x86_64 only** (`:22-25`), `pipenv install` with **only the Pipfile** copied (`:40-42`): the committed `Pipfile.lock` (sagemaker 2.250.0) is not used at build time, so pipenv resolves the newest `sagemaker`. On 2026-11-05 that is 3.28.0, whose package no longer contains `sagemaker/processing.py`, `sagemaker/workflow/`, `sagemaker/tensorflow/` or `sagemaker/lambda_helper.py` (they moved under `sagemaker.core`, `sagemaker.train` and others). `cli.py:13-22` imports the 2.x paths. **Prediction for the capture:** `import` fails before any AWS call; fix by pinning `sagemaker = "==2.250.0"` (or `<3`) in `Pipfile`, or by adding `Pipfile.lock` to the `ADD` line and using `pipenv sync`. Captures decide.
- **Entrypoint:** prints `Container is running!!!`, `AWS Region: ...`, `S3 Bucket: ...`, `Package URI: ...`, runs `aws sts get-caller-identity`, then `pipenv shell`.
- **Under the hood of `--data_collector`** (`src/workflow/cli.py:44-80`): at import, `boto3.client('sts').get_caller_identity()` fetches your account id (`:31-32`) to build the ECR image URIs (`:35-36`); `Processor(image_uri=DATA_COLLECTOR_IMAGE, role=..., instance_type="ml.t3.medium", entrypoint=["python3", "/app/cli.py"])`; `processor.run(arguments=["--search", "--nums","10", "--query", ...4 queries..., "--bucket", S3_BUCKET_NAME], outputs=[...], job_name="cheese-app-data-collector-<8 chars>", logs=True, wait=True)` streams the job's log.
- Capture: live→error (import error, or the credentials error at `cli.py:32`).

**B10. The pipeline** (`README.md:226-240`): `python cli.py --pipeline`; view it in SageMaker Unified Studio → Build → ML Pipelines. The README's two images show the five steps mid-run and all green.
- **Under the hood:** section 3.6. Prints `Defining SageMaker Pipeline`, possibly `Using derived SageMaker execution role: arn:aws:iam::<ACCOUNT_ID>:role/CheeseAppSageMakerExecutionRole` and `Using derived Lambda execution role: ...`, then `SageMaker Pipeline started: arn:aws:sagemaker:<region>:<ACCOUNT_ID>:pipeline/cheese-pipeline/execution/<id>`.
- Capture: live→error; the DAG picture is an `illustration` redrawn from the README images (never the screenshots).

**B11. Test specific components** (`README.md:243-248`): `python cli.py --data_collector`, `--data_processor`, `--model_training`, `--model_deploy`.
- `--data_processor` (`cli.py:84-131`): Processing job with `--clean --prepare`, `wait=True`.
- `--model_training` → `model.py:51-100`: like `model-training/cli.py --train` but with `wait=True` and `model_name` in the hyperparameters.
- `--model_deploy` → `model.py:103-178`: finds the newest `model-output/cheese-*/` folder, deploys `.../output/model.tar.gz` to a **new** endpoint `cheese-app-endpoint-<8 chars>` on `ml.m5.large`. It only sees jobs named `cheese-*` (standalone training), not the pipeline's training jobs.
- Capture: live→error each.

**B12. Clean up** *(not in the README)*: delete the endpoints (`cheese-app-endpoint`, every `cheese-app-endpoint-*`), their configs and models; the Lambda functions `sagemaker-deploy-model-lambda-*`; the pipeline (`aws sagemaker delete-pipeline --pipeline-name cheese-pipeline`); the ECR repositories; the bucket. Slide 41 ("DELETE!!") is the lecture's version of this step.

## 5. Code tour

```
model-deployment-aws/                 (main @ 077f4db)
  Dockerfile            ubuntu:20.04 + AWS CLI v2 + docker-ce + python3.9 + pipenv; USER app; pipenv lock && sync
  Pipfile               boto3, sagemaker, pillow, tensorflow==2.18.0, numpy, requests; python 3.9 (no lock in git)
  docker-shell.sh       bucket, role ARN (masked!), region; arm64 build; mounts ./ and ~/.aws
  docker-entrypoint.sh  aws sts get-caller-identity; pipenv shell
  cli.py                --prepare / --deploy / --predict / --delete   (--test is defined but does nothing)
  data/                 8 sample photos (2 per cheese; gouda-2 is .jpeg)
  images/serverless-model-deployment.png   the 5-step diagram (contains vendor logos: redraw, never show)

ml-workflow-aws/src/                  (main @ f165c6e)
  data-collector/   python:3.11-slim, committed lock; two-mode entrypoint; Bing scraper -> raw.zip
  data-processor/   python:3.11-slim, lock made at build; difPy dedupe + JPEG check -> clean.zip; TFRecords -> tfrecords.zip
  model-training/   python:3.11-slim, committed lock (TF 2.20, sagemaker 2.250.0); USER app; pipenv shell
    package/trainer/task.py   trains MobileNetV2, adds the JPEG-bytes signature, saves <model_dir>/1
    package-trainer.sh        tar package/ -> trainer.tar.gz -> $S3_PACKAGE_URI/cheese-app-trainer.tar.gz
    cli.py                    standalone SageMaker training job (wait=False)
  workflow/         python:3.11-slim, AWS CLI v2 (x86_64), pipenv install from Pipfile only (lock ignored)
    cli.py                    --data_collector / --data_processor / --model_training / --model_deploy / --pipeline
    model.py                  role helpers, model_training(), model_deploy()
    deploy_model_lambda.py    the Lambda handler: endpoint config + create/update endpoint
```

**Excerpts for code panels** (verbatim at the pinned commits; copy to `assets/source/` unchanged):

`model-deployment-aws/cli.py:106-117` — the export and the version folder:
```python
    # Export using Keras 3 export() if available, otherwise fall back to tf.saved_model.save
    if hasattr(prediction_model, "export"):
        print("Using Keras 3 export()")
        prediction_model.export(model_export_path)
    else:
        print("Using tf.saved_model.save()")
        tf.saved_model.save(prediction_model, model_export_path)

    # Create tar.gz archive for SageMaker
    model_tar_path = f"{local_model_dir}/model.tar.gz"
    with tarfile.open(model_tar_path, "w:gz") as tar:
        tar.add(model_export_path, arcname="1")
```

`model-deployment-aws/cli.py:151-174` — Model, then endpoint:
```python
    tensorflow_model = TensorFlowModel(
        model_data=model_data,
        role=role,
        framework_version="2.13",
        sagemaker_session=sagemaker_session,
        name=BEST_MODEL.replace(".", "-").replace(
            "_", "-"
        ),  # SageMaker naming requirements
    )
    ...
    predictor = tensorflow_model.deploy(
        initial_instance_count=1,
        instance_type="ml.m5.xlarge",
        endpoint_name=endpoint_name,
        serializer=JSONSerializer(),
        deserializer=JSONDeserializer(),
    )
```
(`...` stands for lines 160–167; show them or mark the gap.)

`model-deployment-aws/cli.py:221-228` — client-side preprocessing and the request:
```python
        with Image.open(img_path) as img:
            img = img.convert("RGB").resize((224, 224))
            arr = np.asarray(img, dtype=np.float32) / 255.0

        payload = {"instances": [arr.tolist()]}

        try:
            result = predictor.predict(payload)
```

`ml-workflow-aws/src/model-training/package/trainer/task.py:276-301` — the bytes-in signature (the lecture's slide 14, in this repo):
```python
# Preprocess Image
def preprocess_image(bytes_input):
    decoded = tf.io.decode_jpeg(bytes_input, channels=3)
    decoded = tf.image.convert_image_dtype(decoded, tf.float32)
    resized = tf.image.resize(decoded, size=(224, 224))
    return resized


@tf.function(input_signature=[tf.TensorSpec([None], tf.string)])
def preprocess_function(bytes_inputs):
    decoded_images = tf.map_fn(
        preprocess_image, bytes_inputs, dtype=tf.float32, back_prop=False
    )
    return {"model_input": decoded_images}


@tf.function(input_signature=[tf.TensorSpec([None], tf.string)])
def serving_function(bytes_inputs):
    images = preprocess_function(bytes_inputs)
    results = model_call(**images)
    return results


model_call = tf.function(model.call).get_concrete_function(
    [tf.TensorSpec(shape=[None, 224, 224, 3], dtype=tf.float32, name="model_input")]
)
```
and `:314-318`:
```python
tf.saved_model.save(
    model,
    ARTIFACT_URI,
    signatures={"serving_default": serving_function},
)
```

`ml-workflow-aws/src/data-collector/docker-entrypoint.sh:3-8` — the lecture's "callable container":
```bash
set -euo pipefail
if [[ $# -eq 0 ]]; then
  exec bash            # local interactive shell
else
  exec "$@"
fi
```

`ml-workflow-aws/src/workflow/cli.py:212-223` — a step whose input is another step's output property:
```python
    step_process = ProcessingStep(
        name="DataProcessor",
        processor=data_processor,
        job_arguments=["--clean", "--prepare", "--bucket", S3_BUCKET_NAME],
        inputs=[
            ProcessingInput(
                input_name="raw-data",
                source=step_collect.properties.ProcessingOutputConfig
                    .Outputs["raw-data"].S3Output.S3Uri,
                destination="/opt/ml/processing/input",
            )
        ],
```

`ml-workflow-aws/src/workflow/cli.py:262-270`, `:276-288`, `:305-315`, `:320-328` — training, model, Lambda step, build and start (quote as in the file).

`ml-workflow-aws/src/workflow/deploy_model_lambda.py:39-58` — create or update:
```python
    # Check if an endpoint exists and update or create it
    list_endpoints_response = sm_client.list_endpoints(
        SortBy="CreationTime",
        SortOrder="Descending",
        NameContains=endpoint_name,
    )
    print(f"list_endpoints_response: {list_endpoints_response}")

    if len(list_endpoints_response["Endpoints"]) > 0:
        print("Updating Endpoint with new Endpoint Configuration")
        update_endpoint_response = sm_client.update_endpoint(
            EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name
        )
        print(f"update_endpoint_response: {update_endpoint_response}")
    else:
        print("Creating Endpoint")
        create_endpoint_response = sm_client.create_endpoint(
            EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name
        )
        print(f"create_endpoint_response: {create_endpoint_response}")
```

`ml-workflow-aws/src/data-collector/cli.py:63-65` and `src/data-processor/cli.py:93-95` — the real data handoff:
```python
        # Upload to S3 bucket
        print("uploading file", zip_file)
        s3_client.upload_file(zip_file, S3_BUCKET_NAME, "raw.zip")
```
```python
        # Upload to S3 bucket
        print("uploading file", zip_file)
        s3_client.upload_file(zip_file, S3_BUCKET_NAME, "tfrecords.zip")
```

**Small facts worth a caption**
- `model-deployment-aws/cli.py:32`: `BEST_MODEL = "model-mobilenetv2_train_base_True.v1"`; the SageMaker model name is that string with `.` and `_` replaced by `-` (`:156-158`, `:264`).
- `model-deployment-aws/cli.py:337`, `src/data-processor/cli.py:103`: both parsers are titled `"Data Collector CLI"` (copy-paste leftovers); `model-deployment-aws/cli.py:346-358` help texts say "Vertex AI".
- `src/workflow/cli.py:66` vs `:185`: standalone collector job scrapes 10 images per query, the pipeline 50.
- `src/workflow/deploy_model_lambda.py:21`: the endpoint config name gets a `-%m-%d-%H-%M-%S` suffix, so each run makes a new config.

## 6. Gotchas and common errors

1. **Hard-coded architecture flags.** `model-deployment-aws/docker-shell.sh:19`, `src/data-processor/docker-shell.sh:31`, `src/model-training/docker-shell.sh:32` build `linux/arm64/v8`; `src/data-collector/docker-shell.sh:31` and `src/workflow/docker-shell.sh:29` build `linux/amd64`. On the "wrong" machine each build is emulated (slow) or fails with `exec format error` without QEMU. The workflow image can only be amd64 anyway: its Dockerfile downloads the x86_64 AWS CLI (`src/workflow/Dockerfile:22`). Images for SageMaker must be amd64.
2. **`sh docker-shell.sh` on Linux skips the credential check.** On Debian/Ubuntu `sh` is dash, which does not know `[[` and parses `&>` differently. Tested on 2026-11-05 with the same `if` structure as `src/data-collector/docker-shell.sh:13-26`: under dash the script prints `[[: not found` and goes on to build; under bash it stops with the intended message. On macOS `sh` is bash, so the README's command works as intended there. On Linux, run `bash docker-shell.sh`.
3. **Option 2 credentials never reach the Part A container** (`model-deployment-aws/docker-shell.sh:22-28`); see A3.
4. **Region variable.** boto3 reads the region from `AWS_DEFAULT_REGION` or `~/.aws/config`, not from `AWS_REGION` (`botocore-1.40.11/configprovider.py:56`). Part A works because `~/.aws` is mounted; ml-workflow-aws's collector and processor pass `AWS_DEFAULT_REGION`, and the workflow/training code passes `region_name=AWS_REGION` explicitly where it builds sessions. Plain `boto3.client('sts')`/`boto3.client('s3')` calls without a region (`src/workflow/cli.py:31`, `model.py:114`) are where a "You must specify a region" error would show up if your setup differs.
5. **Unpinned dependencies.** `model-deployment-aws` (no lock in git, `.gitignore:68`), `src/data-processor` (no lock) and `src/workflow` (lock exists but is not copied before `pipenv install`, `Dockerfile:40-42`) resolve versions at build time. The workflow one is the dangerous case: today it resolves `sagemaker` 3.x and the 2.x imports fail (B9).
6. **Stale local data.** `src/data-processor/cli.py:41` and `:73` only download from S3 when the local folder is missing; `task.py:96` likewise. Because all stage containers share `../../../persistent-folder`, an old `raw/`, `clean/` or `tfrecords/` there wins over what is in the bucket. Delete the folder to start fresh.
7. **Query strings are labels.** The processor maps folder names to labels with the exact keys `"brie cheese"`, `"gouda cheese"`, `"gruyere cheese"`, `"parmigiano cheese"` (`tfrecords.py:11-16`). Any other `--query` makes `create_tf_example` raise `KeyError`.
8. **The Bing scraper can spin.** `downloader.py:107-147` loops until it has `limit` images. If Bing returns a non-empty page with no `murl` matches, `links` is empty, `download_count` never grows, and the loop requests page after page. `imghdr` (`downloader.py:6`) is deprecated in Python 3.11 and removed in 3.13; the images pin 3.11.
9. **Each run leaves endpoints behind.** Part A: a new timestamped endpoint per `--deploy`; `--delete` only knows the last one. Part B: a new endpoint per `--model_deploy`; the pipeline's endpoint stays up after the run. All bill 24/7.
10. **The Lambda's name check is a substring match.** `list_endpoints(NameContains="cheese-app-endpoint")` (`deploy_model_lambda.py:40-44`) also matches `cheese-app-endpoint-<8 chars>` from `--model_deploy`. If such an endpoint exists and `cheese-app-endpoint` itself does not, the Lambda calls `update_endpoint` on a name that does not exist, and the `DeployModel` step fails. (From the code; not run.)
11. **The Lambda runtime default.** `Lambda(...)` (`src/workflow/cli.py:297-303`) passes no `runtime`, so sagemaker 2.250.0 creates the function with `python3.8` (`sagemaker-2.250.0/lambda_helper.py:40`). AWS has deprecated the Python 3.8 Lambda runtime; if your account refuses to create functions on it, `upsert` fails with a `ValueError` carrying AWS's message. Fix: `runtime="python3.12"` (any supported Python with boto3 works for this handler). Check AWS's runtime deprecation table for the current status.
12. **The Lambda is created from your laptop.** The function is created (or updated) while the pipeline definition is generated on `upsert` (`sagemaker-2.250.0/workflow/lambda_step.py:153-169`), with a fresh random name each run (`cli.py:294-295`). Old functions accumulate.
13. **`DeployModel` returns before the endpoint is ready.** The Lambda only calls `create_endpoint`/`update_endpoint` and returns (`deploy_model_lambda.py:53-65`); the pipeline shows success while the endpoint is still `Creating`. Wait for `InService` before predicting (`model-deployment-aws/README.md:191`).
14. **Caching hides re-runs.** With 30-day caching (`src/workflow/cli.py:165`), steps with unchanged arguments are skipped on later runs; the collector does not scrape again.
15. **`fit(wait=False)`** in `src/model-training/cli.py:74` returns immediately; a failure shows only in the console or `aws sagemaker describe-training-job`. The workflow's `--model_training` waits (`model.py:98`).
16. **Docker-created mount folders.** If `~/.aws` (Part A) or `../../../persistent-folder` (Part B) does not exist, Docker on Linux creates it owned by root, and the container's `app` user (uid 1000, model-training and Part A) may not be able to write or read it. Create the folders yourself first. On Linux, a host user whose uid is not 1000 may also hit permission errors on the mounted `~/.aws` files.
17. **Bucket creation in `--prepare`.** If the bucket name is taken by someone else, `create_bucket` raises `BucketAlreadyExists`, the code prints `Bucket ... already exists` and continues (`cli.py:79-80`), and the upload then fails with access denied. Pick a unique name.

## 7. Where this sits in the course

**Before.** L13 trained the cheese model as a managed training job and packaged the trainer (`package/`, `package-trainer.sh`): ml-workflow-aws's `model-training/` is that trainer adapted to SageMaker. L14 covered serverless deployment (Cloud Functions / Cloud Run on the slides' recap, slide 8); the Part A README calls the model's origin "the serverless training we did in the previous tutorials" (`README.md:111`).

**This lecture (slides decide the concepts).** Two halves, matching the deck's sections 2 and 3: serverless model deployment (slides 9–17) and ML workflow management with a managed pipeline service (slides 18–40). The deck is written for Vertex AI; the AWS tutorials implement the same ideas on SageMaker.

**Vertex AI (slides) ↔ AWS (tutorial)** — for the video's "kindly" bridge lines:

| Slides (Vertex AI / GCP) | AWS tutorial | Where |
|---|---|---|
| GCS bucket | S3 bucket | both READMEs |
| upload to Model Registry (slide 12, step 4) | create a SageMaker **Model** (not a Model Registry package) | `model-deployment-aws/cli.py:151-159`; pipeline `CreateModel` |
| deploy to an Endpoint (step 5) | endpoint configuration + endpoint | `cli.py:168-174`; `deploy_model_lambda.py` |
| update the model signature (slides 13–14) | Part A: **not done** (client sends floats); the trainer does it | `cli.py:221-225`; `task.py:276-318` |
| prebuilt serving container | `TensorFlowModel(framework_version="2.13")` → TF Serving 2.13 image | `cli.py:154` |
| Vertex AI Pipelines on Kubeflow, KFP DSL (slides 24–29) | SageMaker Pipelines, SageMaker Python SDK step classes | `src/workflow/cli.py:157-328` |
| compile to YAML, `PipelineJob(...).run()` (slides 29, 33) | `Pipeline(...).upsert(role_arn)` sends a JSON definition; `.start()` | `cli.py:320-328` |
| `.output` wiring makes the DAG (slide 29) | step **property references** make the DAG | `cli.py:219-220`, `:266-267`, `:277`, `:309` |
| container component, image in a registry Vertex can pull (slides 34–36) | ProcessingStep with `Processor(image_uri=<your ECR>)` | `cli.py:170-197`; README Build & Push |
| two-mode entrypoint (slide 36) | same script, minus gcloud auth | `src/data-collector/docker-entrypoint.sh` |
| Model Training step (slide 37) | native TrainingStep | `cli.py:249-270` |
| Model Deploy step (slide 37) | ModelStep + LambdaStep | `cli.py:276-315` |
| service-account key locally / attached SA in the cloud | IAM user access key locally / execution roles in the cloud | section 3.8 |
| Cloud Functions (slide 8 recap) | Lambda (used here for the deploy step) | `deploy_model_lambda.py` |
| Vertex Online Prediction vs Cloud Run (slides 16–17) | no AWS counterpart in the tutorial | — |

**Where the AWS code matches the slides better than the GCP repo did:** slide 37 lists "convert to TFRecords" under Data Processor; ml-workflow-aws's processor does that (`--prepare`) and the training job reads TFRecords.

**After.** L18 onward builds the app's API and frontend and later deployment/CI; a prediction endpoint like this one is what an API service would call.

## 8. Video plan (suggestion)

Two parts at the lecture's natural break. Lecture tags only while their picture is on screen.

**Part 1 — Deploy one model (≈ 12–14 min).**
1. *Hook (slide 11's cost alert):* an endpoint is a light you forgot to switch off — what exactly is running, and what turns it off? `lecture_ref` 11.
2. *Recap and the AWS bridge (slides 6–8, 10):* where the Cheese App is; "the slides say Vertex AI, we follow the AWS tutorial; same ideas, different names" — the section 7 table as a short animated mapping.
3. *IAM user, role, bucket* (A2–A4): illustration of the console fields; the masked ARN; Option 2's missing `-e` flags as a kind erratum.
4. *Build and enter the container* (A5): real capture up to "Unable to locate credentials".
5. *V1 · Where preprocessing lives* (3.1, slides 13–14): two pipes; `--prepare` (A6) with its real first error and the `extra` export.
6. *V2 · Model → endpoint config → endpoint* (3.2): `--deploy`, `expected` lines; "Model Registry" kindly corrected.
7. *V3 · The request* (3.3): `--predict`; the stale README output (three numbers) vs the four-class model.
8. *Clean up* (A9): `--delete` and the three CLI commands; cost tag. **Ponder 1:** "You ran `--deploy` twice, then `--delete`. How many endpoints still bill?" (answer: one).

**Part 2 — Automate the workflow (≈ 15–18 min).**
9. *From four CLIs to a pipeline (slides 19–22):* four people at four terminals → one DAG.
10. *Collector and processor by hand* (B5–B6): real Bing scrape, difPy, TFRecords, uploads failing honestly. **Ponder 2:** "You ran `--search` with `--query "cheddar cheese"`. Which command fails, and why?" (`--prepare`, `KeyError`, gotcha 7).
11. *Local training* (B7): the one cloud-free run; the bytes-in signature on screen (slide 14 echo); `num_classes = 3` erratum.
12. *Build & push to your ECR* (B8): the bracket `export` trap; "already done" → you must push to your own account.
13. *V4 · Steps and placeholders* (3.5–3.6, slides 28–30, 34–37): property references draw the edges; list order ≠ run order. **Ponder 3:** "Shuffle `steps=[...]`. Does the run order change?"
14. *V5 · Where the data really flows* (3.7): declared folders vs `raw.zip` in the bucket root.
15. *V6 · Two identities* (3.8): keys on the laptop, roles in the cloud.
16. *The pipeline* (B9–B11): workflow container capture (import error or credentials error, whichever is real); the DAG redrawn from the README images (`illustration`); Lambda create-or-update. **Ponder 4:** "The pipeline finished green. Can you send a prediction right now?" (no: the Lambda returns before `InService`).
17. *Teardown and recap* (B12, slide 41): checklist; recap of the six mechanisms.

## 9. Exercises

**E1 (predict, then check).** Before running `python cli.py --predict`, predict how many numbers each `Result:` line contains and which label index 0 means. *Answer:* four (`Dense(4)` in the released model); index 0 = `parmigiano` (`cli.py:42`). The README's three-number output is from another model.

**E2 (debugging, credentials).** You chose Option 2 and exported your keys, but inside the container `aws sts get-caller-identity` says it cannot locate credentials. Why? *Answer:* `docker run` passes only `AWS_REGION`, `S3_MODELS_BUCKET_NAME` and `SAGEMAKER_ROLE` (`docker-shell.sh:22-28`); environment variables are not inherited by containers. Add `-e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY`, or use `aws configure` (Option 1).

**E3 (request format).** Estimate the size of one `--predict` request and explain why the trainer's signature makes requests much smaller. *Answer:* 150,528 floats as JSON text, several megabytes; with the bytes-in signature the request carries the JPEG itself (tens of kilobytes, base64-encoded), and decoding happens on the server.

**E4 (DAG).** Which line makes `ModelTraining` wait for `DataProcessor`? What would happen if you replaced that property with the literal string `f"s3://{S3_BUCKET_NAME}/tfrecords"`? *Answer:* `src/workflow/cli.py:266-267`. With a literal, there is no reference, so no edge: SageMaker could start training in parallel with the processor, on old or missing data. You would need `depends_on=["DataProcessor"]` to restore the order.

**E5 (data flow).** Delete the `outputs=[...]` lists of both Processing steps (and the processor's `inputs=[...]`). Does the processor still get its data? *Answer:* yes — it downloads `raw.zip` from the bucket root itself (`src/data-processor/cli.py:41-49`); but the collector → processor edge disappears with the property reference, so you would need `depends_on` to keep the order.

**E6 (labels).** In `task.py:68`, `num_classes = 3`. What happens to the gouda images during training (label 3)? *Answer:* `tf.one_hot(3, 3)` is `[0, 0, 0]`, so gouda examples contribute no target class (their cross-entropy is 0), and the saved model has three outputs. Fix: `num_classes = 4`.

**E7 (cost).** After the whole tutorial, including `--deploy` twice, `--model_deploy` once and `--pipeline` once, which endpoints are running? *Answer:* two Part A endpoints (`--delete` removes only the last), one `cheese-app-endpoint-<8 chars>`, and `cheese-app-endpoint` — four `ml.m5.*` instances billing 24/7. `aws sagemaker list-endpoints` shows them.

**E8 (platforms).** On an Intel laptop the data-processor build is very slow. Why, and does it matter for SageMaker? *Answer:* `docker-shell.sh:31` forces arm64, so it is emulated. For SageMaker the image you push to ECR must be amd64 (B8), so build that one without the arm64 flag.

## 10. Errata and open questions

**Errata (state kindly in the video, with the fix)**
1. `model-deployment-aws/README.md:77-83` (Option 2): the exported keys never reach the container (`docker-shell.sh:22-28`). Fix: Option 1, or add `-e` flags.
2. `model-deployment-aws/README.md:136-148`: the sample output has three probabilities per image and a label map that does not match `cli.py:41-42`; the released model has four outputs. Expect four numbers.
3. `model-deployment-aws/README.md:7`, `ml-workflow-aws/README.md:7`: "Model Registry" — the code creates plain SageMaker Models; no model package group is used.
4. `ml-workflow-aws/README.md:7`: "Model Deploy: Updates the model signature with preprocessing logic" — the signature is added at the end of *training* (`task.py:276-318`); the deploy steps only create a Model and an endpoint.
5. `ml-workflow-aws/README.md:153`: "This step has already been done for this tutorial" — the pipeline pulls `cheese-app-data-collector:latest` and `cheese-app-data-processor:latest` from **your** account's ECR (`src/workflow/cli.py:35-36`), so every student must push both images. The Docker Hub images to pull in step 1 (`<YOUR_DOCKER_HUB_USERNAME>`) are not named anywhere.
6. `ml-workflow-aws/README.md:169`: `export REGION=us-east-1 [YOUR DEVELOPMENT REGION]` errors when pasted (tested). Type the value only.
7. `ml-workflow-aws/src/model-training/package/trainer/task.py:68`: `num_classes = 3`, but the processor writes labels 0–3 (`tfrecords.py:11-16`). Gouda (3) gets an all-zero one-hot target; the model has three outputs. Fix: `4`.
8. `ml-workflow-aws/src/workflow/Dockerfile:40-42`: the committed lock is ignored, so the build installs the newest `sagemaker` (3.x on 2026-11-05), whose packages lack the 2.x modules `cli.py:13-22` imports. Fix: pin `sagemaker = "==2.250.0"` (matches the lock) or copy the lock and `pipenv sync`. *Captures confirm or refute.*
9. `model-deployment-aws/cli.py:71-82`: `--prepare` creates the bucket first, a step the README's list (`README.md:113-117`) does not mention.
10. Leftover GCP wording: `cli.py:318` "save model to GCS Bucket", help texts "Vertex AI" (`:346-358`), docstring `--upload` (`:5`), parser title "Data Collector CLI" (`:337`), and a `--test` flag that does nothing (`:355-358`).
11. `ml-workflow-aws/README.md:88`: the heading repeats "& Test CLI".
12. `model-deployment-aws/README.md:28`: `IAMFullAccess` is broader than the code needs (it never creates a role).

**Open questions (captures or a real AWS run decide)**
1. **How the pipeline's training step finds its data.** Its channel is the processor's declared prefix `s3://<b>/tfrecords` (`src/workflow/cli.py:266-267`), which the processor never writes into; the processor uploads `tfrecords.zip` to the bucket root. An S3 key prefix `tfrecords` does match the key `tfrecords.zip`, and the README's image shows a successful run, but where SageMaker places such a file in `/opt/ml/input/data/training/` (and so whether `task.py:77-86` finds it) was not verified. The video should show the declared folders and the real uploads, and not claim either outcome.
2. **Part A version skew.** The SavedModel is exported by TensorFlow 2.18 / Keras 3 (`Pipfile:12`) and served by the TF Serving **2.13** container (`cli.py:154`). Whether 2.13 loads it is untested here (no AWS). If the endpoint fails to start, CloudWatch shows the load error (`README.md:186-188`).
3. **`from tensorflow.python.keras import backend as K`** (`task.py:11`) with TensorFlow 2.20 in the local training container: whether this private module path still imports there was not checked; local training (B7) will show it. On SageMaker's TF 2.13 container it exists.
4. **Part A build on Ubuntu 20.04.** `python3.9` with `--no-install-recommends` and `pip install pipenv` under the system Python 3.8, then `pipenv lock` for Python 3.9: whether the lock resolves today (sagemaker 2.x with TF 2.18 on 3.9) is for the capture to show.
5. **Lambda runtime.** Whether AWS still allows creating `python3.8` functions in a given account on 2026-11-05 was not checked (no account). Gotcha 11 gives the fix either way.
6. **Region for bare clients.** Whether `boto3.client('sts')` without a region (`src/workflow/cli.py:31`) works in the workflow container (which passes `AWS_REGION` but not `AWS_DEFAULT_REGION` and mounts no `~/.aws`) depends on botocore's STS endpoint rules; with credentials missing here, the capture will show the credentials error, not this one.
7. **Processing jobs and the region.** The standalone `--data_collector` job passes no `env` (`src/workflow/cli.py:52-59`), unlike the pipeline's (`:177`); the collector calls `boto3.client('s3')` without a region. S3 uploads work without a region in practice; not verified on SageMaker.
