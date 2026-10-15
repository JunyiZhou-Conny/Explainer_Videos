# Bootstrap: the canonical context for any agent, any model

Every agent that works on an episode — Claude, GPT/Astra, Cursor, whichever model, whichever
surface — starts from this file, so that every session holds the same map. If you were pointed
here, read the items below **in this order** before writing anything. Nothing else from any
prior session is assumed; everything that matters is in these files or on the episode's
issue/PR thread.

## Required reading, in order

1. **`AGENTS.md`** (repo root) — the rules: episode lifecycle, content gates, the handoff
   protocol between agents, what never goes into git.
2. **`skill-library/conny-explainer-video/SKILL.md`** — how production actually works:
   presets, narration/caption/music specs, render commands, validation.
3. **`docs/PLAYBOOK.md`** — the operating knowledge from past productions: what slowed
   earlier episodes down, the exact commands, the review rhythm.
4. **The reference episode `videos/git-branch-pointer/`** — a complete, released episode made
   through the current pipeline. Copy its file structure (`BRIEF.md`, `SOURCES.md`,
   `REVIEW.md`, `script.json`, `episode.json`, `scenes.py`, `delivery/`) and its use of the
   shared style components. When unsure what "done" looks like, diff yourself against it.
5. **The episode's own issue thread** — claims, handoff notes (DONE / NEXT / WARN), and
   Conny's answers live there. If you are resuming someone else's work, the latest handoff
   note is your starting point, not this list alone.

## The kickoff prompt (for Conny: paste this to any agent)

> Read `docs/BOOTSTRAP.md` in JunyiZhou-Conny/Explainer_Videos and follow its reading order.
> Then claim issue #<N> with a comment (model + surface + branch), and produce the episode on
> branch `episode/<slug>`, touching only `videos/<slug>/`. Post a 20–30 s narrated sample on
> the draft PR and stop for my review before the full render. Before your session ends for
> any reason, push the branch and leave a DONE / NEXT / WARN handoff comment on the issue.

This one paragraph plus this repository **is** the full context. If an agent needs more than
this to proceed, that gap is a bug: say so on the issue so the missing knowledge gets written
into the skill or the playbook, not retold in chat.

## What you may not assume

- That you are the only agent on the repo (claim before working; see AGENTS.md handoffs).
- That your session will live to finish the episode (hand off early, push often).
- That chat history exists. Anything agreed only in a chat is not agreed; put decisions in
  the brief or on the issue.
- That a style is "whatever looks right". Styles are contracts: tokens + shared components +
  pixel checks (`docs/STYLES.md`); use the components, don't restyle by hand.
- That evidence can be approximate. On-screen code, bytes and numbers are real and pinned in
  the episode's `SOURCES.md`, or they don't appear on screen.
