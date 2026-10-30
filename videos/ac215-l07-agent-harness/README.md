# AC215 · Lecture 7 — LLM: Agents II: the agent harness

A follow-along walkthrough of the Lecture 7 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall 2026)**:
[dlops-io/agent-harness](https://github.com/dlops-io/agent-harness), branch `main` @
[`e25dfe9`](https://github.com/dlops-io/agent-harness/tree/e25dfe9615d78b78e0764a636cc2462f530a1402), the whole
README: *Setup and verification*, *1. Recap — agent and tools*, *2. Context Engineering — choose what the model
sees*, *3. Agent Harness — manage execution and enforce boundaries*, *4. Skills — load reusable guidance when
needed*, *5. Agent Systems — compose a harness and a workflow*, *6. Evaluation — inspect, repeat, and compare*,
*7. Additional Resources* and *Troubleshooting*; and the course Colab notebook
[Agent Harness](https://colab.research.google.com/drive/1ZYMsbG0gqsbs-6Pcj8WtT3WhEa4f80EZ?usp=sharing) (a notebook has
no commit: the copy the video quotes, downloaded on October 17, 2026, is in `assets/source/colab/`).

The tutorial doesn't ask you to write an agent. It hands you one, an OpenAI model with five shop tools in a
fictional cheese shop where nothing is really bought, shipped or emailed, and wraps it in more and more code, act
by act: named harness layers around the loop (Act 1), a context packet chosen by Python (Act 2), a workflow graph
whose edges Python owns, with an approval bound to one exact cart (Act 3), a planner with five kinds of state,
compaction and host-written memory (Act 4), skills that guide and never permit (Act 5), an agent that calls the
whole workflow as a tool (Act 6), and the traces and repeated batches that show what happened (Evaluation). The
rule that ties it together is the course notebook's: **the model proposes; the harness decides.**

Watch it with your `~/AC215/agent-harness` clone open, an empty `~/AC215/secrets` beside it, Docker running, and,
for the live commands, an OpenAI API key with billing (the only cost: OpenAI tokens; no cloud project, no service
account, no ports). The tracker top left shows the README (or notebook) step; pause at every `▶ your turn` to run
the command; a gray `extra` tag marks a check that isn't in the README, a gray `scripted` tag a run whose model
seat is the tutorial's own script (`--fixture`), and a gray "Lecture 7 · slides …" tag top right points to the
lecture slides the scene stands on. The video was recorded on October 20, 2026 **without an OpenAI key**: the build,
the 281 offline tests and every offline and scripted command ran for real (Docker Engine 29.8.2, Python 3.13.16,
uv 0.13.4, agent-framework 1.19.0, default model `gpt-5.6-luna`); every live command ran up to its first model call
and stopped at OpenAI's 401 for the README's placeholder key; live answers are the staff's saved Colab run, tagged
`recorded`, and the README's own descriptions, tagged `expected`. The customer IDs are masked on screen (your
terminal and the README show them). Series format: [`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study
guide with every command:
[MLOps_Learning · guides/L07-agents-2-harness.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L07-agents-2-harness.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l07-agent-harness.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, 31:21 (1881.75 s), 113.7 MiB. Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l07-agent-harness.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. A release asset, not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l07-agent-harness_part1.mp4` | part 1, 13:51 (831.25 s): one agent — setup, the agent loop, harness layers and context (Acts 1–2; S01–S07). A release asset, not in Git: rebuilt with `--no-render` |
| `output/ac215-l07-agent-harness_part2.mp4` | part 2, 17:30 (1050.61 s): the harness takes control — workflows, approvals, memory, skills, agent systems and evaluation (Acts 3–6; S08–S16). A release asset, not in Git: rebuilt with `--no-render` |
| `output/ac215-l07-agent-harness.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l07-agent-harness.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l07-agent-harness.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, thirteen hands-on predict-then-run tasks, all offline and free (CartCheck without the layer, a budget of one call, Comté through the enriched packet, Act 3 without its layers, stock that vanishes during an approval, the fingerprint by hand, four vendor notes, a detector that misses, a link in a skill's template, persistent memory, two declined orders, a comparison with a confounder, a valid cart under the manager threshold), nine debugging and six think questions, with answers |
| `assets/exercise-checks/` | what was run to check `exercises.md`, in throwaway containers of the tutorial's base image with the lockfile's versions, with every log and script; every Python snippet of the exercises run exactly as printed |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the instructor's slides in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from: a fresh laptop with Docker Engine 29.8.2 and the tutorial's own image, every README command in README order, exactly as written, on October 20, 2026, without a key; and in `expected/` the Colab's saved outputs and the README's descriptions of live output. Provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commit (all 126 tracked files), and the Colab notebook's cells |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s (the burned-in copy, the clean video and
the two part cuts) are GitHub release assets.

## Chapters

Paste-ready in `output/chapters.txt` (and `chapters_part1.txt`, `chapters_part2.txt` for the parts).

```
00:00 Which sentence would you trust?
02:00 One container, no ports
04:09 Verify offline, and the Colab road
05:47 Act 1: an agent, measured
07:42 Act 1: wrap it in a harness
09:50 Act 2: same agent, different context
11:49 Act 2: sieves and lanes
13:51 Act 3: rails, not suggestions
15:41 Act 3: approve this exact cart
17:44 Act 4: a planner with five drawers
19:19 Act 4: compaction, the capsule and memory
21:34 Act 5: skills are manuals, not keys
23:44 Act 6: an agent that calls a workflow
25:33 Evaluation: the trace is the evidence
27:16 Evaluation: one change, k runs, a diff
29:17 Tear down, recap, and what's next
```

Part 1 uses the first seven lines as they are. Part 2 starts its clock at 0:00:

```
00:00 Act 3: rails, not suggestions
01:50 Act 3: approve this exact cart
03:53 Act 4: a planner with five drawers
05:28 Act 4: compaction, the capsule and memory
07:43 Act 5: skills are manuals, not keys
09:53 Act 6: an agent that calls a workflow
11:42 Evaluation: the trace is the evidence
13:25 Evaluation: one change, k runs, a diff
15:26 Tear down, recap, and what's next
```

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: whether a copy made with
`harness.without("trace")` still counts and audits its tool calls, and whether the original still traces; whether
the model can still put Comté in its cart after the enriched packet removed it, and what in Act 2 would stop it;
what checkout does when another order takes the Mimolette after the manager approved; how every model call still
knows about the nut allergy after compaction dropped 21 of 26 messages; and whether an edited skill can send the
vendor email to another address. Five test-yourself questions close the video (answers in `exercises.md`).

**Part 1 · one agent — setup, the agent loop, harness layers and context (Acts 1–2)**

1. **Which sentence would you trust?** — one tasting request (12 guests in Pennsylvania, a $150 budget, no nuts, a
   French cheese, one with a funk rating of 4 or more) and two answers from the same model and tools in the staff's
   saved Colab run: 1,050 g for 5,600 cents, and 1,200 g for 6,400 cents "within your 1,5000¢ budget"; which would
   you let charge a card; the second run's independent cart check (1,200 g, $64.00, shop rules satisfied, no order
   placed): the cart was valid, only the sentence was garbled, and nothing checked the first answer's cart; the
   model proposes, the harness decides; the harness as the code around the model (the loop, its limits, its
   context, its checks); lecture 7 and the README share seven sections, in order; the tracker and the slide tag;
   the honest limit (no key: offline for real, live commands up to OpenAI's refusal, live answers from the saved
   run and the README); the only cost, OpenAI tokens.
2. **One container, no ports** — the stage `docker-shell.sh` builds: the clone and an empty `secrets/` mounted, the
   key as an environment variable, no published port, HTTPS to OpenAI the only call out; two extras (`git clone`,
   `cd agent-harness`) and a listing without `docs/`; step 1, `mkdir -p ../secrets` (nothing reads it: no service
   account); step 2, the key export (your key, or skip it offline; typed as written here); step 3, `bash
   docker-shell.sh`: 38 seconds with the base image already on the machine, a minute or more for a first build;
   the lockfile installed before the code is copied (lecture 2's layer trick); a banner that says "activated"
   before it activates; the container ID; from a second terminal, `docker ps` (no ports), `docker images` (1.77 GB,
   since the framework installs every integration) and `docker inspect` (the key sits in the container's
   configuration); step 4: `docker exec` into a running container doesn't bring a new key, so the README's three
   lines put it in hidden and out of your history.
3. **Verify offline, and the Colab road** — `python -m scripts.check_sdk` (Python 3.13.16, agent framework 1.19.0,
   every feature true, at the time of recording); `python -m tests`: 281 tests in about 100 seconds, ending in OK,
   on scripted model responses: they test the machinery, not the model; `--show-logs`: deliberate failures and an
   approval-identity warning; trust the last line; the model check (`gpt-5.6-luna`) and its precedence (`--model`,
   then `OPENAI_CHAT_MODEL`, then the default); the notebook section's two test commands (9 and 12 tests, OK), run
   in the container too; the Colab road: a copy in your Drive, the `OPENAI_API_KEY` secret with notebook access,
   the setup cells; Colab installs the seven pinned packages, not the lockfile (for identical versions, use
   Docker); every recorded answer in the video comes from this notebook's saved run.
4. **Act 1: an agent, measured** — the lecture's recap (a model with instructions and tools, running until the task
   is done); `build_agent`: the shop instructions, five tools and a structured reply format; the model can only ask
   for a tool, the harness runs it; none of the five can place an order (`preview_order` records an unvalidated
   proposal); step 1 live: the ask, call 1 and five tools, then the 401 of the placeholder key (fix it in the
   container shell with setup step 4's lines; the failed run is still recorded); the staff's saved run, round by
   round: catalog, stock, price, pairings, preview, and on call 6 an answer with no tool request; the lecture's seam
   (requested tools is the model's plan, tool call is the harness executing; the trace shows requests and results,
   not hidden reasoning); messages 1 → 11, input 1,942 → 4,540 tokens, about 21,000 billed input tokens for one
   answer; step 2, `--show-json` (null means not provided); the lecture's question: how do we manage what goes into
   the model?
5. **Act 1: wrap it in a harness** — "if you've written a loop that calls a model and runs its tool calls, you're a
   harness engineer", and a bare loop has no stop; step 3, the notebook cell: Trace, Budget (8 model calls, 20 tool
   calls, 120 seconds), basic Context and Cart Check, the same harness the CLI builds; the inner ring that never
   comes off (call admission, the tool audit, the shop rules); Budget as a turnstile (a ninth call fails, and the
   lock stays shut); without Budget, only the framework's fallback of 40 loop iterations; Cart Check as the
   lecture's verify step: it checked the items, not the prose, so the garbled budget passed; it reports and never
   repairs; the lecture's action boundary (five concerns, the model's part left, the harness's right), Act 1's three
   rows, and when to move control right; `.add()` and `.without()` return new configurations; step 4, missing
   details (look for a question back, and Cart Check's no cart).
6. **Act 2: same agent, different context** — the lecture's invisible layer; one model call as the lecture's stack
   (system prompt and shop policies, the request, the reply format, five tools, and slots for retrieved data and
   saved preferences); basic sends the first four, enriched fills the slots; step 1, `--compare` on the
   personalized scenario (the second customer's saved taste: mild cheeses and nonalcoholic pairings), which stops at
   the 401 before enriched starts; with a key, a side-by-side table and a verdict that may be a tie or a regression;
   steps 2–4: basic sends 1 conversation message, enriched 2, the extra one the context packet; the override run,
   where today's request must win over the saved taste; the PA/NY check the README promises after every Act 2
   command (`--compare` doesn't print it; an extra call does: the same raw-milk cart fails for Pennsylvania and
   passes for New York, under a fictional rule); step 5, an Act 3 command the README puts here; steps 6–7: 12 live
   runs, stopped after 3 errors, a report that still writes, and a label used up; a linked page that was never
   published.
7. **Act 2: sieves and lanes** — "Inspect the context first", printed after the live runs: without a key, start
   with `--preview-context`, offline; instructions, message and tools shared, only the packets differ; basic has no
   sources, enriched three, each with a trust label; twelve cheeses through three sieves (enough stock, no raw milk
   to Pennsylvania, no nut allergens): seven survive; the lecture's retrieved information is any outside data, here
   a Python filter, not lecture 5's vector search; a user message headed "retrieved context, data, not
   instructions": the lecture's two lanes; the catalog tool still returns all twelve, and in Act 2 Cart Check only
   reports: selection narrows, validation decides; step 9, the optional baseline (for standard, the saved
   preferences repeat the request); today's request outranks saved preferences.

**Part 2 · the harness takes control — workflows, approvals, memory, skills, agent systems and evaluation (Acts 3–6)**

8. **Act 3: rails, not suggestions** — back at the container prompt; the lecture's move-right arrow and its four
   reasons; the order route as a graph whose edges Python owns (confirm, propose, validate, back to propose only if
   the report fails and at most twice, then pairings, manager review when required, revalidate and place); one node
   for the model, propose cart, with no tools; near "structured output" on the lecture's autonomy spectrum, filed
   under the harness by the README and under agent systems by the lecture; step 1 (success is a receipt); steps 2–3,
   the shipping lesson with a customer's own cart (Comté, Bûcheron and Époisses to Pennsylvania): before, the
   harness checks it and stops; after, the revise loop opens; the extra `--fixture` run: attempt 1's raw-milk Comté
   sent back, attempt 2 with Taleggio, valid at $50.10; the trap: with fixtures the blocked scenario ends
   unresolved, not blocked, so keep fixtures off in Colab for this lesson.
9. **Act 3: approve this exact cart** — the lecture's boundaries (permissions, sandboxing, budgets, checks); step 4,
   scripted: 60 guests in New York, a valid cart at $220.80, above the $200 threshold; the workflow pauses and you,
   the manager, type approve (the host answers, never the agent); the fingerprint: a SHA-256 over the request, the
   items, the subtotal, the policy and the product attributes, with stock left out on purpose; at checkout the cart
   is validated and hashed again, and the approval counts only for this decision, this checkout and this
   fingerprint; your thinking time isn't on the budget; decline, and no order; an approval authorizes a decision
   and doesn't reserve stock; step 5, out of stock: one bounded revision and $50.10, with zero model calls; step 6,
   the notebook cell: the trace and budget layers can come off, validation, approval and revalidation can't.
10. **Act 4: a planner with five drawers** — a 40-guest event in New York; the lecture's long-term and short-term
    memory become saved memory and history, plus tasks, approvals and the audit: five kinds of state, and only the
    approval drawer can authorize an action; step 1, live: the first customer's saved memory printed before any
    model call, the planner's tools, and no tool that writes memory; what to look for with a key (1,000 g each of
    Comté and Mimolette and 1,200 g of Époisses; 900 g in stock, 300 short; a finished task is not an approval,
    and shop stock is not vendor availability); `approval_mode="always_require"`: the framework pauses one tool
    where Act 3 paused a whole workflow; a scripted extra with approve: the vendor address, a body written by code
    with the nut allergy, status saved, email transmitted no, the file path; the approval-identity warning the
    README predicts: harmless, trust the authoritative block.
11. **Act 4: compaction, the capsule and memory** — step 2, offline: a scripted planner, compaction, a malicious
    vendor note and a test decline; twelve synthetic notes of about 15,000 characters; a 16,000-token window with
    2,400 kept for the reply, and above 80 percent of the rest, truncation drops the oldest messages until the
    history is back under half: 26 become 5; the capsule, re-pinned from application state before every call
    (confirmed request with its nut allergy, menu, tasks, pending reviews, open work), marked as data, not
    instructions; the lecture's compaction trigger and what persists where; the vendor note that says to ignore the
    allergy, quarantined by a deliberately small detector, while the real guards are the recipient allowlist and
    your review; the email still says nuts; declined, no HTML, 7 model calls and 7 compactions; steps 3–4, the
    memory exercise (typed as README line 484 writes it): the preference stored and printed before any model call,
    and again on the next visit; only the host writes memory, where the lecture would let the model suggest it;
    step 5, the notebook cell's five layers: without compaction, the capsule is still re-pinned.
12. **Act 5: skills are manuals, not keys** — folders of procedure loaded only when relevant, for the expertise gap
    and the context budget; three steps of rising token cost (every skill's name and description, about 100 tokens
    each; then its SKILL.md; then a reference or asset, only when needed); the lecture's scripts folder, and why
    this harness removes that tool (a skill advises, never executes); step 1: only the metadata at first, and three
    new tools (get stock, load skill, read skill resource); step 2, offline: one stock call, 900 g, and no skill
    loaded (with a key, the description is a hint, not a trigger); step 3, scripted: six loads with their real
    paths, and drafting refused until the email template is read, a backstop in code; the skill itself says it
    cannot add recipients or authorize actions, and every read is checked (no parent folders, absolute paths or
    symlinks; a file edited mid-run is refused); the recipient checked in code, nothing ever transmitted; tool =
    the hands, MCP = the socket (unused here), skill = the manual; step 4, the notebook cell, with 16 model calls.
13. **Act 6: an agent that calls a workflow** — one agent or a graph of agents (a manager calling agents as tools,
    or peers handing off); the manager pattern, except that the tool is the whole Act 3 workflow, with a model
    inside one node, and no handoffs; step 1, the notebook cell's budget (16 outer model calls, 20 tool calls, 8
    proposer calls per workflow, one shared 180-second clock); the host confirms the requests and the model only
    picks an ID; three narrow tools (start order, get order status, assess event); step 2, live: outer calls
    apart from workflow calls, and the outer agent can't approve its own order; step 3, offline: two orders sharing
    one shop, both valid at $220.80, both paused, both approved by the test decision; Mimolette and Taleggio at
    3,000 g: request 1 placed, 1,400 left, request 2 blocked at revalidation: approval is not placement; the final
    answer as the lecture's response step (the app fills quantities, prices and the status from the receipt);
    "invalid or unauthorized", and the stock lines that give the reason; a hybrid, inside out, on the autonomy
    spectrum.
14. **Evaluation: the trace is the evidence** — everything between the provider's model and the product is ours, so
    all of it must be tested; outcome, trajectory and cost as outcome and process checks plus calls and tokens;
    evaluation step 1: every run in one SQLite database, failed live runs included; `--inspect-run RUN_ID` is a
    template (typed literally, it fails); the manager-approval run's events in order (approval requested with the
    fingerprint, approval decided by a human, policy decision allow, order placed, run finished): the evidence for
    "order placed" is an event, not the prose; the first failed live run: a failure is evidence too; evaluation
    step 2, offline: the scripted act 2 batch passes 4 of 4, which tests the machinery, not the model; the report,
    the HTML scorecard at its default path or one you choose, opened from the outputs folder on your laptop; the
    Colab template command, and labels that are immutable.
15. **Evaluation: one change, k runs, a diff** — the lecture's warning that a prompt edit can fix one case and break
    three, so compare per case; the improvement loop (a failure, a test case, one changed layer, the suite run k
    times, a comparison with the baseline, merge or iterate); evaluation step 3: Batch A (4 live runs; without a
    key, 0 of 4, with 3 errors and 1 missing; after a failure, new labels for both), a copy of the prompt edited on
    your laptop (one deliberate change), our extra's appended line and its diff, Batch B with `--prompt-file`, and
    `--compare`, offline: changed configuration, prompt; confounding changes, none (the change-one-layer rule,
    checked in code); compare flags a run only when pass or fail flips; two scripted batches compare as unchanged,
    since fixtures ignore the prompt; evaluation step 4: the checks establish properties, the prose needs your
    review with the README's five questions; three judges in the lecture, two here (code and you); report one
    difference, its evidence and one limit, and keep your cases: the eval set is the most valuable artifact.
16. **Tear down, recap, and what's next** — `python cli.py --help`; what persists (traces and live memory in
    SQLite; inventory, orders, tickets and pending workflows for one process; tasks and history for one session);
    `exit` in each container shell (started with `--rm`, so nothing is left in `docker ps -a`); the outputs folder
    stays on your laptop, with your prompts and outputs (keys redacted): delete it when you're done; `docker image rm
    agent-harness` frees most of the 1.77 GB (the base image stays); close the terminal that held your key, keep the
    key out of files, commits and shell history, watch your usage, and delete the Colab runtime; the action
    boundary filled in, row by row; the model proposes, the harness decides, and where it matters, so do you; the
    README's five reflection questions; five test-yourself questions; next, lecture 8 (fine-tuning on Google's
    Agent Platform, formerly Vertex AI) and lecture 9 (testing with pytest; these 281 unittest tests are a good
    model).

The tutorial's small mistakes and traps are pointed out kindly, with the fix: the README's export line, typed with
its placeholder, makes every live command stop at its first model call with a 401 (put your own key there, skip the
line offline, or use the README's `read -rsp` lines inside a running container, since `docker exec` doesn't bring a
new key); `docker inspect` shows the key, and an `export` line leaves it in your shell history (prefer `read -rsp`);
the container's banner says "Virtual environment activated." before it activates (harmless); `../secrets`, the GCP
variables and the Gemini and Claude packages are unused here (no service account; the image is 1.77 GB, so be
patient on the first build); the Colab installs the seven pinned packages, not `uv.lock` (use Docker for identical
versions); README.md:278-279 says each Act 2 command also prints the PA/NY counterexample, but `--compare` doesn't
(an individual Act 2 run, or the extra call, does); README.md:301 links `docs/TUTORIAL_SCENARIOS.md`, which was
never published (use the README's checkpoints and the end-of-lecture reflection); Act 2's "Inspect the context
first" comes after the live runs (without a key, start with `--preview-context`); the README's `Removed: Comté` is
shorthand for `Removed: Comté 18 mois (comte) — 350 g` (search for `Removed:`); with fixtures (or `USE_FIXTURES =
True` in the Colab) the blocked shipping lesson ends UNRESOLVED, not BLOCKED (keep fixtures off for that lesson); the
SDK's approval-identity warning after every email review is the one the README predicts, and the outcome is still
right (trust the authoritative block); a live evaluation batch that fails uses up its label (rerun with new labels);
and the README's template commands, `--inspect-run RUN_ID` and `--view-report COLAB_LABEL --db outputs/colab.sqlite`,
fail when typed literally (paste a run ID from `--list-runs`; the second needs a database copied from your Colab run).

## Rebuild

```bash
python -m explainer.build videos/ac215-l07-agent-harness -q l                          # fast draft
python -m explainer.build videos/ac215-l07-agent-harness --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l07-agent-harness --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l07-agent-harness --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l07-agent-harness --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes once, then the
`--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy from the scene renders.

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); this video is made for study with the
instructor's permission. The lecture's slides are redrawn in our own pictures, never shown. Colab, its Secrets
panel, the browser scorecard and the editor are schematic drawings (tagged `illustration`), not screenshots; no real
key was used or shown, and the customer IDs are masked on screen.*
