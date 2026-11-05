# AC215 · Lecture 15 — ML workflows: deploy one model, then automate the pipeline on SageMaker (follow-along: model-deployment-aws + ml-workflow-aws)

## 00:00 — Three numbers or four?
Here is a question for a model: what cheese is in this photo? Both answers on screen come from the same predict code in cli.py. And both answers say brie.
Now count the numbers. The top answer, the README output, holds three. The bottom one, from this recording, holds four. One model cannot give both. So which model is behind an endpoint, and what else is there?
Behind an endpoint sit three pieces: an artifact, which model; a container, what runs it; and a machine, where it runs, and who pays. The meter beside the machine keeps running while no request arrives.
In part 2, we stop running these steps by hand. The four stages of the Cheese App become one pipeline that the cloud runs for you.
To follow along, you need an AWS account with billing, the AWS CLI, Docker, and both repositories cloned. This is our first lecture on AWS.
A tracker in the corner names the README step, and a yellow tag, your turn, means pause and run it. Every command is also in the study guide.

## 01:10 — Where we are, in AWS words
First, where this lecture sits. The course project is in its prototype phase, and of the four parts of the Cheese App, three are done. Model deploy is still open.
Part 1 of this video fills that tile. Part 2 connects all four.
Last week, lecture 14 put containers on Cloud Run. Today, the container serves a trained model.
The lecture maps its console onto the course: notebooks, training from lecture 13, and today's two, online prediction and pipelines.
The lecture is written for Vertex AI on Google Cloud. This course also ships an AWS version of both tutorials, and that is the one we follow. Same ideas, different names. I'll point out each one as we meet it.
A Google Cloud bucket becomes S3. A service account key becomes an IAM user with a key on your laptop, plus a role in the cloud. And an endpoint becomes a configuration plus an endpoint.
One thing about this recording: it has no AWS account. Every step that runs on your laptop is real. Every AWS call stops at its honest first error, like this one. Where the cloud would answer, you see the README output, or a tagged local stand-in. Never a faked success.
Versions at the time of recording are on screen.

## 02:33 — A user, a role and a bucket
Step 1: clone the repository. The README says clone or download, so our git clone is extra, and so is the git log that shows the commit we follow. Pause and clone it.
An extra listing: the CLI, a Dockerfile, a Pipfile, eight sample photos, and docker-shell.sh, already executable.
Steps 2 and 3 are in the AWS console. Check that you can use S3, SageMaker and IAM. Then create an IAM user called model deployment, with three policies. The third is broader than this code needs. Create access keys and save both.
Step 4 creates a role named SageMaker Execution Role, trusted by SageMaker, with the SageMaker and S3 policies. Copy its A R N.
Why two identities? Your laptop signs each request with the user key, and the endpoint you create later acts as the role. The key stays on your laptop.
Step 5, then pause: create a bucket with a name of your own, because bucket names are unique across all of AWS. Storage bills while files sit in it. And as the README warns, never put keys in a script, and never commit them to Git.
Run Container, step 1: aws configure. Then come four prompts. You paste your two keys. We have none, so we press Enter twice, then type us-east-1 and json.
Two extras: only the config file exists, since we typed no keys, and the who am I call cannot find credentials. With your keys, it prints your account. Pause and make yours print it.
Step 2 offers a second option: three exports in your shell. AWS rejects our placeholder key.
There is a subtler gap: the script passes only the region, the bucket and the role into the container. So exported keys fall off at the wall. Use option 1, or add the keys with dash e.

## 04:34 — The CLI container: two one-line fixes
Step 3: edit docker-shell.sh with your bucket, the A R N of your role, and your region. Ours are placeholders.
Step 4, chmod, prints nothing. An extra listing shows the script was already executable.
Step 5: sh docker-shell.sh. It pulls the base image for A R M 64, then stops at the first RUN line: exec format error. Our Intel style laptop cannot run those programs.
The fix is in the script. Line 19 is for Apple silicon Macs, and line 17, commented out, is the plain build. Swap them: fix 1, an extra. On Apple silicon the original line works. Elsewhere it means slow emulation, or this error.
Now look at the Pipfile. TensorFlow is pinned to one version, but SageMaker says star: any version. And no lock is used: Git ignores the lock file, and the Dockerfile runs pipenv lock at build time.
Something to ponder. The code worked when it was written, and nobody changed a line. Why does cli.py fail at import today?
Star is a constraint, not a pin, as in lecture 1: the resolver takes the newest release that installs. At the time of recording, on Python 3.9, that is SageMaker SDK version 3, with PyTorch and 14 CUDA packages.
Version 3 is a rewritten package, without the modules cli.py imports: no tensorflow module, no serializers, no get execution role. The imports find nothing.
Here, the unpinned build ran 13 minutes, then ran out of disk. On your laptop it would finish, then fail at the first import.
Fix 2, also an extra: change star to less than 3. The resolver stops at the last version 2 release, and the imports work. Pause and make both fixes.
Run step 5 again. It builds in almost 7 minutes, mostly locking and installing packages. The AWS check fails without keys, but the shell still opens.
Inside, extras show Python 3.9, SageMaker version 2 and TensorFlow 2.18, and the three values from the script. Deprecation warnings are not the error.
A small slip: the help text still says GCS bucket and Vertex AI, and the test flag does nothing. The commands are the AWS ones. The image is about 4 gigabytes.

## 07:19 — Where does preprocessing live?
Before we prepare the model, a design question from the lecture: where does preprocessing happen? In a notebook, you resize and normalize cell by cell. A production endpoint should take the raw photo and do all of that itself.
In this tutorial, the client does it. The predict code opens the photo, converts it to R G B and resizes it to 224 by 224. Then it divides by 255 and sends the numbers as JSON.
An extra check reads the model's front door, which TensorFlow calls a signature. It takes floats, shaped any number by 224 by 224 by 3, and gives four numbers per photo. Preprocessing sits on your side of the wire.
The lecture names the risk: client-side brittleness. Every client must repeat those steps exactly, and a phone app that forgets to divide by 255 gets confident nonsense. One copy inside the model is also easier to roll back and version.
The fix from the lecture sits in the part 2 trainer. The preprocess function decodes the JPEG, converts it to floats, and resizes it.
A function marked as the model's front door takes a batch of JPEG strings, prepares each one, and calls the model. It is saved as the serving default. Raw bytes in, one score per class out.
One trap to avoid. The README says the prepare step converts the model to the SavedModel format. That is a change of format, not the change of signature from the lecture.

## 08:57 — --prepare: a SavedModel in a tarball
Step 1: python cli.py dash dash prepare. The README lists four things. Download the model from GitHub, convert it to the SavedModel format, pack it as model dot tar dot G Z, and upload it to your bucket. Those are steps 1 and 3 of the lecture deployment picture. Step 2, the signature change, is not in part 1.
Pause and run it. Ours stops right away: no credentials, at line 73 of cli.py, which creates the bucket. And the artifacts folder does not exist, so nothing was downloaded.
A small gap in the README: the code creates the bucket before it downloads anything, a step the list does not mention. With your keys, it creates the bucket, or reuses yours if it already exists.
To show what comes next, an extra: the same prepare function, with S3 replaced by a stub that sends nothing. The release zip downloads, the model is exported, and the stub stops the upload. Nothing reaches AWS.
Here is what it made. A SavedModel is a folder: the graph and its named entry points in saved model dot P B, and the weights in a variables folder.
The code puts it in a folder named 1, because TensorFlow Serving finds models by name, then version. The tarball holds that folder at its top.
An extra git status shows your two edits, and Git ignores the artifacts folder. In your account, the tarball now sits in S3, and storage bills while it exists.

## 10:38 — --deploy: model, endpoint configuration, endpoint
Step 2: deploy. Remember the three pieces from the start. In code, it first describes a TensorFlow model: the tarball in S3 and the serving container, plus the role. Nothing exists in AWS yet.
The lecture uploads to a model registry here. Both READMEs say model registry too, but the code creates a plain model in SageMaker.
You never write an image name: the SDK picks the AWS TensorFlow Serving image from framework version 2.13. Our model was exported by TensorFlow 2.18. In step 3, a local check shows that Serving 2.13 loads it.
Then deploy, with one instance of type M L M5 extra large, under a name with a timestamp. That one call creates all three: the model in SageMaker, an endpoint configuration, which names the machine and the model, and the endpoint, the address you call.
Pause and run python cli.py dash dash deploy. Ours stops at line 168, the deploy call: no credentials. With yours, the README says 5 to 10 minutes, then it prints the endpoint name and saves it in endpoint config dot JSON.
The lecture calls this serverless, meaning no server for you to manage. It is still one machine, billing around the clock, even with zero traffic. Unlike Cloud Run in lecture 14, this endpoint, as the code creates it, does not scale to zero.
The lecture compares two ways to serve. A model endpoint deploys a trained model directly, with versioning, A B testing and monitoring available. A general container service like Cloud Run runs anything, and you build the rest yourself.
Its rule of thumb: an endpoint to serve a trained model, a container service when the model is one part of a larger app. Here, those features go unused.

## 12:38 — --predict: 150,528 numbers per photo
Step 3: python cli.py dash dash predict. Ours finds no endpoint config dot JSON and falls back to a default name. It picks five photos and fails five times: unable to locate credentials. Pause and run yours.
Each try would send one photo. The client resizes it to 224 by 224, with 3 color channels. How many numbers travel to the endpoint for that one photo?
224 times 224 times 3: one hundred fifty thousand, five hundred twenty-eight floats. Python writes each one as text in JSON, so a few megabytes per photo. A signature that takes bytes would send the JPEG itself.
The answer is a list of four probabilities. The code takes the largest with arg max and looks it up: 0 parmigiano, 1 gruyere, 2 brie, 3 gouda.
To see a real answer, we use an extra local stand-in, not SageMaker. The AWS serving image runs TensorFlow Serving, so we started the public Serving 2.13 image on our export. It loads version 1.
Then the same predict function sends the same JSON to it. Brie comes back brie, and gruyere comes back gruyere, four numbers each.
And parmigiano comes back brie, at 98 percent. That is a real mistake of the released model. Its own metrics file reports about 72 percent accuracy.
Now the opening puzzle. Same code, different artifact: the README output came from an older model, with three classes and another label order. A small gap: expect four numbers, and index 0 is parmigiano.
An extra command removes the stand-in. It never touched AWS.

## 14:39 — --delete: turn off the meter
The lecture warns that an endpoint costs money while it is up, and the slides shout one word: delete. The README gives three ways, and any one will do. Way 1, the console: SageMaker, Endpoints, select yours, Delete.
Way 2 gives three AWS CLI commands. Typed exactly as written, the first one is a shell error: the angle brackets are placeholders, and the shell takes them as a redirection.
A small gap: type your own names, without brackets. Ours then fails: no credentials. Delete in this order: the endpoint, then its configuration, then the model.
Way 3: python cli.py dash dash delete stops at its first SageMaker call. Pause and run it. With keys, it deletes the endpoint named in the JSON file. Then come matching configurations and the model, by naming convention, then the tarball in S3.
Each deploy makes a new endpoint with a new timestamp, but the JSON file keeps only the last name. You ran deploy twice, then delete once. How many endpoints still bill?
One. Delete removes only the endpoint the file names. The older one keeps running. Check with aws sagemaker list endpoints, and confirm in the console.
That is part 1. You ran four commands by hand to deploy one model. The Cheese App has four stages before that. Who runs all of them, in the right order, every time?

## 16:19 — From four terminals to one workflow
Part 2. The lecture draws the problem: four stages, each run by a person at a terminal. How do we execute these steps? And can we automate this flow?
The answer is an orchestrator. The lecture uses Vertex AI Pipelines, on Kubeflow. This tutorial uses SageMaker Pipelines, the same idea of managed steps in a graph.
Workflow management runs the steps in order, makes a run repeatable, gives each step its machine, and shows it. This repo covers those four. Scheduling waits for lecture 23. And it is managed: no cluster for you to run.
Setup, step 1: clone ml workflow AWS. Our git clone is extra again. An extra tree shows four folders under source: three stages and the workflow.
Steps 2 to 5 are console work: quick setup for SageMaker AI, and a Unified Studio domain, where you will watch the pipeline. Then your bucket, and a user named ml workflow user, with four policies.
Create an access key for the command line, and download the C S V file. Quick setup and the Studio domain stay in your account: check them when you clean up.
Steps 6 and 7: install the AWS CLI, then aws configure, and paste the two values from the C S V. From here on, we typed obviously fake placeholders, so AWS answers with real errors.
Step 8 tests the configuration. AWS itself rejects the fake token and the fake key. With yours, these print your account and your buckets. Don't go on until they do.
Step 9 creates two roles: Cheese App SageMaker Execution Role, for every job, and Cheese App Lambda Execution Role. The code builds each A R N from your account number and the exact role name, so spell them exactly, and pause here.

## 18:19 — Collector and processor, by hand
Data collector, step 1. A small gap first: all four part 2 scripts name the bucket from the README, so put yours in each one. Then, in this folder, run sh docker-shell.sh. Without keys, the script stops itself: AWS not configured.
With keys, it builds in 40 seconds and opens a root shell. Two notes. This script builds for A M D 64, which Apple silicon emulates. And on Ubuntu or Debian, sh is dash, which skips the key check, so run bash docker-shell.sh.
Why a shell? The entry point script has a switch. No arguments: it opens bash, development mode, where you are now. Arguments: it runs them and exits, production mode. The lecture calls that a callable container.
Step 2: the search command, four cheeses, ten images each. It scrapes the web, writes four folders, zips them, and tries to upload raw dot zip. AWS rejects our fake key.
Step 3, check your bucket, cannot pass here. An extra listing shows 40 images on disk. On the laptop, a root-owned persistent folder appeared beside the clones.
Data processor, step 1: the A R M 64 line fails again, and the same swap fixes it.
Step 2: python cli.py dash dash clean. A duplicate finder checks each label, finds none among these 40, and the upload of clean dot zip fails. Pause and run it.
Steps 3 and 4: check your bucket, then dash dash prepare. All 40 images split into 32 for training and 8 for validation, in two real TFRecord files. The upload fails again. Step 5 finds them only on disk.
The duty cards from the lecture match: download, then verify, remove duplicates and convert to TFRecords. And the four labels are just the folder names: your search queries, so type them exactly.

## 20:26 — Train locally, sign the model
Model training, step 1. Same A R M 64 line, same swap. This image installs from its committed lock, with SageMaker version 2, so it needs no pin.
Step 2, local training. TensorFlow 2.20 on the CPU finds the TFRecords from the processor, through the shared folder. Look at the last layer: three outputs. One epoch runs. Its accuracy means nothing yet.
Then saving fails: permission denied, slash persistent slash model. Pause here for two small fixes.
First, line 68 says three classes, while the data has four labels, so gouda gets no target. Change it to 4.
Second, on Linux, Docker created the persistent folder as root, and this container runs as the app user. Exit, and on your laptop create the folder yourself, or change its owner. Then run step 2 again. Docker Desktop on a Mac avoids this.
It would write to slash persistent slash model slash 1: the persistent folder on your laptop, or the SageMaker model folder inside a training job.
Just before the save sits the signature change from the lecture: decode, convert, resize, inside the model. A small slip: the README gives this job to model deploy. The trainer does it.
Step 3: sh package-trainer.sh packs the package folder and copies it to S3. The tar file is real. The upload fails on our fake key.
Step 4: python cli.py dash dash train. It asks AWS who you are, to build the role A R N, and stops there. With keys, it starts a training job on M L M5 extra large, and returns at once.
Step 5: watch it in the console, under Training, then Training jobs. Its name starts with cheese.

## 22:22 — Build and push: your own registry
Build and push. The README says this step has already been done for you. A small gap: the workflow code pulls both images from the ECR registry of your own account, so you push them yourself, once each.
That is the second step the lecture gives for your own containers: push the images to a registry the platform can pull from.
Steps 1 to 3 go through Docker Hub: log in, build, push. The Mac line builds A M D 64, because SageMaker runs that.
Step 4 sets five variables. Pasted exactly as written, the first line prints two errors, because export rejects the bracket note, though the region is still set. The account lookup fails on our fake key, and the URI starts with a dot.
So paste only the value, us-east-1. And if your URI starts with a dot, the account lookup failed: fix your keys first.
Step 5 pulls your image. Step 6 creates the repository, and the or true at the end hides the error: the command exits with zero.
Steps 7 to 11 log Docker in to ECR, tag the image, push it, list it, and print the URI. Tag only adds a second name to the same image. Run them on your laptop, not in the workflow container, which has no docker command. Then repeat for the processor image.

## 23:49 — The workflow container and one processing job
Automate the data collector, step 1, in the workflow folder. Before you run sh docker-shell.sh, the star problem returns. A lock is committed, but the Dockerfile copies only the Pipfile, so the build would resolve version 3.
The checks show the imports failing. So make the same fix first: less than 3.
Now run sh docker-shell.sh. The banner shows region and bucket, and the who am I check fails. Extras: SageMaker version 2 now, and no docker command. The socket is mounted, but no docker program is inside.
From here, the SDK is your remote control, as the lecture puts it. Your Python asks, and AWS machines run.
Step 2: python cli.py dash dash data collector. It stops at line 32, a lookup of your account at the top of the file, before the function even starts. Every flag of this CLI needs a working key at import time.
With keys, it builds a processor from your ECR image, on one M L T3 medium. Its entry point is python 3 with the collector cli.py. Then it runs the job with the search arguments, and waits, showing the logs.
This is production mode. SageMaker puts its own command in front of the arguments. Same image, same cli.py, on a machine you never log in to. The job acts as the role, not with your key.
Step 3: watch it under Processing, then Processing jobs.

## 25:32 — A pipeline drawn by references
Now the whole pipeline. The slides write steps in the Kubeflow D S L, wired by dot output and compiled to YAML. Here: SageMaker step classes, property references and JSON.
First, caching, for 30 days. The first step is a processing step named data collector, with one declared output, raw data.
The second step, the processor, takes as input a property of the collector: its raw data output, S3 URI. Not a string: a reference, and it draws an edge.
Training takes the TFRecords output of the processor the same way, and the model step takes the trained model artifacts. Each reference draws one more edge.
Last, the Lambda step named deploy model takes the model name from the model step. Then the pipeline lists all five steps, creates the deploy Lambda from your laptop, upserts its definition, and starts it.
Something to ponder. Reverse the list of steps in the Pipeline call. Does the run order change?
No. The order comes from the references: each input names the output of another step. The list is a set of steps, not a schedule.
An extra, built offline and never sent: the JSON definition from the SDK. Five steps, each edge a get on a property of another step. Upsert sends this.
The lecture draws four steps. Here, deploy splits in two. Create model makes the model, and a Lambda, a small function AWS runs on demand, creates or updates the endpoint.
One honest caveat. The edges set the order, but files also travel by fixed names through the bucket: raw, clean and tfrecords dot zip. We could not check, without an account, how the training job finds its data on SageMaker.
Step 1: python cli.py dash dash pipeline stops at the same line 32. With keys, it prints that the pipeline started. Step 2: in Unified Studio, under Build, ML Pipelines, you would see this graph.
If every step succeeds, caching skips unchanged steps for 30 days, so the collector won't scrape again. And a green deploy model only means the Lambda asked: wait until the endpoint is in service.
Step 3 tests each component with its own flag. Here, all four stop at that line. With keys, model deploy makes yet another endpoint.

## 28:17 — Tear down, recap, test yourself
Before you leave, clean up. List your endpoints and delete every one: the timestamped ones from part 1, and cheese app endpoint. Then delete their configurations and models.
Empty and delete both buckets. Delete the two ECR repositories, the deploy Lambda functions, and the cheese pipeline.
Deactivate and delete the access keys, and the users and roles you no longer need. Finally, check the SageMaker AI domain and the Unified Studio domain you created.
The lecture ends on a factory: your Python is the recipe, and SageMaker Pipelines runs it. Today's pictures: a key on the laptop and a role in the cloud. A star is not a pin. Preprocessing sits in the client or in the model. Three pieces stand behind an endpoint, and references draw the edges.
Under it, part 1 in four commands. Prepare packs the model, deploy builds the model, configuration and endpoint. Predict sends the numbers, and delete turns off the meter.
Test yourself. Your laptop and the endpoint both reach S3: which identity does each use? And why do the option 2 exports never reach the part 1 container?
Name the three things deploy creates. Which one is the address, and which one bills while nobody calls it? Where does preprocessing sit in part 1, and in the part 2 trainer, and why move it into the model?
Which lines make training wait for the processor? Which two one-line fixes did today need, and which would an Apple silicon Mac skip? The answers are in the exercises, and lecture 23 triggers the pipeline from GitHub.
