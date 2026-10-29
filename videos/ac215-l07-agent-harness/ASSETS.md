# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing, a notebook output) is read
from a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

## `source/` — the tutorial's own files

**The whole repository** [dlops-io/agent-harness](https://github.com/dlops-io/agent-harness), branch `main` (its only
branch), commit `e25dfe9615d78b78e0764a636cc2462f530a1402` (2026-09-28 19:59:31 −0400, "update"; still the head of
`main` on 2026-10-20, `terminal/laptop/02-x-git-log.txt`): all 126 tracked files, copied with
`git show e25dfe9:<path>` at the repo's own relative paths and checked against their git blob hashes (126/126 equal);
`Dockerfile`, `docker-shell.sh` and `docker-entrypoint.sh` keep mode 755, as committed. A code panel's
`path · lines a–b` therefore matches a viewer's clone. The files the scenes are most likely to quote:

- setup: `README.md` (866 lines; Setup 43-165, Acts 1-6 169-662, Evaluation 666-769, Additional Resources 773-826,
  Troubleshooting 828-866), `Dockerfile`, `docker-shell.sh`, `docker-entrypoint.sh`, `pyproject.toml`, `uv.lock`
  (214 packages), `.gitignore`, `scripts/check_sdk.py`, `tests/__main__.py`;
- the code: `cli.py`, `acts/act1_agent.py` … `acts/act6_composition.py`, every module of `formaggio/` (agents, shop,
  operations, evaluation, fixtures), `formaggio/config.py` (the default model, line 9);
- the inputs: `prompts/*.md`, `skills/tasting-planning/**`, `skills/vendor-outreach/**`, `data/*.json`;
- `tests/` (27 test files) and `notebooks/` (six notebooks, saved outputs cleared by the authors).

Course material by the AC215 teaching staff (Harvard IACS), used for study with the instructor's permission.
**Never on screen:** the `name` fields of `data/customers.json` and cell 0 of `notebooks/full_notebook.ipynb` hold the
full names of two course staff; the CLI prints only the customer IDs (`pavlos`, `shivas`), and so do the captures.
`tests/test_observability.py:35-41` contains a made-up string shaped like an API key: it is the tutorial's own
redaction-test input, not a credential.

**`source/colab/cell-NN.py|.md`**: every non-empty cell (58 of 60) of the course Colab "Agent Harness"
(https://colab.research.google.com/drive/1ZYMsbG0gqsbs-6Pcj8WtT3WhEa4f80EZ, downloaded as JSON on 2026-10-17; a
notebook has no commit), its source unchanged; `NN` is the cell's 0-based index in the `.ipynb` (Colab shows no
numbers; `digest.md` uses the same indices). **One change:** `cell-00.redacted.md` is the title cell with the two
staff names replaced by `<name>`. Made by `terminal/expected_outputs.py`.

## `terminal/` — real terminal sessions

Captured on **2026-10-20, 20:17–20:24 UTC** by `terminal/capture.sh` (which starts a fresh "laptop") and
`terminal/run_steps.sh` (which types the commands one by one). Each file starts with the command (`$ ...`; a
multi-line command keeps its lines), then its output, then its exit status (`[exit N]`); ANSI colour codes are
removed. **Every command of the README runs in README order, exactly as written** (the table at the end maps each
one to its file). Files with `x-` in their name are **extras** (not README steps: checks, offline counterparts,
gotcha demos); scenes mark them `extra`. Per-step UTC times and durations: `capture-only/*-timings.txt`.

| folder | what |
| --- | --- |
| `laptop/` | your laptop's terminal, in `~/AC215/agent-harness` (README.md:92 "Run these commands on your host machine"): clone, `../secrets`, the key placeholder, `bash docker-shell.sh` (build, banner, prompt), a second terminal's checks, `bash docker-shell.sh` again with the README's hidden-key lines, and the state after `exit` |
| `container/` | typed at the `agent-harness` container's prompt, `app@<id>:/app$` (README.md:108 "Run every remaining command inside the container, from /app"): verification, Acts 1-6, evaluation, `--help` |
| `expected/` | what the tutorial documents for what cannot run here: the Colab's saved outputs (`recorded`) and the README's own descriptions of live output (`expected`); the first line of each file says exactly where it comes from |
| `capture-only/` | not tutorial material: the base-image Dockerfile the capture needs and its build log, per-folder timings |
| `capture.sh`, `run_steps.sh`, `tty_session.py`, `proxy_relay.py`, `expected_outputs.py` | the scripts that made all of the above (`tty_session.py` and `proxy_relay.py` are L06's helpers, copied unchanged) |

Chronological order: `laptop/00-07` (07 stays open: the container's shell), `laptop/08-12` (a second terminal),
`container/00-92`, then `exit` closes 07, then `laptop/13-15`. Re-run with
`bash assets/terminal/capture.sh` (needs Docker, privileged containers and `pyte`; see the script's header), and
`python3 -I assets/terminal/expected_outputs.py <L07_agent_harness.ipynb> videos/ac215-l07-agent-harness`.

### The machines and versions

- **Your laptop:** a fresh, empty Docker Engine **29.8.2** (client and engine, API 1.56, linux/amd64), git 2.54.0
  (`laptop/00-x-env.txt`); user `student` (uid 1000), workspace `~/AC215` holding `agent-harness/` and `secrets/` side
  by side (`docker-shell.sh:8-9`). Linux x86_64 only: an Apple Silicon (aarch64) build was not captured.
- **The `agent-harness` image**, built by `docker-shell.sh:20` from the tutorial's `Dockerfile`
  (`laptop/07-docker-shell.txt` and `.plain.txt`): `python:3.13-slim-bookworm` (Debian 12), **Python 3.13.16**, apt
  installs 65 packages for `build-essential curl libpq5` (0 upgrades), **pip 26.2.2**, **uv 0.13.4** (`pip install uv`,
  unpinned), then `uv sync`: `Using CPython 3.13.16 interpreter at: /usr/local/bin/python3`, `Resolved 214 packages`,
  `Installed 209 packages`. Build **38.2 s** here (51.3 s in a first trial run the same day); image **1.77 GB**
  (`laptop/09`), `/.venv` **646 MB** (`container/01`).
- **Installed** (`container/01-x-packages.txt`, `03-check-sdk.txt`): **agent-framework 1.19.0**, agent-framework-core
  1.19.0, **agent-framework-openai 1.14.4**, agent-framework-gemini 1.0.0b260910, claude-agent-sdk 0.2.160 (both
  installed by `agent-framework`'s `[all]` extra, never imported), openai 3.19.2, httpx 0.28.1, pydantic 2.13.5,
  opentelemetry-api/sdk 1.40.0; **no IPython and no pandas** in the image. Default model **`gpt-5.6-luna`**
  (`container/06`).
- **Tests:** `Ran 281 tests in 99.378s` / `OK` (`container/04`); notebook tests 9 OK; chat-view tests 12 OK.
- Versions move: narration says "at the time of recording" for every version above.

### Live commands: run as written, with the README's placeholder key

There is no OpenAI key here. The README's export line was typed exactly as written,
`export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"` (`laptop/06`), so `docker-shell.sh:28` passed the placeholder into the
container (`laptop/10-x-container-env.txt` shows it in `docker inspect`). Every **live** command therefore ran for real
up to its first model call, printed its real header (scenario, customer ask, `🤖 Model call 1 · … · gpt-5.6-luna`, the
tools on offer, `Memory for …`, `Skills available (metadata only): …`), and then OpenAI refused the placeholder:
`❌ Model call 1 failed: (… Error code: 401 - {'error': {'message': 'Incorrect API key provided: YOUR_OPE*******_KEY.
…', 'code': 'invalid_api_key'}} …)`, `Run stopped: …`, `Inspect the recorded error with --list-runs and --inspect-run.
Database: /app/outputs/observability.sqlite`, `[exit 1]`. **Kept as instructive:** this is exactly what a student sees
who copies the export line without replacing the placeholder, and each failure is recorded as a run with status
`error` (`container/70`, `73`). These files are real; the part of a live run after the first model call is not in
them. What a working key prints is shown from `expected/` (the Colab's recorded Act 1 run and the README's own
descriptions) and, for the same code paths, from the offline `--fixture` captures, tagged as scripted, never as the
live model's output.

### `laptop/` — your laptop's terminal

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-env.txt` | extra | date, `x86_64`, Docker 29.8.2, git 2.54.0, `student`, uid 1000, `~/AC215` |
| `01-x-clone.txt` | extra (README.md:48 assumes "A local copy of this repository"; no clone command) | `git clone https://github.com/dlops-io/agent-harness.git` → `Cloning into 'agent-harness'...` |
| `02-x-git-log.txt` | extra | `e25dfe9 …` `2026-09-28 19:59:31 -0400 update` = the pinned commit; only `main` |
| `03-x-ls.txt` | extra | `ls -a`: `.git .gitignore Dockerfile README.md acts cli.py data docker-entrypoint.sh docker-shell.sh formaggio notebooks prompts pyproject.toml scripts skills tests uv.lock` (no `.dockerignore`, no `docs/`) |
| `04-mkdir-secrets.txt` | **README.md:96** | `mkdir -p ../secrets`, no output |
| `05-x-ls-workspace.txt` | extra | `agent-harness` and `secrets` side by side; `secrets` empty (`0`) |
| `06-export-key.txt` | **README.md:99** | `export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"` (the placeholder, as written) |
| `07-docker-shell.txt` (+ `.plain.txt`) | **README.md:101** | `bash docker-shell.sh` in an 80×40 terminal, in the shell of 06: `Container 'agent-harness' is not running. Building and starting new container...`, BuildKit's `[+] Building 38.2s (11/11) FINISHED` (`[2/6] RUN set -ex; …` 25.1 s, `[5/6] RUN uv sync` 7.0 s, context 2.11 MB), the entrypoint banner (`Container is running!!!`, `Architecture: x86_64`, `Environment ready! Virtual environment activated.`, `Python version: Python 3.13.16`, `UV version: uv 0.13.4 (x86_64-unknown-linux-gnu)`, `Activating virtual environment...`), the prompt `app@13a6188396ca:/app$`, and `exit` at the end of the session. `.plain.txt` = the build's step log (713 lines: the apt, pip and `uv sync` output, every `+ package==version`) |
| `08-x-docker-ps.txt` | extra | the container `agent-harness`, `PORTS` empty: nothing is published |
| `09-x-docker-images.txt` | extra | `agent-harness:latest` **1.77GB**; the `python:3.13-slim-bookworm` line is the capture's rebuilt base (see below) |
| `10-x-container-env.txt` | extra (digest §6: the key is stored in the container) | `docker inspect`: `GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json`, `GCP_PROJECT=ac215-project`, `OPENAI_API_KEY=YOUR_OPENAI_API_KEY` |
| `11-x-mounts.txt` | extra | `…/AC215/agent-harness -> /app`, `…/AC215/secrets -> /secrets`, `ports: {}  user: app  workdir: /app` |
| `12-docker-shell-again-read-key.txt` | **README.md:101 again (the `docker exec` path, README.md:106) + README.md:113-115** | a second terminal runs `bash docker-shell.sh` while the container runs: `Container 'agent-harness' is already running. Shelling into existing container...` (the 80-column terminal wraps its last `.` onto the next line; scenes join it), the same banner, then the README's three lines typed at the prompt: `read -rsp "OpenAI API key: " OPENAI_API_KEY` (the typed value, the README's placeholder, is not echoed), `export OPENAI_API_KEY`, `printf '\n'`; extra check `echo ${#OPENAI_API_KEY}` → `19` (its length, not its value); `exit` |
| `13-x-ps-after-exit.txt` | extra (digest §2 "Shutting down") | after `exit` in 07: `docker ps -a` is empty (`--rm`) |
| `14-x-outputs-on-host.txt` | extra (README.md:469, 709, 805-816) | the bind mount left `outputs/` on the laptop (owned by `student`): `observability.sqlite` 5.0 MB, `customer_memory.sqlite`, the run folders, `reports/`, `my-report.html`, `context-comparison.json`; `git status`: `?? prompts/shop_assistant_v2.md`, `!! outputs/` (git-ignored, `.gitignore:64`) |
| `15-x-image-rm.txt` | extra (digest teardown) | `docker image rm agent-harness` → `Untagged: agent-harness:latest`, `Deleted: sha256:…` |

### `container/` — typed at the container's prompt

While the session of `laptop/07` was open, each command ran in that container as user `app` in `/app`, after
activating `/.venv` exactly as `docker-entrypoint.sh:12` does (`docker exec` from a second terminal, stderr joined to
stdout; the output is what the session's terminal shows). The prompt to draw is the session's,
`app@13a6188396ca:/app$`. These files are not wrapped (scenes fold long lines); 33 and 34 ran in a real terminal 250
columns wide, so they are not wrapped either. Run IDs, ticket IDs and receipt IDs are random per run.

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-whoami.txt` | extra | `app`, uid 1000, `/app`, `/.venv/bin/python`, Python 3.13.16, uv 0.13.4, `VIRTUAL_ENV=/.venv`, `GCP_PROJECT=ac215-project`, `GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json`, `/secrets` **empty** (nothing reads it, README.md:147-157) |
| `01-x-packages.txt` | extra | the versions above; `packages in /.venv: 209`; `646M /.venv`; `No module named 'IPython'`, `No module named 'pandas'` |
| `02-x-ls-app.txt` | extra | `/app` = the bind-mounted clone (owned by `app`) |
| `03-check-sdk.txt` | **README.md:123** | the JSON: `"python": "3.13.16"`, the six dependency versions, all 11 `features` `true`, `skills_signature`, `tool_signature`, `otel_setup_available: true`, and the long `compaction_factory_source` (the SDK's private `_assemble_compaction`) |
| `04-tests.txt` | **README.md:124** | a row of dots, `Ran 281 tests in 99.378s`, `OK` |
| `05-tests-show-logs.txt` | **README.md:132** | the same suite with diagnostics (1,889 lines): deliberate failures and tracebacks (e.g. `Function failed. Error: Injected nested checkout audit outage`), 118 approval-identity warnings, then `OK` (README.md:837) |
| `06-model.txt` | **README.md:142** | `gpt-5.6-luna` |
| `07-tests-notebook.txt` | **README.md:69** (inline) | `python -m tests -p test_notebook.py` → `Ran 9 tests`, `OK`: the six repo notebooks' lesson cells, offline |
| `08-tests-chat-view.txt` | **README.md:88** (inline) | `python -m tests -p test_chat_view.py` → `Ran 12 tests`, `OK` |
| `10-act1-standard.txt` | **README.md:178** (live) | `🧀 Agent and tools lesson — model: gpt-5.6-luna.`, `🧪 Act 1 · BASIC context · scenario: standard`, `👤 Customer ask:` (12 guests, PA, $150.00, nuts, France, funk 4+), `🤖 Model call 1 · Shop assistant`, `🧰 Available tools: get_catalog, check_stock, price_order, get_pairings, preview_order`, then the 401 (see above) |
| `11-act1-show-json.txt` | **README.md:195** (live) | as 10, plus the real `📋 Exact customer message sent to the model:` with the structured request JSON, before the 401 |
| `12-act1-missing-details.txt` | **README.md:245** (live) | the missing-details ask (`I still need to confirm the destination. I still need to check everyone's allergies.`), then the 401 |
| `13-x-act1-fixture.txt` | extra (digest §6) | `cli.py: error: --fixture applies only to --act 3, 4, 5 or 6.`, exit 2 |
| `20-act2-compare.txt` | **README.md:269** (live) | the personalized ask, `Two fresh live runs: basic receives no saved profile; enriched receives the customer's saved preferences.`, `Starting basic context with gpt-5.6-luna`, then the 401 |
| `21-act2-personalized-basic.txt`, `22-…-enriched.txt`, `23-act2-preference-override.txt` | **README.md:272-274** (live) | basic: `📥 Input: 1 conversation messages.`; enriched: `2 conversation messages` (the context packet is the extra message); then the 401, so the evidence block and the PA/NY counterexample are not reached (see 29) |
| `24-act3-pa-shipping.txt` | **README.md:286** (live, in the Act 2 section) | `🧪 Scenario: pa-shipping · LIVE proposals`, `Customer-cart lesson: … then asks the model to correct violations before checkout.`, the ask ending `For this tasting, here's what I have in mind: My starting cart is 350 g of Comté, 350 g of Bûcheron, and 300 g of Époisses. …`, `Step: confirm_request`, `Step: propose_cart`, `🤖 Model call 1 · Cart proposer`, `🧰 Available tools: none (structured proposal only)`, then the 401 |
| `25-act2-evaluate-live.txt` | **README.md:295** (live) | `LIVE evaluation: 4 cases × 3 repeats = 12 runs.` (case × mode), three 401s, then `LIVE EVALUATION act2-context-live-1: 0/12 scheduled runs passed`, `Failures: 0; errors: 3; missing: 9.` (it stops after three consecutive errors), exit 1 |
| `26-view-report-act2-live.txt` | **README.md:296** | `Saved evaluation report: /app/outputs/reports/act2-context-live-1.html` (works on the failed batch) |
| `27-preview-context.txt` | **README.md:311** (offline) | the JSON: `same_system_instructions`, `same_customer_message`, `same_tools`, `basic`, `enriched`; enriched `excluded_products`: brie and comte `fictional_shipping_policy`, munster `insufficient_stock_for_minimum`, walnut_chevre and pistachio_manchego `allergen_conflict` |
| `28-act2-standard.txt` | **README.md:321** (live) | the standard ask, `Starting basic context …`, then the 401 |
| `29-x-shipping-demo.txt` | extra (README.md:277-281) | the PA/NY counterexample every individual Act 2 run prints after its runs (`print_shipping_demo()`, called directly; no model): `PA: REJECTED`, `shipping: Fictional shop policy blocks raw-milk shipping to PA.`, `NY: PASS` |
| `30-act3-standard.txt` | **README.md:364** (live) | `Workflow lesson — model: gpt-5.6-luna.`, `🧪 Scenario: standard · LIVE proposals`, steps, the Cart proposer call, then the 401 |
| `31-act3-blocked.txt` | **README.md:376** (live) | `🧪 Scenario: pa-shipping-blocked · LIVE proposals`, `Customer-cart lesson: the model records the submitted cart; the harness checks it and stops. No order will be placed.`, the same ask as 24, then the 401 |
| `32-act3-pa-shipping.txt` | **README.md:379** (live) | the same as 24 (the README gives this command twice) |
| `33-act3-manager-approval.txt` | **README.md:407** | in a real terminal; typed at the prompt: `approve`. `Workflow lesson — FIXTURE proposals; no model calls.`, the 60-guest NY ask, `🧺 Proposed cart — attempt 1:` Comté 1600 g `RAW MILK`, Mimolette, Taleggio, `Cart attempt 1: valid; $220.80`, `MANAGER REVIEW — ticket …`, the cart ($72.00 + $80.00 + $68.80), `Approve this exact cart? Type approve or decline: approve`, `Step: revalidate_and_place`, `--- WORKFLOW PLACED — run 7409b343… ---`, `Order placed.`, `Receipt: …`, pairings, `Proposal attempts: 1. Model calls: 0.` |
| `34-x-act3-manager-decline.txt` | extra | the same, typed `decline`: `--- WORKFLOW DECLINED — run … ---`, `Manager declined this cart. No order placed.` |
| `35-act3-out-of-stock.txt` | **README.md:415** (offline) | attempt 1 Munster 300 g → `Cart attempt 1: stock: munster — Requested 300 g; available 0 g.`, `🛡️ Cart rejected; requesting a revised proposal before checkout.`, attempt 2 with `🔄 Changes from the previous proposal:` `Removed: Munster (munster) — 300 g` / `Added: Époisses (epoisses) — 300 g`, `Cart attempt 2: valid; $50.10`, `--- WORKFLOW PLACED …`, `Proposal attempts: 2. Model calls: 0.` |
| `36-x-act3-pa-shipping-fixture.txt` | extra (README.md:401 "`--fixture` remains available") | the shipping lesson's revision path with scripted proposals: Comté 350 g `RAW MILK` → `Cart attempt 1: shipping: comte — Fictional shop policy blocks raw-milk shipping to PA.` → `Removed: Comté 18 mois (comte) — 350 g` / `Added: Taleggio (taleggio) — 350 g` → `Cart attempt 2: valid; $50.10`, `✅ Shipping policy for PA: passed; …` → PLACED. Fixtures skip the live intake, so the ask has no "starting cart" sentence |
| `37-x-act3-blocked-fixture.txt` | extra (digest §6) | `pa-shipping-blocked` with `--fixture` is not review-only: the same cart three times (`No changes; the same cart was proposed again.`), `🛡️ Revision limit reached; no order will be placed.`, `--- WORKFLOW UNRESOLVED — run … ---` (not BLOCKED), `⚠️ shipping: …`, `Proposal attempts: 3.` |
| `40-act4.txt` | **README.md:457** (live) | `Harness lesson — model: gpt-5.6-luna.`, `Memory for pavlos: French cheeses; funky cheeses`, `🤖 Model call 1 · Event planner`, tools `assess_event, read_vendor_document, draft_vendor_email, save_vendor_email, todos_add, todos_complete, todos_remove, todos_get_remaining, todos_get_all` (no memory-write tool), then the 401 |
| `41-act4-compaction.txt` | **README.md:476** (offline) | `Harness lesson — SCRIPTED local SDK responses; no service calls.`, `TEST email response configured: decline`, seven scripted model calls, each with `Compaction: 26 → 5 messages; confirmed constraints and open work restored.` (then 27 → 7 … 37 → 12), `Plan: [open] …`, `Vendor evidence: quarantined (malicious)`, the `MOCK EMAIL REVIEW` (To `vendor@example.com`, the code-generated body: `Époisses: 300 g additional`), the SDK's approval-identity warning (see "Surprises"), `--- HARNESS DECLINED — run … ---`, `Menu: 3200 g; cheese quote $177.80.`, `Unconfirmed sourcing: epoisses — 300 g short.`, `No HTML email saved.`, `Model calls: 7. Compactions: 7.` |
| `42-x-act4-fixture-approve.txt` | extra (README.md:469 "An approved save prints the file path") | the same path, clean vendor note, test decision approve: `Vendor evidence: included (clean)`, `status: saved; path: /app/outputs/<run>/vendor-email-<draft>.html; … email transmitted: no`, `--- HARNESS SAVED …`, `HTML file: /app/outputs/…html`, `Compactions: 0` |
| `43-act4-remember.txt` | **README.md:484** (live) | `Memory for shivas: mild cheeses; nonalcoholic pairings; Prefer nonalcoholic pairings today` (the host writes it before the first model call), then the 401 |
| `44-act4-shivas.txt` | **README.md:485** (live) | the second visit prints the same merged memory: it persisted. Then the 401 |
| `45-x-memory-db.txt` | extra | `outputs/customer_memory.sqlite`: `pavlos ['French cheeses', 'funky cheeses']`, `shivas ['mild cheeses', 'nonalcoholic pairings', 'Prefer nonalcoholic pairings today']` |
| `50-act5.txt` | **README.md:542** (live) | `Skills lesson — model: gpt-5.6-luna.`, `Skills available (metadata only): tasting-planning, vendor-outreach`, tools add `get_stock`, `load_skill`, `read_skill_resource` (no `run_skill_script`), then the 401 |
| `51-act5-stock-question.txt` | **README.md:552** (offline) | one `get_stock` call, `product: epoisses; stock g: 900`, `--- HARNESS ANSWERED …`, `Skills loaded: none`, `Skill resources: none`, `Stock: epoisses — 900 g`, `Model calls: 2.` |
| `52-act5-approve.txt` | **README.md:560** (offline) | `Skill loaded: tasting-planning/SKILL.md`, `…/references/serving-guide.md`, `…/assets/tasting-plan.md`, `vendor-outreach/SKILL.md`, `…/references/vendor-guide.md`, `…/assets/email-template.html`, the review, `--- HARNESS SAVED …`, `Skills loaded: tasting-planning, vendor-outreach`, four `Skill resources`, `HTML file: …`, `Model calls: 13.` |
| `53-x-saved-html.txt` | extra | the run folder of 52 (`memory.sqlite`, `vendor-email-<draft>.html`) and the saved mock email's HTML (`Mock email preview — nothing transmitted.`) |
| `54-x-act5-tasting-plan.txt` | extra (README.md:639; Colab cell 47) | `--fixture --scenario tasting-plan`: only `tasting-planning` loads; the rendered `## Host tasting plan — event` (sequence Bûcheron, Époisses, Taleggio; `1000 g · Cheese subtotal $50.10`; `Authoritative status: Proposal only; no order placed.`), `--- HARNESS PLAN_PROPOSED …` |
| `60-act6.txt` | **README.md:634** (live) | `Composition lesson — model: gpt-5.6-luna.`, `Harness → ordering workflow → host manager review when required → authoritative result.`, `🤖 Model call 1 · Customer assistant`, tools `start_order, get_order_status, assess_event, todos_*, load_skill, read_skill_resource`, then the 401 |
| `61-act6-two-orders.txt` | **README.md:648** (offline) | `TEST manager response configured: approve`; `start_order request-1` and `request-2`, each running the Act 3 steps to `pending_approval` ($220.80 each); two `MANAGER REVIEW` blocks; `Order request-1: placed`, `Order request-2: blocked`; the tasting plan for request-1; `Final checkout blocked: Invalid or unauthorized order. No order placed.` with `⚠️ stock: Requested 1600 g; available 1400 g.` twice (mimolette and taleggio, 3,000 g each); `Outer model calls: 10; workflow model calls: 0.` |
| `62-x-act6-fixture.txt` | extra (the CLI form of the README.md:622 notebook cell) | `--act 6 --fixture`: one order placed ($50.10), the structured tasting plan, `--- COMPOSITION COMPLETED …`, `Outer model calls: 8` |
| `70-list-runs.txt` | **README.md:675** | the JSON list of all 32 runs so far (`run_id`, `case_id`, `repetition`, `status` `error`/`completed`, `mode` `live`/`fixture`) |
| `71-inspect-run.txt` | **README.md:681** (`RUN_ID` = the run of 33) | 66 events numbered `0214`…`0279` (the sequence is global across the database): `run.started`, `request.brief`, `workflow.step`, `context.selected`, the proposal, validation, `approval.requested`, `approval.decided`, `order.placed` with `approval_ticket_id`, `checkout_key` and the SHA-256 `fingerprint`, `run.finished … completed` |
| `72-x-inspect-run-literal.txt` | extra | the placeholder typed as is: `cli.py: error: Unknown run ID`, exit 2 |
| `73-x-inspect-failed-run.txt` | extra (`Inspect the recorded error with --list-runs and --inspect-run`) | the first live failure (10): `run.started`, `context.selected`, `model.request` (the full message), `model.failed` with the 401, `run.finished` with the error |
| `74-evaluate-fixture.txt` | **README.md:691** | `FIXTURE evaluation: 2 cases × 2 repeats = 4 runs.`, four scripted runs, `FIXTURE EVALUATION context-fixture-1: 4/4 scheduled runs passed`, four `PASS … — run …` lines |
| `75-report.txt` | **README.md:699** | the same report read back from SQLite |
| `76-view-report.txt` | **README.md:705** | `Saved evaluation report: /app/outputs/reports/context-fixture-1.html`, `Open this HTML file in your host browser. No model calls were made.` |
| `77-view-report-html-output.txt` | **README.md:713** | `Saved evaluation report: /app/outputs/my-report.html` |
| `78-view-report-colab.txt` | **README.md:714**, placeholders as written | `cli.py: error: Recorded database not found: /app/outputs/colab.sqlite`, exit 2 (a template for a database copied from Colab) |
| `79-x-ls-reports.txt` | extra | the two report files and `my-report.html` |
| `80-evaluate-live-a.txt` | **README.md:728** (live) | `LIVE evaluation` of standard/missing-details (enriched), three 401s, `0/4 scheduled runs passed`, `errors: 3; missing: 1`, `FAIL/ERROR … execution: …`, exit 1 |
| `81-cp-prompt.txt` | **README.md:734** | `cp prompts/shop_assistant.md prompts/shop_assistant_v2.md` |
| `82-x-edit-prompt.txt` | extra, stands in for README.md:737 ("Open the copy in your editor. Make one deliberate change") | the capture appends one line with `printf`: `Keep the customer message under 120 words. Start it with two labeled lines: "Price:" … and "Action status:" …` |
| `83-x-diff-prompt.txt` | extra | `diff -u` shows that one added line (`[exit 1]` is how `diff` says "the files differ") |
| `84-evaluate-live-b.txt` | **README.md:742** (live) | the same batch with `--prompt-file prompts/shop_assistant_v2.md`: three 401s, `0/4`, exit 1 |
| `85-compare.txt` | **README.md:748** (offline) | the JSON comparison of the two failed batches: `"changed_configuration": ["prompt"]`, `"confounding_changes": []`, `"evaluator_changed": false`, per-run `"outcome": "unchanged"` (error vs error), the `interpretation` sentence, `JSON saved: outputs/context-comparison.json` |
| `86-x-evaluate-fixture-b.txt`, `87-x-compare-fixture.txt` | extra | the same A/B with scripted responses (both batches complete, 4/4): the comparison shows `changed_configuration: ["prompt"]`, `outcome: unchanged` for all four runs (fixtures ignore the prompt), token usage and check counts |
| `88-x-label-exists.txt` | extra (README.md:835) | `Evaluation stopped: Experiment label already exists. Choose a new label; previous results are immutable.`, exit 1 |
| `89-x-report-text.txt` | extra (README.md:702-709) | the visible text of `outputs/reports/context-fixture-1.html` (tags removed by a short Python filter, shown in the file's command): `SCRIPTED RESPONSES · These results test the evaluation machinery…`, `4/4 Passed / scheduled`, the per-case table (`Outcome agreement 100% (2/2)`), effort per run, every run's checks and trace |
| `90-help.txt` | **README.md:795** | `python cli.py --help`: usage and every option |
| `91-x-outputs.txt` | extra | `outputs/` from inside the container (5.4 MB) |
| `92-x-render-run.txt` | extra (README.md:88 `render_run(DB_PATH, run_id)`) | the chat view of the run of 33 as text: `Act 3 · manager-approval`, `Scripted responses Execution: completed Recorded view · not a live chat`, the request, `Workflow outcome: placed`, the receipt, workflow steps, context sources, `Manager approved · source: human`, the recorded events |

### `expected/` — what the tutorial documents, for what cannot run here

Made by `expected_outputs.py` from the Colab JSON and `source/README.md` (no Docker, nothing run). First line of each
file: where it comes from.

| file | tag | source | used for |
| --- | --- | --- | --- |
| `colab-c08-install.txt` | recorded | Colab cell 8 ("Install Dependencies"), saved output: `CompletedProcess(args=['/usr/bin/python3', '-m', 'scripts.check_sdk'], returncode=0)` | the Colab path's setup |
| `colab-c11-utils.txt` | recorded | cell 11 ("Utils"): `Model: gpt-5.6-luna`, `live model` | the Colab path |
| `colab-c13-catalog.txt`, `-c14-policies.txt`, `-c15-pairings.txt` | recorded | cells 13-15: the 12-cheese catalog, the seven policies (`Manager approval above $200 cheese subtotal`, `Raw-milk shipping blocked to PA, NJ, MD, NC`, `Revisions allowed 2` …), the seven pairings | the shop's data |
| `colab-c16-customers.txt` | recorded, **names replaced by `<name>`** | cell 16: `pavlos … [French cheeses, funky cheeses]`, `shivas … [mild cheeses, nonalcoholic pairings]` | saved preferences (show IDs and preferences only) |
| `colab-c17-request.txt` | recorded | cell 17: the standard request sentence and the structured fields | the confirmed request |
| `colab-c18-data-constraints.txt` | recorded | cell 18's styled table as text: each cheese against `raw-milk → PA`, `nut allergen`, `out of stock`, `eligible`, `French & funk≥4` (only Époisses is both) | context selection |
| `colab-c21-bare-agent.txt` | recorded (**live model**) | cell 21, the bare SDK agent: `Proposed tasting for 12 guests: 1,050 g … Cheese subtotal: 5,600¢ … the order has not been placed.` | Act 1 without the harness |
| `colab-c23-agent-harness.txt` | recorded (**live model**) | cell 23, the traced Act 1 run: six model calls (1942 … 4540 input tokens), five tools, `🧾 BASIC CONTEXT — run 5a53…`, the answer with **"within your 1,5000¢ budget"**, `🔍 Independent cart check (no automatic repair):` `✅ Cart satisfies the shop rules.`, `📊 Model calls: 6. Tool calls: 5.` | Act 1 live (`python cli.py --act 1 --scenario standard`); the hook |
| `colab-c24-response-view.txt` | recorded (**live model**) | cell 24, `show_chat(...)`'s HTML as text: the request, the answer, `Independent cart check: passed`, 22 agent-activity lines, `Inspect recorded events · 38` with every event's JSON | the chat view |
| `readme-verify.txt` | expected | README.md:118-133 | "The test suite should finish with `OK`" |
| `readme-act1-standard.txt`, `readme-act1-missing-details.txt` | expected | README.md:175-200, 242-252 | Act 1 live: the scenario, what the console shows, what to look for |
| `readme-act2-intro.txt`, `readme-act2-pa-ny.txt`, `readme-act2-evaluate-live.txt`, `readme-act2-standard.txt`, `readme-act2-compare-notes.txt` | expected | README.md:258-266, 277-281, 292-301, 316-330, 849-866 | Act 2 live: what the comparison measures, the PA/NY block, 12 live runs, the baseline |
| `readme-act3-pa-shipping-preview.txt`, `readme-act3-standard.txt`, `readme-act3-shipping-lesson.txt`, `readme-act3-manager-fixture.txt` | expected | README.md:283-290, 361-367, 369-402, 404-410 | Act 3 live: `Cart attempt 1: shipping`, `RAW MILK`, `WORKFLOW BLOCKED`, a second model call, `Removed: Comté`, a validated order |
| `readme-act4-live.txt`, `readme-act4-memory.txt` | expected | README.md:454-471, 481-488 | Act 4 live: 1,000 g Comté + 1,000 g Mimolette + 1,200 g Époisses, $177.80, the 300 g shortfall, the review prompt, the second visit's memory |
| `readme-act5-live.txt`, `readme-act5-stock-question.txt` | expected | README.md:537-545, 549-555 | Act 5 live: which skills and resources load; 900 g |
| `readme-act6-live.txt`, `readme-act6-two-orders.txt` | expected | README.md:631-641, 643-658 | Act 6 live: outer vs workflow model calls, receipt quantities |
| `readme-eval-live-compare.txt`, `readme-eval-judge.txt` | expected | README.md:723-751, 753-765 | the live A/B and what the checks do not establish |

The README prints no sample output for any live command; it describes what to look for. These passages are README
text, not program output: scenes show them as the README's words (a quote card, or the command with "what to look
for" beside it), never inside a terminal panel. The Colab outputs are the staff's own live run (no date stored; cells
26-58, Acts 2-6 and evaluation, have no saved outputs) and are tagged `recorded`.

### `capture-only/` and the differences from a student's laptop

- **`base-python-3.13-slim-bookworm.Dockerfile` + `-build.txt`:** before the README steps the capture pulled
  `python:3.13-slim-bookworm` into the laptop and rebuilt it under the same name with the recording proxy's CA, https
  apt sources and `SSL_CERT_FILE`/`REQUESTS_CA_BUNDLE`/`PIP_CERT` (the L05/L06 recipe), so the tutorial's own
  `Dockerfile` builds unchanged behind the proxy. Visible effects: in `laptop/07` step `[1/6] FROM` takes 0.0 s
  (a student's first build pulls the base image there); `laptop/09` lists the rebuilt base image (128 MB), which a
  student's `docker images` after a BuildKit build would not show.
- **Network:** the laptop reaches the internet through `proxy_relay.py` (container `l07-relay`); the laptop's
  `~/.docker/config.json` passes the relay to builds and to the `agent-harness` container as `HTTPS_PROXY`. That is
  why the live commands reached OpenAI at all (and got the 401). `laptop/10` filters the container's environment to
  the three variables `docker-shell.sh` sets.
- **Storage:** the laptop's engine keeps its images in a 6 GB tmpfs (classic overlay2 store, so `docker images` shows
  `CONTENT SIZE 0B`); the student's home is a 1 GB tmpfs. Not visible in any output except the size columns.
- **Terminals:** `laptop/07` and `laptop/12` ran in a real 80×40 terminal (`tty_session.py` with `pyte`), so BuildKit
  printed its live view; `container/33-34` in a 250-column terminal; everything else without a terminal (plain lines).
- **The editor step** (README.md:737) is `container/82`, a one-line `printf` append, so that 84's prompt file differs.
- **Timings vary:** the build took 38.2 s here and 51.3 s in a trial run ten minutes earlier (downloads go through the
  recording proxy); `python -m tests` took 99-103 s. Say "about" for durations.
- **Not reproduced:** the `PermissionError` of digest §6 (the clone here is owned by uid 1000, the same as `app`);
  Windows CRLF line endings; an Apple Silicon build.
- `capture-only/laptop-timings.txt`, `container-timings.txt`: per-step UTC end time and duration (tty steps: seconds
  to exit).

## Steps that cannot be captured, and how the video shows them

| step | why not | shown as |
| --- | --- | --- |
| Everything a live command prints after its first model call (Acts 1-6 live, `--act 2 --compare`, the live `--evaluate` batches; README.md:178, 195, 245, 269, 272-274, 286, 295, 321, 364, 376, 379, 457, 484-485, 542, 634, 728, 742) | needs an OpenAI key and paid tokens | the real capture up to the first call (headers, ask, tools, memory, skills metadata) and, where the scene needs it, the 401 as the "forgot the placeholder" moment; Act 1's full run from Colab cells 21/23/24 tagged `recorded`; the other live runs by the README's own words (`expected/readme-*.txt`, tagged `expected`) and by the offline `--fixture` runs of the same code path (`container/33-37, 41-42, 51-54, 61-62, 74`), labelled "scripted proposals", never as model output |
| The PA/NY block after an individual Act 2 run (README.md:277-281) | printed only after the live runs | `container/29` (the same function, called directly) |
| The Colab path (cells 7-10: clone into `/content`, `pip install`, the Secrets key) | needs Colab and a key | the cell sources from `source/colab/`; the saved outputs of cells 8 and 11 (`recorded`); the Secrets panel as a schematic drawing tagged `illustration` (no screenshot) |
| `show_chat(...)` in a notebook (README.md:82-83) | the image has no IPython | Colab cell 24 (`recorded`) and `container/92` (`render_run`, same HTML, as text) |
| Opening the HTML scorecard in the host browser (README.md:709) | no browser here | `container/89` (its visible text); a drawn scorecard tagged `illustration`, with the numbers from 89 |
| "Open the copy in your editor" (README.md:737) | an editor is interactive | `container/82-83`: the one-line change and its diff |
| The notebook cells the README prints (README.md:76, 82-83, 209-224, 422-431, 493-503, 567-575, 618-624) | notebook code with top-level `await`, not shell commands | code panels quoting `source/README.md`; their offline counterparts run in `container/07` (the notebook tests), 35, 41, 51 and 62 |

## Surprises (README vs what ran)

1. **The README's placeholder key fails loudly.** With `export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"` typed as written,
   every live command stops at its first model call with `Incorrect API key provided: YOUR_OPE*******_KEY` (OpenAI's
   own masking), exit 1, and the run is still recorded (status `error`). Live `--evaluate` batches give up after three
   consecutive errors (`Failures: 0; errors: 3; missing: 9.`) and exit 1, but `--view-report` and `--compare` still
   work on those batches. `docker inspect` shows the key in the container's configuration (`laptop/10`).
2. **The SDK's "misleading approval-identity warning" is real and appears on every email review** (README.md:837,
   847; digest O3, which could not reproduce it): `Ignored an approval response with id 'af-call-…' because it did not
   match the active approval occurrence identity; the pending request was retained for retry.` It prints right after
   the `MOCK EMAIL REVIEW` in `container/41`, `42` and `52`, and the outcome is still correct (DECLINED / SAVED, the HTML
   saved once). `--show-logs` prints it 118 times.
3. **`--fixture --scenario pa-shipping-blocked` ends `UNRESOLVED`, not `BLOCKED`** (`container/37`): fixtures skip the
   review-only intake, so the bad cart is proposed three times until the revision limit. The live "before" run is the
   one that stops at `BLOCKED` (README.md:382-383; not capturable here).
4. **The README's `Removed: Comté` is shorthand** (E4): the real line is `Removed: Comté 18 mois (comte) — 350 g`
   (`container/36`).
5. **The live shipping lesson changes the customer ask.** Live runs append `For this tasting, here's what I have in
   mind: My starting cart is 350 g of Comté, 350 g of Bûcheron, and 300 g of Époisses. …` (`container/24, 31, 32`);
   the fixture runs do not (`container/36, 37`).
6. **"12 live runs" is counted as 4 cases × 3 repeats** (`container/25`: the CLI counts each case × context mode as a
   case); the README says "both modes (12 live runs total)", the same number.
7. **The banner claims activation before it happens** (E10, `laptop/07`): `Environment ready! Virtual environment
   activated.` prints before `Activating virtual environment...`; the Python it reports, 3.13.16, is the base image's.
8. **The image is big:** 1.77 GB, `/.venv` 646 MB, 209 packages, including `claude-agent-sdk` 0.2.160 and
   `agent-framework-gemini` that the tutorial never imports. No `.dockerignore`: the build context (2.11 MB) includes
   `.git`.
9. **Memory is host-written** (SLIDES.md conflict 6): Act 4's tools include no memory tool (`container/40`), and the
   first `--remember-preference` run already prints the merged memory before any model call (`container/43`).
10. **No skill scripts** (SLIDES.md conflict 2): Act 5's tools are `load_skill` and `read_skill_resource`, no
    `run_skill_script` (`container/50`).
11. **Two approvals, one order** (README.md:651, `container/61`): request-2 is blocked at final checkout with
    `⚠️ stock: Requested 1600 g; available 1400 g.` for mimolette and taleggio.
12. **The README's two template commands fail as written**, as templates do: `--inspect-run RUN_ID` → `Unknown run ID`
    (`container/72`), `--view-report COLAB_LABEL --db outputs/colab.sqlite` → `Recorded database not found`
    (`container/78`), both exit 2.
13. **Date:** the captures were made on 2026-10-20 (not 2026-10-13); the repo's `main` was unchanged since 2026-09-28.
