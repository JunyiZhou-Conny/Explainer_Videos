# AC215 · Lecture 15 — ML Workflows with Vertex AI (exam edition) — narration script & visual plan (v2)

Audience: an AC215 student the day before Quiz 4. They sat Lecture 15 (or skimmed it), know Python, have seen Docker
and the cheese app's collector, processor and trainer in earlier lectures, and may never have run the `ml-workflow` or
`model-deployment` tutorials. They watch on a laptop with no clone open, to prepare for conceptual multiple-choice
questions, not to type along.

Goal (BRIEF.md "Audience and goal"): after the video they can answer conceptual questions on this lecture **and say
why each wrong option is wrong**: (1) a pipeline is a DAG — tasks are nodes, data dependencies are edges; in kfp,
`@dsl.component` defines a step, `@dsl.pipeline` wires steps, and calling a component inside the pipeline function
creates a task (a node; nothing runs until Vertex runs the compiled YAML); (2) `task.output` / `task.outputs["name"]`
is a placeholder for a value that exists only after the upstream task succeeds — consuming it creates the edge and
hands over this run's value; a hard-coded or guessed path creates no edge and may read stale data; `.after()` orders
without data; (3) maximum safe overlap — no path between two tasks → parallel; a join waits for all its inputs; the run
lasts its longest path; (4) enforcing a sequence with edges preprocess → train → deploy, never cron offsets, `&` or
"trigger on preprocessing + pick the best model from the tracker"; an edge waits for the *task*, not for work the task
launched; (5) deployment: Model Registry (a catalogue entry) → endpoint (an address) → deploy (a machine, billed hourly)
→ predict; the Cheese App chain collector → processor → training → deploy; SageMaker Pipelines as the same DAG idea.

Sources of truth: `BRIEF.md` (design, binding); the lecture digest `../ac215-l15-vertex-ml-workflows/SLIDES.md`
(slide numbers = PDF pages of the 42-slide deck); the tutorial digest `../ac215-l15-vertex-ml-workflows/digest.md`
(written at `ml-workflow@972ffbb`, `model-deployment@3fbf63f`); the study guide
`MLOps_Learning/guides/L15-vertex-ml-workflows.md`; `assets/source/<repo>/<path>`, the current files at the commits in
`video.yaml` (`ml-workflow@3730009`, `model-deployment@cf0b7c7`, `ml-workflow-aws@f165c6e`). Where the digest and the
current repo differ, **the current files win** (BRIEF.md's table: versioned upload, reused endpoint,
`traffic_percentage=100`, `ExportArchive`, `sync=True`). Where the slides and the repo differ, the panel shows the repo
and the SAY says what each shows, in one clause (S06: `tf.saved_model.save` vs `ExportArchive`; S07: slide 37's
TFRecords hand-off vs `main`, where training downloads its own dataset; S02: "Agent Platform" in today's console).

Conventions
- **Exam edition.** No README tracker, no `▶ your turn`, no terminal captures, no typed commands, no `recorded` or
  `expected` output boxes, **no live runs**: this lecture's video runs nothing. Every mechanism is an animated diagram
  (V1–V6, BRIEF.md "Visual set pieces"); code and README panels are evidence beside it. Every mechanism scene (S02–S07)
  ends with a YELLOW **takeaway card** "If the question says X → think Y" (one visual group, centred lower third),
  spoken as the scene's last SAY, then an empty frame. S08 collects the seven rules.
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at most about 55
  words; ponder answers and the recap may run a little longer) and become the subtitles. Plain spoken English: no
  backticks, no symbols, no markdown. Identifiers are on screen and said in words: `.output` → "dot output",
  `.outputs["name"]` → "dot outputs, with the output's name", `.after()` → "dot after", `@dsl.component` → "d s l dot
  component", `@dsl.pipeline` → "d s l dot pipeline", `kfp` → "K F P", `dependentTasks` → "dependent tasks",
  `square-2` → "square 2", `sync=True` → "sync set to true", `bytes_inputs` → "bytes inputs", `raw.zip` → "raw zip",
  `clean.zip` → "clean zip", `model/` → "the model folder", `cheese-app-endpoint` → "cheese app endpoint",
  `aip.PipelineJob` → "a pipeline job", `Model.upload` → "upload", `model.deploy` → "deploy", `&` → "a background
  ampersand". Numbers as digits; a number that matters gets its own short sentence ("Training at 2. Deploy at 3.").
  No decimals spoken (the toy's 9.0, 16.0, 25.0, 5.0 are said "9", "16", "25", "5"; on screen they stay decimals, as
  the YAML types them). Times as "1 in the morning", never "a.m.". No "!" after a digit.
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences` splits only there;
  the split drives the TTS gaps, the subtitle cues and the one-to-one Chinese alignment). No sentence opens with a
  lower-case identifier or file name. No `'s` after a digit or on a word with a lexicon entry. No abbreviations with
  inner dots ("e.g.", "vs.") in SAY. American spelling on screen and in the SAY ("gray", "catalog"; the colour
  constants stay GREY).
- **Names.** The instructor's full name never appears, spoken or on screen (the deck's title page is never redrawn;
  slide 42's captions are never quoted). The SAY says "the lecture" or "the slides". Commit authors are "the course
  staff". The quoted ranges contain no person's name (checked: `ml-workflow/src/workflow/cli.py:190-318`,
  `model.py:52-103`, `sample-pipeline1.yaml:176-232`, `pipeline.yaml:180-209`, `README.md:69-78`, `:212`, `:218`;
  `model-deployment/cli.py:101-123`, `:179-271`, `README.md:64-66`; `ml-workflow-aws/src/workflow/cli.py:212-222`,
  `:262-270`, `:320-324`). `model-deployment/cli.py:71-83` (a W&B entity) is never quoted. No credentials, keys, project
  numbers or endpoint ids: placeholders are `gs://my-bucket/…` and `<ENDPOINT_ID>`. The constants the compiler bakes
  into `pipeline.yaml` (`pipeline.yaml:200`, the bucket name) appear only inside that panel, with a GRAY chip "value
  baked in at compile time".
- `SHOW:` lines describe what is on screen during that SAY, and what moves. ≤ 3 visual groups at once; something moves
  every ~4 s except during ponder timers.
- `Lecture: a–b.` under a scene header lists the slides the scene stands on. `LECTURE a–b` in a SHOW line: from that
  SAY block on, the GRAY `lecture_ref(15, "a–b")` tag sits top right ("Lecture 15 · slides a–b"; "slide" for one)
  until a SHOW changes it. S01 explains the tag once. The slides are never shown: every lecture picture is our own
  redrawing in the series colours with the slide's structure and terms (the four people at four CLIs of 20–21, the
  Y-shaped toy graph of 28–29, the zig-zag of 37 with ✓ badges, the five-step layout of 12, the assembly line of 40);
  no slide image, QR code, meme ("DELETE!!" on 41 is not drawn), logo or console screenshot, and none of the README's
  `images/*.png`.
- `CODE(repo/path: a–b)`: `code_panel(...)` quoting `assets/source/repo/path` from line a to b with the real line
  numbers, header `path · lines a–b` (the repo name kept as the first path segment, since three repos share file
  names: `ml-workflow/src/workflow/cli.py · lines 280–301`). At most 12 rows on screen; a longer range is shown in
  windows of ≤ 12 lines that Transform into each other, or *folded* (only the listed lines, a GRAY `…` row between
  gaps, header suffix `(folded)`). Lines longer than 65 characters wrap (continuation rows indented, a GRAY ↪). Lit
  lines: a YELLOW bar behind the named line(s) unless the SHOW names another colour. An *excerpt chip* quotes an exact
  sub-string of one line, headed `path · line N (excerpt)`.
- `PANEL(repo/README.md: a–b)`: a README text panel (same frame as a code panel, markdown shown as plain text, `**`
  and backticks stripped, link targets dropped, line numbers kept), header `repo/README.md · lines a–b`.
- **Invented code** (S01's three cron jobs, S03's sticky note and two-output snippet, S04's DAG, the three ponder
  snippets) is drawn on a GRAY-outlined card with the tag `illustration`, never with a `path · lines` header, never in
  the repo-panel frame. Buckets in invented code are `gs://my-bucket/…`; task names are neutral (`prep`, `train_a`,
  `train_b`, `compare`, `deploy`, `split`, `ingest`, `clean`).
- `PONDER(8 s, Pn)`: the multiple-choice ponder (`mcq_ponder`). The SHOW before it gives the card: a YELLOW-outlined
  card in the lower two thirds with the question, four option rows A–D (letter in a circle) and an 8-second YELLOW
  timer bar that drains; tag `illustration`. The SAY that introduces it ends "Pause here if you want." Nothing on
  screen during the timer shows the answer. The next SAY block reveals: the right row fills YELLOW with a ✓; under each
  wrong option a one-line RED reason writes in (text given in the SHOW) as the SAY reaches it; then the card fades.
  Three in the video: P1 (S03), P2 (S04), P3 (S05), all new (BRIEF.md "Ponder questions"); the practice questions Q11,
  Q12 and Q13 are never quoted, paraphrased or answered.
- `TAKEAWAY: "…"`: the scene's YELLOW takeaway card, written in as its SAY speaks it; in S08 it returns as one of the
  seven rule rows.
- Tags (GRAY unless stated): `illustration` on every schematic and invented card (the cron clock, the four lanes, the
  leaderboard, the die, the registry card, the endpoint plate, the request envelope, the bucket blackboard); `kfp
  2.14.6 · read, not run` (PURPLE chip) next to the quoted kfp error message in P1's reveal; `README example` on the
  four probability values from `model-deployment/README.md:211`; `slide 37` / `main today` chips on the S07 conflict.
- Semantic colours (BRIEF.md "Colours"; series table applied):

  | meaning | colour |
  | --- | --- |
  | your laptop, the `workflow` container that **compiles and submits**, the people at four CLIs (slide 20) | GREY |
  | the cloud: Vertex AI Pipelines, the run, the step machines, the bucket, the Model Registry, the endpoint; SageMaker on the AWS side | BLUE |
  | step containers and images: `dlops/cheese-app-data-collector`, `…-data-processor`, the `python:3.10` image a Python component runs in | TEAL |
  | OS-owned scheduling that knows nothing about data: the cron clock, `&` background jobs | ORANGE |
  | what this run produces and owns: a task's output value (9.0, 16.0, 25.0, 5.0), a fresh model, the compiled YAML; the ✓ badge of a succeeded task | GREEN |
  | tools and libraries: `kfp` (`dsl`, `compiler`), `google-cloud-aiplatform` (the SDK), the SageMaker SDK | PURPLE |
  | races, stale reads, the wrong model deployed, a failed task, the reason line under a wrong option | RED |
  | "look here now": the running wavefront, a running task's fill, the ponder card and timer, the takeaway cards | YELLOW |
  | money: the endpoint's machine and its hourly meter | GOLD |
  | edges and routes: a data edge from `.output` is PINK **solid** with a value token riding it; an ordering edge from `.after()` is PINK **dashed** with no token; the prediction request's route | PINK |
  | last run's leftovers (an old file at a guessed path, the previous model version), the longest-path halo's off-path nodes dimmed | GREY dashed |

  Task-node states, the same in every scene: pending = WHITE outline; running = YELLOW fill; succeeded = GREEN ✓ badge
  at the right end (slide 37); failed = RED; never-run = GREY dashed.
- Visual set pieces V1–V6 (BRIEF.md) live in `scenes/common.py`: `TaskNode` (outline, socket, the four states),
  `Wire` (solid data edge with a token / dashed ordering edge), `Tracer` (V1), `WirePlug` (V2), `Wavefront` + `Gantt`
  (V3), `FourLanes` + `Die` (V4), `RegistryEndpoint` (V5), `TwoClouds` (V6), plus `mcq_ponder(...)`,
  `takeaway(...)`, `illustration_card(...)` and `lecture_ref`.
- Running example: the repo's `sample_pipeline` (`ml-workflow/src/workflow/cli.py:280-301`): `square(3)` and
  `square(4)` in parallel → `add` → `square_root` = 5.0; tasks named in the YAML `square`, `square-2`, `add`,
  `square-root`. The Cheese App: `ml_pipeline` (`cli.py:219-257`), images `dlops/cheese-app-data-collector` and
  `dlops/cheese-app-data-processor` (`cli.py:27-28`), bucket files `raw.zip` → `clean.zip` → `model/`
  (`ml-workflow/README.md:70`).

Notes for scene authors
- The committed `sample-pipeline1.yaml` was compiled by an older kfp (`python:3.7` image at line 164, `kfp-2.3.0` at
  line 248): never quote those lines; the quoted DAG lines (176–232) are what any kfp 2 compile writes for this
  function. The committed `pipeline.yaml` matches `cli.py` on `main`.
- `model.py:5-7` and `:67-69` say "Define a Container Component" above lightweight *Python* components (a stale
  comment); fold those comment lines out (`model.py:4` and `:66` are never shown) so the panel does not contradict the
  SAY.
- `model.py:88-103` (the pipeline's deploy step) still uses `traffic_split={"0": 100}` on `n1-standard-4` and makes a
  new endpoint each run; `model-deployment/cli.py:179-224` is the newer, versioned flow. S06 explains with
  `model-deployment`; the pipeline's step is shown only as "the same two calls" (upload, deploy).
- `model.py:53` is the old comment `# sync=True, # If you want to wait for the job to finish`; line 62 is the live
  `sync=True,`. Light 62, never 53. Never claim that the earlier `sync=False` was observed to race; the commit "Wait
  for training to finish before deployment" (27f286e, 2026-10-27, by the course staff) switched `sync=False` to
  `sync=True` and *made the wait explicit*. What it buys (digest §6 item 10): with `sync=True` the step also fails when
  the training job fails, so the edge never lets deploy run after a failed training.
- The training step does not consume `clean.zip`: `task.py:103-104` downloads `cheese_4_labels.zip` from a GitHub
  release. Its saved model lands at `gs://<bucket>/model` (`task.py:376`), the same name `model.py:84` deploys.
- V3 timings (illustration): `prep` 2, `train_a` 6, `train_b` 4, `compare` 1 (units of minutes on the Gantt axis);
  good run 9; over-serialised (`train_b.after(train_a)`) 13; over-parallel: `compare` at 0, RED. P2 numbers: ingest 2,
  clean 3, train_cnn 10, train_tree 4, compare 1, report 2; longest path 16; all in sequence 22; trainings serialised
  20; the longest single task 10.
- V4 (illustration): one clock 0:00–4:00 (1 in the morning to 5); cron lane `prep` 1:00, `train` 2:00, `deploy`
  3:00; train takes 50 min, deploy 10 min. Die rolls 40, 75, 55 min. Cron lane: 40 ✓, 75 RED (train reads a
  half-written file), 55 ✓ (tight). `&` lane: all three bars start at 0 on every roll, RED each time. Tracker lane:
  an event starts `train` when `prep` writes its output, and it fires on the first file prep writes (RED
  "half-written" flash on the 75 roll); `deploy` takes the top row of a leaderboard whose top row is an older run
  (`model · run 12 · acc 0.91`, GREY dashed) while today's model, once trained, lands *below* it (`model · today · acc
  0.88`): RED on every roll ("not this run"). Edge lane: bars snap to each ✓, the lane just stretches (GREEN every
  roll).
- V5 probability bars: the four values of `model-deployment/README.md:211` (0.0591, 0.1099, 0.6348, 0.1962), tag
  `README example`, labels "class 0–3" (the README does not say which cheese index 2 is: never name it).
- Lexicon (block `# AC215 L15-exam` in `explainer/lexicon.yaml`, added at the merge step): DAG, DAGs ("dag"),
  acyclic, Acyclic, Kubeflow, and the option-letter phrases "A hard-codes", "A adds", "so A is wrong" (Kokoro reads a
  bare "A" as the article). Checked by phonemes and needing no entry: YAML, SageMaker, cron, JPEG, "base 64", "Docker
  Hub", "TF records", "square 2", "d s l", "K F P", Keras, Kubernetes, SDK, undeploy, ampersands. Keep "writes down"
  (not "records") after YAML. "A hard-coded or guessed path" is an article and must stay unmatched.
- Buildability (review_exam S22): write `TaskNode`, `Wire`, `Gantt`, `Die`, a clock face, a leaderboard (L08
  `table_card`), `mcq_ponder` (card + four option rows + draining bar) and `takeaway` once in `scenes/common.py`. The
  laptop has no "SDK hand": draw a PURPLE arrow labelled `aiplatform` from `laptop()` across the border, carrying the
  YAML sheet. The compiler roller is a rounded PURPLE bar sweeping over the graph while the graph Transforms into
  `file_glyph("sample-pipeline1.yaml")`, under 1.5 s. Takeaway cards at 20–24 pt, at most 3 lines: break at each `·`.
- i18n `en_display` candidates (spoken → literal): dot output → `.output`; dot outputs → `.outputs["name"]`; dot after
  → `.after()`; d s l dot component → `@dsl.component`; d s l dot pipeline → `@dsl.pipeline`; K F P → kfp; dependent
  tasks → `dependentTasks`; square 2 → `square-2`; sync set to true → `sync=True`; bytes inputs → `bytes_inputs`; raw
  zip → `raw.zip`; clean zip → `clean.zip`; cheese app endpoint → `cheese-app-endpoint`; base 64 → base64.
- Word budget (BRIEF.md, ±15 %): S01 210 · S02 260 · S03 300 · S04 250 · S05 300 · S06 260 · S07 240 · S08 180 =
  2,000 (allowed 1,800–2,300). v2 target ≤ 1,950 (review_exam M3: the series' measured Kokoro rate is 141.4 wpm,
  `videos/ac215-l08-llm-finetuning/REVIEW.md:108`, so 2,139 words ran past 15 min); if the narrated sample measures
  ≥ 150 wpm, ~2,050 is acceptable. Actual counts: see the table at the end of this file.

---

## S01 · The 2 a.m. race — `s01_race.py` · `Race`

Lecture: 19–22.

SHOW: Cold open, no lecture tag. Tag `illustration`. An ORANGE clock face writes in at the left; to its right three
WHITE-outlined job boxes on a horizontal timeline 0:00–4:00 labelled `prep · 1:00`, `train · 2:00`, `deploy · 3:00`,
each hanging from an ORANGE tick. The clock hand sweeps; on each tick the box fills YELLOW, then gets a GREEN ✓. A
GRAY counter in the corner flips "night 1 … night 90".
SAY: Three nightly jobs on a clock. Prepare the data at 1 in the morning. Train at 2. Deploy at 3. For months, it works.

SHOW: The counter stops at "night 91". The `prep` bar grows past the 2:00 tick (to 2:15); at 2:00 `train` fills
YELLOW anyway and an arrow from it reaches into a file glyph under `prep` that is only half filled (hatched GREY
half), the arrow turns RED. At 3:00 `deploy` fills and ships a small model glyph labelled "trained on half the data".
SAY: Then one night, preparation takes 75 minutes. At 2, training starts anyway, on a file that is only half written. At 3, deployment ships whatever training produced.

SHOW: Three GREEN "exit 0" chips pop over the three boxes; to the right, a BLUE endpoint plate now holds the half-data
model, outlined RED. Two lines write in, centred: "Nothing failed." (GREEN) "Nothing was right." (RED).
SAY: Every job exits with status zero. Nothing failed. And the endpoint now serves a model trained on half the data. Nothing was right either.

SHOW: LECTURE 20–21. The timeline shrinks away. Our redrawing of slides 20–21: four tiles in a row, "1 Data
Collector", "2 Data Processor", "3 Model Training", "4 Model Deploy", each above a GREY person-at-a-terminal glyph
labelled "CLI"; a dashed BLUE "Google Cloud" box below. The headline writes "How do we execute these steps?", then
transforms into "Can we automate this flow?"; a hollow arrow points to a BLUE chip "Vertex AI Pipelines".
SAY: The lecture opens on the same problem: four steps of the cheese app, each run by a person at a terminal. How do we execute these steps? Can we automate this flow?

SHOW: LECTURE 22. The tiles fade. Two phrases write in large: an ORANGE "at 2:00" crossed out, a PINK "when prep ✓"
beside it; under it, a PINK arrow from a GREEN ✓ to the next box.
SAY: To automate it, you need a different instruction. Not: train at 2. Instead: train when preparation has finished. That is what a pipeline is for.

SHOW: The words shrink to the top. The map of the video builds left to right as the SAY names each item, six small
icons with labels: "graph" (three nodes), "wires" (a PINK solid edge with a token), "overlap" (two parallel bars),
"order" (four lanes), "deployment" (a GOLD meter), "the Cheese App" (a zig-zag of four nodes).
SAY: Here is the plan: graphs, wires, overlap, order, deployment, and the cheese app.

SHOW: A GRAY specimen tag "Lecture 15 · slides 20–21" pulses once top right; a GRAY chip "no live runs · concepts, not
clicks".
SAY: The gray tag, top right, names the slides behind each idea. Nothing here is a live run.

SHOW: The map and chips fade. TAKEAWAY: "fixed times (cron offsets) → think race: clocks don't know about data".
Then everything fades to an empty frame.
SAY: If an option schedules steps at fixed times, think race: a clock knows nothing about data.

---

## S02 · A pipeline is a graph — `s02_graph.py` · `TasksAndEdges`

Lecture: 22, 24–30, 32–34, 40.

SHOW: LECTURE 22, 34. Three WHITE task nodes and two PINK edges draw in; labels write in as named: "task = node",
"data dependency = edge". Then a chip "DAG = directed acyclic graph"; "directed" lights an arrowhead (one way,
producer → consumer); "acyclic": a dotted edge tries to loop back to the first node and is struck out RED.
SAY: Workflow management, in the lecture's words, knows which step needs which. The structure that records this is a directed acyclic graph, or DAG.

SHOW: The labels stay; the nodes rename themselves "task", "task", "task"; the edges pulse.
SAY: Directed, because data flows one way, from producer to consumer. Acyclic, because no step ever waits on itself. Tasks are the nodes; data dependencies are the edges.

SHOW: LECTURE 24–25. The small graph slides left. Right: a PURPLE chip "Kubeflow Pipelines · kfp" (the DSL), an arrow
to a BLUE box "Vertex AI Pipelines" (runs it), and a GRAY struck-out chip "your own Kubernetes cluster". A small GRAY
excerpt chip `ml-workflow/README.md · line 212 (excerpt)`: "Agent Platform > Pipelines".
SAY: Vertex AI Pipelines runs these graphs for you. You describe the graph with Kubeflow Pipelines, the K F P library, and there is no Kubernetes to manage. Today's console calls it Agent Platform.

SHOW: LECTURE 28–29. Everything fades. CODE(ml-workflow/src/workflow/cli.py: 280–301) in two windows: lines 280–293
(the three `@dsl.component` functions, the decorators lit PURPLE) Transform into lines 295–301 (the pipeline).
SAY: Here is the toy pipeline from the slides and the demo repo. Three Python functions marked d s l dot component: square, add and square root. A fourth, marked d s l dot pipeline, wires them together.

SHOW: V1, the tracer. The panel (lines 295–301) moves left; a canvas on the right. `@dsl.pipeline` lights PURPLE and a
cursor steps to line 298 (`square(x=a)`; `a: float = 3.0` on line 297 glows GRAY: "pipeline input · default 3.0"):
instead of a number, a WHITE node `square` drops onto the canvas with an empty GREEN-outlined socket labelled `.output`.
A GRAY chip "no number yet".
SAY: When the pipeline function runs, the component calls compute nothing. Calling square on a, the pipeline's input, which defaults to 3, creates a task: a node in the graph, with an empty output socket. No number yet.

SHOW: The cursor steps through 299, 300, 301; nodes `square-2`, `add`, `square-root` drop in a Y shape, sockets empty.
As the second square node drops, a PURPLE stamp "component: square" sits above both square nodes and the second node's
label writes `square-2`. The connections from 300–301 are drawn thin GRAY dotted, the first labelled "?" (S03 turns them
into wires). A GRAY chip "the function ran once → a graph".
SAY: Line by line, four calls drop four nodes. Square is called twice, so one component gives two tasks; the second is named square 2. The function ran once, and produced only a graph.

SHOW: LECTURE 29–30, 32–33, 40. The panel Transforms to CODE(ml-workflow/src/workflow/cli.py: 303–318) folded to 303–304,
…, 311–318. A PURPLE `compiler` roller presses the graph into a GREEN sheet "sample-pipeline1.yaml"; a PURPLE arrow
labelled "aiplatform" from the GREY laptop carries the sheet across a border into a BLUE "Vertex AI" region as lines
311–318 light (`aip.PipelineJob(`, `job.run(`). Then the code panel fades, and only then slide 40's chain writes along
the bottom: "recipe (DSL) → printed YAML → operator (SDK) → engine (Kubeflow) → manager (Vertex AI Pipelines)" (at
most three groups: graph and sheet, laptop and Vertex, chain).
SAY: The compiler presses that graph into a YAML file. The Vertex AI SDK, the lecture's remote control, submits it as a pipeline job. Your laptop compiles and submits. Vertex executes.

SHOW: Inside the BLUE region the graph re-forms; a TEAL machine slides under each node; the two `square` nodes fill
YELLOW, then GREEN ✓, and GREEN 9.0 and 16.0 appear in their sockets; then 25.0, then 5.0.
SAY: Only now, on Google's machines, does each task get a container, and do numbers appear.

SHOW: The canvas fades. TAKEAWAY: "calling train() inside the pipeline function → creates a task (a node), trains
nothing · nothing runs until the compiled job runs on Vertex". Then an empty frame.
SAY: If an option says calling train in the pipeline function trains the model, think again: it only creates a task. Nothing runs until the compiled job runs.

---

## S03 · task.output: the wire that makes an edge — `s03_output.py` · `OutputWire`

Lecture: 28–29, 34.

SHOW: LECTURE 28–29. CODE(ml-workflow/src/workflow/cli.py: 297–301), line 300 lit; the two `.output` sub-strings
light GREEN. Beside it the V1 graph from S02 (four nodes, empty sockets, thin GRAY dotted connections, no wires yet).
SAY: Look at the add call. For x, it passes the first square task, dot output. For y, the second task, dot output. So what is being passed?

SHOW: V2, the wire. The GRAY dotted connection from `square`'s empty socket to `add`'s `x` input turns into a PINK solid
wire, then the one from `square-2` to `y`. The socket stays empty; a GRAY chip "placeholder: exists after `square` succeeds".
SAY: Not a number. Dot output is a placeholder for a value that exists only after the upstream task succeeds. Plugging it in draws a wire.

SHOW: A second panel slides in at the right: CODE(ml-workflow/src/workflow/sample-pipeline1.yaml: 176–193) in two
windows: 176–187 (181–183 `dependentTasks: - square - square-2` lit PINK, 187 lit GREEN), Transforming into 186–193
(187–189 and 191–193, `taskOutputParameter … producerTask: square` / `square-2`, lit GREEN). Then a window folded to
218, …, 223–230 (10 rows; `square-root` ← `add`: 223–224 and 228–230 lit) as the third wire draws.
SAY: The compiled YAML writes down each wire twice: add's dependent tasks list square and square 2, and each input names its producer task.

SHOW: The YAML panel shrinks to the right edge. Run: `square` fills YELLOW, then GREEN ✓; only then a GREEN token
"9.0" leaves its socket and rides the PINK wire into `add`. `square-2` does the same with "16.0". `add` lights only when
both tokens have arrived.
SAY: At run time, square turns green, and only then does 9 ride the wire into add. One argument gave add both its data and its dependency.

SHOW: Tag `illustration`. A small invented card: a node `split` with two labelled sockets `train_uri` and `test_uri`;
`split.outputs["train_uri"]` writes under it and a PINK wire leaves only the `train_uri` socket.
SAY: With several outputs, you name the one you want: dot outputs, with the output's name in brackets.

SHOW: The toy graph moves up and dims. Below it, tag `illustration`, two rows side by side. Left: `prep → train` with a
PINK solid wire; when `prep` gets its ✓, a GREEN token `gs://my-bucket/runs/0427/clean.csv` (this run's path) leaves its
socket and rides into `train`. Right: the same two nodes, no wire, `train` holding a GRAY sticky note
`"gs://my-bucket/clean.csv"`; at t = 0 `prep` and `train` both fill YELLOW together.
SAY: Now the contrast. Often the output is itself a path: the file this run wrote. With the wire, train gets that exact path, after prep succeeds. Hard-code a path instead, and there is no wire: train starts right away, alongside prep.

SHOW: Right row: `train` pulls a GREY dashed file "clean.csv · last week" from a BLUE bucket; the file stamps RED
"stale". After `train` has read it, `prep` finishes and its fresh GREEN `clean.csv` lands at the same path, overwriting
it, one beat too late. `train` still gets a GREEN ✓, outlined RED.
SAY: The file there is last week's, and the step succeeds on stale data. A guessed path looks like a dependency to you, not to the pipeline.

SHOW: A PINK **dashed** wire draws from `prep` to `train` with the label `train(...).after(prep)`; at run time `train`
waits for `prep`'s ✓, but no token rides the dashed wire.
SAY: For order without data, dot after adds a dashed edge: the task waits for the other one to succeed, but nothing travels down it.

SHOW: The canvas clears. PONDER P1 card (tag `illustration`). Question: "`split = split_data()` has two outputs,
`train_uri` and `test_uri`. `TRAIN_URI = "gs://my-bucket/split/train.csv"`. Which call gives `train` the file **this
run** produced, and makes it wait for `split`?"
A · `train(data_uri="gs://my-bucket/split/train.csv")` · B · `train(data_uri=split.outputs["train_uri"])` · C ·
`train(data_uri=TRAIN_URI).after(split)` · D · `train(data_uri=split.output)`.
SAY: Try one. Pause here if you want.
PONDER(8 s, P1)

SHOW: Reveal. B fills YELLOW ✓, GREEN note "named output → this run's file + the edge". RED reason under A: "no edge →
may start at once, reads last run's file".
SAY: B. Naming the output hands over this run's file, and creates the wait. A hard-codes a path: no edge, so train may start at once and read last run's file.

SHOW: RED reason under C: "waits, but reads a path you assumed: if split writes anywhere else, it's stale or missing".
Under D: "two outputs →
must name one"; an excerpt card beside it: "The task has multiple outputs. Please reference the output by its name."
with the PURPLE chip `kfp 2.14.6 · read, not run`. The card fades.
SAY: C waits, but it reads a path you assumed, not the one split reported. D fails before anything runs: with two outputs, K F P refuses plain dot output.

SHOW: TAKEAWAY: "`.output` → waits for success, gets this run's value · hard-coded or guessed path → no edge, maybe
stale · `.after()` → order, no data". Then an empty frame.
SAY: If the question says dot output, think: waits for success, and gets this run's value. A hard-coded or guessed path: no edge, maybe stale. Dot after: order, but no data.

---

## S04 · Maximum safe overlap — `s04_overlap.py` · `SafeOverlap`

Lecture: 29, 34, 40.

SHOW: LECTURE 29. The toy graph again (Y shape), beside CODE(ml-workflow/src/workflow/cli.py: 297–301) with 298–299
lit. The two `square` nodes have no wire between them; both fill YELLOW at the same instant.
SAY: Back to the toy graph. No path of wires connects the two square tasks, so Vertex is free to run them at the same time.

SHOW: The panel Transforms to the excerpt CODE(ml-workflow/src/workflow/sample-pipeline1.yaml: 181–183), lit PINK.
`square` finishes first (GREEN ✓, token waits at `add`'s input); `add` stays WHITE until `square-2` finishes; a GRAY
label "join".
SAY: Add is a join. Its YAML lists both squares as dependent tasks, so it starts only when the second one finishes.

SHOW: LECTURE 34, 40. The toy fades. V3, tag `illustration`: a DAG `prep → {train_a, train_b} → compare` in three
topological columns, PINK solid wires.
SAY: The same shape, one size up: one preprocessing task, two trainings that read its output, and a comparison that reads both models.

SHOW: The YELLOW wavefront sweeps left to right; a node lights when every incoming wire carries a token. Beneath, a
Gantt chart grows in real time: `prep` 0–2, `train_a` 2–8 and `train_b` 2–6 side by side, `compare` 8–9; a vertical
PINK guide drops from `train_a`'s end to `compare`'s start.
SAY: A task lights up when every incoming wire carries a token. Both trainings start together, and the comparison starts exactly when the slower one ends.

SHOW: A second Gantt row slides in under the first, labelled `train_b.after(train_a)`: an extra PINK dashed wire on a
mini-DAG; bars chain `prep`, `train_a`, `train_b`, `compare`, ending at 13; a GRAY chip "same answer, slower".
SAY: Add an edge the data does not need: same answer, longer run.

SHOW: A third row: `compare` fed two GRAY sticky-note paths instead of its wires; its bar starts at 0, reads two
half-drawn model glyphs, turns RED; chip "guessed paths → no edges → race".
SAY: Replace those wires with guessed paths, and the comparison starts at time zero and reads half-finished results. That is a race.

SHOW: The two variant rows fade. On the good DAG the path `prep → train_a → compare` gets a YELLOW halo; `train_b`
dims; the Gantt's total "9" lights. Then `train_a` turns RED and `compare` turns GREY dashed ("never runs").
SAY: Maximum safe overlap means exactly the edges the data needs, no more and no fewer. The run then lasts its longest path. If an upstream task fails, the join never runs.

SHOW: The canvas clears. PONDER P2 card (tag `illustration`), with a small DAG drawing beside the text: `ingest` (2
min) → `clean` (3) → `train_cnn` (10) and `train_tree` (4) → `compare` (1); `report` (2) after `clean` only. Question:
"Every task gets its own machine. What is the shortest possible run?" A · 22 min · B · 16 min · C · 10 min · D · 20 min.
SAY: Your turn to compute one. Pause here if you want.
PONDER(8 s, P2)

SHOW: Reveal. B fills YELLOW ✓; on the DAG the path ingest → clean → train_cnn → compare gets the YELLOW halo and the
sum "2 + 3 + 10 + 1 = 16" writes under it; `train_tree` and `report` slide under `train_cnn`'s bar.
SAY: B, 16 minutes. The longest path is ingest, clean, the big training, and compare. 2, plus 3, plus 10, plus 1. The small training and the report overlap with the big one.

SHOW: RED reasons: A "adds every task in sequence"; D "runs the two trainings one after the other"; C "ignores the
edges: training needs clean, compare needs both". The card fades.
SAY: A adds every task in sequence. D runs the two trainings one after the other. C ignores the edges: training needs clean data, and compare waits for both models.

SHOW: TAKEAWAY: "no path of wires between two steps → parallel · a step that consumes several outputs → waits for all
of them". Then an empty frame.
SAY: If there is no path of wires between two steps, think parallel. If a step consumes several outputs, it waits for all of them.

---

## S05 · Enforcing order: edges, not clocks — `s05_order.py` · `EdgesNotClocks`

Lecture: 20–22, 34, 37.

SHOW: LECTURE 20–22. V4, tag `illustration`: four horizontal lanes share one clock axis (1:00 to 5:00), each with
three bars `prep`, `train`, `deploy`. The lane labels write in as the next SAY names them.
SAY: Now the sequence: preprocess, train, deploy. Here are four ways to make each step wait, on one clock.

SHOW: Lane labels: ORANGE "cron · 1:00 / 2:00 / 3:00" (bars hang from ORANGE ticks); ORANGE "`prep & train & deploy`"
(all three bars start at the left edge); "event: prep wrote its output → start train · deploy: take the best model in
the tracker" (a small BLUE leaderboard beside it with two rows: `model · run 12 · acc 0.91` on top, GREY dashed, an
older run; once today's training ends, `model · today · acc 0.88` appears *below* it); PINK "pipeline edges" (each bar
snapped to a ✓).
SAY: Lane one, cron offsets. Lane two, background ampersands. Lane three, an event starts training when preprocessing writes its output, and deploy takes the best model in the tracker. Lane four, pipeline edges.

SHOW: A die rolls (tag `illustration`) and lands on "40 min": every `prep` bar resizes to 40 minutes; the other bars
react by their lane's rule. Then "75 min", then "55 min".
SAY: Roll the length of preprocessing. 40 minutes. Then 75. Then 55.

SHOW: Replay of the 75 roll, slower: in the cron lane `train` starts at 2:00 under a still-running `prep`, a RED
"half-written file" flash; in the `&` lane all three bars start together, RED on every roll (three small RED marks
stacked beside the lane).
SAY: The clock lane is fine at 40, and broken at 75: training reads a half-written file. The background lane is broken on every roll, because nothing waits.

SHOW: The tracker lane: on the 75 roll the event fires on the first file prep writes (a RED "half-written" flash);
`deploy` reaches into the leaderboard and picks the top row `run 12` (RED outline "not this run") on every roll, even
when today's training finished first and landed in row 2. The edge lane: GREEN on every roll, its bars only slide
right; a chip "it just stretches".
SAY: The tracker lane fails twice. The event can fire on the first file, before preprocessing is done. And the tracker's best model is the best of all runs, not this run's. Only the edge lane is right on every roll. It just stretches.

SHOW: LECTURE 34, 37. The lanes shrink to the top. CODE(ml-workflow/src/workflow/cli.py: 229–257) folded to 231–233, …,
247–248, …, 255–256 (9 rows: each step's `set_display_name` and `.after`); lines 233, 248, 256 (`.after(...)`) lit
PINK; beside it the four-node chain draws with PINK dashed wires as each line lights.
SAY: The cheese app pipeline does exactly this: processing after collection, training after processing, deployment after training, each with dot after.

SHOW: Beside the chain: CODE(ml-workflow/src/workflow/pipeline.yaml: 180–209) folded to 185–188, …, 194–195, …, 208–209
(10 rows; 188 shows "name: Data Processor"); the three `dependentTasks` pairs lit PINK, the two lower pairs labelled by
PINK node names drawn beside them, "Model Deploy ← Model Training" and "Model Training ← Data Processor". Under it PANEL(ml-workflow/README.md: 218) with "Each step
starts only after the previous one succeeds." lit YELLOW.
SAY: In the compiled YAML they become dependent tasks. And the README says it plainly: each step starts only after the previous one succeeds.

SHOW: Panels clear. One beat before the card: a `train` node with a small BLUE "job" bubble leaving it for a separate
machine (no timing shown, no ✓ yet), label "a step can launch work elsewhere". Then PONDER P3 card (tag
`illustration`). Question: "`deploy` has `.after(train_task)`. The `train` step
submits a training job to another machine and returns after 5 seconds, without waiting. When can `deploy` start?"
A · "only when the training job finishes: Vertex tracks every job a step starts" · B · "about 5 s after `train`
starts — it may deploy the previous model" · C · "never: `.after()` fails because no data was passed" · D · "at the
same time as the first task: `.after()` is only a hint".
SAY: One more, a subtle one. Some steps only launch work on another machine. Remember exactly what an edge waits for. Pause here if you want.
PONDER(8 s, P3)

SHOW: Reveal. B fills YELLOW ✓. V4 coda, the launcher bubble: a `train` task bar that is 5 s long, from which a BLUE
"training job" bar on another machine continues for an hour; `train`'s GREEN ✓ appears at 5 s and the PINK dashed edge
snaps to it; `deploy` starts and picks a GREY dashed "previous model". RED reason under A: "the edge waits for the
task, not for the job it launched".
SAY: B. An edge waits for the task, and this task succeeded after 5 seconds. The pipeline never sees the job it launched, so A is wrong, and deploy may ship the previous model.

SHOW: RED reasons under C: "`.after()` needs no data"; under D: "enforced: it is `dependentTasks` in the YAML". The
card fades.
SAY: C: dot after needs no data. D: dot after is enforced, written into the YAML as a dependent task.

SHOW: CODE(ml-workflow/src/workflow/model.py: 52–63) folded to 52, 54–56, 61–63 (line 62 `sync=True,` lit GREEN; line
53 never shown). The launcher bubble stretches: `train`'s bar now covers the whole BLUE job, and its ✓ moves to the
job's end; a RED "job failed" variant flashes once and the step's badge turns RED with it, so `deploy` stays GREY
dashed. A GRAY chip "commit: Wait for training to finish before deployment · sync False → True".
SAY: The repo's training step is such a launcher. With sync set to true, it waits for its job, and fails if the job fails, so deploy never runs on a failed training. A recent commit made that wait explicit.

SHOW: Everything fades. TAKEAWAY: "cron offsets, `&`, or 'pick the best from the tracker' → race or wrong model ·
edges preprocess → train → deploy → correct by construction". Then an empty frame.
SAY: If an option uses cron offsets, background commands, or the best model from the tracker, think race or wrong model. Edges from preprocess to train to deploy are correct by construction.

---

## S06 · Registry, endpoint, deploy, predict — `s06_deploy.py` · `RegistryToEndpoint`

Lecture: 10–17, 41.

SHOW: LECTURE 12. V5: our redrawing of slide 12 in series colours: a GREY "Model Deployment CLI container" at the
bottom left; a dashed BLUE "GCP" box at the right holding a bucket and a "Vertex AI" panel with two framed boxes "Model
Registry" and "Endpoints". Five PINK numbered labels write in as the SAY names them: 1 get the saved model, 2 update
its signature, 3 upload to the bucket, 4 register, 5 deploy.
SAY: The lecture draws deployment in five steps: get the saved model, update its signature, upload it to a bucket, register it, and deploy it to an endpoint.

SHOW: LECTURE 13–14. CODE(model-deployment/cli.py: 101–114) folded to 101–105, …, 109–114 (12 rows); lines 102–104 light one by one as a JPEG glyph unfolds
"decode → float → resize 224×224", then line 114 "→ model". GRAY chip "the slides: `tf.saved_model.save` · the repo
today: `ExportArchive` (lines 117–123)".
SAY: The signature step moves preprocessing into the model: decode the JPEG, convert to floats, resize to 224 by 224, then call the model. The slides save it one way, the repo with the Keras export archive.

SHOW: LECTURE 12. Back to V5. A GREEN model folder sits in the BLUE bucket. CODE(model-deployment/cli.py: 187–192)
lights; a catalog card slides into "Model Registry": "where the files are" (a PINK pointer to the folder), "which
container serves it"; beside it "callable?" with a RED ✗. Excerpt chip from PANEL(model-deployment/README.md: 65).
SAY: Registering creates a catalog card. It records where the files are, and which container serves them. Nothing is running, and it costs nothing. Can you call it? Not yet.

SHOW: CODE(model-deployment/cli.py: 197–203) lights 198–202; an empty BLUE address plate `cheese-app-endpoint` rises
over "Endpoints"; a GRAY chip "exists? reuse : create".
SAY: Next, the endpoint: an address. The repo reuses cheese app endpoint if it exists, or creates it.

SHOW: CODE(model-deployment/cli.py: 210–218), 213–215 lit; a BLUE machine slides under the plate carrying the
model; a "100 %" traffic arrow; a GOLD meter starts ticking "per hour". Excerpt chip PANEL(model-deployment/README.md:
66).
SAY: Deploy slides a machine under that address and sends it all the traffic. From now on, you pay for that machine while it is deployed, even when nobody calls it.

SHOW: CODE(model-deployment/cli.py: 249–255), line 251 lit. A JPEG becomes a base64 string inside an envelope
`{"bytes_inputs": {"b64": …}}` that travels the PINK route to the plate; inside, the signature unfolds; four bars
rise (tag `README example`, values from `model-deployment/README.md:211`), the tallest lights YELLOW "argmax".
SAY: To predict, the client wraps each JPEG in base 64, under the key bytes inputs. The signature unfolds it, the model returns four scores, and the largest names the cheese.

SHOW: CODE(model-deployment/cli.py: 259–270), 269–270 lit. The machine slides out; the GOLD meter stops; the plate is
removed; the registry card and the bucket folder stay.
SAY: Cleanup undeploys the model, so the machine stops, then deletes the endpoint. The registry card and the bucket files stay.

SHOW: LECTURE 16–17. V5 shrinks left. Excerpt CODE(ml-workflow/src/workflow/model.py: 88–103) folded to 88–92, …,
95–97, with a chip "the pipeline's deploy step: the same two calls"; 90–92 ("upload") then 95–97 ("deploy") light in
turn as "the same two calls" is said.
Below it a one-line card (our drawing), written one half at a time: "Vertex AI · serve the trained model" | "Cloud Run ·
the model is one part of a bigger app".
SAY: The pipeline's deploy step makes the same two calls. And by the slides' rule of thumb, Cloud Run fits when the model is one part of a bigger app.

SHOW: LECTURE 41 (tag only; nothing of the slide is drawn). Everything fades. TAKEAWAY: "registered → not callable
until deployed to an endpoint · deployed → a machine billing until you undeploy (then delete the endpoint)". Then an
empty frame.
SAY: If the question says registered, think: not callable until it is deployed to an endpoint. If it says deployed, think: a machine is billing until you undeploy it. Then delete the endpoint too.

---

## S07 · The Cheese App pipeline, and the same DAG on AWS — `s07_cheese.py` · `CheesePipeline`

Lecture: 34–37, 39–40.

SHOW: LECTURE 37. V6: our redrawing of slide 37's zig-zag: four WHITE nodes "Data Collector", "Data Processor",
"Model Training", "Model Deploy" on BLUE Vertex; as each runs it fills YELLOW, then gets its GREEN ✓ at the right end.
SAY: Now the whole cheese app pipeline: collector, processor, training, deploy. Each gets a green check as it succeeds.

SHOW: LECTURE 34. CODE(ml-workflow/src/workflow/cli.py: 190–203) folded to 190–195, …, 202–203 (9 rows; the collector's
`@dsl.container_component`, line 193 `image=DATA_COLLECTOR_IMAGE` lit) with the excerpt chip `cli.py · line 27
(excerpt)`: `"dlops/cheese-app-data-collector"`; the two top nodes turn TEAL "image from Docker Hub". The two lower nodes
get a PURPLE "Python + Vertex AI SDK" chip (PANEL(ml-workflow/README.md: 73, 76, 78)). A GRAY chip "slide 34: Artifact
Registry · repo: Docker Hub · any registry Vertex can reach".
SAY: Two kinds of steps. The collector and processor are container components that pull published images from a registry, Docker Hub in this repo, the Artifact Registry on the slides, because Google's machines cannot see your laptop. Training and deploy are Python components that call the Vertex AI SDK.

SHOW: A BLUE bucket "blackboard" spreads under the chain; `raw.zip`, `clean.zip`, `model/` chalk in as each step
finishes. Every edge turns PINK **dashed**. PANEL(ml-workflow/README.md: 70), "The pipeline only decides when each
step starts." lit YELLOW.
SAY: So why dot after, and not dot output? The steps never call each other. Each reads from the bucket and writes back: raw zip, clean zip, then the model folder. The pipeline only decides when each step starts.

SHOW: Excerpt chip `ml-workflow/src/workflow/model.py · line 84 (excerpt)`: `ARTIFACT_URI = f"gs://{bucket_name}/model"`.
The deploy node reaches into `model/` by name. Then the edge training → deploy is cut: deploy starts early and grabs a
GREY dashed "model/ · last run", stamped RED.
SAY: So deploy finds the model by name, in the model folder, and the edges make that name safe. Delete one, and deploy may grab last run's model: the stale read from earlier.

SHOW: The GRAY "slide 37" chip writes in with a small TEAL arrow processor → training labelled "TF records"; as the
GREEN "main today · training downloads its own dataset" chip writes in, that arrow is struck GRAY and a BLUE arrow from
a "release download" glyph into training replaces it; excerpt chip
`ml-workflow/src/model-training/package/trainer/task.py · lines 103–104`.
SAY: One difference from the slides: on the main branch today, training downloads its own dataset, so these edges carry order, not data.

SHOW: AWS. The four nodes morph into five BLUE SageMaker steps `DataCollector`, `DataProcessor`, `ModelTraining`,
`CreateModel`, `DeployModel`. CODE(ml-workflow-aws/src/workflow/cli.py: 262–270), lines 266–267
(`step_process.properties…`) lit PINK; the edge processor → training turns **solid** PINK with a token; the other
edges follow (lines 219–220, 277, 309 as excerpt chips).
SAY: On AWS, SageMaker Pipelines runs the same idea. The training step's input points at the processing step's output property, and that reference is the edge.

SHOW: CODE(ml-workflow-aws/src/workflow/cli.py: 320–324), line 322 `steps=[…]` lit. The list's five chips shuffle into a
different order; the graph above does not move.
SAY: Shuffle the pipeline's list of steps, and the graph does not move: order comes from the references.

SHOW: Everything fades. TAKEAWAY: "SageMaker Pipelines → the same DAG idea: referencing a step's properties makes the
edge". Then an empty frame.
SAY: If the question says SageMaker Pipelines, think: the same DAG. Referencing a step's properties makes the edge.

---

## S08 · Seven rules for the quiz — `s08_recap.py` · `Recap`

Lecture: 40–41.

SHOW: Seven empty rule rows, one line each at ≥ 20 pt, each with a small thumbnail (~0.6 units tall) of its diagram at
the left that plays its 1-second loop once as its row writes in, then holds still. Row 1 (V1's tracer) writes in:
"pipeline = DAG · a call creates a task".
SAY: Seven rules. One: pipelines are DAGs. Calling a component creates a task, a node. Nothing runs until the compiled job runs.

SHOW: Rows 2 (V2's token) and 3 (the stale sticky note) write in: "`.output` → edge + this run's value"; "guessed path
→ no edge, maybe stale".
SAY: Two: dot output, or a named output, makes the edge and passes this run's value. Three: a guessed path makes no edge, and may be stale.

SHOW: Rows 4 (a dashed wire) and 5 (V3's Gantt): "`.after()` → order, no data"; "no path → parallel · join waits for
all".
SAY: Four: dot after orders without data. Five: no path between tasks means parallel, a join waits for all its inputs, and the run lasts its longest path.

SHOW: Row 6 (V4's lanes): "edges, not clocks · launcher must wait".
SAY: Six: order comes from edges, not clocks, and a step that launches work must wait for it.

SHOW: Row 7 (V5's plate and meter): "registry → endpoint → deploy ($) → predict". All seven rows glow YELLOW once.
SAY: Seven: upload to the Model Registry, create an endpoint, deploy, then predict. Billing starts at deploy. SageMaker builds the same DAG from step properties.

SHOW: LECTURE 40. The list shrinks left. Right: slide 40's chain as an assembly line: "recipe (DSL)" → "printed YAML
(compiler)" → "operator (SDK)" → "engine (Kubeflow)" → "manager (Vertex AI Pipelines)", TEAL worker glyphs under the
last box.
SAY: And the lecture's chain: a recipe in the D S L, printed as YAML, submitted by the SDK, run on the Kubeflow engine, and managed by Vertex AI Pipelines, with no Kubernetes to set up.

SHOW: LECTURE 41 (tag only). A GOLD meter beside the endpoint plate stops as two GRAY chips write "undeploy", "delete
the endpoint". Everything fades except a small GRAY line "AC215 · Lecture 15 · exam edition", then an empty frame.
SAY: When you are done, undeploy and delete the endpoint. Good luck on the quiz.

---

## Word budget (v2, `python -m explainer.script`)

| scene | budget (±15 %) | v1 | v2 |
| --- | --- | --- | --- |
| S01 | 210 | 219 | 178 |
| S02 | 260 | 279 | 262 |
| S03 | 300 | 331 | 305 |
| S04 | 250 | 273 | 252 |
| S05 | 300 | 314 | 321 |
| S06 | 260 | 284 | 251 |
| S07 | 240 | 247 | 217 |
| S08 | 180 | 192 | 164 |
| total | 2,000 (1,800–2,300; v2 target ≤ 1,950) | 2,139 | 1,950 |
