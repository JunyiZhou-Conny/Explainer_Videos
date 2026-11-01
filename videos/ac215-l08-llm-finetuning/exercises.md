# Exercises · AC215 L8 — LLM: Finetuning

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real: the captures from October 31, 2026
(`assets/terminal/`; `laptop/…`, `dataset-creator/…`, `gemini-finetuner/…` and `expected/…` name files there), or
checks run the same day in throwaway containers of the tutorial's base image (`python:3.12-slim-bookworm`) with the
packages `cli.py` imports at the exact versions of the repo's `uv.lock` (pandas 2.3.3, scikit-learn 1.7.2,
google-genai 1.39.1, google-auth 2.41.1, google-cloud-storage 3.4.1), and, for the LoRA counts, the notebook's
pinned transformers 5.16.1 with peft 0.20.0 on a CPU. [`assets/exercise-checks/README.md`](assets/exercise-checks/README.md)
lists every command; a file name ending in `.log` below is one of its [`logs/`](assets/exercise-checks/logs/).

There was **no service-account key and no GPU**. Every hands-on task in Part B runs **offline and free** in the
`llm-dataset-creator` container (or with plain Python), except the ones marked *with your key* (billed: Gemini calls,
tuning) or *in Colab* (a GPU runtime). For those, the answers come from the code, the README (`expected`) or the
course staff's saved Colab run on an A100 (`recorded`), and say so. Anything marked **scripted** is hand-written
stand-in data in the shape `--generate` writes, never Gemini's output. The persona is the instructor's voice; the
instructor's name is written `‹instructor›` here.

**Working with data/ safely.** `--prepare` always reads `data/cheese_qa_*.txt` and overwrites the five output
files. Before Part B, park your real files on the laptop side: in `~/AC215/llm-finetuning/dataset-creator`, run
`mv data data.mine` (bring them back afterwards with `rm -r data && mv data.mine data`). The five scripted files the
video uses are not in the repo: any five `cheese_qa_N.txt` files in the right shape will do, and B2 shows how to make
some. **Running a Python snippet:** save it in the `dataset-creator` folder (it is `/app` in the container) and run
`python <name>.py` at the container prompt. Don't name a scratch file after a standard-library module (C10 shows
why).

---

## Part A · The five questions from the end of the video

**Q1. What did this fine-tune change, and what didn't it? Use the sky.**

<details><summary>Answer</summary>

The staff's saved run (5.2, `expected/colab-c82-base-vs-finetuned.txt`) asks both models "Why is the sky blue?".
The base model answers like a textbook and blames **refraction** ("**Light Refraction**: When sunlight enters the
atmosphere, it bends (refracts)…"). The fine-tuned model opens in the persona's voice ("Yello - this is
‹instructor› your cheese monker, ready to unravel the mystery of the sky's blue!") and blames "the scattering of light
by the **water molecules** in the atmosphere". Both are wrong: air molecules scatter short (blue) wavelengths much
more than long (red) ones, which is Rayleigh scattering.

- **Changed:** the style. The model learned the training data's openers, tone and length habits; on the 100 test
  examples the loss fell from 2.6498 to 1.3872 and the perplexity from 14.15 to 4.00 (5.1,
  `expected/colab-c80-eval-loss-perplexity.txt`): the persona's text is now what the model expects.
- **Not changed:** the facts. 900 persona-flavoured answers taught a voice, not physics, and the loss counts every
  token (questions and template included), so a lower perplexity doesn't mean more correct answers. The frozen
  weights W₀ didn't change either: inside `disable_adapter()` the original 4-bit model is back (`cell-80.py:54`).

Fine-tuning reliably moves the model's default voice and habits; for facts, use retrieval (L05) and check them.
</details>

**Q2. Why did `python cli.py --generate` exit with status 0 without a key, and where did the error finally show up?**

<details><summary>Answer</summary>

The genai client looks for credentials only on its first request. Each of the five batches raises google-auth's
`File /secrets/llm-service-account.json was not found.`, and the `except Exception as e:` at
`dataset-creator/cli.py:200-201` catches it, prints `Error occurred while generating content: …` and goes on to the
next batch. Nothing re-raises, so the program ends normally: exit status 0 (`dataset-creator/05`). No
`cheese_qa_*.txt` is written; `data/` exists, empty (`os.makedirs`, `cli.py:167`; `dataset-creator/06`).

The error surfaces **one command later**: `--prepare` finds no files, prints `Number of errors: 0`, `[]` and
`Shape: (0, 0)`, builds an empty table, saves a 1-byte `instruct-dataset.csv` (a single newline) and then crashes at
`cli.py:243`, the first read of the `question` column: `KeyError: 'question'`, exit 1 (`dataset-creator/07`;
reproduced in [`q2.log`](assets/exercise-checks/logs/q2.log)). Read the lines, not the exit code. The fix is the key:
`~/AC215/secrets/llm-service-account.json`, exact name, checked with `ls -la /secrets` in the container.
</details>

**Q3. Which shapes does one question–answer pair take on its way to Qwen's chat template?**

<details><summary>Answer</summary>

1. **An object in Gemini's JSON reply**, `{"question": …, "answer": …}`, one of about 20 in an array saved as
   `data/cheese_qa_N.txt` (the response schema, `cli.py:146-160`; written at `:196-199`).
2. **A table row**: `--prepare` merges the files into a pandas DataFrame, drops duplicate questions and empty rows
   (`:233-234`) and saves `instruct-dataset.csv` with the columns `question,answer` (`dataset-creator/13`).
   (`train.csv`/`test.csv` hold a `human: … \nbot: …` text column for the unused `autotrain-runner`.)
3. **A JSONL line** in Gemini's tuning format, one example per line (`:251-257`, `:270-273`):
   `{"contents":[{"role":"user","parts":[{"text":"<question>"}]},{"role":"model","parts":[{"text":"<answer>"}]}]}`
   (`dataset-creator/11`, `12`). `--upload` copies it to your bucket, and the tuning job reads it from there.
4. **In the Colab**, the staff's `train_16k.jsonl` has the same `contents` format (3.2,
   `expected/colab-c53-sample-1000.txt`); 3.3 pulls `question` and `answer` back out (`expected/colab-c55-…`).
5. **Chat-template text** (3.5, `tokenizer.apply_chat_template`, `cell-59.py:10-13`):
   `<|im_start|>user\n<question><|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n<answer><|im_end|>`
   (`expected/colab-c63-one-example.txt`). The empty think block is how Qwen3 answers without thinking.
6. **Token IDs**, which the trainer predicts one at a time. With a plain `text` column and trl's defaults, the labels
   are the input IDs themselves, so the loss covers every token, question and template included (trl 1.14.0's
   `sft_config.py:259-280`, `sft_trainer.py:1625-1652`, read in [`trl-source.log`](assets/exercise-checks/logs/trl-source.log)).
</details>

**Q4. Why does `python cli.py --train` print `Tuned model info: None`, and where do you get the endpoint?**

<details><summary>Answer</summary>

`main()` calls `train(wait_for_job=False)` (`gemini-finetuner/cli.py:126`). `train_client.tunings.tune(...)`
(`:61-65`) only submits the job to Google in `us-central1` and returns at once; the script prints
`Training job started. Monitoring progress...` and `Job name: …` (`:67-68`), sleeps 60 seconds (`:71`), fetches the
job again (`:72`) and, because `wait_for_job` is false, skips the polling loop (`:74-87`). A minute in, the job is
still queued or running, so it has no tuned model yet: `Tuned model info: None` (`:89`), and the hint that tells you
to paste the endpoint (`:90-96`) never prints. The container only submitted the job; training goes on at Google.

The endpoint comes from the console: Agent Platform › Tuning (`README.md:261`), once the job says succeeded. Copy
the path `projects/<your-number>/locations/us/endpoints/<id>` into `MODEL_ENDPOINT` (`cli.py:107`, which still holds
the instructor's endpoint), then run `--chat`. Or set `train(wait_for_job=True)` and let the script poll (B8).
*(Predicted from the code: without a key, `--train` stops at the missing key, `gemini-finetuner/02`.)*
</details>

**Q5. Where does 1,146,880 come from, and what does QLoRA keep in GPU memory in this notebook?**

<details><summary>Answer</summary>

LoRA adds, beside each adapted matrix W₀ (out × in), two trainable strips A (r × in) and B (out × r): r × (in + out)
numbers. The config in 4.1 sets r = 8 and names no `target_modules`, so PEFT uses its default for Qwen3: `q_proj` and
`v_proj` ([`peft.log`](assets/exercise-checks/logs/peft.log)). Qwen3-0.6B's shapes (2.2, `expected/colab-c42`):
hidden 1,024; 16 query heads × 128 = 2,048; 8 key-value heads × 128 = 1,024; 28 layers.

- `q_proj` 1,024 → 2,048: 8 × (1,024 + 2,048) = 24,576
- `v_proj` 1,024 → 1,024: 8 × (1,024 + 1,024) = 16,384
- per block 40,960; × 28 blocks = **1,146,880**

The trainer cell prints exactly that: `trainable params: 1146880 || all params: 376995840 || trainable%:
0.3042155584528466` (4.3, `expected/colab-c72`). The same count came out of PEFT 0.20.0 on Qwen3's shapes
(`peft.log`) and of plain arithmetic ([`snippets.log`](assets/exercise-checks/logs/snippets.log)).

What sits in GPU memory while it trains:

1. **The frozen base.** Its 440.4 million linear weights in **NF4**, two 4-bit values per byte (about 0.22 GB), with
   one absmax constant per block of 64 weights, those constants quantized again (double quantization). The 155.6
   million embedding weights (shared with the output head) and the norms are not quantized;
   `prepare_model_for_kbit_training` casts them to **float32** (about 0.62 GB; peft's source in `peft.log`).
   For each matrix multiply, a layer's 4-bit weights are expanded to a 16-bit copy, used, and dropped.
2. **The adapters A and B**: 1,146,880 numbers in **float32** (the trainer cell casts them back from BF16,
   `cell-72.py:10-14`), their gradients, and the paged 32-bit AdamW's two states each: about 18 MB in all.
3. **Activations** for the backward pass, computed in **FP16** (`bnb_4bit_compute_dtype`, `fp16=True`), most of
   them dropped and recomputed by gradient checkpointing (turned on in 1.3).

By our estimate that is under 1 GB plus activations (full fine-tuning: about 7 GB before activations). These are
estimates from the shapes; the saved run's peak memory was not recorded.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Two broken batches.** Next to five good `cheese_qa_0..4.txt`, add a sixth batch wrapped in a Markdown fence
and a seventh that stops mid-answer, the way a reply cut off by `max_output_tokens` does:

```bash
printf '```json\n[{"question": "What is the rind of Camembert made of?", "answer": "Good question! A bloomy white mould. (scripted)"},\n {"question": "Why is Halloumi good for grilling?", "answer": "Glad you ask! Its high melting point. (scripted)"}]\n```\n' > data/cheese_qa_5.txt
printf '[{"question": "What is a washed-rind cheese?", "answer": "I have slides for that! Brine. (scripted)"},\n {"question": "How long is Comte aged?", "answer": "Remember rule number 672, at least four months, and the best' > data/cheese_qa_6.txt
python cli.py --prepare
```

Predict `Number of errors`, the shape, and the line counts of `train.jsonl` and `test.jsonl` (start from your
own count of good rows, N).

<details><summary>Answer</summary>

The fence is harmless: `prepare()` deletes every `` ```json `` and `` ``` `` before parsing (`cli.py:219`), so both
pairs of batch 5 count. Batch 6 is invalid JSON: `json.loads` fails, the whole file is skipped (even its complete
first pair) and recorded as one error (`:221-226`). With the video's 19 scripted rows the check printed
`Number of errors: 1`,
`[{'file': 'data/cheese_qa_6.txt', 'error': 'Unterminated string starting at: line 2 column 52 (char 154)'}]`
(the string that never ends: the last answer), `Shape: (21, 2)`, and `train.jsonl` 18 lines, `test.jsonl` 3
([`b1.log`](assets/exercise-checks/logs/b1.log)). In general: N + 2 rows, ⌈0.1 × (N + 2)⌉ test. The error list prints
only the first five (`errors[:5]`), so with many truncated batches, read `Number of errors`. If a real batch is cut
off, ask for fewer pairs per call or raise `max_output_tokens` (`cli.py:176`).
</details>

**B2. How big is the validation file?** Make N scripted pairs, 20 per file, and run `--prepare`. Save this as
`make_pairs.py` in the `dataset-creator` folder (run it with `rm -rf data` first, each time):

```python
# make_pairs.py N: write N scripted pairs into data/ as cheese_qa_<i>.txt, 20 per file (the shape --generate writes).
import json, os, sys
n = int(sys.argv[1]); os.makedirs("data", exist_ok=True)
for f in range((n + 19) // 20):
    pairs = [{"question": f"Scripted question {k}?", "answer": f"Good question! Scripted answer {k}."}
             for k in range(f * 20, min(n, f * 20 + 20))]
    with open(f"data/cheese_qa_{f}.txt", "w") as out:
        json.dump(pairs, out, indent=2)
print(f"{n} pairs in {(n + 19) // 20} files")
```

Predict the lines of `train.jsonl` and `test.jsonl`, and the rows of `test.csv`, for N = 21, 100 and 2,600.

<details><summary>Answer</summary>

`train_test_split(test_size=0.1, random_state=42)` (`cli.py:260-262`) puts ⌈0.1 × N⌉ rows in the test split. Then
`df_test[:256]` (`:267`, "Gemini: Max numbers of examples in validation dataset: 256") caps the **JSONL** file only:
`test.csv` was already written (`:264`) with every test row ([`b2.log`](assets/exercise-checks/logs/b2.log)):

| N | train.jsonl | test.jsonl | test.csv rows |
| --- | --- | --- | --- |
| 21 | 18 | 3 | 3 |
| 100 | 90 | 10 | 10 |
| 2,600 | 2,340 | **256** | 260 |

At 2,600 pairs, 4 examples end up in neither JSONL file: the cap bites once ⌈0.1 × N⌉ > 256, from N = 2,561. A fix
would be to give `train_test_split` a whole-number `test_size` of at most 256. Also note the order:
`ls data` and `glob` + `sort` put `cheese_qa_10.txt` before `cheese_qa_2.txt` (text order, not number order), which
decides which copy of a duplicate question `drop_duplicates` keeps (the first).
</details>

**B3. Flag order.** With five good batch files in `data/`, run `python cli.py --upload --prepare` (no key). Which
function runs first, what's left in `data/`, and what's the exit status?

<details><summary>Answer</summary>

`main()` checks the flags in a fixed order, generate, then prepare, then upload (`cli.py:300-307`), whatever order
you type them: `CLI Arguments: Namespace(generate=False, prepare=True, upload=True)`, then `prepare()` runs fully
(`Shape: (19, 2)` on the scripted data) and writes all five outputs; then `upload()` dies at `storage.Client()` with
`google.auth.exceptions.DefaultCredentialsError: File /secrets/llm-service-account.json was not found.`, exit 1
([`b3.log`](assets/exercise-checks/logs/b3.log)). Unlike `--generate`, `--upload` has no catch-all, so it fails loudly.
*With your key*, `python cli.py --prepare --upload` is a handy one-liner; look for five `Uploading file:` lines
(`:293`).
</details>

**B4. Which rows survive?** Add this batch to five good ones and predict the shape:

```bash
cat > data/cheese_qa_7.txt <<'EOF'
[
  {"question": "What does rennet do in cheesemaking?", "answer": "Good question! A second answer. (scripted)"},
  {"question": "what does rennet do in cheesemaking?", "answer": "Good question! Lower case. (scripted)"},
  {"question": "Is Feta a brined cheese?"},
  {"question": "Is Mozzarella stretched?", "answer": null}
]
EOF
python cli.py --prepare
```

(The first question repeats one of the video's scripted pairs; with your own files, copy one of your questions.)

<details><summary>Answer</summary>

On the 19 scripted rows: `Shape: (20, 2)` ([`b4.log`](assets/exercise-checks/logs/b4.log)). `drop_duplicates(subset=
["question"])` (`cli.py:233`) compares exact strings and keeps the first occurrence, so the repeated rennet question
goes (the original answer from `cheese_qa_0.txt` stays) and the lower-case copy **stays**. A missing `answer` key and
`null` both become NaN in the DataFrame, and `dropna()` (`:234`) removes both rows. So only 1 of the 4 new pairs
survives. Deduplication is exact-match only: near-duplicate questions from a teacher model pass straight through.
</details>

**B5. Count before you train.** Predict the `trainable params` line of 4.3 if you change 4.1 to (a) `r=16`,
(b) `r=8, target_modules="all-linear"`, (c) `r=8, target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]`. Check
with this snippet (plain Python, runs anywhere), then *in Colab* re-run 1.3 (reload the model), 4.1, 4.2 and 4.3:

```python
hidden, heads, kv_heads, head_dim, inter, layers = 1024, 16, 8, 128, 3072, 28
shapes = {"q_proj": (hidden, heads * head_dim), "k_proj": (hidden, kv_heads * head_dim),
          "v_proj": (hidden, kv_heads * head_dim), "o_proj": (heads * head_dim, hidden),
          "gate_proj": (hidden, inter), "up_proj": (hidden, inter), "down_proj": (inter, hidden)}
def lora(r, names):  # A is r x in, B is out x r
    return layers * sum(r * (shapes[n][0] + shapes[n][1]) for n in names)
print(f"{lora(16, ['q_proj', 'v_proj']):,}", f"{lora(8, list(shapes)):,}", f"{lora(8, ['q_proj', 'k_proj', 'v_proj', 'o_proj']):,}")
```

<details><summary>Answer</summary>

(a) **2,293,760**: the count is linear in r. (b) **5,046,272**: per block 8 × (3,072 + 2,048 + 2,048 + 3,072 +
4,096 + 4,096 + 4,096) = 8 × 22,528 = 180,224, × 28. (c) **2,293,760** again: adding `k_proj` and `o_proj` at r = 8
costs exactly as much as doubling r on `q_proj` and `v_proj`. PEFT 0.20.0 on Qwen3's shapes gives the same three
numbers, and `all-linear` adapts all seven projections but not the output head
([`peft.log`](assets/exercise-checks/logs/peft.log), [`snippets.log`](assets/exercise-checks/logs/snippets.log)).
In Colab, `all params` is the 4-bit count 375,848,960 plus the adapters: (a) and (c) `378142720`, trainable%
0.6066; (b) `380895232`, 1.3248 (our arithmetic; the r = 8 default reproduces the saved run's `376995840` and
0.3042155584528466 exactly). More rank or more matrices buy capacity at more memory and time; for a persona, the
default is plenty. Reload in 1.3 first, or C8 happens.
</details>

**B6. Steps, perplexity and file size.** From 4.2's settings (900 training examples, `per_device_train_batch_size=4`,
`num_train_epochs=2`, no gradient accumulation), predict the step count; then with batches of 8. From 5.1's losses
(2.6498 base, 1.3872 fine-tuned), predict the perplexities. And the size of 1,146,880 float32 numbers.

<details><summary>Answer</summary>

900 / 4 = 225 steps per epoch, × 2 = **450**: the saved run's `[450/450 03:36, Epoch 2/2]`
(`expected/colab-c75-train.txt`). With batches of 8: ⌈900 / 8⌉ = 113 per epoch (the last batch has 4), 226 in all.
Perplexity is e to the average token loss: e^2.6498 = **14.15**, e^1.3872 = **4.00**, as printed
(`expected/colab-c80`). The adapters: 1,146,880 × 4 bytes ≈ **4.59 MB** ([`snippets.log`](assets/exercise-checks/logs/snippets.log),
`steps.py`), the "about 4.6 MB" adapter file that 6.1 saves, besides the tokenizer files (the saved run's sizes were
not recorded). The notebook says a T4 takes about 6–7 minutes for the 450 steps (`cell-75` comment); the A100 took
3 min 36 s.
</details>

**B7. absmax by hand.** Predict the int8 values of the lecture's ten numbers, then run:

```python
X = [1.5, 2.3, 3.7, 4.1, 5.6, 6.8, 7.9, 8.4, 9.2, 10.2]
c = 127 / max(abs(x) for x in X)          # the scale: 127 over the largest magnitude
q = [round(x * c) for x in X]              # what is stored: one int8 per value
back = [v / c for v in q]                  # dequantized
print("c =", round(c, 4))
print("int8:", q)
print("back:", [round(b, 3) for b in back])
print("max error:", round(max(abs(a - b) for a, b in zip(X, back)), 4))
```

Then change 10.2 to 102 (one outlier) and predict what happens to the other nine.

<details><summary>Answer</summary>

`c = 12.451`, `int8: [19, 29, 46, 51, 70, 85, 98, 105, 115, 127]`, `back: [1.526, 2.329, 3.694, 4.096, 5.622,
6.827, 7.871, 8.433, 9.236, 10.2]`, `max error: 0.0362` ([`snippets.log`](assets/exercise-checks/logs/snippets.log)).
The slide shows 18 and 69 for 1.5 and 5.6; rounding gives 19 and 70. With an outlier of 102, c drops to 127 / 102 ≈
1.245 and the other nine values squeeze onto the integers 2 to 11: `[2, 3, 5, 5, 7, 8, 10, 10, 11, 127]`. 3.7 and
4.1 now share a level, so do 7.9 and 8.4, and the largest error grows tenfold, from 0.036 to 0.375 (`absmax_outlier.py`
in `snippets.log`). That is
why bitsandbytes keeps one constant per block of 64 weights, and why NF4 spaces its 16 levels by the bell-shaped
weight distribution instead of evenly.
</details>

**B8. Wait for the job** *(with your key; billed)*. Change `gemini-finetuner/cli.py:126` to
`train(wait_for_job=True)` and run `python cli.py --train`. Predict what it prints and when it stops. Is there a
state in which it never stops?

<details><summary>Answer</summary>

After `Training job started…`, `Job name: …` and a minute's wait, it prints `Check status of tuning job:` and the
state, then `Job in progress... State: …` every 60 seconds (`:74-87`) until the state is succeeded, failed or
cancelled. On success, `:90-96` prints `Tuned model name`, `Tuned model endpoint` and the hint to paste it into
`MODEL_ENDPOINT` (expect `locations/us/…`). The comparison with the three strings works because google-genai's
`JobState` is a string enum. In google-genai 1.39.1, `JobState` also has `JOB_STATE_PAUSED`, `JOB_STATE_EXPIRED`,
`JOB_STATE_UPDATING` and `JOB_STATE_PARTIALLY_SUCCEEDED`, none of them in the script's set, so a job that expires
or pauses keeps the loop going forever ([`c.log`](assets/exercise-checks/logs/c.log)). More robust: loop
`while not tuning_job.has_ended:` (the SDK's property: true for expired, false for paused) and add a timeout.
*(The states and `has_ended` were checked offline; the live run was not done here: no key.)* Remember the container
is not needed for the job: `Ctrl-C` stops the script, not the training.
</details>

**B9. Make the trainer read your bucket.** Replace `gemini-finetuner/cli.py:10-11` so the URIs come from the
`GCS_BUCKET_NAME` variable that `docker-shell.sh` already passes in:

```python
GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]
TRAIN_DATASET = f"gs://{GCS_BUCKET_NAME}/llm-finetune-dataset-small/train.jsonl"
VALIDATION_DATASET = f"gs://{GCS_BUCKET_NAME}/llm-finetune-dataset-small/test.jsonl"
```

Predict `python -c "import cli; print(cli.TRAIN_DATASET)"` in the container, and what `--help` does without the
variable (`env -u GCS_BUCKET_NAME python cli.py --help`).

<details><summary>Answer</summary>

With env.dev's value: `gs://cheese-dataset/llm-finetune-dataset-small/train.jsonl`; with your bucket in env.dev
(and the container restarted), your bucket. Without the variable, even `--help` fails: `KeyError:
'GCS_BUCKET_NAME'`, because the line runs on import, before argparse ([`b9.log`](assets/exercise-checks/logs/b9.log)).
Now env.dev line 7 is the one place to change, for `--upload` and `--train` alike, and the two can't drift apart.
</details>

---

## Part C · Debugging

**C1. "`docker-shell.sh: 7: source: not found`".** A classmate on Ubuntu runs `sh docker-shell.sh` in
`gemini-finetuner` and nothing else happens. Why line 7, why "not found", and why didn't Docker even start?

<details><summary>Answer</summary>

On Debian, Ubuntu and WSL, `/bin/sh` is **dash**, which has no `source` command. Line 7 of
`gemini-finetuner/docker-shell.sh` is `source ../env.dev` (line 8 in `dataset-creator`, `laptop/20`); `set -e` on
line 4 stops the script at that failure (status 127), before `docker build`. Reproduced for both folders in
[`c.log`](assets/exercise-checks/logs/c.log). Fix: `bash docker-shell.sh` (macOS's `sh` accepts `source`, so the
README works there), or change the line to the POSIX `. ../env.dev`.
</details>

**C2. "`can't open '../env.dev'`".** From the repository root, `sh dataset-creator/docker-shell.sh` prints
`dataset-creator/docker-shell.sh: source: line 8: can't open '../env.dev': No such file or directory` (BusyBox's
wording; bash says `line 8: ../env.dev: No such file or directory`). Why, and what would go wrong even if it found an
`env.dev`?

<details><summary>Answer</summary>

Relative paths in the script are relative to **your** current folder, not the script's (`README.md:68`): from the
repo root, `../env.dev` points above the repo (`laptop/21`). Even with an env.dev there, `BASE_DIR=$(pwd)` would mount
the repo root as `/app`, `SECRETS_DIR=$(pwd)/../../secrets/` would point two levels too high, and `docker build … .`
would use the wrong context. `cd dataset-creator` first.
</details>

**C3. A second shell without pandas.** While the container runs, you open another shell with
`docker exec -it llm-dataset-creator bash` and `python cli.py --prepare` fails with `ModuleNotFoundError: No module
named 'pandas'`. Why, and how do you fix it?

<details><summary>Answer</summary>

`docker exec` starts a new process in the running container; it doesn't run `docker-entrypoint.sh`, so
`/.venv/bin/activate` was never sourced and the Dockerfile doesn't put `/.venv/bin` on `PATH`: `python` is the base
image's `/usr/local/bin/python`, with no pandas (`laptop/12`). Run `source /.venv/bin/activate` first (or call
`/.venv/bin/python`). The variables from `docker-shell.sh` (`GCP_PROJECT` …) are there, since they belong to the
container.
</details>

**C4. "The container name is already in use".** Running `sh docker-shell.sh` again from a second terminal ends with
`docker: Error response from daemon: Conflict. The container name "/llm-dataset-creator" is already in use…`. Why?

<details><summary>Answer</summary>

`docker run --rm --name $IMAGE_NAME` (`docker-shell.sh:16`) gives every run the same name, and the first container is
still running (`laptop/11`, exit 125; the build itself was all cached). Use the laptop shell for laptop-side work, or
`exit` the first container, or open a second shell with `docker exec` (and C3's fix).
</details>

**C5. `KeyError: 'GCP_PROJECT'` on `--help`.** Someone runs `uv run python cli.py --help` on the laptop, outside the
container, and gets a traceback ending in `KeyError: 'GCP_PROJECT'`. How can `--help` need a project?

<details><summary>Answer</summary>

`GCP_PROJECT = os.environ["GCP_PROJECT"]` (`dataset-creator/cli.py:17`, `gemini-finetuner/cli.py:9`) runs when the
module is loaded, before argparse ever sees `--help`. Inside the container, `docker-shell.sh` passes the variable in
(`-e GCP_PROJECT=…`, from env.dev); outside, nothing sets it ([`b9.log`](assets/exercise-checks/logs/b9.log)
reproduces it with the variable removed). Run the CLI in the container, or `source ../env.dev` in that shell first
(it also sets `GOOGLE_APPLICATION_CREDENTIALS` to `/secrets/…`, a path that only exists in the container).
</details>

**C6. "`Expecting value: line 1 column 1 (char 0)`".** After a run *with* a key, `--prepare` prints
`Number of errors: 1` and `[{'file': 'data/cheese_qa_4.txt', 'error': 'Expecting value: line 1 column 1 (char 0)'}]`,
and `wc -c data/cheese_qa_4.txt` says 0 bytes. The generate output for that batch was `Error occurred while
generating content: write() argument must be str, not None`. What happened?

<details><summary>Answer</summary>

When Gemini's reply has no text (for example a candidate with no parts, finished for `MAX_TOKENS`, or a reply with
no candidates at all), google-genai's `response.text` is `None`. `generate()` opens `cheese_qa_4.txt` with `"w"` **before**
writing (`cli.py:198`), which creates an empty file; `file.write(None)` then raises the `TypeError`, which the
catch-all prints. `--prepare` finds the empty file, and `json.loads("")` fails with "Expecting value". The batch's
pairs are lost; the rest of the data is fine (here `Shape: (16, 2)` from the other four scripted files). Both halves
were reproduced offline in [`c.log`](assets/exercise-checks/logs/c.log) (a reply object built by hand; no live call).
Delete the empty file and generate again, or check `response.text` before opening the file.
</details>

**C7. `--chat` is refused.** Your job succeeded, your key works for `--train`, and `--chat` is refused with a
permission error. Your `GCP_PROJECT` is right. What's wrong, and why doesn't `project=GCP_PROJECT` in the client save
you?

<details><summary>Answer</summary>

`MODEL_ENDPOINT` (`gemini-finetuner/cli.py:107`) still holds the instructor's endpoint,
`projects/‹instructor-project-number›/locations/us/endpoints/‹endpoint-id›`. A model name that starts with
`projects/` is a full resource path, used as it is, so the request goes to the instructor's project, where your
service account has no rights. Paste your own endpoint from the console (Q4). *(Not reproduced here: no key; the
SDK behaviour is the digest's reading of google-genai 1.39.1, gotcha 5.)* While you're there, lines 10–11 (the
course bucket) are the same kind of trap for `--train` (B9).
</details>

**C8. A second LoRA in Colab.** You change `r=8` to `r=16` in 4.1 and re-run 4.1–4.3 without reloading. PEFT warns
`You are trying to modify a model with PEFT for a second time. If you want to reload the model with a different
config, make sure to call .unload() before.` Why?

<details><summary>Answer</summary>

`SFTTrainer` injected the LoRA layers into `base_model`'s modules in place the first time (that's also why 5.2 can
use `base_model` as the fine-tuned model). Building a second trainer on the same object calls `get_peft_model`
again, and PEFT finds LoRA layers already there; it also warns `Already found a peft_config attribute in the model.
This will lead to having multiple adapters in the model.` Both warnings reproduced with PEFT 0.20.0 on Qwen3's shapes
([`peft.log`](assets/exercise-checks/logs/peft.log); the full trainer run needs a GPU and was not reproduced). Re-run
1.3 (reload the 4-bit model and `prepare_model_for_kbit_training`) before 4.1–4.3.
</details>

**C9. torchao in Colab.** Someone skipped `!uv pip uninstall torchao` in section 3. What goes wrong, and when?

<details><summary>Answer</summary>

The notebook's own comment (`cell-08.py:6`): "Colab ships torchao 0.10; peft refuses to add LoRA layers to a
full-precision model while it is installed." Not during 4-bit training: the error (an `ImportError` about an
incompatible torchao version) comes in 6.2, where the adapter is loaded onto the fresh FP16 model for the merge (the
digest's reading of peft 0.20.0, gotcha 13; not reproduced: no GPU). Fix: run the uninstall cell, then restart the
session, since peft was already imported.
</details>

**C10. `cannot import name 'Number' from 'numbers'`.** You keep scratch scripts in one folder. After saving your
perplexity check as `numbers.py`, a script that only does `import torch` fails with
`ImportError: cannot import name 'Number' from 'numbers' (/tmp/work/numbers.py)`. Why?

<details><summary>Answer</summary>

Python puts the script's own folder first on `sys.path`, so your `numbers.py` hides the standard library's `numbers`
module, which torch imports. Rename the file (`ppl.py`) and it works ([`c-shadow.log`](assets/exercise-checks/logs/c-shadow.log);
it happened to us while writing these checks). The same goes for `json.py`, `random.py`, `math.py` … in the
`dataset-creator` folder: `cli.py` imports `json`.
</details>

---

## Part D · Think

**D1. Prompt, RAG or fine-tune?** For each, pick the cheapest dial that works: (a) the cheese-shop bot must quote
this week's prices; (b) every answer must open in the instructor's voice, with a catchphrase; (c) replies must be
JSON in a fixed schema; (d) the bot must know a 40-page course policy document that changes each term.

<details><summary>Answer</summary>

(a) Retrieval or a tool call: prices change weekly, and a fine-tune would freeze last week's facts. (b) A system
prompt gets you most of the way; fine-tuning makes the voice the default and saves the prompt tokens on every call,
which is what this tutorial does. (c) Structured output (`response_schema`, as `--generate` itself uses, and L06/L07's
structured outputs); no training needed. (d) RAG (L05): the facts must be current and checkable, and the saved run
shows that a fine-tune learns a voice, not reliable facts.
</details>

**D2. Track A or Track B?** Compare the README's managed Gemini tuning with the Colab's QLoRA on: who holds the
weights, what you pay for, what you can inspect, and what you ship.

<details><summary>Answer</summary>

Track A: Google trains and hosts; you never see a weight; you pay for generation, storage, tuning per training token
(the README's cost table is stale; check the pricing page) and the calls to the endpoint; you get an endpoint in
`us`, a console with loss curves, and little control (an epoch count, a learning-rate multiplier,
`ADAPTER_SIZE_FOUR`). Track B: you train on a Colab GPU (a T4 is free when available), see and count every
parameter, choose r, α, target modules and the optimizer, and keep the result: a 4.6 MB adapter that needs its
base, or a merged 1.2 GB model that stands alone, which you can serve anywhere (or push to Hugging Face). The price
is that you run the training and the serving yourself.
</details>

**D3. Check the teacher.** The system prompt asks Gemini for "specific data such as optimal pH levels, aging
temperatures, and humidity percentages" (`cli.py:45`). Before you spend money on tuning, how would you check 100
synthetic pairs?

<details><summary>Answer</summary>

Every wrong number becomes a training target that the student repeats confidently in the instructor's voice. Read a
sample by hand; look at `Number of errors` and the shape (B1); find near-duplicate questions, which
`drop_duplicates` misses (B4); spot-check the specific numbers against a trusted source, or have a second model or a
person flag doubtful claims; consider asking the teacher for fewer invented specifics; and keep the validation split
for the tuning job's curves. The cheapest mistakes to fix are the ones caught before `--upload`.
</details>

**D4. Why merge into a fresh 16-bit model?** In 6.2 the notebook loads the base again in FP16 and merges B·A there,
instead of merging into the 4-bit model it trained. Why? And when would you keep the 4.6 MB adapter separate instead?

<details><summary>Answer</summary>

The update (α/r)·B·A is small. Added to 4-bit weights, each sum would have to be stored as one of the same 16 NF4
levels (per block), and most of the update would round away; in FP16 it survives. The merged model (about 1.2 GB)
stands alone and runs without PEFT. Keep the adapter separate when you want several personas or tasks on one shared
base (swap 4.6 MB files instead of 1.2 GB models), want to switch it off (`disable_adapter()`), or plan to keep
training it.
</details>

**D5. Is 14.15 → 4.00 a fair win?** Name two reasons the 5.1 table overstates "better answers", and design a better
evaluation.

<details><summary>Answer</summary>

(1) The loss counts every token, questions and chat template included, and all 100 test examples share the
persona's openers: a model that has learned "Welcome welcome welcome…" gains a lot on those tokens alone. It
measures style fit. (2) The two notebook baselines differ: the table's base is the 4-bit model with the adapter off,
the side by side's base is a fresh FP16 model. Better: compare like with like (the same base for both views);
compute the loss on the answer tokens only; add held-out factual questions with known answers (and the sky) scored
by a person or a judge model; and check that general skills didn't get worse. The lecture shows LoRA matching full
fine-tuning on a published benchmark; this notebook doesn't measure answer quality.
</details>

**D6. Scale it up.** By the same rule of thumb as the video (FP16 weights and gradients, two FP32 Adam states:
12 bytes per parameter, before activations), estimate full fine-tuning of a 7-billion-parameter model, then QLoRA's
frozen base in NF4. What changes in the notebook to try it?

<details><summary>Answer</summary>

Full: 7 × 10⁹ × 12 bytes ≈ 84 GB before activations: several large GPUs. QLoRA: the base at about half a byte per
parameter ≈ 3.5 GB (plus embeddings, norms, block constants and activations), and adapters of a few tens of MB with
their gradients and optimizer states: it can fit a 16 GB T4, which is the point of the recipe (at 0.6 B, even full
fine-tuning would fit). In the notebook: `model_name`, possibly `target_modules` (the PEFT default depends on the
architecture), a smaller batch or `max_length` if memory runs out, and a lot more training time. These are estimates
by the video's rule, not measurements.
</details>
