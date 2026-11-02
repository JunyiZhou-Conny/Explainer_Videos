# Brief · AC215 L15 — ML Workflows with Vertex AI (exam edition)

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md` and
`.claude/skills/ac215-video/SKILL.md` (scene-code pitfalls, never-do list). Facts:
`../ac215-l15-vertex-ml-workflows/SLIDES.md` (the lecture, slide numbers) and
`../ac215-l15-vertex-ml-workflows/digest.md` (the tutorial digest), both read-only, plus the repos
themselves, copied unchanged into `assets/source/<repo>/<path>` at the commits in `video.yaml`.

**This is an exam edition, not a follow-along.** It teaches the mechanisms that Quiz 4 tests about
Lecture 15, each as a real animated diagram, with code and README panels from the demo repos as
evidence. It does not walk the README command by command: no README tracker, no "▶ your turn" tags,
no terminal captures, no `ASSETS.md` capture list. Every code panel quotes `assets/source/` with its
real `path · lines a–b`.

**The repos moved since the digest.** The digest was written at `ml-workflow@972ffbb` and
`model-deployment@3fbf63f`; the clones are now at `ml-workflow@3730009` and `model-deployment@cf0b7c7`.
Where they differ, **the current files in `assets/source/` win**:

| topic | digest | current repo (use this) |
| --- | --- | --- |
| deploy in `model-deployment` | `Model.upload` + `model.deploy` creates a new endpoint each time | `cli.py:183-192` registers a new *version* (`parent_model`), `:197-203` reuses or creates the endpoint `cheese-app-endpoint`, `:210-218` deploys with `traffic_percentage=100` on `n1-standard-2`, `:222-224` undeploys older versions; `--predict` (`:229-256`) and `--cleanup` (`:259-271`) exist |
| saving the serving signature | `tf.saved_model.save(...)` | `cli.py:101-123`: `serving_function` + Keras `ExportArchive` (comment `:117-119` says why) |
| training step in the pipeline | `job.run(..., sync=False)` | `model.py:54-63`: `sync=True`, from the commit titled "Wait for training to finish before deployment" (2026-10-27) |
| README framing | old step list | `ml-workflow/README.md:69-70`: "The pipeline only decides **when** each step starts"; `:218`: "Each step starts only after the previous one succeeds" |

## Audience and goal

An AC215 student **the day before Quiz 4**. They sat Lecture 15 (or skimmed it), know Python, have
seen Docker and the cheese app's collector/processor/trainer from earlier lectures, and may never have
run the tutorial. They want to walk into the quiz able to reason, not recite.

After the video they can answer conceptual multiple-choice questions on this lecture **and say why
each wrong option is wrong**:
- a pipeline is a **DAG**: tasks are nodes, data dependencies are edges; in kfp, `@dsl.component`
  defines a step, `@dsl.pipeline` wires steps, and **calling a component inside the pipeline function
  creates a task** (it records a node; nothing runs until Vertex runs the compiled YAML);
- `task.output` (one output) and `task.outputs["name"]` (several) are **placeholders for a value
  that exists only after the upstream task succeeds**; consuming one creates the edge and hands over
  *this run's* value. A hard-coded string or a guessed path creates **no edge** and may read stale
  data; `.after(task)` gives order **without** data;
- **maximum safe overlap**: tasks with no path between them run in parallel; a join task waits for
  *all* its inputs; the run takes as long as its longest path;
- **enforcing a sequence**: edges from preprocessing's output to training to deployment hold;
  cron offsets, background shell commands (`&`) and "trigger on preprocessing + pick the best model
  from the tracker" all race or deploy the wrong model; and an edge waits for the *task*, not for
  work the task merely launched;
- **deployment in the repos**: upload to the **Model Registry** (a catalogue entry, nothing runs),
  create an **endpoint** (an address), **deploy** (a machine, billed every hour), **predict**; the
  `ml-workflow` chain data collector → data processor → model training → model deploy; AWS
  SageMaker Pipelines is the same DAG idea.

## Length and format

**12–15 minutes**, one part (no `parts:` key). Narration **~2,000 words** (range 1,800–2,300; Kokoro
`af_heart`, speed 0.9, ~150 wpm in this series ≈ 13.3 min of speech); three ponder timers (8 s each)
and the diagrams' silent beats add about a minute. Scene budgets below are targets (±15 %).

Every mechanism scene (S02–S07) ends on a YELLOW **takeaway card**: "If the question says *X* → think
*Y*." S08 collects them as seven rules of thumb. The three PONDER beats are **new** quiz-style
multiple-choice questions (never the practice questions Q11–Q13, never their wording).

## The lecture behind it (SLIDES.md)

Every scene teaching a slide idea carries the GREY `lecture_ref(15, "a–b")` tag (top right). The
diagrams echo the lecture's own pictures: the manual four-CLI workflow (20–21), the Y-shaped toy
pipeline implied by slides 28–29, the four-step Cheese App graph (37), the five-step deployment
diagram (12) and the recipe-to-factory chain (40, with slide 40's mapping: the SDK only *submits*).
Slide conflicts to respect, said kindly in one clause where they matter:
- slide 37 shows TFRecords and a data hand-off; on `main` the edges are `.after()` ordering edges,
  data moves through bucket files by convention, and training downloads its dataset itself
  (`task.py:103-104`), not the processor's output;
- slide 12 saves with `tf.saved_model.save`; the current `model-deployment` uses `ExportArchive`;
- the console now says "Agent Platform" where the lecture says "Vertex AI" (`README.md:212`): say it
  once, keep "Vertex AI" on screen.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop, the `workflow` container that **compiles and submits**, the people at four CLIs (slide 20) | GREY |
| the cloud: Vertex AI Pipelines, the run, the step machines, the bucket, the Model Registry, the endpoint; SageMaker on the AWS side | BLUE |
| step containers and images: `dlops/cheese-app-data-collector`, `…-data-processor`, the `python:3.10` image a Python component runs in | TEAL |
| OS-owned scheduling that knows nothing about data: the cron clock, `&` background jobs | ORANGE |
| what this run produces and owns: a task's output value (9.0, 16.0, 25.0, 5.0), a fresh model, the compiled `pipeline.yaml`; the ✓ badge of a succeeded task (slide 37) | GREEN |
| tools and libraries: `kfp` (`dsl`, `compiler`), `google-cloud-aiplatform` (the SDK), the SageMaker SDK | PURPLE |
| races, stale reads, the wrong model deployed, a failed task, the ✗ beside a wrong option | RED |
| "look here now": the running wavefront in a DAG, the ponder timer, the takeaway cards | YELLOW |
| money: the endpoint's machine and its hourly meter | GOLD |
| **edges and routes**: a data edge from `.output` is PINK **solid** with a value token riding it; an ordering edge from `.after()` is PINK **dashed** with no token; the prediction request's route | PINK |
| last run's leftovers (an old file at a guessed path, the previous model version), future lectures | GREY dashed |

Task-node states are the same everywhere: pending = WHITE outline; running = YELLOW fill;
succeeded = GREEN ✓ badge at the right end (as on slide 37); failed = RED; skipped = GREY dashed.

## Running example

- **Toy pipeline:** the repo's own `sample_pipeline` (`ml-workflow/src/workflow/cli.py:280-301`):
  `square(3)` and `square(4)` in parallel → `add` → `square_root` = 5.0. Real numbers, real YAML.
- **Cheese App:** the four steps of `ml_pipeline` (`cli.py:219-257`), images from Docker Hub
  (`cli.py:27-28`), the bucket files `raw.zip` → `clean.zip` → `model/` (`README.md:70`).
- **Invented examples** (the hook's three jobs, the ponder snippets, the two-training DAG in S04)
  use neutral names (`prep`, `train_a`, `train_b`, `compare`, `deploy`) and the GREY `illustration`
  tag; they are never styled as repo panels (no `path · lines` header) and use `gs://my-bucket/…`.

## Visual set pieces (mechanisms, not cards)

- **V1 · The tracer (S02).** On the left, the `sample_pipeline` body. `@dsl.pipeline` lights PURPLE
  and "calls the function once": the cursor steps line by line, and each component call **drops a
  node** onto the canvas instead of computing — a WHITE outline box with an empty socket labelled
  `.output` (no number yet). The finished graph is pressed by a PURPLE `compiler` roller into a GREEN
  YAML sheet; the GREY laptop's SDK hand passes the sheet across the border to BLUE Vertex AI, where
  TEAL machines appear under each node (slide 40's chain: recipe → printed YAML → operator → engine →
  manager). Only now do numbers appear.
- **V2 · The wire (S03).** Plugging `a_sq_task.output` into `add(x=…)` draws a PINK solid edge from
  the empty socket; the YAML panel beside it grows the matching lines (`dependentTasks: square`,
  `taskOutputParameter … producerTask: square`). Run: `square` turns YELLOW, then GREEN ✓, and only
  then a GREEN token `9.0` leaves the socket and rides the wire. Contrast on the same canvas: a node
  fed a sticky note `"gs://my-bucket/clean.csv"` has **no wire**; at run time it turns YELLOW at t = 0
  alongside the first task and pulls a GREY dashed file from last week — the file stamps RED "stale".
  Then `.after()`: a PINK dashed wire with no token — the node waits, but receives nothing.
- **V3 · The wavefront (S04).** A DAG `prep → {train_a, train_b} → compare` laid out in topological
  layers. A YELLOW wavefront sweeps left to right: a node lights when every incoming wire carries a
  token. Beneath it a Gantt chart grows in real time: `train_a` and `train_b` bars side by side, the
  `compare` bar starting exactly at the *later* of the two ends (a vertical PINK guide drops from it).
  Two variants slide in under the good one: over-serialised (`train_b.after(train_a)`) — the bar
  chain gets longer, same answer; over-parallel (`compare` without its edges) — `compare` starts at
  t = 0 and reads half results, RED. The highlighted longest path is the run's duration.
- **V4 · Four ways to say "then" (S05).** Four horizontal lanes share one clock: cron at fixed
  ORANGE ticks; `prep & train & deploy` (all three bars start together); "trigger training when prep
  starts, deploy picks the best model from the tracker" (a small leaderboard beside the lane where the
  old model is still on top); pipeline edges (each bar snaps to its predecessor's ✓). A die rolls
  `prep`'s duration (40, 75, 55 min); on every roll the first three lanes produce a RED outcome at
  least once (training reads half-written data; deploy ships the old model), while the edge lane only
  stretches. Coda, the launcher bubble: a `train` task that only *submits* a job to another machine and
  returns — the edge snaps to the task's ✓, not the job's end; `sync=True` stretches the task's bar
  to cover the job.
- **V5 · Bucket → registry → endpoint → traffic (S06).** Slide 12's layout in series colours. A GREEN
  model folder in the BLUE bucket; `Model.upload` creates a catalogue card in the Registry (records
  *where the files are* and *which serving container*; a "callable?" ✗ next to it); `Endpoint.create`
  puts up an empty address plate; `model.deploy` slides a machine under the plate and a GOLD hourly
  meter starts. `predict`: a JPEG becomes base64 inside `{"bytes_inputs": {"b64": …}}`, travels the
  PINK route, the serving signature unfolds `decode → float → resize 224×224 → model`, four bars rise,
  the argmax picks a label. `--cleanup`: the machine leaves (meter stops), the plate is removed, the
  card stays.
- **V6 · One graph, two clouds (S07).** The Cheese App chain as slide 37's zig-zag of four nodes
  running on BLUE Vertex, the bucket as a shared blackboard underneath (`raw.zip`, `clean.zip`,
  `model/` appear as each step finishes); every edge PINK **dashed** (`.after()`), because the data
  travels through the bucket by name. Then the same four nodes morph into SageMaker steps
  (`DataCollector`, `DataProcessor`, `ModelTraining`, `CreateModel`, `DeployModel`) and the edges turn
  **solid**: each step's input references the previous step's `properties`. The `steps=[…]` list
  shuffles; the graph does not move.

## Scene plan

Budgets total **~2,000 words**. Slide ranges are SLIDES.md page numbers; code panels quote
`assets/source/<repo>/<path>` with real line numbers, ≤ 12 lines on screen at a time.

**S01 · The 2 a.m. race (~210 words).** Lecture 19–22. No code. Cold open on a broken thing (tag
`illustration`): three nightly jobs on a cron clock — `prep` at 1:00, `train` at 2:00, `deploy` at
3:00. For months it works. One night `prep` takes 75 minutes; `train` starts at 2:00 on a half-written
file, `deploy` ships at 3:00; every job exits 0 and the endpoint serves a model trained on half the
data. "Nothing failed. Nothing was right." The question of the lecture (slides 20–21: four people at
four CLIs, "Can we automate this flow?"): how do you tell a computer *then*, not *at*? Map of the
video: graph → wires → overlap → order → deployment → the Cheese App. Takeaway: *"If an option
schedules steps at fixed times → think race: clocks don't know about data."*

**S02 · A pipeline is a graph (~260).** Lecture 22, 24–30, 34, 40. V1. Vocabulary from slides 22 and
34: workflow management knows which step needs which; the structure is a DAG — directed (data flows
one way), acyclic (no step waits on itself). Kubeflow Pipelines (`kfp`) is the DSL, Vertex AI
Pipelines runs it, no Kubernetes for you (24–25). Panel `ml-workflow/src/workflow/cli.py:280-301`:
three `@dsl.component` functions and `@dsl.pipeline`; the tracer drops four nodes. Panel `:303-304`
(compile) and `:311-318` (`aip.PipelineJob(...)`, `job.run(...)`): your laptop compiles and submits;
Vertex executes. Takeaway: *"If an option says calling `train()` in the pipeline function trains the
model → no: it creates a task, a node; nothing runs until the job runs."*

**S03 · task.output: the wire that makes an edge (~300).** Lecture 28–29, 34. V2. Panel
`cli.py:297-301` beside `ml-workflow/src/workflow/sample-pipeline1.yaml:176-193` (`add`'s
`dependentTasks: [square, square-2]` and its two `taskOutputParameter`s) and `:218-230`
(`square-root` ← `add`). `.output` is a placeholder for a value that exists only after the upstream
task succeeds; passing it is *both* the data and the dependency. `.outputs["name"]` when a component
has several outputs (said, with an invented two-output snippet, tag `illustration`). The no-wire
contrast (hard-coded path → no edge, stale read). `.after()` = order without data. PONDER 1 (8 s).
Takeaway: *"`.output` → waits for success and gets this run's value; hard-coded or guessed path → no
edge, maybe stale; `.after()` → order, no data."*

**S04 · Maximum safe overlap (~250).** Lecture 29, 34, 40. V3. Back to the toy: the two `square`
tasks (`cli.py:298-299`) share no wire, so Vertex runs them at the same time; `add` is a **join** and
waits for both (`sample-pipeline1.yaml:181-183`). Generalise with the invented DAG: two trainings
after one preprocessing run side by side; the comparison waits for the slower. Over-serialising wastes
time; under-connecting races. "Maximum safe overlap" = exactly the edges the data needs, no more, no
fewer; the run's length is its longest path. If an upstream task fails, the join never runs. PONDER 2
(8 s). Takeaway: *"Two steps that don't consume each other's outputs → parallel; a step that consumes
several → waits for all of them."*

**S05 · Enforcing order: edges, not clocks (~300).** Lecture 20–22, 34, 37. V4. The four lanes and
the die. Why each fails: a clock offset guesses a duration; `&` starts everything now; "trigger on
preprocessing + best model from the tracker" deploys whatever is on top of the leaderboard *now* —
yesterday's model. Pipeline edges encode *then*. The repo does exactly this: panel `cli.py:229-257`
(`.after(data_collector_task)`, `.after(data_processor_task)`, `.after(model_training_task)`) and
`ml-workflow/src/workflow/pipeline.yaml:185-186`, `:194-195`, `:208-209` (`dependentTasks`); the
README's own words (`ml-workflow/README.md:218`). PONDER 3 (8 s), then the launcher coda with
`ml-workflow/src/workflow/model.py:52-63` (`sync=True`; the commit "Wait for training to finish before
deployment" made the wait explicit — say "made explicit", not "fixed a race we observed"). Takeaway:
*"cron offsets, `&`, or 'pick the best from the tracker' → race or wrong model; edges preprocess →
train → deploy → correct by construction."*

**S06 · Registry, endpoint, deploy, predict (~260).** Lecture 10–17, 41. V5. The five-step diagram
(12) in one breath; serving signature in one beat (13–14; panel `model-deployment/cli.py:101-114`:
preprocessing travels with the model, so clients send JPEG bytes). Panels
`model-deployment/cli.py:187-192` (`Model.upload`), `:197-203` (reuse or create the endpoint),
`:210-218` (`model.deploy`, `traffic_percentage=100`, one `n1-standard-2` replica), `:249-255` (the
`{"bytes_inputs": {"b64": …}}` request, `endpoint.predict`), `:259-270` (undeploy, delete). The
README's distinction (`model-deployment/README.md:64-66`): the registry is a catalogue and costs
nothing; the endpoint runs a machine and bills every hour (slide 11's alert, slide 41). The pipeline's
deploy step does the same two calls (`ml-workflow/src/workflow/model.py:88-103`). Vertex vs Cloud Run
in one clause (16–17). Takeaway: *"Registered → not callable until deployed to an endpoint; deployed
→ billing until undeployed and deleted."*

**S07 · The Cheese App pipeline, and the same DAG on AWS (~240).** Lecture 34–37, 39–40. V6. The
four steps, two kinds of component: container components running Docker Hub images
(`ml-workflow/src/workflow/cli.py:190-217`; images must be in a registry Vertex can pull from,
`README.md:72-73`) and Python components that call the Vertex SDK (`README.md:75-78`). Why the edges
are `.after()`: "the steps do not call each other… the pipeline only decides **when** each step
starts" (`README.md:69-70`) — deploy finds the model at `gs://…/model` by name (`model.py:84`), so the
edges are what make that name safe; delete one and the step may grab last run's model (connect to
S03). AWS: `ml-workflow-aws/src/workflow/cli.py:262-270` (training's input is
`step_process.properties…`) and `:320-324` (`Pipeline(steps=[…])`): SageMaker Pipelines infers the
same DAG from those references; the list order is not the run order. Takeaway: *"SageMaker Pipelines
→ same DAG idea: referencing a step's properties makes the edge."*

**S08 · Seven rules for the quiz (~180).** Lecture 40–41. The seven rules (below) appear one by one,
each with a 1-second thumbnail of its diagram; the slide-40 chain closes the loop; one line on cleanup
(undeploy, delete the endpoint). Ends on an empty frame.

## Ponder questions (new; 4 options, 8 s timer, then why each wrong option is wrong)

| # | scene | question (on screen, tag `illustration`) | options | answer and why the others fail |
| --- | --- | --- | --- | --- |
| 1 | S03 | `split = split_data()` has two outputs, `train_uri` and `test_uri`. Which call gives `train` the training file **this run** produced, and makes it wait for `split`? | A `train(data_uri="gs://my-bucket/split/train.csv")` · B `train(data_uri=split.outputs["train_uri"])` · C `train(data_uri=TRAIN_URI).after(split)` · D `train(data_uri=split.output)` | **B.** A: no edge — `train` may start at once and read last run's file. C: waits, but the path is a guess, not what `split` handed over. D: `.output` is for a single output; with two you must name one: kfp raises "The task has multiple outputs. Please reference the output by its name." while it builds the graph (kfp 2.14.6 `dsl/pipeline_task.py:259-262`, read, not run). |
| 2 | S04 | `ingest` (2 min) → `clean` (3) → `train_cnn` (10) and `train_tree` (4) → `compare` (1). `report` (2) needs only `clean`. Every task gets its own machine. Shortest possible run? | A 22 min · B 16 min · C 10 min · D 20 min | **B** = 2 + 3 + 10 + 1 (the longest path; `train_tree` and `report` overlap with `train_cnn`). A adds everything in sequence. D serialises the two trainings. C forgets that training needs `clean` and `compare` needs both trainings. |
| 3 | S05 | `deploy` has `.after(train_task)`. The `train` step submits a training job to another machine and returns after 5 seconds, without waiting. When can `deploy` start? | A only when the training job finishes: Vertex tracks every job a step starts · B about 5 s after `train` starts — it may register the previous model · C never: `.after()` fails because no data was passed · D at the same time as the first task: `.after()` is only a hint | **B.** An edge waits for the *task's* success; the pipeline doesn't see the job the task launched (A). `.after()` needs no data (C) and is enforced, as `dependentTasks` in the YAML (D). Fix: the step waits (`sync=True`, `model.py:62`). |

## The seven rules (S08; also the README/exercises answer key later)

1. A pipeline is a DAG: tasks are nodes, data dependencies are edges. Calling a component inside
   `@dsl.pipeline` creates a task; nothing runs until the compiled job runs on Vertex.
2. Consuming `.output` / `.outputs["name"]` creates the edge **and** passes this run's value.
3. A hard-coded or guessed path creates no edge: the step may run early and read stale data.
4. `.after()` orders without data — the Cheese App uses it because its steps share files by name.
5. Maximum safe overlap: no path between two tasks → parallel; a join waits for all its inputs; the
   run lasts its longest path.
6. Order comes from edges, not clocks: cron offsets, `&` and "pick the best from the tracker" race
   or deploy the wrong model — and a step that launches work must wait for it.
7. Deploy = upload to the Model Registry → create an endpoint → deploy (billing starts) → predict;
   undeploy and delete when done. SageMaker Pipelines: the same DAG, edges from step properties.

## Things never to do on screen

- Never quote, paraphrase or answer the practice questions Q11, Q12 or Q13; the ponders above are new.
- No slide images, PDF pages, memes or QR codes; redraw the idea and cite it with `lecture_ref`.
- No Google, Vertex AI, Kubeflow, AWS, SageMaker, Docker or TensorFlow logos; no console screenshots
  and none of the README's `images/*.png` (schematic drawings tagged `illustration` instead).
- No real person's name (commit authors included: say "the course staff"); no credentials, keys,
  project numbers or endpoint ids. Never quote `model-deployment/cli.py:71-83` (a W&B entity). The
  YAML's `ac215-project` / bucket constants may appear only as "values baked in at compile time", and
  placeholders are `gs://my-bucket/…`, `<ENDPOINT_ID>`.
- No terminal output: this edition runs nothing and shows no captures; no invented console output.
- Invented code (ponders, the hook, S04's DAG) is never styled as a repo panel.
- Never claim the old `sync=False` code was observed to race; say the commit made the wait explicit.
- Never present slide 37's TFRecords hand-off as what `main` does.
