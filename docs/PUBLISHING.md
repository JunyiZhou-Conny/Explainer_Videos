# Publishing a video without turning Git into a render cache

Use Git for the editable recipe: brief, topic evidence, narration, translations, scene source,
original/redistributable assets, style snapshot, caption sidecars and candid review notes. Use
GitHub Releases for newly produced final MP4s and a SHA-256 manifest. Existing tracked movies
remain available; this policy does not rewrite their history.

GitHub recommends releases for distributing large binary files rather than continually growing
Git history. See [GitHub's documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github#distributing-large-binaries).

## A release procedure

1. Inspect the completed episode and record its actual source revision. Keep a versioned
   `REVIEW.md` identifying decoding/metadata checks, visual sampling, listening and full playback
   separately. Do not equate audio energy with intelligibility.
2. Select final deliverables. Omit scene fragments, TTS caches, failed samples, scratch exports,
   private source inventories and downloaded creator reference footage. Keep personal notes in
   ignored `references-private/` or files ending `.local.md`/`.local.json`.
3. Stage the chosen media under ignored `release-staging/`. Run FFmpeg decoding and ffprobe
   checks; inspect captions and listen. Compute SHA-256 for every uploaded asset. Record gaps
   when a legacy source or review cannot be recovered.
4. Commit the source and small sidecars on a topic branch. Add entries to `catalog/videos.json`
   and `docs/VIDEOS.md` with stable filenames, revision/source status, technical metadata,
   checksum and release URLs. Keep language variants and excerpts labeled.
5. When publishing is part of the user's request, create a GitHub release for that revision,
   upload the staged assets and checksum manifest, and verify returned file sizes/digests.
   Otherwise deliver a reviewable package locally; a render request alone is not a publish request.
6. Confirm the actual public links. Record release availability independently of editorial
   approval. Never merge another agent's open work merely to collect its video.

For a release that is not public yet, `gh release create` supports `--draft`; use `--notes-file`
for exact multiline notes. Attach the final review record to the episode. Do not upload API
keys, environment files, application logins, private chats or local configuration dumps.
Claude Code cloud sessions cannot create releases; they run `.github/workflows/` jobs
(`rehost-media.yml`, or a release step) whose Actions token can.

## The publish manifest and the Mac worker

`tools/release_episode.py` runs after an episode merges: it refuses to release without a
matching `validation.json` (its `script_sha256` must equal the committed `script.json`) and a
human-review line in `REVIEW.md`, then tags `episode/<slug>-vN`, uploads the deliverables plus
`SHA256SUMS.txt`, and emits **`PUBLISH.md` / `PUBLISH.json`** — a mechanical manifest any
executor can follow: asset name + sha256, bilingual title/description/tags/cover, the issue
number to report back to. The fenced JSON in `PUBLISH.md` is ground truth.

`tools/publish_worker.py` is the primary executor. It runs on Conny's Mac (launchd/cron,
~15 min; `--upload` to act, default is a dry run) because that is the one machine holding a
Bilibili login: it polls releases for unpublished `PUBLISH.json` manifests, downloads and
sha256-verifies the MP4, uploads with `biliup` (one-time QR login; `cookies.json` stays in
`~/.config/biliup/`, never in git or CI secrets; renew weekly with `biliup renew`; benchmark
upload lines once and pin `--line`), comments the BV link on the episode issue, flips the
label to `state:published` and closes it. Failures (geetest `-352`, error 601 rate limits)
are commented on the issue and retried next run; a computer-use agent or a human rescues the
rest. Setup, once: `npm i -g @biliup/cli && biliup login && gh auth login`, then schedule
`python3 tools/publish_worker.py --repo JunyiZhou-Conny/Explainer_Videos --upload`.

## Current collection

The initial incubator release collects seven full videos. The catalog links all 23 current
variants across eight episode projects, including the Mandarin and short/split versions already
on the post-PR1 source branch. CareOneX files are the latest bytes from the existing public
PR #2 at its pinned revision, which remains independent. Full making-of and short scene sources
also exist on the post-PR1 branch. The MLOps pilot is unfinished source work. Opening previews,
fragments and unrelated demos are excluded from the finished-video inventory.

This public repository is an incubator, so a technical preview may be shared with its review
limits. Human approval is not invented. Before replacing a release asset, create a new version
or obtain explicit replacement scope so existing links/checksums remain meaningful.

## Repository checks

```bash
.venv/bin/python -m pip install -r setup/requirements-dev.txt
.venv/bin/python -m pytest -q tests
python3 tools/check_incubator.py
python3 tools/setup-runtime --verify-only
```

The offline catalog check validates style hashes, episode snapshots, aliases and release
metadata. It does not download videos or check live publication URLs.
