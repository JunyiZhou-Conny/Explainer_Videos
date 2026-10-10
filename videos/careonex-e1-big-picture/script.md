# CareOneX E1 · The big picture — script draft (v0, not rendered)

**Draft.** Written before Marco's branch was pushed; S05 now has his branch (read the same evening).
S06 (where we are) waits for E7. Format as in E2: no narrator, SAY = subtitles.

Audience: the five teammates. Goal: after E1, anyone can draw the system from memory, say which
branch holds which layer, and say how far the build is from the Milestone 1 plan.

Sources: Milestone 1 Statement of Work (`feat/prompt-tuning:Milestone1_Statement_of_Work.docx.pdf`),
`data-retrieval@d96a4ad`, `feat/sonic_with_rag@eff4a96`, `feat/prompt-tuning@92a2bf0`, `main@e26d20e`.

---

## S01 · The gap — `s01_gap.py` · `TheGap`

SHOW: A family member (WHITE) fills the careonex.com form at 9 pm: "Mom needs help at home". The
form goes into a queue; a clock runs; a coordinator icon is busy / asleep; the queue grows.
SAY: A family fills out a form on careonex.com: a parent suddenly needs help at home. What has to happen next is a phone call. Today that call waits for a person to be free, so evening requests wait until morning, and some families are never called.

SHOW: The SOW's problem statement, condensed into one card.
SAY: CareOneX Voice is the team's answer: an AI agent that calls back within minutes, at any hour, explains how home care is paid for, and takes down what the family needs.

## S02 · What a good call means — `s02_targets.py` · `Targets`

SHOW: A call timeline with three kinds of turns: ANSWER (YELLOW question → GREEN passage → reply),
INTAKE (one question at a time → a form filling up), HAND-OFF (distress → a person).
SAY: On a call, the agent does three things. It answers questions about paying for care, from official documents only. It takes the intake, one question at a time. And when someone is confused or upset, it hands the call to a person.

SHOW: The Milestone 1 targets as a table that builds row by row: turn latency p95 < 1.0 s ·
grounded claims ≥ 95 %, medical or legal advice 0 · intake field accuracy ≥ 90 % · word error rate
on older and accented voices < 15 % · calls without consent 0.
SAY: The team wrote down what "good" means before building anything. Answers within a second. Every claim traceable to a document, and no medical or legal advice. At least 90 percent of intake fields right. And nobody called without consent.

## S03 · Two halves — `s03_map.py` · `TwoHalves`

SHOW: The system map, as in E2, built half by half.
SAY: The system has two halves. The first runs before any call: five containers turn 20 public documents into a searchable library of 232 passages. The second runs during a call.

SHOW: A call animates through the bottom half: caller speaks → voice → Nova 2 Sonic → toolUse
lookup_program_info → retrieve → Knowledge Base → passages back → spoken reply.
SAY: The caller's voice streams to Amazon's Nova 2 Sonic, a model that hears and speaks directly. When it needs a fact, it asks our voice container to run a tool. The tool asks the retrieve container, which searches the library and returns passages. Nova reads them and answers.

## S04 · Why containers — `s04_containers.py` · `Containers`

SHOW: Seven boxes, each with one job; the only contracts between them highlighted: S3 prefixes
(raw/, text/, chunks/, config/) and one HTTP call (POST /retrieve).
SAY: Each container does one job and can be rebuilt on its own. They only meet in two places: folders in one S3 bucket, and one HTTP call, POST retrieve. Change anything else inside a container, and nobody else has to know.

SHOW: `docker compose` file → `make run` / `just run`; `make serve`; `make smoke`.
SAY: One file, docker compose, wires them together. One command runs the whole library pipeline, one starts the retrieve service, and one runs a test call without a microphone.

## S05 · Who built what — `s05_branches.py` · `Branches`

SHOW: A branch timeline (colours by person): `main` (Sep 17–29: Junyi's Nova Sonic foundation,
Nadir's team AWS setup) → `data-retrieval` (Nadir, Oct 3–10: all six services, 42 commits) →
`feat/sonic_with_rag` (Caroline, Oct 8: grounding rules, tool round-trip checks, speakable
passages) · `feat/prompt-tuning` (Junyi, Sep 28–Oct 2: intake schema with a confidence per field,
consent model, hard rules) · `feat/sonic_with_rag_updated` (Marco, Oct 10: ONE commit on `main`,
213 files; the pipeline and voice app copied in from a ZIP of `feat/sonic_with_rag`, plus his search
experiments, E6) · Helen (no commits of hers on GitHub yet).
SAY: Nadir built the library pipeline on one branch. Caroline joined it to the voice app on another. Junyi worked on the intake rules on a third. Marco's branch is different: one big commit on top of main that copies everything in and adds his experiments. So git cannot show what he changed, and merging the branches into one main line is the team's next real job.

SHOW: Divergences, side by side: `data-retrieval` switched from make to just, `sonic_with_rag` still
uses make; `prompt-tuning` grounds the model with "program cards" pasted into the prompt, but the
module it imports (`nova_sonic.knowledge`) and the cards were never committed, so that grounding
block is silently empty; the other branches ground through retrieval instead.
SAY: (to be written: two ideas of grounding coexist; the branches have drifted)

## S06 · Where we are — `s06_status.py` · `Status`

SHOW: Milestones M1–M5 on a timeline with today (Oct 10) marked; M2 deliverables ticked or not;
"SOW: GCP (Cloud Run, Vertex AI)" vs. "built: AWS (Bedrock, S3 Vectors)".
SAY: (to be written with E7's findings)

## S07 · How to watch this series — `s07_series.py` · `Series`

SHOW: The episode list over the map: each episode lights its layer.
SAY: (to be written)
