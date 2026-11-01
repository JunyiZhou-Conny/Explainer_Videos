# Exercise checks · ac215-l08-llm-finetuning (2026-10-31, 03:45–04:00 UTC)

What was run to verify `exercises.md`, beyond the captures in `assets/terminal/`, which the answers cite directly
(`laptop/NN`, `dataset-creator/NN`, `gemini-finetuner/NN`, `expected/…`). Logs and the check scripts are in
[`logs/`](logs/). Every step in a log starts with its command (`$ …`) and ends with `[exit N]`, as in
`assets/terminal/run_steps.sh`. Where a step pipes the CLI into `grep`, `sed` or `tail`, `[exit N]` is the last
command's status; B3 prints the CLI's own status (`cli.py exit status: 1`).

There was **no service-account key, no GCP project and no GPU**, and every check container ran with
`--network none` (only the two setup steps and `trl-source.sh` had network, to download packages). Nothing called
Google: the failures are google-auth's, raised before any request. Data marked **scripted** is hand-written: the
capture's five files (`assets/terminal/capture-only/scripted/`) and the files the exercises' own commands write.
No log contains a person's name, a key, a project number or an endpoint id.

## Setup (disposable; nothing from the repo ran on the host)

- Docker Engine 29.8.2 on the session machine; image `python:3.12-slim-bookworm`, the tutorial `Dockerfile`'s base
  (already on the machine; **Python 3.12.15**, where the capture's freshly pulled image had 3.12.16).
- [`setup.sh`](logs/setup.sh) ([`setup.log`](logs/setup.log)): the repo's `README.md`, `env.dev`, `dataset-creator/`
  and `gemini-finetuner/` at the pinned commit `44ef6f0` (a `git archive` of the read-only clone) and the five
  scripted files into the volume `l08ex-work`; then uv **0.13.6** (the capture's) exported `dataset-creator/uv.lock`
  (`uv export --frozen`; the gemini-finetuner lock is identical, `laptop/16`) and installed **only the packages the
  two `cli.py` import**, constrained to the lock's exact versions: pandas 2.3.3, scikit-learn 1.7.2, google-genai
  1.39.1, google-auth 2.41.1, google-cloud-storage 3.4.1, numpy 2.3.3 and their dependencies (43 lines, 283 MB:
  [`setup-packages.txt`](logs/setup-packages.txt)). **Difference from the image:** the 133-package lock's unused
  chromadb, langchain, openai and onnxruntime were left out (no module imports them; every check ran without an
  import error), and the venv sits at `/venv`, not `/.venv`, so tracebacks show `/venv/lib/…` and `/repo/…/cli.py`
  where a student sees `/.venv/lib/…` and `/app/cli.py`.
- [`hrun.sh`](logs/hrun.sh) runs one check the way a student types at the `llm-dataset-creator` prompt: a fresh copy
  of the pinned repo in `/repo` (a tmpfs, so every check starts with no `data/`), the venv first on `PATH` (as the
  entrypoint activates it), user uid 1000 (the image's `app`), the three variables `docker-shell.sh` passes with
  env.dev's defaults (`GCP_PROJECT=ac215-project`, `GCS_BUCKET_NAME=cheese-dataset`,
  `GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json`) and an empty `/secrets`, as in the captures.
- [`setup-peft.sh`](logs/setup-peft.sh) ([`setup-peft.log`](logs/setup-peft.log)): a second venv (volume
  `l08ex-peft`) with the notebook's pinned transformers 5.16.1, tokenizers 0.23.1 and huggingface-hub 1.29.0 (nb cell
  8), peft 0.20.0 (the saved run's, nb cell 12) and torch 2.11.0 as a **CPU** wheel (the saved run: 2.11.0+cu128 on an
  A100). No bitsandbytes (it needs a GPU). [`prun.sh`](logs/prun.sh) runs a check in it, offline. The model is built
  from nb cell 42's configuration on PyTorch's `meta` device: real module shapes, no weights, no download.
- `snippets/` holds the exercises' code blocks exactly as printed in `exercises.md` (`b1-batches.sh`,
  `make_pairs.py`, `b4-batch.sh`, `b5_count.py`, `absmax.py`, `b9_lines.py`, the last inserted by `b9.sh`'s `sed`),
  plus the checks' own arithmetic (`lora_count.py`, `steps.py`, `peft_meta.py`, `absmax_outlier.py` = `absmax.py` with
  10.2 changed to 102).

## Checks

| exercise | what was run | result |
| --- | --- | --- |
| Q2 | `q2.sh`: `ls -la /secrets`, `--generate`, `ls -A data`, `--prepare`, `od -c` of the CSV ([`q2.log`](logs/q2.log)) | the five `Error occurred while generating content: File /secrets/llm-service-account.json was not found.`, exit 0; `data/` empty; `Shape: (0, 0)`, `KeyError: 'question'` at `cli.py` line 243, exit 1; `instruct-dataset.csv` is 1 byte, `\n` (the same as the captures `dataset-creator/05`, `07`) |
| Q3 (labels) | `trl-source.sh`: trl 1.14.0's wheel downloaded and unzipped in a container, `sft_config.py:259-280` and `sft_trainer.py:1625-1652` printed, nothing imported ([`trl-source.log`](logs/trl-source.log)) | `completion_only_loss` defaults to the full sequence for language-modeling (text) datasets; labels are masked only by `completion_mask` (prompt-completion data) or `assistant_masks` (`assistant_only_loss=True`); "With no applicable mask, every token contributes (labels == input_ids)" |
| Q5, B5, C8 | `peft.sh` → `snippets/peft_meta.py`: Qwen3-0.6B's shapes on the meta device, nb cell 67's `LoraConfig` and two variants; a second injection into the same model; `prepare_model_for_kbit_training`'s source ([`peft.log`](logs/peft.log)) | default targets for qwen3 `['q_proj', 'v_proj']`; 596,049,920 parameters (Linear modules 595,984,384 *including* `lm_head`, which shares the 155,582,464 embedding weights; norms 65,536); trainable 1,146,880 (r = 8), 2,293,760 (r = 16), 5,046,272 (`all-linear`, all seven projections, no `lm_head`); the second injection warns "You are trying to modify a model with PEFT for a second time…" and "Already found a `peft_config` attribute…"; the source freezes every parameter and casts FP16/BF16 parameters that are not `Params4bit` to float32 |
| Q5, B5, B6, B7 | `snippets.sh`: `b5_count.py`, `absmax.py`, `absmax_outlier.py`, `lora_count.py`, `steps.py` ([`snippets.log`](logs/snippets.log)) | `2,293,760 5,046,272 2,293,760`; c = 12.451, int8 `[19, 29, 46, 51, 70, 85, 98, 105, 115, 127]`, max error 0.0362; with 102: `[2, 3, 5, 5, 7, 8, 10, 10, 11, 127]`, max error 0.3748; 1,146,880, 4-bit count 375,848,960, + LoRA 376,995,840 (= the saved run's `all params`); e^2.6498 = 14.15, e^1.3872 = 4.0; 450 and 226 steps; 4.59 MB |
| B1 | `b1.sh`: the five scripted files plus `snippets/b1-batches.sh` exactly as printed (a fenced batch, a cut-off batch, `--prepare`) ([`b1.log`](logs/b1.log)) | `Number of errors: 1`, `[{'file': 'data/cheese_qa_6.txt', 'error': 'Unterminated string starting at: line 2 column 52 (char 154)'}]`, `Shape: (21, 2)`; `train.jsonl` 18 lines, `test.jsonl` 3 |
| B2 | `b2.sh`: `snippets/make_pairs.py` for 21, 100 and 2,600 pairs, `--prepare`, line and row counts ([`b2.log`](logs/b2.log)) | 18/3 (test.csv 3); 90/10 (10); 2,340/**256** (test.csv 260); `ls data` lists `cheese_qa_10.txt` and `cheese_qa_100.txt` before `cheese_qa_2.txt` |
| B3 | `b3.sh`: `python cli.py --upload --prepare` on the scripted files ([`b3.log`](logs/b3.log)) | `Namespace(generate=False, prepare=True, upload=True)`, `prepare()` (`Shape: (19, 2)`), then `upload()` and `DefaultCredentialsError`, `cli.py exit status: 1`; all five outputs in `data/` |
| B4 | `b4.sh`: the scripted files plus `snippets/b4-batch.sh` exactly as printed ([`b4.log`](logs/b4.log)) | `Shape: (20, 2)`; the CSV keeps the original rennet answer and the lower-case question; the Feta and Mozzarella rows are gone (`grep -c` 0, exit 1 = no match) |
| B8 | `c.sh`, last step: google-genai 1.39.1's `JobState` members, membership in the script's three-state set, `TuningJob(state=…).has_ended` ([`c.log`](logs/c.log)) | 12 states, among them `JOB_STATE_PAUSED`, `JOB_STATE_EXPIRED`, `JOB_STATE_UPDATING`, `JOB_STATE_PARTIALLY_SUCCEEDED`; `JOB_STATE_SUCCEEDED in done? True` (string enum); `has_ended`: PAUSED False, EXPIRED True, SUCCEEDED True |
| B9, C5 | `b9.sh`: `gemini-finetuner/cli.py --help` with and without `GCP_PROJECT`; lines 10–11 replaced by B9's three lines (`sed`); `import cli` with and without `GCS_BUCKET_NAME`; `dataset-creator/cli.py --help` without `GCP_PROJECT` ([`b9.log`](logs/b9.log)) | `usage: cli.py [-h] [--train] [--chat]`; `KeyError: 'GCP_PROJECT'`; `gs://cheese-dataset/…/train.jsonl`, `gs://my-own-bucket/…/train.jsonl`; `KeyError: 'GCS_BUCKET_NAME'` on `--help`; `KeyError: 'GCP_PROJECT'` |
| C1 | `c.sh`: in each folder, `sh docker-shell.sh` with Debian's `/bin/sh` (`/usr/bin/dash`), then `bash docker-shell.sh` (no Docker inside the check container) ([`c.log`](logs/c.log)) | `docker-shell.sh: 8: source: not found` (dataset-creator) and `docker-shell.sh: 7: source: not found` (gemini-finetuner), status 127, nothing after it; with bash the script gets past `source` to `docker build` (`line 13` / `line 12: docker: command not found`) |
| C6 | `c.sh`: a hand-built `GenerateContentResponse` (a candidate with no parts, `finish_reason="MAX_TOKENS"`; and one with no candidates) written the way `cli.py:196-201` writes, into `data/cheese_qa_4.txt`; then `--prepare` ([`c.log`](logs/c.log)) | `response.text: None` for both; `Error occurred while generating content: write() argument must be str, not None`; a 0-byte file; `Number of errors: 1`, `'Expecting value: line 1 column 1 (char 0)'`, `Shape: (16, 2)` |
| C10 | `c-shadow.sh`: a `numbers.py` next to a script that imports torch, then renamed ([`c-shadow.log`](logs/c-shadow.log)) | `ImportError: cannot import name 'Number' from 'numbers' (/tmp/work/numbers.py)`; after `mv numbers.py ppl.py`: `2.11.0+cpu` |

## Not run (and why)

- **Everything that needs a key**: a live `--generate`, `--upload`, `--train`, the tuning job, `--chat`, B8's waiting
  loop, C7's permission error. Their answers cite the code, the README (`expected/readme-*`) or the digest's
  reading of google-genai 1.39.1, and say so; the no-key failures are the captures `dataset-creator/05`, `14` and
  `gemini-finetuner/02`, `03`.
- **Everything that needs a GPU**: the Colab run itself (4-bit loading, training, evaluation, merge, push), the
  trainable% lines B5 predicts for the variants, C8 inside a real `SFTTrainer`, C9's torchao error. Answers use the
  staff's saved A100 run (`expected/colab-*`, `recorded`) and the notebook's own comments; Q5's and D6's memory
  figures are estimates from the shapes, as in the video.
- **C2, C3, C4**: captured in `laptop/21`, `laptop/12` and `laptop/11`; not repeated (C1 re-checks the `sh` case
  for both folders).

## Cleanup

Removed afterwards, by name: the volumes `l08ex-work`, `l08ex-venv` and `l08ex-peft`. Every check container ran with
`--rm`. The image `python:3.12-slim-bookworm` was already on the machine and was kept. Nothing was written outside
the volumes and this folder.
