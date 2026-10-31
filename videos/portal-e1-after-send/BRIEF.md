# Brief: Isn't it just an API call? (项目周记 E1)

Series: [docs/PORTAL_SERIES.md](../../docs/PORTAL_SERIES.md) · batch plan:
[videos/portal-series/README.md](../portal-series/README.md) · week digest:
[2026-w44](../portal-series/weeks/2026-w44.md).

- **Question.** Conny, 2026-10-30: "everything is wrapped around the openai api … However it is
  distinctly different from the most pristine version of an api because there are thinking parts
  … and there are also parts specifically written for parents … I am not sure how that is
  accomplished and what else can we do with this particular feature?"
- **Learning objective.** The viewer can name the four jobs our server does between "send" and the
  answer (build the request, hand the model a form, check every line, lay the form out), and can
  say exactly why the parent summary exists (a required box on the form) and where each row of the
  receipt comes from (sources is the model's word alone).
- **Audience.** Conny: knows that apps call the OpenAI API and that prompts exist; reads Python, not
  TypeScript; has seen the screens but not the server. First episode of the series, so every term is
  new: harness, instructions / system prompt, token, prompt caching, structured outputs, lint,
  fallback; reasoning model and effort are named briefly (E2 goes deep).
- **Style / format.** `swiss`, saved production defaults (English narration Kokoro `af_heart` 0.95,
  burned Chinese-above-English captions, composed score). Measured: 1,487 words, 538 s of speech;
  `duration_seconds` 584 (9:44), the slack spent on ponder pauses (scene helper `pause`).
- **Evidence rule.** Screens are redrawn with strings copied from Conny's screenshots (2026-10-30)
  or from the source files. Numbers come from the code, the decision records, the PR descriptions
  and the week digest; each is listed in [SOURCES.md](SOURCES.md). The user's greeting bubble is
  not in the screenshots and is tagged `illustration`; so are the dose and diagnosis examples in s05.
- **Must include.** The real hello exchange and receipt; the request as a stack with the cached
  prefix; the 13-box form with the parent-summary box; the checker, the one rewrite, the fallback,
  "an emergency is never taken back"; the receipt rows mapped to their origins; the 21:21 turn of PR #36.
- **Skip.** Streaming and what "thinking" is (E2); the UI copied from Claude (E3); the review bots and
  the agents' night (E4); the evaluation arms beyond one sentence; any TypeScript.
- **Ponder questions.** s03: why does code, not the model, state the time and whether the clinic is
  open? s05: the model was told not to diagnose; why check again? s06: which receipt row is
  unchecked?
- **Structure.** s01 hook (three answers to one word) → s02 more than a call: a harness, four jobs → s03 the
  request (instructions = system prompt, prefix caching, ponder) → s04 the form (structured outputs, parent summary) → s05 the checker
  (rewrite, fallback, ponder) → s06 the page and the receipt (thinking is real: reasoning
  model, effort, the page's stopwatch; ponder) → s07 how PR #36 got here →
  s08 same look, different machine; a new feature is a new box → s09 recap, three questions, next.
