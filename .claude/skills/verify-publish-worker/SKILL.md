---
name: verify-publish-worker
description: Exhaustively check tools/publish_worker.py (the Mac job that uploads released episodes to Bilibili) for duplicate uploads and for a worker that stops publishing for good, by running its real main() under every interleaving of overlapping runs, crashes, torn state.json writes and failed uploads. Use before merging any change to tools/publish_worker.py, its state.json handling, its biliup call, or how and how often it is scheduled, and whenever someone asks whether the worker can upload a video twice.
---

# Verify the publish worker

## What is checked, and why

`tools/publish_worker.py` runs on Conny's Mac every ~15 minutes (launchd or cron), and also by
hand: the Studio board shows the command with a 复制 button and says each run uploads one episode.
It lists GitHub releases that carry `PUBLISH.json`, skips tags recorded in
`~/.config/explainer-publish/state.json`, uploads the next MP4 with `biliup`, writes the tag into
`state.json`, then comments on the issue, relabels it and closes it.

Two properties, each stated with the harm it prevents:

- **at-most-once.** Every release tag reaches Bilibili at most once. *Harm:* a duplicate public
  video on the channel. Someone has to delete it by hand, and the registry and the issue then
  point at only one copy.
- **eventually.** If clean runs keep coming, every release tag reaches Bilibili at least once.
  *Harm:* a released episode never goes live, while each scheduled run fails silently on the
  Mac.

## The tool, and why this one

`scripts/explore.py` is a stateless model checker over the **real** code. It imports
`tools/publish_worker.py` and runs `main()` once per worker run, each in its own thread. It
replaces only the `subprocess` calls (a fake GitHub with two releases and a fake Bilibili that
records every video it keeps) and `STATE` (the real file, in a temp dir). Every run pauses at
each step that touches state shared between runs:

| Pause | Code |
| --- | --- |
| read state.json | `load_state()`: `STATE.read_text()` |
| write state.json | `save_state()`: `STATE.write_text()` (may die before the write, or tear it in half) |
| biliup upload | `main()`: `subprocess.run(["biliup", "upload", …])` (ok / fails / kept-but-exit-non-zero) |

The explorer chooses which paused run moves next and how its step ends, then backtracks
depth-first until every choice sequence has been tried. A test samples schedules. This enumerates
all of them within the bounds below. A TLA+ model would describe the same design, but it would
be a hand copy that drifts from the Python. Here, editing `tools/publish_worker.py` changes what
gets checked, with nothing to keep in sync. No off-the-shelf verifier handles Python that
shells out and writes files. The script needs only the standard library and runs in under a
second.

## Run it

```bash
python3 .claude/skills/verify-publish-worker/scripts/explore.py --expect          # all scenarios
python3 .claude/skills/verify-publish-worker/scripts/explore.py overlap crash     # some; prints counterexamples
```

`--expect` exits 0 when every verdict matches the expectation recorded in `SCENARIOS` at the top of
the script. Known findings are recorded as expected violations, so the command stays green until
something changes. Without `--expect` it exits 1 whenever a property is violated. Every violated
property prints its shortest counterexample as numbered steps in the code's terms (`run2 read
state.json`, `run1 biliup upload episode/alpha-v1`, `run2 dies before: write state.json`).

| Scenario | Schedules | at-most-once | eventually |
| --- | --- | --- | --- |
| `baseline`: one run at a time, ≤1 failed upload, no crashes | 3 | holds | holds |
| `overlap`: a scheduled run and a hand run overlap | 20 | **violated** | holds |
| `crash`: one run at a time, one run dies at any pause or tears a write | 9 | **violated** | **violated** |
| `ambiguous`: biliup exits non-zero although Bilibili kept the video | 5 | **violated** | holds |

## Findings at the sync commit (report these; do not "fix" the model)

1. **Overlapping runs upload the same episode twice.** Run 1 reads `state.json` and starts
   uploading `episode/alpha-v1`. Run 2 (Conny pressing 复制 and running it while the scheduled run
   is still uploading, or a cron run that outlasts 15 minutes) reads `state.json` before run 1
   writes it, sees alpha unpublished, and uploads it again. Nothing in the worker stops two runs at
   once. launchd does not start a second instance of the same job, but cron does, and a hand run
   always can. The `overlap` scenario confirms that a non-blocking `fcntl.flock` taken before
   `load_state()` makes this property hold.
2. **A crash after the upload and before `save_state` re-uploads.** If the process dies after
   biliup returns (or while biliup is finishing a long upload Bilibili already accepted) and
   before `state.json` records the tag, the next run uploads it again.
3. **A failed upload Bilibili kept is retried as new.** The worker treats every non-zero biliup
   exit as "not uploaded" and retries next run. If biliup can fail after Bilibili accepted the
   video (a timeout on the final response), the retry duplicates it. Whether biliup does this is
   an assumption about biliup. The `ambiguous` scenario is the only place it is assumed.
4. **A torn `state.json` stops all publishing.** `save_state` writes in place
   (`Path.write_text`). A death mid-write leaves invalid JSON. `load_state` catches only
   `FileNotFoundError`, so every later run stops with `JSONDecodeError` before uploading
   anything, until someone repairs the file by hand.

## Bounds and assumptions (a pass covers only this)

- Two release tags, the default `--limit 1`, and the command the Studio shows
  (`--repo o/r --upload`). There are at most 3 scenario runs, at most 2 of them alive at once
  (`overlap`), then 3 clean runs one after another.
- At most one crash or torn write per schedule, and at most one failed upload per schedule.
- Code between two pauses runs atomically. This is sound because it touches only the run's own
  temp dir, the fakes, and issue comments, labels and the registry, which no run reads back.
  A new worker runs up to its first pause before anything else moves. Today that covers only
  argument parsing.
- GitHub never fails, release assets always match their sha256, and the registry PUT always
  succeeds. The sha-mismatch branch, `record_on_github` races, the issue comments, labels and
  closing, `--line`, covers and `biliup renew` are outside both properties.
- Each tag is a separate video. A re-release (`episode/<slug>-v2`) uploads again by design.

## Coverage and sync

| File | Functions | Covered how |
| --- | --- | --- |
| `tools/publish_worker.py` | `load_state`, `save_state`, `main` | run for real, with pauses at the steps in the table above |
| `tools/publish_worker.py` | `record_on_github`, `sh`, `gh_json`, `sha256`, `parse_publish_md` | run for real against the fakes; their outcomes are not checked |
| `tools/bilibili_registry.py` | `record`, `dumps` | run for real; not checked |

**Sync commit:** `e627b1ff0a0db7ff4cd5772c9457599b11ba305b` (`tools/publish_worker.py` last changed
in `9e2c5025f1383400d0c3919763e44a18abf42aad`). To see whether the covered code changed since:

```bash
git log --oneline e627b1ff0a0db7ff4cd5772c9457599b11ba305b..HEAD -- tools/publish_worker.py tools/bilibili_registry.py
```

Move the sync commit forward only after you have read the diff, confirmed that the pause table,
the fakes and the bounds still describe the code at the new commit, and run `--expect`.

## Reading a result

- **`<--` on a property that held** (e.g. `baseline` at-most-once now VIOLATED): the change broke
  the worker. Read the counterexample. It is a real bug unless the bullets below explain it.
  Do not edit `SCENARIOS` to make it pass.
- **`<--` on a known finding that now holds**: a fix landed. Check that the fix is intended and
  does not just skip uploads: `eventually` must still hold in that scenario. Then flip the
  expectation in `SCENARIOS`, update the findings and the table above, and move the sync commit.
- **`AssertionError: unexpected run […]` or `unexpected check_output`**: a modeling gap. The worker
  now calls a command the fake world does not know. Teach `FakeSubprocess` the command, and if
  the command touches state another run reads, give it a pause.
- **`IndexError` inside `choose()`, or a hang**: replay is no longer deterministic. Some shared step
  now runs between pauses (a new file, a lock, a thread), or a blocking call waits on another
  run. Add a pause at that step. Model a lock as a pause before `fcntl.flock`, and model a
  blocking lock as non-blocking-or-wait. Never let a thread block outside `pause()`.

## Updating the verification when a change is intended

- A new step that reads or writes shared state (a second state file, a lock, a remote "already
  uploaded?" lookup) gets a pause, so the explorer can interleave around it.
- A new failure mode the change handles (e.g. checking Bilibili for an existing title before
  uploading) gets an outcome in `Scheduler.outcomes()`, and usually a scenario.
- Keep `baseline` as the scenario that must always hold. It is what catches ordinary regressions.

## Proved before hand-off

At the sync commit the checks catch both scratch breaks in the real file, and both verdicts return
to the recorded expectations once the break is reverted:

- Deleting `if tag in state["published"]: continue` turns `baseline` at-most-once into VIOLATED
  (alpha uploaded 6 times).
- Recording a failed upload under `published` instead of `failed` turns `baseline` eventually into
  VIOLATED (beta never uploaded).
