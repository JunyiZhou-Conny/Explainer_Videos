## Evaluation

**Test the agents across requests and repeated runs**

We have watched individual runs. Now ask: **does the system do the right thing across
several requests, and does it keep doing the right thing when we repeat them?**

A **golden case** is a mock request with an expected outcome. We check properties,
such as “ask for missing details” or “place one valid mock order,” rather than requiring
one exact answer or cheese selection. A refusal or clarification can be a success.

Use the shared settings at the top:

- `EVAL_ACT`: which act to evaluate; start with Act 6, which combines the assistant and workflow.
- `EVAL_N`: number of different applicable cases, selected from the list below.
- `EVAL_M`: repetitions of each case. There are **n × m scheduled runs**.
- `EVAL_FIXTURES`: start with `True` to learn the evaluation process using scripted responses.
  Set it to `False` to measure the live model. This setting is independent of `USE_FIXTURES`.
- `EVAL_CONTEXT`: select basic or enriched context when evaluating Act 2.

With the defaults, three requests run twice: **six scripted runs, with no API calls**.
Scripted consistency does not demonstrate model robustness. Live runs make multiple
model calls per request and incur API usage. To study one request repeatedly, use
`EVAL_N = 1` and increase `EVAL_M`.

Every run starts with fresh inventory, session state, and preference memory. Review
choices are explicit test decisions supplied by each case, even in live mode; the
model never acts as its own manager. No real purchases or emails are sent.


