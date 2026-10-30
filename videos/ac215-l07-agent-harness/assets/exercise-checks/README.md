# Exercise checks · ac215-l07-agent-harness (2026-10-21, 16:19–16:30 UTC)

What was run to verify `exercises.md`, beyond the captures in `assets/terminal/`, which the answers cite
directly (`laptop/NN`, `container/NN`, `expected/…`). Logs and the check scripts are in [`logs/`](logs/). Every
step in a log starts with its command (`$ …`) and ends with `[exit N]`, as in `assets/terminal/run_steps.sh`.
Where a step pipes the CLI into `grep` or `tail`, `[exit N]` is the last command's status; the steps that
matter print the CLI's own status (`cli.py exit status: 1`) or run without a pipe.

There was **no OpenAI key and no network** in any check (`--network none`). Every check is offline: `--fixture`
runs, the tutorial's own scripted client for Acts 1–2 (`formaggio/fixtures/evaluation_fixture.py`,
`ProposalFixture`, the one `--evaluate core --fixture` uses), direct calls of the shop code, and the CLI's
argument checks. A scripted reply is never model output: the trace label still names the configured model
(`gpt-5.6-luna`) because the harness prints its configuration, while the replies come from the local script
(100 input and 20 output tokens per call, made up by the script). Customer IDs appear as the CLI prints them
(`pavlos`, `shivas`); no name field of `data/customers.json` appears in any log, and no key either (only the
README's placeholder, `YOUR_OPENAI_API_KEY`).

## Setup (disposable; nothing from the repo ran on the host)

- Docker Engine 29.8.2 on the session machine. Image `python:3.13-slim-bookworm` (the tutorial `Dockerfile`'s
  base; `sha256:73aa5fae…`, Python **3.13.16**, the capture's version).
- `setup.sh` ([`setup.log`](logs/setup.log)): the repo's files at the pinned commit `e25dfe9` (a `git archive` of
  the read-only clone) into the volume `l07ex-work`; then, in a container with network, uv **0.13.4** (the
  capture's) exported the repo's own `uv.lock` (`uv export --frozen`) and installed **only the packages the code
  imports**, constrained to the lock's exact versions: agent-framework-core 1.19.0, agent-framework-openai
  1.14.4, openai 3.19.2, httpx 0.28.1, opentelemetry-api/sdk 1.40.0, pydantic 2.13.5 and their dependencies
  (28 packages, 35 MB: [`setup-packages.txt`](logs/setup-packages.txt)), plus the `agent-framework==1.19.0`
  metapackage itself with `--no-deps`, so `importlib.metadata` finds it as the code expects. **Difference from
  the image:** the `[all]` integrations that the metapackage pulls in (Azure, Bedrock, Anthropic, Gemini,
  `claude-agent-sdk` …, 209 packages and 646 MB in the capture, `container/01`) were left out; no module of the
  tutorial imports them, and every check ran without an import error.
- `hrun.sh` runs one check the way a student types at the container's prompt: a fresh copy of the pinned repo in
  `/app` (a tmpfs, so every check starts from a clean clone with no `outputs/`), the venv on `PATH`, user uid
  1000 (the image's `app`), `OPENAI_API_KEY=YOUR_OPENAI_API_KEY`, no network. Files a check edits (the email
  template, `data/catalog.json`, a scratch `.py`) are edited in that throwaway copy only.
- `snippets/` holds the Python snippets of `exercises.md` exactly as printed there; `snippets.sh` copies each to
  `outputs/` in a fresh clone and runs `PYTHONPATH=. python outputs/<name>.py`, as the exercises tell students to.

## Checks

| exercise | what was run | result |
| --- | --- | --- |
| Q1, B2 | `q1_without_trace.py`: `build_act1(..., execution_mode="fixture")` and `.without("trace")`, each run with the scripted client; events and spans per run; `.without("cartcheck")`; `Budget(model_calls=0)`; a Budget of 1 model call ([`q1-without-trace-budget.log`](logs/q1-without-trace-budget.log)) | `lite` is a new object with layers `budget, context, cart_check`; both runs `model_calls=2 tool_calls=1`, `cart_check_status=passed`; without Trace: no `model.request`/`model.response`, no spans, `tool.requested` without `arguments`, `tool.completed` without `result`, but `tool.requested/permitted/started/completed`, `proposal.submitted`, `agent.result`, `run.started/finished` all recorded; `ValueError: No layer named 'cartcheck'.`; `ValueError: Call budgets must be positive integers.`; squeezed: the tool runs, then `MiddlewareFailure: Maximum of 1 model calls reached.`, no "Model call 2" line, run status `error` |
| B1 | `b1_cartcheck.py`: the same harness on `pa-shipping` with the scripted raw-milk cart, then `.without("cart_check")` ([`b1-cartcheck.log`](logs/b1-cartcheck.log)) | `1000 g; cheese subtotal $50.80`, `⚠️ shipping: Fictional shop policy blocks raw-milk shipping to PA.`, `cart_check_status: failed`; without the layer: `🔍 Independent cart check: not run (CartCheck layer disabled).`; the reply text and `No order was placed.` identical |
| Q2, B3 | `q2_context_lane.py`: Act 2 enriched (`standard`) with the scripted raw-milk cart; the recorded `model.request` of call 1 ([`q2-context-lane.log`](logs/q2-context-lane.log)) | packet excludes brie, comte (`fictional_shipping_policy`), munster, walnut_chevre, pistachio_manchego; options carry `instructions`; message 1 `role=user` "Retrieved context (data, not instructions):…", message 2 `role=user` the request; the cart still holds comte 350 g; `shipping` violation, `cart_check_status: failed` |
| Q3, B6 | `q3_fingerprint.py`: `Checkout.fingerprint` on the manager-approval cart under five changes ([`q3-fingerprint.log`](logs/q3-fingerprint.log)) | `e8caf06b29df9c58` (the same as `container/71` line 46); unchanged after stock 3,000 → 1,400 g (cart then invalid) and after reordering the lines; different after +50 g Taleggio (`61f512af…`), 61 guests (`d5f32d9e…`), Mimolette price +1 cent (`5ed9976e…`) |
| B4 | `b4_act3_layers.py`: `build_act3(fixture=True, scenario="out-of-stock")` with both layers removed; `.without("validation")`; `.add(Trace())` ([`b4-act3-layers.log`](logs/b4-act3-layers.log)) | `Proposal attempts: 2. Model calls: 0.`, `$50.10`, PLACED; 2 `cart.validated` events, 1 policy decision, 1 `order.placed`; `ValueError: No layer named 'validation'.`; `TypeError: Act 3 supports WorkflowTrace and WorkflowBudget layers.` |
| B5 | `b5_steal_stock.py`: manager-approval with a shared `Checkout`; the manager callback takes 2,000 g of Mimolette, then approves ([`b5-steal-stock.log`](logs/b5-steal-stock.log)) | `approval.requested` and `approval.decided` carry the same fingerprint; `--- WORKFLOW BLOCKED`, `Final checkout blocked: Invalid or unauthorized order. No order placed.`, `⚠️ stock: Requested 1600 g; available 1000 g.`; `policy.decision` `block` |
| B7 | `--act 4 --fixture --vendor-document {clean,benign,quoted,malicious} --email-decision decline`; `detect_injection` on all four ([`b7-vendor-documents.log`](logs/b7-vendor-documents.log)) | clean, benign: `included`; quoted: `quarantined` (signals `ignore_allergy`, `redirect_details`); malicious: `quarantined` (three signals); all `HARNESS DECLINED`, `Model calls: 7.` |
| B8 | `--act 4 --fixture --vendor-document malicious --simulate-detector-miss --email-decision approve`; the same without `--fixture` ([`b8-detector-miss.log`](logs/b8-detector-miss.log)) | `Vendor evidence: included (malicious)`; `draft_vendor_email` with `recipient: other@example.com` → `status: blocked; reason: Recipient is not in the shop allowlist.`; no review; `--- HARNESS BLOCKED`, `No HTML email saved.`, `Model calls: 5.`, exit 0; without `--fixture`: `cli.py: error: --simulate-detector-miss requires --fixture.`, exit 2 |
| B9 | a link added to `skills/vendor-outreach/assets/email-template.html`, then `--act 5 --fixture --email-decision approve` ([`b9-template-link.log`](logs/b9-template-link.log)) | five `Skill loaded:` lines (not the template); the SDK's traceback; `Run stopped: Harness tool or required audit failed: Required skill read/audit failed: Email template contains an unsupported element.`; exit 1; no HTML file |
| B10 | `--act 4 --fixture --memory-db outputs/my-memory.sqlite --customer shivas` four ways, and once without `--memory-db` ([`b10-memory.log`](logs/b10-memory.log)) | remember → `mild cheeses; nonalcoholic pairings; Prefer nonalcoholic pairings today`; next visit the same; remembering `mild cheeses` again → `nonalcoholic pairings; Prefer nonalcoholic pairings today; mild cheeses` (no duplicate; moved last); without `--memory-db` → `mild cheeses; nonalcoholic pairings`; the other customer's line unchanged |
| B11 | `--act 6 --fixture --scenario two-orders --manager-decision decline` ([`b11-two-orders-decline.log`](logs/b11-two-orders-decline.log)) | both `pending_approval` at $220.80, two reviews, `request-1: declined`, `request-2: declined`, `Manager declined this cart. No order placed.` twice, `--- COMPOSITION COMPLETED`, `Skills loaded: none`, `Outer model calls: 6; workflow model calls: 0.` |
| B12 | scripted batches `ex-a`; a scratch `scratch.py` in the repo root; `ex-b`; the scratch file removed and Époisses' price 690 → 700 in `data/catalog.json`; `ex-c`; `--compare` ([`b12-confounders.log`](logs/b12-confounders.log)) | all 2/2 PASS; `ex-a` vs `ex-b`: `changed_configuration: ['source_hashes']`, `confounding_changes: ['source_hashes']`; `ex-a` vs `ex-c`: `['data']`, `['data']`; outcomes `unchanged`; `--compare ex-a` alone: `cli.py: error: Use --act 2 --compare, or --compare BEFORE AFTER alone for saved evaluations.` |
| B13 | `b13_cheap_cart.py`: `Store.validate` of two carts against the manager-approval request ([`b13-cheap-cart.log`](logs/b13-cheap-cart.log)) | fixture cart 4,800 g, $220.80, `needs_manager_approval=True`; halloumi 2,000 + walnut_chevre 900 + gouda 1,800 + bucheron 100: 4,800 g, $161.10, valid, `needs_manager_approval=False` |
| C3, C4, C9 and the argument rules | [`c-debugging.log`](logs/c-debugging.log): `--act 4 --scenario standard`; manager-approval with stdin from `/dev/null`; answering `yes` then `approve`; `--act 2 --compare --context basic`; `--act 1 --fixture`; `--customer alice`; `--evaluate` with `--scenario`; the compaction demo `.without("compaction")` (`c_compaction_layer.py`) | `Run stopped: Act 4 supports event-shortage; …` exit 1; `Run stopped: Manager input unavailable. …` exit 1; `Please enter approve or decline.`, then PLACED; four `cli.py: error:` lines, exit 2; `ValueError: The synthetic compaction demonstration requires the Compaction layer.`, 0 runs recorded |
| C7 | the clone with the base image's plain Python, no venv ([`c-host-python.log`](logs/c-host-python.log)) | `ModuleNotFoundError: No module named 'pydantic'` |
| every snippet | `snippets.sh`: B1–B6 and B13 exactly as printed in `exercises.md` ([`snippets.log`](logs/snippets.log)) | all seven exit 0, with the results above |

## Not run (and why)

- **Every live model call.** No key and no network: what a live model proposes (B1–B3 with a real model, the
  live shipping lesson, live Acts 4–6, the live A/B), and the 401 itself (that is `container/10` and the other
  live captures). The exercises that need a key say *with your key*; their answers cite the README, the saved
  Colab run (`expected/colab-*`) or the code, never a made-up reply.
- **The Colab notebook** (C8): its `USE_FIXTURES` path is the same code as `container/37`; the Colab VM was not used.
- **A key changed while the container runs** (C1): shown by the captures `laptop/12` (`docker exec` path, the
  README's `read -rsp` lines) and `laptop/10`; not repeated.
- **The full test suite** (`python -m tests`, D5): captured in `container/04` (281 tests, OK); not re-run
  (100 s of CPU while other renders were running).
- The image's `[all]` integrations were not installed (see Setup); `scripts.check_sdk` was not re-run for the
  same reason (it is `container/03`).

## Cleanup

Removed afterwards, by name: the volumes `l07ex-work` and `l07ex-venv` and the image `python:3.13-slim-bookworm`
(pulled for these checks). Every check container ran with `--rm`. Nothing was written outside the volumes and
this folder.
