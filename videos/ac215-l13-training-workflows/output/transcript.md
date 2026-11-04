# AC215 · Lecture 13 — Advanced training workflows: a run is a record, a job is a rented machine (follow-along: model-training + two Colab notebooks)

## 00:00 — Two tables, two winners
Two notebooks from this lecture, run by the instructors: the same data pipeline, the same 1,156 cheese photos, the same five models. Notebook A crowns the fine-tuned MobileNet, at 68.97 percent. Notebook B crowns the frozen MobileNet, also at 68.97 percent, and puts the fine-tuned one at 62.93.
So which recipe is better, fine-tuning or freezing? And from these two tables, can you even tell what was different? One clue is visible: look at the epochs column. Hold that question. Part of the answer is in the table, and part of it is in what the table never wrote down.
Then the fine-tuned MobileNet leaves Colab. It gets packed into a 4 kilobyte tarball and trains on a machine you rent for the length of one job, from one command. That command carries your W and B key.
To follow along you need two Colab copies with a free T4 GPU, a free account on W and B, Docker, and a Google Cloud project with billing. Vertex AI jobs cost money while they run; gold tags mark each point, without amounts. A yellow tag means pause and run it, and the study guide has every command. Today's two words, from the lecture: reproducibility and accountability.

## 01:24 — Three levers and a missing row
The lecture starts from three levers for better deep learning: more data, better models, and faster hardware. Today we pull the third one: you rent hardware. And you add the bookkeeping that shows whether it helped.
On the Cheese App roadmap, the dashed box around experiment tracking and baseline models is today. Your third milestone asks for exactly this.
Where does each piece of an experiment go? Code to GitHub, data to the versioning from lecture 11, and the environment to pyproject.toml and uv.lock. Weights, metrics and logs have no home yet. A complete run should keep seven things: environment, code, data, model, metrics, artifacts and notes.
The course uses Weights and Biases, W and B for short, which is hosted for you. MLflow is the usual choice if you must host it yourself.
Here is the map. On top, the Colab lane: notebook A fills a folder and uploads it, and notebook B streams its runs to W and B. Below, the repo lane: your laptop packs the code, a bucket holds it, Vertex AI runs it, and the run reports to W and B. Today we light both.

## 02:40 — A tracker made of folders
Open notebook A from the course page, save a copy, and switch the runtime to a GPU; pause and set it up. Its stored outputs show the instructors' run on one Tesla T4.
Run the dataset cells: 1,156 photos from one GitHub release, with four cheese labels. Remember their order. Then the split: 936 to train, 104 to validate, 116 to test. Pause and run them.
Something to ponder. The cell sets the validation percent to 0.2, yet validation is 104 out of 1,156. What did the code actually do?
Both splits use the test percent. 10 percent of 1,156 is 116 for testing, then 10 percent of the remaining 1,040 is 104, the validation set. A small slip, copied into the repo trainer.
Now the home-made tracker. Cell 31 makes a folder named after the current Unix time. After each model trains, the helper from cell 12 drops five files into it: the model, its weights, its structure, its history and its metrics. Pause and train the five models.
Cell 54 gathers the metric files into one table, and cell 56 picks its top row as the best model; pause and run through the predictions. A small slip: accuracy becomes text before sorting, so it sorts strings; 9.5 percent would rank above 68 percent.
Here is a first answer. The folder keeps settings and scores, but not which 116 photos were the test set. The split has no seed, so every run is graded on a different 116. One photo is worth 0.86 points, and the winner in notebook A leads by two photos.
Sign in with cell 62, put your own project and bucket into cell 63, and run cell 66. Any bucket of yours works; scene 7 creates one. Pause and run it. A gold tag: those files now sit in your bucket, 10 to 104 megabytes of weights per model, plus a copy.

## 05:09 — Runs on a shared axis
Notebook B adds W and B. Its first cell installs it, and the dash U flag means whatever is newest. An extra check in our signed-out stand-in shows 0.31.0 at the time of recording, while the stored run used 0.22.2. Pause and run it.
The data cells, through cell 32, match notebook A, but one also downloads a zip of about 510 megabytes you never use. You may delete that line; then pause and run them.
Copy your API key from the user settings on W and B. In Colab, open the key icon and add a secret named exactly as on screen, with notebook access on. Pause and add yours. Cell 34 signs in with it.
Now pause and run the five training cells. Each starts its run with wandb init in one project, cheese app demo. In the ledger, the five rows become five runs on one shared epoch axis.
But only the two block run shows curves. Compare its model fit call with another cell's. Something to ponder: what do the other four lack?
A callback: code that model fit calls after every epoch. Only the two block cell passes the W and B callback, so only its loss and accuracy arrive, epoch by epoch. Without one, wandb init gives you system charts, never your curves.
Both MobileNet runs share one name, so tell them apart by run ID. No cell finishes the last run, so add wandb finish after cell 52, an extra.
Cell 55 builds the second table from the opening. The fine-tuned MobileNet trained 10 epochs here and 15 in notebook A: not a fair comparison. Now the frozen MobileNet, with the same settings and epochs: 67.24 in notebook A, 68.97 here. Two photos apart by chance alone: the size of the winning margin.
To upload, edit the bucket and project inside cell 13 and run cell 13 again, then run cells 64 and 66; pause and do it.

## 07:31 — Three lines, and an assignment that goes nowhere
The lecture shows the pattern as three lines around unchanged training code. Start the run with wandb init. Watch the model with a callback inside model fit. And finish the run when training ends.
Now notebook B's real cell. It starts the run, then assigns a dictionary to wandb config, renames the run, and calls run save.
Something to ponder. After that assignment, and a later update with the execution time, what does the run's config hold?
Watch the name. The call wandb init points the name wandb config at the run's config drawer. The assignment does not fill that drawer; it moves the name onto a new, loose dictionary. The update then writes into the loose one, and the run finishes with its drawer empty.
The proof, on today's W and B in offline mode, as our stand-in. The name points at a plain dict, and the run's config is empty. The fix passes the dictionary to wandb init itself, and the config holds all four keys plus the execution time.
The call run save with the word test uploads files matching test; it does not save the run.
The repo's trainer gets the first and last lines right: config inside wandb init, then update and finish. But the middle line is gone. One commit in October 2025 removed the callback, without saying why. So its runs get config and system charts, and no curves; exercise 1 adds the callback again.

## 09:17 — Rent the machine, not the server
The second half of the lecture is Vertex AI, Google Cloud's machine learning platform. Three console entries matter: Workbench for notebooks, Training for jobs, and Pipelines for workflows. Today is Training, on the custom jobs tab; lecture 15 uses Pipelines.
Serverless training means you rent the hardware only for the training step. Nobody sets up a server, and billing stops when the step ends. There is still a machine; you just don't manage its lifetime.
Step one: move the notebook code into a Python file, and turn its hard-coded choices into flags. The flags are epochs, batch size and model name, plus train base and your W and B key.
Step two packs that file into a tarball, one compressed archive, and uploads it to a bucket. Step three runs from what the lecture calls the Model Trainer CLI Container, our cockpit on your laptop: it asks Vertex AI for a job. Vertex AI then starts a machine, CPU only or with one T4. It loads Google's prebuilt TensorFlow image, installs your tarball, runs your trainer with your flags, and deletes the machine.
Two facts drive everything after this. The job cannot see your laptop: its data comes from the internet, and anything it should keep must be written somewhere durable. And the image is Google's, not yours.
A quick prediction. Your laptop has no GPU and no TensorFlow. Which machines in this picture will ever import TensorFlow?
Two: the Colab runtime, and the container inside each Vertex job. Never the cockpit on your laptop; scene 9 proves it.

## 11:05 — A project, two keys and a bucket
Clone the model training repo and move into it; pause and run it. Two extras show the course pin and the repo's files.
In the console, enable the Vertex AI API. Then request GPU quota, an allowance per region. Filter for custom model training, pick T4 GPUs, include us-central1, where cli.sh runs, set a new limit and submit. Pause and do both. Approval may take hours or be refused; cli.sh runs on CPU without it.
Next, a secrets folder beside the repo, never inside it; pause and make it.
Then the identity: a service account called model trainer, with Storage Admin, AI Platform Admin and Vertex AI Administrator, and one JSON key saved in secrets as model-trainer.json. Pause and create yours.
One honest note. This recording machine has no Google credentials, no W and B account, no GPU and no browser. The key in that listing is an obviously invalid stand-in, moved out before the container starts. So each cloud step shows the failure a misplaced key gives, and successes come from named sources.
Then create a bucket with your own name; pause and create it. Two extras show why: our placeholder returns 404, it exists nowhere, while the README's name returns 401, it belongs to someone else. A gold tag: the bucket stores your code and experiment folders.
Last, copy your W and B key and export it in the terminal you'll use for the container. Pause and do it. An extra echo prints its length, 40 for our placeholder. It must not be zero, and the trainer's pinned wandb accepts exactly 40.
Something to ponder. You exported the key, closed that terminal, and opened a new one. What does the same echo print now?
Zero: an exported variable exists only in that shell and its children. Part 1 is done: the key is set, the bucket has a name. Next, we build the cockpit, and today it won't build.

## 13:39 — The cockpit that won't build: two one-line fixes
Part 2 ships the trainer: build the cockpit, pack the code, send one job. Put your bucket and project on lines 8 and 9 of docker-shell.sh; pause and edit yours.
A small slip: the README's copy of this script is not the real file. It has notes in brackets and an older line for Apple chips, so edit the script itself. It builds for amd64 and mounts your code and secrets.
Now run sh docker-shell.sh from inside the repo; pause and run it. Today it fails at step 2 of 14. All 22 packages return 404 Not Found from the Debian mirror, and the build stops at line 18. The script's set dash e, exit on error, then stops it before docker run.
Something to ponder. Every error says 404 from the Debian mirror, and your internet works. Which line of the Dockerfile picks your Debian?
Line 2, the FROM line. Bullseye is Debian 11, and at the time of recording its security mirror lists packages it no longer serves; they moved to an archive. The first fix, an extra, switches the base to bookworm, Debian 12; pause and make it.
Pause and run it again. Now it stops at step 8: google-cloud-sdk has no installation candidate, and google-cloud-cli replaces it. Google renamed its apt package.
The second fix, also an extra: install google-cloud-cli instead, on line 37; pause and make it. An extra git diff shows everything you changed: your two values, the two fixes, and nothing else.
Pause and run it a third time: it builds, about 5 minutes here, longer on Apple Silicon, where amd64 is emulated. The banner says running, then gcloud cannot open the key file: our missing key. With yours, this line confirms the service account. The script carries on anyway, because the entrypoint has no set dash e.
The architecture is x86 64, on a Mac too; the versions are on screen. A small slip: activated is printed before the activation, a label, not a fact.

## 16:04 — What goes in the tarball
Inside the cockpit, a few extra checks. Slash secrets is empty, our sandbox. Project, bucket and key came through; gcloud, gsutil and uv are here. Pause and check yours: the last number must be 40, not 0. But importing TensorFlow fails: this container submits jobs, it never trains.
Review setup.py; pause and open it. It is the label pip uses to install the tarball. The only declared dependency is wandb, pinned to 0.15.11. Its find packages call finds the trainer folder because the folder has its own init file, so once installed, python dash m trainer dot task works. TensorFlow and scikit-learn are not declared: they are assumed to come from the image Google provides, and scene 11 shows the tarball lacks them. Requests only arrives because wandb needs it.
Review task.py next; pause and open it. The notebook choices are flags now, and the key flag defaults to the text 16: remember that. The data comes from one GitHub release, since the job cannot see your laptop, and the W and B login runs after that download.
Now pack it: run sh package-trainer.sh inside the container; pause and run it. Tar lists eight entries, and the upload fails: our placeholder bucket does not exist. Line 4 uses a fixed name, so each upload overwrites the last.
Extra checks: the tarball is 4,016 bytes. On our Linux engine it belongs to root, because the container wrote it; on Docker Desktop, to you. Git ignores it either way.
Something to ponder. You fix a typo in task.py. Do you rebuild the image, run the package script again, or both?
Only the package script. Vertex AI runs the tarball in your bucket, and your image never travels. The cockpit mounts your code folder, so it already sees the edit. A gold tag: the tarball is stored in your bucket, and it is tiny.

## 18:24 — One command, and a key inside it
Review cli.sh; pause and open it. It names the job with random hex, asks for one n1-standard-4 machine, and sets a GPU image. Then it points at your tarball in the bucket and the module to run, and builds the arguments, ending with your W and B key.
Further down, the GPU block is commented out and line 31 swaps in the CPU image, so only the CPU command runs. A small slip: the README shows GPU first and CPU as optional, but the script already runs on CPU.
A gold tag first: once the job's machine is provisioned, your project pays until the script exits. Check that your key length is 40; if not, watch scene 11 before you submit. Now sh cli.sh; pause and run it. The first line is real: the Vertex AI endpoint in us-central1. Then it stops with no active account, because the key never loaded; an extra auth list confirms it. With your key, gcloud reports the job as created.
An extra trace with sh dash x shows the job it tried to send. The GPU image is set, then overridden by the CPU image. Then the full command. The worker pool spec is the job's machine order: machine type, one replica, meaning one machine, image and module. Last come the arguments, ending with your W and B key in plain text.
Something to ponder. Your W and B key is now part of the job's arguments. Who can see it later?
Anyone who can view jobs in this project, because the job spec keeps its arguments, plus your shell history if typed inline. Use a dedicated key and rotate it at the end; the exercises use Secret Manager.
The other way it goes wrong: a terminal where the key was never exported. Inside, its length is 0, and the arguments end with an empty key. So the job would download its data, and only then fail at login. Exit, export, and start again; first exit any old cockpit, which holds the name.

## 20:47 — Who submits, who runs
Three badges take part in every job. The first is your key file, for the model trainer service account. Its three roles let it write to your bucket and create jobs: it submits.
The third is your W and B key, for a different building altogether, carried by hand inside the job's arguments. The middle lanyard is still empty.
Something to ponder. The job installs your package from your private bucket, but your key file never left your laptop. How?
The second badge: your project's Vertex AI service agent, a service account Google manages. By default the job runs as it, and it can open buckets in the same project. Your key only proved who submitted. If a job ever gets a 403 on your bucket, that is the identity to grant access.
On Vertex, the job's first step installs your tarball into Google's image. We can't run Vertex here, so we rerun that step on the laptop, tagged as a stand-in. In a plain Python 3.10 container, pip installs the tarball: your package, plus wandb 0.15.11.
An extra pip list shows wandb, requests and their helpers, but no TensorFlow and no scikit-learn. The trainer counts on the prebuilt image for those, which we did not pull to check. Without it, the trainer cannot even print its help.
Then the trainer's first W and B step, line 153, with three keys. The empty key from scene 10 fails with api key not configured, and on Vertex that comes after the data download, on billed machine time. The default of 16 fails: API key must be 40 characters long, yours was 2. Our 40 character placeholder passes the offline length check, and nothing more.
One more: this old wandb pin accepts exactly 40 characters, and 47 fails. We could not check which key format W and B gives out today. If yours differs, this pin refuses it, so check before you submit.

## 23:05 — What the job prints, what W&B can show
To view jobs, open Vertex AI, then Training, then Custom jobs; pause and look for yours. It is a custom job, not a training pipeline, so look on that tab. Open your job and follow its logs link; wait for the line training job complete.
What will the job print? No job log exists for this video, so here is its shape, built from the code's own print lines. The counts are the ones both notebooks printed for the same code.
The labels line has no fixed order, as the two notebooks show, and no label map is saved. The summary ends with a stray None, because the code prints what summary returns. Training itself is a gap here, with no epochs, loss or times, then the line training job complete.
To view metrics, the README sends you to the W and B project cheese training vertex AI. It promises training metrics, tracked and updated automatically. To put it kindly, not with this code. From task.py, the run named after the model gets its config, including the execution time, and system charts, and its curve slots stay empty. Pause and open your project.
Something to ponder, with the lecture's list of seven. Which of them does this run actually keep?
The model and its settings, yes. The environment only partly: system charts, while the image tag sits in cli.sh. Metrics, none: the execution time goes into the config. Logs yes, weights no. Code, data and notes, no: no commit, a fixed zip, and an unseeded split. The folder from notebook A has no commit, no split and no notes either. So the verdict: these tables cannot crown a recipe. Seed the split, match the epochs, keep the code version, then compare. Exercise 1 adds a small callback.

## 25:09 — Three switches for one GPU
Now the reverse of the README's optional CPU step: what would it take to train on a GPU? Three switches must agree. The accelerator: one T4 in the worker pool spec. The image: TensorFlow built for GPUs, with CUDA, the GPU libraries. And the quota: T4s for custom training in this region. The chip lights only when all three are on.
The quota is the console request from scene 7. An extra check shows Google still serves both GPU images, at the time of recording.
To switch, uncomment the GPU block and comment out the CPU block. Leave both active, and you submit two jobs with the same name.
Here the GPU block would fail the same way as in scene 10, with no active account, so there is nothing new to show, and nothing we fake.
A gold tag: a GPU adds to the bill for as long as it is attached, used or not.
Something to ponder. You add the accelerator to the CPU block. The job runs, and its log says GPU available, with an empty list. Why?
Line 31 sets a CPU image, which has no CUDA. The T4 is attached, idle, and still billed. Exercise 5 lets you try it.

## 26:34 — Two GPUs, one model
The last idea of the lecture is multi-GPU training, in three shapes: one machine with one GPU, one machine with several, and several machines. Today is the middle one, the mirrored strategy. The single-GPU trainer also creates one, but only to count GPUs.
Here is the idea. Each GPU holds an identical copy of the model, called a replica. A global batch of 64, one step's worth, splits into two halves of 32. Each GPU computes gradients on its half. The two are averaged across a link called all-reduce, and both copies take the same step, so they stay identical. Variables created inside the scope are mirrored, one synced copy per GPU; a model built outside is not mirrored.
Review cli-multi-gpu.sh first, in README order; pause and open it. It asks for one n1-standard-32 machine with two T4s, for 5 epochs. A small slip: its TensorFlow image is older, 2.14, where cli.sh uses 2.17.
Then review the multi-GPU trainer; pause and open it. These are the lecture's three changes. It creates the mirrored strategy. It multiplies the batch size by the number of replicas. And it builds and compiles the model inside the scope of the strategy. Model fit is unchanged.
Something to ponder. Two GPUs, a batch size flag of 32, and 936 training images. How many steps per epoch, and how many images does each GPU see per step?
The global batch is 64, so 15 steps, the last one partial, and 32 images per GPU on each full step. Two caveats. The learning rate stays at 0.001 while the batch doubles. And two GPUs are not twice as fast, because start-up, image pull and download don't shrink.
You need quota for two T4s and 32 virtual CPUs of custom training in your region. A gold tag: this is the biggest machine of the lecture, so check the pricing page first. If your quota came through, pause and run sh cli-multi-gpu.sh. Here it fails like cli.sh, with no active account.

## 29:10 — The missing model, teardown and recap
One launcher the README never mentions is cli.py, the Python SDK route. As an extra run, it fails at once, because only cli.sh sets the region variable. Export it, and it fails at the missing key file.
And where is the trained model? When the script ends, the machine is deleted, and the weights with it: nothing calls model save, and the model dir flag is ignored. Lecture 15 saves the model to a bucket; exercise 4 does it today.
Time to shut down; pause and work through the list. From inside the cockpit, or in the console, make sure no custom job is running or pending. Remove the tarball and experiment folders too. Then exit; an extra docker ps shows nothing left. Finish the last W and B run, and disconnect the Colab runtimes. At the end of term, delete the model trainer key and rotate your W and B key, which traveled in a job.
The whole lecture on one map. A run is only as useful as what it keeps. Curves need a callback; config goes into wandb init. Only the tarball travels, into Google's image, run as the service agent, your key in its arguments. One GPU needs three switches; two GPUs split the batch and average gradients.
5 questions to test yourself. One: what did neither table write down? Two: what travels to Vertex AI, and what never does? Three: why is the config empty? Four: who submits, who runs, and where does your key end up? Five: with two GPUs, what is split, averaged, and created inside the scope?
Answers are in the exercises. Next, lecture 14 serves containers without servers, and lecture 15 saves this model and chains the steps. Hardware rented, and a log of what you rented it for.
