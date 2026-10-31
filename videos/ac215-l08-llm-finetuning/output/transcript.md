# AC215 · Lecture 8 — LLM: Finetuning (follow-along: llm-finetuning)

## 00:00 — Why is the sky blue?
Why is the sky blue? We asked two versions of the same small language model. Both answers come from the course staff's saved Colab run.
The original answers like a textbook. The fine-tuned one opens with a cheesy greeting in the instructor's voice, and then explains.
Now check the physics. One blames refraction, the other water molecules. Both are wrong: air molecules scatter blue light more than red. The voice changed completely; the facts did not get better.
Chat models learn their habits the same way; the lecture shows one that starts with the words, sure, here's. This one kept 596 million weights frozen and trained 1.15 million new ones. It took about 3 and a half minutes on an A100, and fits in a file of about 4.6 megabytes.
So what did it learn, and what didn't it? Two tracks answer that. In track A, the README, Gemini writes a persona dataset and Google tunes Gemini for you. In track B, the course Colab, you fine-tune an open model yourself and keep the weights.
The tracker, top left, shows the step; the gray tag, top right, shows the lecture slides. When a tag says your turn, pause and run the command.
One honest limit: we recorded this on October 31, 2026, with no service account key and no GPU. Every README command ran exactly as written; the ones that talk to Google stop at the missing key, and we keep those real errors. Working outputs come from the README and the saved Colab run.

## 01:42 — Three dials: prompt, context, weights
There are three ways to change what a model says. A prompt changes the input every time you ask. Retrieval, the RAG app from lecture 5, adds looked-up text to the input. Both leave the model itself untouched.
Fine-tuning turns the third dial: it changes the weights, by showing the model many examples of an input and the output you want. In this course that usually means instruction fine-tuning: pairs of an instruction and its answer. A persona is a task-specific fine-tune.
Compare a model that was never instruction-tuned. The notebook gives OPT 350m the words, hello, my cheese name is. It simply keeps going: my cheese name is cheese, I'm not sure if you're joking or not.
An instruction-tuned model answers instead of continuing, often with a habit like, sure, here's. Our fine-tuned Qwen answers the way the instructor would. That's the lesson of the saved run: style is learnable; facts are not guaranteed.
A useful mental model: fine-tuning moves the model's default voice; RAG changes the open book on its desk. In track A, Google trains the model and you never see a weight. In track B, you train a small adapter on a Colab GPU, and it is yours to save.

## 03:04 — A key next to the repo
Start in your workspace, the AC215 folder, with Docker installed and running. The README only links the repository, so cloning it is an extra step. Your prompt shows your own user name and machine.
Recorded at the commit on screen; yours may be newer. Inside are two folders, dataset-creator and gemini-finetuner, each with the same six files. The autotrain folder is not part of the README, so leave it alone.
Step 2 happens in the cloud console. Create a service account called llm-service-account with two roles: Storage Admin, and Agent Platform User, formerly Vertex AI User. Under keys, add a JSON key, which downloads to your laptop. If you kept the account from lecture 5, reuse it.
Step 3: make a folder called secrets next to the repository, not inside it. Move the key in and name it exactly llm-service-account.json; with hidden file extensions it can end up as dot json dot json. Ours stays empty on purpose. Watch what that does.
Why next to the repository? A key outside the clone can never be committed by accident. The env.dev file looks two folders up from wherever the script runs, so both container folders reach the same key.
An extra step 4, implied by the file's own comments: in env.dev, set your own project ID and bucket name on lines 6 and 7. The scripts pass both into the containers.
The README also assumes the Agent Platform and Storage APIs are enabled, and a bucket of your own. Bucket names are global, and cheese-dataset belongs to the course. Pause here and finish all four steps.

## 04:56 — The dataset-creator container
Step 1 of the dataset section: go into the dataset-creator folder. Step 2: sh docker-shell.sh. The first build installs everything. Here it took 45 seconds on a fast connection; expect a few minutes. If you see source, not found, the fix is coming.
What did the script do? It reads env.dev, builds the image, and runs it with two folders mounted: this folder becomes slash app, and your secrets folder becomes slash secrets. Three variables carry the key's path, your project and your bucket. The dash dash rm flag removes the container when you exit.
Read the banner kindly: it says activated before the activation line runs, and the prompt never shows an app prefix. Both are harmless; an extra check shows Python comes from slash dot venv, and your settings arrived. The part after app and the at sign is the container ID; yours will differ.
Step 3 is the README's tip: ls dash la slash secrets, inside the container. With a key, you'd see llm-service-account.json here. Ours shows only the folder itself, on purpose.
Step 4: python cli.py dash dash help. Three flags: generate, prepare and upload. It works without a key, because the code only looks for credentials when it first calls Google. Pause, and get to this prompt.
Two traps, shown as extras from a second terminal. On Debian, Ubuntu or WSL, sh is dash, which has no source command: run bash docker-shell.sh instead. And from the repository root, the script cannot find env.dev: cd into the folder first.
One more extra: docker images reports 1.64 gigabytes. The lockfile installs 133 packages, among them the RAG lecture's chromadb and langchain, which this code never imports.

## 07:05 — Manufacturing a persona
The lecture's instruction dataset has three parts per example: an instruction, optional context, and the output you want. The tutorial drops the context: each example is a question and an answer. Who writes a hundred of them? Another model, a teacher.
Here the teacher is Gemini 3.1 Flash Lite, called in the global location. It gets a system instruction describing the persona, an input prompt asking for 20 pairs, and a JSON schema that fixes the answer's shape: question and answer objects.
Step 1: python cli.py dash dash generate. With a key, it costs cents: the README estimates 2 dollars per 1,000 iterations. Without one, every batch prints the same line: the key file was not found. And yet the exit status is zero, which means success. Remember that zero.
Step 2 explains the system prompt, which lives in cli.py. It tells the teacher to open each answer with one of the instructor's catchphrases, such as good question, or glad you ask. And it asks for technical, passionate answers.
Step 3 is the input prompt, asking for 20 diverse pairs. Step 4: the number of iterations is a constant on line 170, not a flag; edit it for a bigger dataset. Temperature 0.9 adds variety, and the response schema makes Gemini return JSON in that shape.
With a key, the files would hold answers like the README's samples: Yello, this is the instructor, your cheese monker. A small slip: the README's prompt excerpt lists older openers than cli.py, but cli.py's own samples still open with Yello and Welcome. Expect a mix.
One question before we move on. The prompt asks the teacher for specifics, such as optimal pH levels.
It becomes a training target. The student learns to say it, confidently, in the instructor's voice. Synthetic data carries the teacher's mistakes, so check what the teacher wrote.

## 09:26 — Prepare: a failure that surfaces late
Now step 1 of the prepare section, as a student would type it right after that run: python cli.py dash dash prepare. Zero errors, a shape of zero by zero, and then a crash: key error, question, from line 243 of cli.py.
Trace it back. In generate, each batch runs inside a try block, and the except on line 200 catches any exception, prints it, and carries on. So no file was written, and the command still exited with zero.
Prepare found no files, built an empty table, and failed the first time it read the question column. The error was there all along; the catch-all only moved it one command later. Read the lines, not the exit code.
The fix is the key itself: put it in the secrets folder with the exact name, and check with ls dash la slash secrets.
So we can watch a real run, an extra: five hand-written files, tagged scripted, in exactly the shape Gemini returns. They hold 20 pairs, where Gemini would write about a hundred; your generate writes its own. Note the 1-byte CSV the failed run left behind.
Now prepare again. Five files processed, zero errors, and a shape of 19 by 2. The last scripted pair repeats the first question on purpose, and drop duplicates on line 233 removed it. Every answer opens with a catchphrase.
The rows are saved as instruct-dataset.csv: the lecture's term, in the file name. Pause, and run generate and prepare yourself.

## 11:10 — Rows to JSONL, then upload
Step 2 of prepare is about format. Follow one pair. It starts as a CSV row. Lines 241 to 247 glue it into one text with human and bot labels, the text column the repository's autotrain folder reads. Track A doesn't use that one.
Lines 251 to 257 build what Gemini tuning expects: a list called contents, with a user turn and a model turn, each holding parts and text.
An extra look at the real train.jsonl: the same nesting as the README's example, but each example on a single line. That's the L in JSONL: JSON lines.
Then train test split holds out 10 percent with a fixed seed: 17 examples for training, 2 for validation. The code's comment says Gemini accepts at most 256 validation examples, hence the cap.
Whatever the wrapping, training is still next-word prediction, now on the instructor's answers.
An extra from the laptop side: the bind mount left these files in your clone. Git status shows the data folder as ignored, so it stays out of your commits.
Next section, upload: python cli.py dash dash upload. This time it fails loudly, with a default credentials error: file not found. With a key, no output is documented. Look for one line per file starting with uploading file, five in all, then find them in your bucket.
A small slip: the README never says to create that bucket, and upload assumes it exists. Make it first. If you just changed env.dev, restart the container. Then pause and upload.

## 13:03 — Hand it to Google: the tuning job
On to the fine-tune section. Type exit; the container removes itself, and an extra docker ps dash a shows nothing left. Step 1: go to the gemini-finetuner folder.
An extra edit the README leaves out: lines 10 and 11 still point at the course bucket, cheese-dataset. Point them at your own. The folder is mounted into the container, so there's no need to rebuild.
Step 2: sh docker-shell.sh again. It's instant: every layer up to uv sync is cached, because both folders share the same Dockerfile, pyproject and lockfile, as an extra diff shows.
Step 3: python cli.py dash dash help shows two flags, train and chat. The train client creates tuning jobs in us-central1. The chat client calls the tuned model in the multi-region location US, at its own address.
The train function wraps your bucket files as tuning datasets, and asks for one epoch and an adapter of size four. By our reading, that's Google's managed version of the idea you'll build in part 2. One call starts the job.
Step 1 of the fine-tune model section: python cli.py dash dash train. The experimental warning is harmless. Then the missing key: no job was created.
With a key, look for training job started, a job name in us-central1, and after a minute, tuned model info, none. Main calls train with wait for job set to false, so the command hands in the job and leaves, like a ticket at the dry cleaner. Read the cost table next, then pause and start your job.
Training needs far more GPU memory than a laptop has; here that's Google's problem. Step 2: watch the job in the console until it says succeeded, with a tuned model and an endpoint.
A question to pause on.
On Google's hardware in us-central1, reading your bucket directly. Deleting the container loses nothing: it only submitted the job.

## 15:22 — Cost, endpoint and chat
Step 1 of the cost section: the README's table. At 0.008 dollars per thousand tokens, 16,444 documents over 3 epochs come to 112 dollars 73; the table calls that way too much data. 88 documents cost about 57 cents.
A small slip: the table prices Gemini 1.5 Flash for 3 epochs, while the code tunes Gemini 3.1 Flash Lite for 1. Treat these numbers as stale and check the pricing page the README links.
Before you chat, one more extra edit. Line 107 still holds the instructor's endpoint. Copy yours from the console: a path ending in locations, US, endpoints and an ID. Paste it there; otherwise chat points at the instructor's endpoint, which your key can't reach.
Step 2: python cli.py dash dash chat. It prints its question, how is cheese made in Greece, answered the instructor's way. Then it prints the serving location, US, and the same missing key. Pause and run it once your endpoint is in.
The README shows a working endpoint's answer to an older question: the same Yello opener. Your answer will differ.
Step 3, the hosted demo, is optional. Step 4: the console's training monitor shows your job's loss curves and its data distribution.
That's track A: a teacher wrote the data, Google ran the job, and you have an endpoint to call. And you never saw a single weight. In part 2, the weights are in your hands.

## 17:05 — Colab, and the 120 GB bill
Part 2 happens in the course Colab, Tutorial, Finetuning with QLoRA. First: File, Save a copy in Drive; the original is view-only. Then: Runtime, Change runtime type, and pick a GPU. A free T4 is enough.
Section 3 pins transformers, bitsandbytes and trl, and removes torchao, which, the notebook notes, makes peft refuse to add LoRA layers.
Section 4 reads your Hugging Face token from Colab secrets; both models are public, so it matters mostly for the optional upload. Section 5 imports the libraries, prints the versions, at the time of recording torch 2.11 and transformers 5.16, and mounts your Drive. Section 6 caches both models there. Pause and run part A.
Now the lecture's question. Why not simply train all the weights? Take a model with 10 billion parameters in 16-bit floats: the weights alone take 20 gigabytes.
The gradients, one per weight, take another 20 gigabytes. And the Adam optimizer keeps two running averages per weight in 32-bit floats: 80 gigabytes. That's 120 in total, the memory of five GPUs with 24 gigabytes each, before any activations.
LoRA trains only small adapters, so gradients and optimizer states nearly vanish, but the frozen base still sits in memory for the forward pass. The lecture puts that at about 40 gigabytes. QLoRA stores the base in 4 bits, and the lecture's total drops to about 12. The next chapters are those three bars.

## 18:59 — Quantization: 16 buckets per weight
Quantization means splitting a range into buckets and storing only which bucket a number fell into. The lecture builds LoRA first; we follow the notebook, which quantizes first.
Round 27, 55.3 and 83.78 to whole numbers: 27, 55 and 84. Round to tens: 30, 60 and 80. Fewer buckets need fewer bits, and lose more detail.
The lecture's worked example uses absmax. Ten values from 1.5 to 10.2 are multiplied by 127 over the largest, so 10.2 lands exactly on 127. Then each value rounds to an integer: 1.5 becomes 19, and 5.6 becomes 70.
Divide back, and 19 becomes 1.526, 70 becomes 5.622. Those small red gaps are the dequantization error: quantization always loses a little. The slide shows 18 and 69; rounding gives 19 and 70.
One constant for a whole matrix is risky: one large weight squashes everyone else's precision. So bitsandbytes keeps one absmax constant per small block of 64 weights.
Four bits give 16 levels. Weights are bell-shaped, so 4-bit NormalFloat, NF4, puts them at quantiles: dense near zero, sparse in the tails. Each weight is stored as a 4-bit index; two of them fit in one byte.
Those block constants add up, so double quantization quantizes them as well. The lecture skips it; the notebook turns it on, right here, beside NF4.
Stored in 4 bits, computed in 16: for each matrix multiply, the layer's weights are expanded to a 16-bit copy, used, then dropped. The lecture computes in BF16; this notebook in FP16, as the training chapter explains.
Section 1 of part B prints the small OPT model: every linear layer is now Linear4bit, while the embeddings and the output head stay as they were. Section 2 tokenizes and generates the continuation we met earlier. Pause, and run part B.
Two misconceptions to drop: a 4-bit model does not do 4-bit arithmetic, and the win is memory, not speed.

## 21:31 — Qwen in 4 bits, and its chat template
Step 1 loads the real student, Qwen3 0.6B, with the same 4-bit recipe. Then prepare model for k-bit training freezes every weight and turns on gradient checkpointing, a memory trick the training chapter shows.
Section 2.1 counts the parameters: 375.8 million. But Qwen3 0.6B has 596 million.
The 440 million weights in linear layers are packed two 4-bit values to a byte, so they count as 220 million. The 155.6 million embedding weights and the norms are not quantized. Add them up: 375.8 million. The configuration, in 2.2, confirms NF4.
In 2.3 the base model continues a sentence, and it drifts off topic. And 2.4 counts trainable parameters: zero. Everything is frozen.
The notebook's step 3 prepares the data. It downloads a 23 megabyte file and samples 1,000 pairs. Look at a row: contents, a user turn, a model turn. It's exactly the format of track A: the brick from part 1 arrives here.
Section 3.5 lets the tokenizer write Qwen's chat template: im start user, the question, im end, im start assistant, an empty think block, and the answer. The empty think block is how Qwen3 answers without thinking, and chat uses the same prefix later.
Section 3.6 splits 900 for training and 100 for testing, and 3.7 checks one example. Then the ribbon becomes integers, and the loss covers every token, question and template included. It's still next-word prediction. Pause, and run steps 1 to 3.

## 23:39 — LoRA: a thin correction
Parameter-efficient fine-tuning trains a small part and freezes the rest. The lecture sorts the methods into three families: additive, selective and reparameterization. LoRA is a reparameterization.
Start small. A 5 by 5 matrix has 25 numbers. A 5 by 1 column times a 1 by 5 row also makes a 5 by 5 matrix, from only 10 numbers. That's rank 1; rank 2 needs 20. At this size it's barely a saving.
At real size it's different. Qwen's query projection is a 2,048 by 1,024 matrix: over 2 million numbers. A rank 8 pair of strips, 2,048 by 8 and 8 by 1,024, holds 24,576.
So LoRA decomposes the update, not the weights. The new layer is the frozen W naught, plus alpha over r, times B times A. Only B and A are trained.
B starts at zero and A at random. The lecture draws A from a normal distribution; the library uses a uniform one. What matters is that B times A starts at exactly zero, so at step zero the model is the pretrained one. Both branches' outputs add.
Now the notebook's step 4, the LoRA config: alpha 16 and rank 8, so the update is scaled by 2, plus a dropout of 0.1 for regularization. Pause and run it.
Which layers? The config names no target modules. So for Qwen3, the PEFT library's default adapts the query and value projections: two of the seven matrices in each of the 28 blocks. That's 40,960 per block, 1,146,880 in all.
The lecture's table treats a whole model as one square layer; the real count depends on these shapes. Now, try it yourself.
Rank 16 doubles it, to 2,293,760. All seven projections at rank 8 give 5,046,272. More rank buys capacity at more memory and time; for a persona, rank 8 on two projections is plenty. To try it, reload the model in 1.3 first.

## 26:18 — Training on a small GPU
Back to the memory column, at Qwen's size, by our own estimate. Full fine-tuning would need about 7 gigabytes before activations; this notebook's QLoRA, under 1. At 0.6 billion parameters, even full fine-tuning would fit a T4. The recipe matters because the same notebook scales to models that wouldn't.
The rest of the memory goes to activations, the values each layer computes on the way forward, kept for the backward pass. Gradient checkpointing keeps only a few and recomputes the rest when needed: compute traded for memory.
Step 2, the training arguments. Sequences are capped at 512 tokens and grouped by length: 2 epochs, batches of 4, and a learning rate of 2 times 10 to the minus 4. The optimizer is a paged 32-bit Adam. Paging moves optimizer state to CPU memory when the GPU fills up. Ours never needs to.
Then fp16 on and bf16 off. BF16 keeps the range of float 32 with less precision, and the lecture uses it for QLoRA. The T4 has no fast BF16, so this notebook computes in FP16.
Step 3 builds the trainer. The trainer turns the adapters into BF16, which FP16 training cannot unscale, so this cell casts them back to float 32. And the count confirms our arithmetic: 1,146,880 trainable parameters, 0.3 percent.
In the backward pass, the gradient flows down through W naught, and only B and A are updated. W naught is used on the way down; it just gets no gradient and no update.
Step 4, train: 900 examples in batches of 4 for 2 epochs is 450 steps, 3 minutes and 36 seconds on the saved A100 run. The notebook says 6 to 7 minutes on a T4. The loss falls from 2.0 to 1.35. Step 5, TensorBoard, shows these curves in your own run. Pause and train.

## 28:36 — Did it work? Perplexity and the sky
Did it work? Step 1 measures it. Perplexity is the exponential of the average token loss: roughly how many equally likely next tokens the model is choosing among.
On 100 test examples, 30,681 tokens, the base model has a loss of 2.65 and a perplexity of 14.15. The fine-tuned model: 1.39, and a perplexity of 4.
The base row is the same model inside disable adapter. Switch the adapter off and the original model, in 4 bits, is back, because W naught never changed. That's the lecture's point about catastrophic forgetting, losing old skills while learning new ones: with LoRA, the old model is one switch away.
In the saved run, every base answer starts with the word the. The fine-tuned ones start with welcome or Yello, the openers of its training data. Those bars are an illustration; the measured numbers sit beside them.
What does the drop measure? The loss counts every token, questions and template included. It says this style is what the model now expects, not that its answers are more correct.
Step 2 compares answers. Both cheese answers now open with welcome welcome welcome, cheese lovers, in the instructor's voice. And the sky: the voice transferred, the physics did not. Pause, and run step 5.
Two kind notes. In this comparison the base is a fresh 16-bit model, not the 4-bit one from the table, so the baselines differ. And the lecture shows LoRA matching full fine-tuning on a published benchmark; this notebook measures style fit, not answer quality.

## 30:25 — Ship it, tear down, recap
The notebook's step 6 saves your work. First the adapters: 1,146,880 numbers, about 4.6 megabytes in float 32, saved to your Drive with the tokenizer.
Then the merge. The notebook loads a fresh 16-bit copy of the base and adds B times A into it. Not into the 4-bit weights: there, the update would round back onto 16 levels. The merged model is about 1.2 gigabytes.
Step 3 can push the merged model to a private Hugging Face repository. So you can ship three things: an adapter that needs its base, a merged model that stands alone, or Google's endpoint, with no weights in your hands.
Teardown. Exit the container and remove both images with docker image rm. Delete the dataset folder in your bucket. Keep the tuned model and endpoint for lecture 10, then delete them. Delete unused service account keys, and disconnect and delete the Colab runtime. Pause, and tear down.
Here's where we are. Prompts and retrieval change the input; fine-tuning changes the weights, and here it taught a voice, not facts. In track A, a teacher wrote the data and Google tuned the model. In track B, QLoRA froze a 4-bit base and trained two thin matrices: 120, then 40, then 12 gigabytes.
Five questions to test yourself. What did this fine-tune change, and what not? Why did generate exit zero without a key? Which shapes does one pair take on its way to the template? Why does train print tuned model info, none? And where does 1,146,880 come from?
Next, lecture 9 tests code, and in lecture 10 an app calls your endpoint. The study guide and the exercises are in MLOps Learning.
