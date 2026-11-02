# AC215 · Lecture 13 — Advanced Training Workflows (exam edition)

## 00:00 — The run with no curves
Here is a training run that finished without a single error. The job succeeded, and the run exists in Weights and Biases. Its config is there, and so are its system charts.
But there is no loss chart, and no accuracy chart. Where are the curves? Here is the line that trained this model. Hold that thought; we come back to it in a few minutes.
The gray tag in the corner names the lecture slides behind each idea. On the lecture's roadmap, experiment tracking is set up early, together with the baseline models, right after data collection.
This is the exam edition of Lecture 13. It follows five places where a training workflow quietly breaks: the run record, the package, the GPUs, the batch, and the job itself.
Each part ends with one rule: if the question says this, think that. Three times, a quiz-style question appears on screen. Pause, pick an answer, and then hear why each wrong option is wrong.
The lecture names the reason to track at all. If the question says experiment tracking, think: what produced this result, and can I repeat it?

## 01:11 — What a run records
What should a run record hold? The lecture lists seven things: the environment, the code, the data, the model, the metrics, the artifacts, and your notes.
Most of these already have a home. Code lives in GitHub, data in a versioning system, and the environment in the pyproject file and the lock file. Weights, metrics and logs get a question mark.
One word on data. A data version is a pair: the archived snapshot in a bucket, and the version record that names it, linked by a content hash. This trainer instead downloads a fixed release of the data, and never writes it into the config.
Recording by hand gets forgotten, so the lecture automates it with Weights and Biases. Picture a ledger in which every training run is one row.
The repo trainer, task dot py, talks to that ledger in four calls. First it logs in with a key passed as a flag, never written in the code.
Then wandb dot init opens a new row, with a project, a name, and a config: learning rate, epochs, batch size, and model name. It also makes that row the active run, and the pointer called wandb dot run now points at it.
After training, the script adds one more config value, the execution time. Then wandb dot run dot finish seals the row, and the pointer falls back to nothing.
Notice what this run recorded on its own: the config, and system charts such as CPU and memory. It did not record a loss. Something still has to log the metrics.
If the question says record of a run, think: init opens it, a logger writes the metrics, and finish closes it.
First question. The run shows its config but no loss curve. Which change puts a loss curve on it? Three options can be ruled out with what you know already. Pause here if you want.

## 03:18 — The callback writes to the active run
The answer is C: pass the Wandb Metrics Logger in the callbacks of fit, created after init. A: a name only labels the row. B: one number in the config is not a history over epochs. D: logging in again writes no metrics.
A callback is a pen that Keras holds during training. At the end of every epoch it calls wandb dot log, and that call writes to wandb dot run: whichever row is active right now, not the run the pen was created with.
The lecture's notebook does exactly this. It calls init, and then fit, with a callbacks list that holds the Wandb Callback.
By default, that is one history entry per epoch. Per batch happens only if you ask.
Now four experiments. First, no pen. Fit runs two epochs, and the strip stays empty. That is our opening run.
Second: init, fit for two epochs, then fit for four more, with no finish in between. The pointer never moved, so ticks three to six land on the same row. One run, six entries.
Third: finish after the first fit, then init again, and fit four epochs with the same callback. The first row is sealed with two entries. The callback was made during row one, but it follows the pointer, so the new row gets entries one to four.
Fourth: finish, then fit again without a new init. The first epoch trains, and then the pen follows the pointer to nothing and stops with an error: you must call init before log. Nothing reaches any row.
Creating the logger with no active run fails at once.
Now the hook. The repo trainer imports both callbacks but passes none to fit, so its run has a config and system charts, and no curves. The lecture's middle line, the callback, is the line that is missing.
One detail: the notebook warns that the Wandb Callback is deprecated. For the curves, its replacement is the Wandb Metrics Logger.
If the question counts history entries, think: one per epoch, into whichever run is open when the epoch ends. A finish ends the count, and a new init starts a new one.

## 05:32 — What the package carries
The lecture moves training to the cloud in three steps: a Python file with arguments, a package in a bucket, and a training job on Vertex AI.
Here is the package folder: setup dot py, and a trainer folder with an empty init file and the two training scripts.
Setup dot py keeps two lists. Install requires is a shopping list that pip downloads from the Python Package Index; here, one pinned wandb version. Find packages decides which of your own folders get installed: only folders with an init file.
The packaging script tars the package folder, compresses it, and copies it into your bucket. The job script points Vertex AI at that file and names the module: trainer dot task.
Here is the key fact. Your own Docker image packages, uploads and submits, but it never trains. The job runs in Google's prebuilt training image, and your code reaches it only through the tarball.
That image already ships TensorFlow, scikit-learn and requests, so the trainer imports them although setup dot py never names them.
On the job machine, pip unwraps the tarball. The shopping list fetches wandb, and the trainer package is installed. Then Vertex runs python dash m trainer dot task.
Now add a teammate's module, augment dot py, a made-up example, beside the package folder. The script tars only that folder, so the module never leaves your laptop. Placed next to setup dot py instead, it travels, but find packages skips it.
The task reaches import augment; Python searches its import path and finds nothing. Module Not Found Error, right under the line that says every dependency installed. Locally it worked, because the file sat in the folder you ran from.
The fix: put the file inside the trainer folder, or list it in setup dot py. A new import line alone moves nothing; the file has to travel.
Adding it to install requires is wrong. That list downloads from the Python Package Index, never from your tarball, and a package there with that name would be someone else's code.
If the question says dependencies installed but Module Not Found Error, think: the file never travelled inside the package that setup dot py builds.

## 07:57 — One machine or many
The lecture sorts training hardware into three shapes. One machine with one GPU uses One Device Strategy. One machine with several GPUs uses Mirrored Strategy. Several machines use Multi Worker Mirrored Strategy.
The repo sits on the middle row. Its multi GPU script asks Vertex AI for one machine, type n1 standard 32, with two T4 GPUs. A replica count of one there means one machine.
The trainer creates the Mirrored Strategy and asks how many replicas are in sync: one per GPU, so two. Then it builds and compiles the model inside strategy dot scope, so every weight and optimizer variable is mirrored, one copy per GPU.
Here is one training step. Each GPU takes its own slice of the batch and computes a gradient. The gradients meet in an all-reduce and are averaged, and the same update goes back to both copies.
Now two machines, each running its own Mirrored Strategy on its own shard of the data. Inside each machine the ring works, but between the machines there is no wire. After a few steps they hold different weights: two separate models, not one.
To train one model across machines, use Multi Worker Mirrored Strategy. Each machine reads a TF config: the list of all the workers, and its own index in that list. Same shards as before; the only change is the wire, and now every copy stays the same.
The repo does not use it; on Vertex AI the extra machines would go in a second worker pool, and Vertex sets the TF config for you. One naming trap: the repo, like the lecture, calls its replica count num workers, but it counts GPUs on one machine.
If the question says several machines must train one model, think Multi Worker Mirrored Strategy with TF config. A Mirrored Strategy never looks past its own machine.

## 10:01 — Global batch, per-replica batch
Now the batch. Under a strategy, whatever dataset dot batch produces is the global batch, the whole tray for one step. The strategy cuts that tray into equal slices, one per replica.
So the per replica batch is the global batch divided by the number of replicas in sync. Turn it around, and the global batch is the per replica batch times the replicas.
Take 8 replicas, and say you want 16 examples on each. Batch by 16, and each GPU gets only 2. Batch by 128. Each GPU gets 16.
The repo does the same multiplication. It takes the batch size flag, multiplies it by the replica count, and hands the product to the data pipeline. Its own comment says it: batch expects the global batch size.
Second question. The repo's multi GPU trainer now runs on 4 GPUs, with a batch size flag of 32. What is the global batch, and what does each GPU see per step? Pause here if you want.
The answer is B. The trainer multiplies first: 32 times 4 is 128, and the strategy splits 128 four ways, so each GPU sees 32. A: that is a script that never multiplied. C: the flag is the per replica size, not the global batch. D: the global batch is split, not copied to every GPU.
If the question says per replica, multiply before you batch: the global batch is the per replica batch times the replicas.

## 11:52 — Training that outlives the request
Last mechanism. Suppose a web app has a retrain button, and training takes an hour. Where should that hour run?
Every piece of work lives as long as the thing that holds it. Inside the request handler, it dies at the request timeout.
In a server thread, it lives only as long as that server instance, which the platform recycles whenever it likes.
A longer client timeout moves the wrong clock. The server and the proxies still cut the request, and a sleeping laptop loses the answer anyway.
And W and B is not a clock at all: it logs runs, but has no engine to execute them.
The right design: the handler submits a durable job and returns its id at once. The job moves through its states, queued, pending, running, succeeded, on its own machine, billed only while it runs. Anyone with access to the project can poll the id.
That is the lecture's serverless training: hardware rented only for the training step, and no server to manage. There is still a machine; you just do not own its lifetime.
In the repo, the ticket is one command, gcloud AI custom jobs create, with a region, a name, the package in the bucket, and a worker pool: machine type, replica count, prebuilt image, and module.
Third question. Your custom job shows running, and you close the laptop for the night. What happens to the training? Pause here if you want.
The answer is B: it keeps running on its own machine until it finishes or fails. A: the CLI container only submitted it. C: W and B only logs; it never drives training. D: nothing on your laptop holds the job's state.
If the question says training takes longer than the request, think: submit a durable job, return its id, and poll. W and B only watches.

## 14:03 — Six rules for Tuesday
Six rules for Tuesday. Rule one: a callback logs one entry per epoch into the active run; init opens a run, and finish closes it.
Rule two: pip installs only what setup dot py declares; your own modules must be inside the package it builds, not just inside the tarball.
Rule three: a Mirrored Strategy covers the GPUs of one machine; across machines, use Multi Worker Mirrored Strategy with TF config, because separate strategies make separate models.
Rule four: under a strategy, what dataset dot batch makes is the global batch, split across the replicas in sync.
Rule five: long training goes to a durable job with an id, never into a request handler, a thread, or a longer timeout.
Rule six: a data version is an archived snapshot plus the record that points at it.
The lecture began with three levers for better deep learning: more data, better models, and faster hardware. Today was the hardware lever, plus the bookkeeping that shows whether it helped. Good luck on Tuesday.
