# Exercises · AC215 L6 — LLM: Agents I (function calling by hand, ADK, MCP, many agents, the harness)

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real captures from
2026-10-18 (`assets/terminal/`), or were checked on 2026-10-19 in throwaway containers:
llm-rag's own `uv.lock` (Python 3.12.15, google-genai 1.39.1, chromadb 1.1.0) against the same Chroma
server image, loaded with the staff's recorded vectors (`68e0bde`); the ADK repo at `f89faa7` on uv's
CPython 3.13.16 with the capture's versions (google-adk 2.12.0, litellm 1.106.0, mcp 2.3.0, Node.js
24.22.0); and the notebooks' own install cells (openai-agents 0.3.2; agent-framework-core 1.18.0;
the Cheese Quiz's unpinned fastmcp 4.1.1 and openai-agents 0.24.0).
[`assets/exercise-checks/README.md`](assets/exercise-checks/README.md) lists every command; a file
name ending in `.log` below is one of its [`logs/`](assets/exercise-checks/logs/), and `laptop/…`,
`cli-container/…`, `adk-laptop/…`, `mcp-remote/…`, `expected/…` name captures in `assets/terminal/`.

There was **no key** (no Google Cloud, no AI Studio, no OpenAI). Items marked *with your key* need
one. Where a check needed a model's reply, it used a **stand-in**: a reply written by hand that drives
the tutorial's own, unchanged code down one path. A stand-in is never model output, and the answers say
what it stood in for. The logs write the instructor's name as `<instructor>`. Container IDs, session
IDs and the MCP fun fact differ on your laptop.

---

## Part A · The five questions from the end of the video

**Q1. In function calling, who runs the function, and what travels back to the model in call 2?**

<details><summary>Answer</summary>

**Your code runs it**, never the model. Call 1's answer is only an order, a `function_call` part:
`name='get_book_by_author'`, `args={'author': …, 'search_content': 'cheese making importance
location'}`, `id='call_1212960'` (`out.txt:20-27`), plus a `thought_signature` (`out.txt:28`).
`automatic_function_calling_history=[]` (`out.txt:51`): the SDK ran nothing, because it was given
declarations, not Python functions.

In the CLI container, `cli.py:457-460` collects the `function_call` parts and hands them to
`agent_tools.execute_function_calls` (`agent_tools.py:84-127`). The dispatcher matches the name
(lines 88, 111) and calls the real function with the model's two arguments plus two the model never
sees, `collection` and `embed_func` (line 41). That function embeds the search text (one paid
embedding call, `agent_tools.py:43` → `cli.py:75-84`), queries Chroma with `n_results=10` and
`where={"author": author}` (lines 46-48), joins the 10 chunks into one string and wraps it as
`Part.from_function_response(name=…, response={"content": …})` (lines 103-110).

Call 2 (`cli.py:465-477`) then sends three contents (the request, built but not sent, in
`cli-container/33`, lines 137-233):

1. the question, role `user`;
2. **the model's own turn, unchanged**, role `model`: its `functionCall` (id, args, name) with the
   `thoughtSignature` (line 151). Gemini's thinking models sign their turn and want it back exactly as
   sent;
3. **your function response**: `functionResponse {name, response: {content: …}}`, the 10 chunks as one
   string of 3,509 characters (line 135: 10 chunks × 350 characters + 9 line breaks), with no role
   and no `id`: it is matched by name.

The tools go along again, but no `toolConfig`, and `"generationConfig": {}` (line 231). The system
instruction is not in either call (`cli.py:40-58` defines it, nothing sends it). Per question: two
Gemini calls and one embedding call, all paid.
</details>

**Q2. What does `mode="any"` change, and why only on call 1?**

<details><summary>Answer</summary>

`mode="any"` becomes the enum value `ANY` (`cli-container/32`) and travels as `"toolConfig":
{"functionCallingConfig": {"mode": "ANY"}}` (`cli-container/31`, lines 86-90). google-genai 1.39.1
documents it as "Model is constrained to always predicting function calls only", any one of the
declared functions (`types.py:500-501`; `q2-function-calling-modes.log`). So call 1 **must** come
back as a function call: retrieval is guaranteed, and the model chooses only *which* search and its
arguments. What it loses is the choice the lecture's Self-RAG starts with: whether to retrieve at all
(slides 10-11). Without a tool config the mode is `AUTO`, "model decides to predict either function
calls or natural language response" (`types.py:498-499`).

Only call 1, because call 2 is where the answer has to come out as **text**. Under `ANY` every reply
must be a function call, so a forced call 2 could never answer. `cli.py` passes the tools again on call
2 but no `tool_config` (`cli-container/33`: no `toolConfig`), so the mode is back to `AUTO`: the model
may answer, or ask for another tool, which `cli.py` would print and never run (C2). The same split holds
for `temperature=0`: set on call 1 (`cli.py:445`) for a repeatable tool choice, not on call 2.
</details>

**Q3. What ends an agent loop, what cap do frameworks add, and which lecture block is that?**

<details><summary>Answer</summary>

**The stop rule:** a reply with no function call is the final response. The model decides it is done
by answering in plain text. ADK writes it as `Event.is_final_response()` (google-adk 2.12.0,
`events/event.py:286-308`): no function calls, no function responses, not partial, no trailing
code-execution result. (Also final: an event that carries an error code, lines 297-302; C5 shows what
that does to module 4.)

**The caps,** in case the model never stops (`q3-caps-*.log`):

| framework | cap | default | in the tutorial | when it is hit |
| --- | --- | --- | --- | --- |
| OpenAI Agents SDK | `max_turns` (model calls of one `Runner.run`) | 10 (0.3.2 and 0.24.0) | 12: Cheese Quiz cell 71 line 6, Travel Planner cell 21 line 17 | raises `MaxTurnsExceeded` (0.3.2 `run.py:538`) |
| Microsoft Agent Framework | `max_iterations` (model round trips) | 40 (`_tools.py:102`) | 16 for the Newsletter's orchestrator (cell 25 line 8), 6 and 3 for the researcher and editor (cells 21-22) | no error: one last response is requested with tools disabled (`_tools.py:3734-3740`) |
| ADK | `RunConfig.max_llm_calls` | 500 (`run_config.py:38`, or `ADK_MAX_LLM_CALLS`) | not set | |

**The block:** dynamic control, the steering wheel (slides 25-27). Slide 41 grays it out among the
building blocks: you configure the LLM core, instructions, tools and memory, and the framework writes
the loop. llm-rag has no loop at all: two hand-written calls, one lap (S08; B3 makes it a loop).
</details>

**Q4. How does `TripSummarizer` get the travel plan without a message from `TravelPlanner`?**

<details><summary>Answer</summary>

Through the **session**. `TravelPlanner` has `output_key="travel_plan"` (`1-baseline/agent.py:25`):
when it finishes, its final text is written into the session state under that key. `TripSummarizer`'s
instruction contains the placeholder `{travel_plan}` (line 31), and ADK fills it from the state just
before the summarizer's call. The `SequentialAgent` (lines 35-39) only runs the three in order; no agent
calls another.

Checked with ADK's own Runner and stand-in models (`q4-a-whiteboard.log`): the summarizer's system
instruction arrived as "Provide a concise, traveler-friendly summary based on (stand-in reply written
for TravelPlanner). Include total estimated cost…"; after the run the state held
`itinerary_validation`, `travel_plan` and `trip_summary`, and the session four events (the user's and
one per agent). ADK 2.12 also passes the earlier agents' replies as history: the summarizer's request
held the user's message plus two quoted blocks, "For context: … [ItineraryValidator] said: …" and
"… [TravelPlanner] said: …". So the plan reaches it twice, through the state and through the
session's events. A new session starts empty (`state {}`, 0 events), and the planner run without the
validator before it stops with `` KeyError: "Context variable not found: `itinerary_validation` in
agent 'TravelPlanner'." `` (C4).
</details>

**Q5. In the last two notebooks, what decides that a run succeeded, and why not the model's final
text?**

<details><summary>Answer</summary>

**Python state that only the checked path can set.**

- *Travel Planner.* `finalize_plan` (cell 15) computes the plan with Python's prices, but stores it as
  a pending proposal until a **later human turn** approves that exact proposal: `apply_confirmation`
  (cell 18, lines 55-65) runs on the human's message before the agent starts (line 106). `run_turn`
  then decides what the user sees from that state (lines 122-131): a pending proposal is shown as its
  exact JSON with a request for "yes"; a plan finalized in this turn is shown from `checked_plan` with
  Python's budget report (2,690 of 6,000 dollars, which cell 27 asserts); an "itinerary" reply without
  a same-turn check raises an error (hard guardrail), and a dollar amount in the model's prose only
  prints a warning (soft guardrail, lines 133-135).
- *Newsletter.* `generate_newsletter` (cell 18, lines 118-126) succeeds only if `context.receipt`
  exists, which only `save_newsletter` sets after validation and rendering (cell 16, lines 132-148),
  **and** the receipt's file is on disk.

Checked with stand-in agents in place of the models (`b9-travel-gate.log`, `b10-newsletter.log`): a
stand-in that claims an itinerary without calling the tool gets one corrective retry, then
`RuntimeError: The agent returned an itinerary without a successful same-turn check.`; an orchestrator
that just says "Newsletter sent successfully!" gets `RuntimeError: No successful tool receipt.
Orchestrator response: Newsletter sent successfully!`; one whose file disappears after saving gets
`RuntimeError: The mock email receipt points to a file that does not exist.`

Why not the model's words: they are a claim. The model may never have called the tool, its call may
have returned `{"status": "error", …}` (to the model that is just more text), or it may skip a rule
that lives only in its prompt (B10). In the Newsletter, the model's reply appears only inside the error
message.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Steer the tool choice** *(llm-rag, with your key)*. In your editor, change the question on
`cli.py` line 435 to `"What does George E. Newell say about rennet?"` and run
`python cli.py --agent --chunk_type char-split` in the container. Then try
`"Which books mention goat cheese?"`. Before each run, predict the function, its arguments, and which
books the 10 retrieved chunks can come from.

<details><summary>Answer</summary>

- **Newell:** a listed author is named, so expect `get_book_by_author` with
  `author='George E. Newell'`, spelled exactly as in the enum (`agent_tools.py:22`; the enum, lines
  19-29, lists the only author values the declaration allows), and a `search_content` about rennet. The
  filter `where={"author": author}` then keeps only that author's 395 chunks (`cli-container/34`): all
  10 results come from *Hand-book on cheese making* (`cli.py:64`).
- **Goat cheese:** no author, so expect `get_book_by_search_content`: the 10 nearest of all 8,248
  chunks, from any book.

`mode="any"` guarantees that one of the two is called. What was checked without a key
(`b1-two-tools.log`): the tutorial's dispatcher, given each function call by hand and the same query
vector (a stand-in: the stored vector of a chunk about rennet): by author, 10 of 10 from *Hand-book on
cheese making*; across all books, 6 from it and 4 from *The Book of Cheese*. Both function responses
are 3,509 characters (Q1). Which function the model actually picks needs your key: two Gemini calls
and one embedding call per run. `/app` is your folder, mounted, so the edit is live without a rebuild;
undo with `git checkout cli.py`.
</details>

**B2. Let the model skip retrieval.** Delete the `tool_config=…` block on `cli.py` lines 447-451,
change the question on line 435 to `"Hi! Who are you?"`, and run the agent again (with your key).
Predict what is sent, and what `cli.py` prints if the model answers in plain text.

<details><summary>Answer</summary>

The request has no `toolConfig` any more: its top-level keys are `contents`, `tools` and
`generationConfig` (still `"temperature": 0.0`) (`b2-a-diff.log`, `b2-b-request-no-tool-config.log`,
built, not sent). The mode is `AUTO`, so the model may answer a greeting in text. If it does, `cli.py`
prints the whole response object (line 454), then `Function calls: []`; the dispatcher returns no
parts, so line 462 prints `Function calls did not result in any responses...` and **there is no call
2**. Checked with a stand-in plain-text reply (`b2-c-text-reply.log`: one model call, those lines).
The greeting itself is visible only inside the printed object.

With your key, whether the model greets or searches anyway is its choice; there is nothing to retrieve
for a greeting. That is the trade: `ANY` guarantees retrieval and takes away the decision Self-RAG
starts with; `AUTO` gives it back (Q2, D2). Undo with `git checkout cli.py`.
</details>

**B3. Turn the two calls into a capped loop** *(stretch)*. Replace `cli.py` lines 439-478 with:

```python
    contents = [user_prompt_content]
    config = types.GenerateContentConfig(temperature=0, tools=[agent_tools.cheese_expert_tool])
    for step in range(5):
        response = llm_client.models.generate_content(
            model=GENERATIVE_MODEL, contents=contents, config=config)
        model_turn = response.candidates[0].content
        calls = [p.function_call for p in model_turn.parts if p.function_call]
        if not calls:                      # final answer: no more tool requests
            print("Answer:", response.text)
            break
        contents.append(model_turn)        # keep the model's turn verbatim (thought signatures)
        contents.append(Content(role="user", parts=agent_tools.execute_function_calls(
            calls, collection, embed_func=generate_query_embedding)))
    else:
        print("Gave up after 5 steps")
```

Predict how many contents each call sends if the model searches twice and then answers, and what
happens if it never stops asking for tools.

<details><summary>Answer</summary>

Each lap adds two contents, the model's turn and your function responses: call 1 sends 1 content
(`user`), call 2 sends 3 (`user`, `model`, `user`), call 3 sends 5. When a reply has no function call,
the loop prints `Answer:` and stops: the stop rule of Q3. If the model never stops, the cap ends it after
5 model calls and 5 tool runs with `Gave up after 5 steps`; the fifth results are never sent back.

Checked with scripted stand-in replies on the real collection (`b3-a-diff.log`, `b3-b-loop-*.log`):
exactly those roles and counts; and with two scripted laps followed by the real SDK, the third request
builds with roles `user, model, user, model, user` and parts `text, functionCall, functionResponse,
functionCall, functionResponse` (built, not sent). There is no `tool_config`, so the model can stop;
a reply may also carry two function calls at once, and the dispatcher runs both. With your key, ask
"Compare what Newell and Curtis say about curd temperature" and count the laps; each one costs a
Gemini call and an embedding call per search.
</details>

**B4. Watch the whiteboard** *(ADK, with your AI Studio key)*. In the dev UI pick `baseline`, send
"2 adults, Boston to Montreal, Oct 30 - Nov 2, 1500 dollars, train preferred", and open the State
and Events tabs. Predict the state keys and who wrote each, and what `TravelPlanner`'s instruction
looks like when it reaches Gemini. Then start a new session: what is in its state? Stop and restart
`adk web`: is the first session gone?

<details><summary>Answer</summary>

Three keys, one per agent, from their `output_key`s: `itinerary_validation` (ItineraryValidator),
`travel_plan` (TravelPlanner), `trip_summary` (TripSummarizer). The planner's instruction reaches the
model with `{itinerary_validation}` already replaced by the validator's reply, and its request also
carries the validator's reply as quoted history (Q4). A new session starts with `state {}` and no
events. Checked with ADK's Runner and stand-in models (`q4-a-whiteboard.log`).

Restarting `adk web` does **not** remove sessions: they are stored in `baseline/.adk/session.db`
(`b11-adk-sessions-git.log`); after a restart, `GET /apps/baseline/users/student/sessions` still listed
the two sessions made earlier (`c1-module-env.log`). Session state lasts for one session, but sessions
last on disk until you delete them (B11, D3). Each request costs three Gemini calls.
</details>

**B5. Fix the router two ways.** In `custom_agent/conditional_agent.py` (the video's renamed
`5-custom-agent`), the classifier's answer decides the handler (lines 85-102). Make (a) a copy where
line 85 ends in `.strip().lower()`, and (b) a copy where the classifier gets a structured output:

```python
from typing import Literal
from pydantic import BaseModel

class Classification(BaseModel):
    complexity: Literal["simple", "complex", "ambiguous"]
```

with `output_schema=Classification,` after `output_key="query_complexity"` (line 171), and line 85
reading `ctx.session.state.get("query_complexity", {}).get("complexity", "simple")`. With your key, run
each from the module folder with `uv run --project .. python conditional_agent.py`. Predict the routes
when the classifier answers `Simple` and `complex` followed by a line break.

<details><summary>Answer</summary>

| classifier says | as committed | (a) `.strip().lower()` | (b) `output_schema` |
| --- | --- | --- | --- |
| `simple` / `complex` / `ambiguous` | Simple / Complex / Clarification handler | same | same |
| `Simple` | **ClarificationHandler** | SimpleHandler | ruled out by the schema; if it came anyway: `ValidationError` |
| `complex` + line break | **ClarificationHandler** | ComplexHandler | ruled out by the schema |

`output_key` stores the classifier's raw text, and `complexity == "simple"` is an exact comparison
(`b5-b`, `b5-c`: the committed code sends `Simple` and `complex\n` to clarification; `b5-d`: the
normalized copy routes them correctly). With `output_schema`, ADK sends the class as the response schema
with MIME type `application/json` on every classifier call, and `output_key` stores the validated
fields as a dict (`b5-e`: all three routes right). If a reply ever broke the schema, ADK would stop
with a `ValidationError` ("Input should be 'simple', 'complex' or 'ambiguous'", `b5-f`) instead of
silently picking clarification. Those runs used stand-in classifier replies and ADK's own Runner; the
handlers' answers need your key (two Gemini calls per query).

Why `--project ..`: it runs the module with the root `.venv` (`b5-g-which-venv.log`). Plain `uv run`
inside the folder would make a second environment from the module's own `pyproject.toml`
(`google-adk[all]`: "Would install 276 packages").
</details>

**B6. Your agent as a web API** *(module 4)*. From `4-production-ready/` start the FastAPI app with the
root environment, `uv run --project .. uvicorn app.main:app --port 8080` (the module README's `uv sync`
would make a second environment). Before adding your key, predict the answers to
`curl -s http://localhost:8080/health`, `http://localhost:8080/docs`, and the README's
`curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '{"user_message":
"Hello!"}'`, and to the same request with `"message"` as the field name. With your key, send
`"My name is Sam."`, then `"What is my name?"`.

<details><summary>Answer</summary>

`/health` → `{"status":"healthy"}`; `/docs` → `200` (FastAPI's Swagger page); `/chat` →
`Internal Server Error`, `500` (the model call fails; the log's last error is misleading, C5); the
wrong field name → `422` with `"msg":"Field required"` for `user_message` (`b6-a-module4-api.log`). The
app reads the root `.env` (its `load_dotenv()` walks up from `app/`), so the model is your
`GEMINI_MODEL`.

The second question gets no memory of the first: `AgentRunner.run` creates a **new random session and
user for every request** (`app/runner.py:24-32`). Checked with a stand-in model (`b6-b-two-requests.log`):
the second call's request held only "What is my name?", and the service ended with two sessions for two
users. To keep a conversation, the client must send a session ID and the server must reuse it (D3). The
module's Docker variant passes only `GOOGLE_API_KEY`: without `-e GEMINI_MODEL=…` the agent falls back to
the retired `gemini-2.0-flash` (`app/agent.py:12`; reasoned, not run).
</details>

**B7. Make module 2 really use LiteLLM** *(with an OpenAI key)*. `2-litellm/agent.py` asks for
`model="gpt-4"`. Copy the folder to a name ADK accepts, put `OPENAI_API_KEY=…` in the root `.env`, and
change the model to `LiteLlm(model="openai/gpt-5.6-luna")` (import it with
`from google.adk.models.lite_llm import LiteLlm`). Predict: what does ADK 2.12 do with the bare
`"gpt-4"`, and which folder name would you choose?

<details><summary>Answer</summary>

On google-adk 2.12.0, `"gpt-4"` resolves to ADK's own `OpenAILlm` class, **not** LiteLLM;
`"openai/gpt-5.6-luna"` resolves to `LiteLlm` (`b7-b-load.log`). The folder name matters three ways
(same log): `2-litellm` → `Invalid agent name` (S10); **`litellm`** → `No root_agent found for
'litellm'`, because `import litellm` finds the real LiteLLM package first; `litellm_agent` loads, with
`model LiteLlm(model='openai/gpt-5.6-luna', …)` (`b7-a-patch.log` has the diff).

The key's name: `litellm_config.py:28` reads `OPENAI_API_KEY`; the `.env.example` files' `AWS_OPENAI_API_KEY`
is read by no Python file in the repo. Without the key, the first message fails on your machine before
any request leaves: `OpenAIError: Missing credentials. Please pass an api_key …` (same log). With it,
each message is one OpenAI call, billed per token. `gpt-5.6-luna` is the model the notebooks use.
</details>

**B8. MCP: the filter, and a tool on its way out.** In a copy of `mcp_tools/agent.py`, add
`'read_text_file'` to `tool_filter` (line 28). Predict which tools the agent sees, what the server says
about `read_file`, and what `search_files` returns for the pattern `agent` and for `**/*agent*`.

<details><summary>Answer</summary>

Four instead of three: `list_directory`, `read_file`, `read_text_file`, `search_files`; the server
offers 14 (`adk-laptop/35`). The server (`@modelcontextprotocol/server-filesystem` 1.0.0) describes
`read_file` as "Read the complete contents of a file as text. DEPRECATED: Use read_text_file instead."
If a future version drops it, the committed filter would silently leave the agent without a read tool:
a filter naming a tool the server doesn't have raises no error, the agent just sees fewer tools
(`b8-b-missing-name.log`: `read_file_v0`, `list_directory`, `search_files` → two tools).

`search_files` matches **file names** with glob patterns, not file contents: `agent` → "No matches
found"; `**/*agent*` → `mcp_tools/__pycache__/agent.cpython-313.pyc` and `mcp_tools/agent.py`. So the
README's "Search for files containing 'agent'" can only find names. A `read_file` of the repo's `.env`,
one folder up, is refused: "Access denied - path outside allowed directories" (`b8-a-mcp-filter.log`;
no model involved, the toolset's own client). With your key, ask in the dev UI and watch the Events
tab for the calls.
</details>

**B9. Travel Planner: try to approve your own plan** *(no model calls)*. Run the notebook's cells up to
*Travel Agent*, then in a new cell call the tool's function yourself, as the model would in turn 3:

```python
ctx = TravelContext()
plan = dict(outbound_id="SEA-SFO-20261106-1", return_id="SFO-SEA-20261110-1", hotel_id="SFO-BAY",
            travelers=2, budget_usd=6000, daily_food_usd=60, local_transport_usd=150,
            pet_friendly=True, attraction_ids=["SFO-BRIDGE", "SFO-MUSEUM"])
print(finalize_plan(ctx, **plan)["status"]); print(finalize_plan(ctx, **plan)["status"])
apply_confirmation("Yes!", ctx)
print(finalize_plan(ctx, **plan)["total_usd"])
```

Predict the three lines. Then predict which of these replies approve a pending proposal: `Yes!`,
`yes please`, `Yes, please.`, `y`, `Confirm.`, `OK`, `sure`, `Yes go ahead`. Finally predict
`check_itinerary` with the 15:00 outbound flight (`SEA-SFO-20261106-2`), and with hotel `SFO-GATE`.

<details><summary>Answer</summary>

`needs_confirmation`, `needs_confirmation`, `2690.0`, each after a `[tool] finalize_plan: …` line
(`b9-b-snippet.log` runs this cell as printed; `b9-travel-gate.log` the rest). Calling the tool again in
the same turn changes nothing: only `apply_confirmation` copies the pending proposal to the approved one
(cell 18, lines 55-65), and in the notebook it runs only on the human's message, before the agent
(line 106). That is the ponder's answer.

`apply_confirmation` strips the reply, lower-cases it, removes trailing `.`, `!` and spaces, then
compares it with six exact strings: `Yes!`, `yes please`, `y`, `Confirm.` (and `yes, confirm`)
approve; `Yes, please.`, `OK`, `sure`, `Yes go ahead` don't. Any other reply also **drops** the
pending proposal and leaves nothing approved (lines 62-65), so the model has to propose again. A gate
this strict is the point: only an explicit yes counts.

Variants: the 15:00 flight costs 50 dollars more per person, so flights 980 and a total of **2,790**;
`SFO-GATE` with `pet_friendly=True` raises `ValueError: Hotel does not meet the destination/pet-friendly
requirements.`, because it isn't pet-friendly; with `pet_friendly=False` it totals **2,410**, but
`finalize_plan` returns `needs_confirmation` again: the earlier yes approved a different proposal.
Note the order in `finalize_plan`: `check_itinerary` runs first (cell 15, line 19), so a bad selection
raises before the gate. None of this calls a model, so it is free.
</details>

**B10. Newsletter: make the URL rule a check.** The editor is told "no embedded URLs" (cell 22, line
16), and the saved preview has one. Add these lines at the end of `validate_newsletter` (cell 18, after
line 33), then rerun the cells from *Business Logic* down and the demo (with your key):

```python
    URL = re.compile(r"https?://|www\.", re.IGNORECASE)
    for text in [draft.subject, draft.introduction, draft.offers_note, draft.closing,
                 *(f"{item.title} {item.summary}" for item in [*draft.news, *draft.offers])]:
        if URL.search(text):
            raise ValueError("Remove embedded URLs from the newsletter text; sources are linked by ID.")
```

Predict what the editor's tool returns for a draft whose offer says "Promotion URL: https://…", and
what `send_email` does with it.

<details><summary>Answer</summary>

As committed, such a draft passes: `review_draft` → `{'status': 'ready'}`, and `send_email` saves it
(`b10-newsletter.log`, stand-in orchestrator, the notebook's own functions). With the check,
`review_draft` (cell 16, lines 110-117) returns `{'status': 'error', 'message': 'Remove embedded URLs
from the newsletter text; sources are linked by ID.'}` as `editor_agent`'s tool result, and `send_email`
returns the same error, with no receipt (`save_email` validates again, cell 18 line 100). The same
draft without the URL → `ready`. Links still appear in the letter: the renderer adds each story's
sources from the registry (cell 18, lines 45-48), which is where URLs belong.

With your key, the orchestrator reads the error as feedback and asks the editor for a revision (cell
24: "Tool validation errors are feedback"); expect more editor calls, each billed (Summerville already
took four in the saved run). A rule that matters belongs in code the model can't talk its way past.
</details>

**B11. Keep your sessions out of git.** After the video's rename and one session in the dev UI, predict
what `git add --all --dry-run` would add. Then add `.adk/` to `.gitignore` and check again with
`git check-ignore -v baseline/.adk/session.db`.

<details><summary>Answer</summary>

`adk web` keeps each agent's sessions in a SQLite file inside the agent's folder: the log says
"Creating local session service at …/baseline/.adk/session.db" (`b11-adk-sessions-git.log`). The repo's
`.gitignore` ignores `.env`, `.venv` and `uv.lock`, not `.adk/`, so `git add --all --dry-run` lists
`add 'baseline/.adk/session.db'` along with your renamed folders. That file holds every message and
reply of every session, including anything you pasted in. After `echo ".adk/" >> .gitignore`,
`git check-ignore -v` answers `.gitignore:73:.adk/  baseline/.adk/session.db` and the dry run no longer
lists it. If you already committed one: `git rm --cached baseline/.adk/session.db`.
</details>

---

## Part C · Debugging

**C1. "My baseline runs on `gemini-2.0-flash` and says the API key is not valid, but my root `.env` is
right."** A classmate followed `1-baseline/README.md`'s Setup inside the folder (`cp .env.example
.env`). What happened, and what else could that file leak?

<details><summary>Answer</summary>

ADK loads **only the nearest** `.env`, walking up from the agent's folder (S09). Checked
(`c1-module-env.log`): with only the root file, the log says `Loaded .env file for baseline at
…/llm-agent-google-adk/.env` and the agent tree shows `model gemini-3.1-flash-lite` three times; after
`cp .env.example .env` in `baseline/`, it says `… at …/baseline/.env` and every agent shows
`model gemini-2.0-flash`. That module file has the placeholder key and `GEMINI_MODEL` commented out
(`1-baseline/.env.example:6, 16`), so the code's fallback, the retired `gemini-2.0-flash`
(`baseline/agent.py:12`), comes back with a key Google refuses (`adk-laptop/29`).

Fix: delete the module `.env` files (or put your key and model in each), and skip the module READMEs'
Setup steps; the root sync and root `.env` cover every module. The leak: a `.env` copied into
`mcp_tools/` sits inside the folder the filesystem server may read. Checked: `list_directory` shows it,
and `read_file` on it returned the whole file (`c1-b-mcp-module-env.log`, placeholder key, no model).
With a real key there, one "read the .env file" request would hand your key to the model.
</details>

**C2. "I applied the video's fix, `print(response.text)` on line 478, and my run printed `None`."**
Why, and what does that say about the program?

<details><summary>Answer</summary>

Call 2 answered with **another function call** instead of text. Its mode is `AUTO` (Q2), so that is
allowed; `response.text` joins only text parts, so it is `None`, and google-genai warns: "there are
non-text parts in the response: ['function_call'], returning concatenated text result from text
parts." Checked with the staff's recorded call 1 and a stand-in function call as reply 2
(`c2-a-diff.log`, `c2-b-second-call.log`): exactly that warning, then `None`, and the program ends after
two model calls. Nothing runs the second call: that is S08's ponder. Fix: look at
`response.candidates[0].content.parts`, and either run the new calls in a loop (B3) or keep the original
print, which shows the function call.
</details>

**C3. "`uv sync` fails with `onnxruntime` and `cp315`, although my laptop has Python 3.12."**
`python3 --version` says 3.12. Why does uv use 3.15?

<details><summary>Answer</summary>

uv prefers the Pythons **it** manages over the system's. Checked on a laptop with a system Python
3.12.15 (`c3-python-pick.log`): with no uv-managed Python, `uv sync --dry-run` says `Using CPython
3.12.15 interpreter at: /usr/local/bin/python3` and would install; after `uv python install 3.15` (as
an earlier project, or the video's first sync, would leave behind), the same command says `Using
CPython 3.15.0` and stops with `Distribution onnxruntime==1.31.0 … can't be installed because it
doesn't have a source distribution or wheel for the current platform`. `requires-python = ">=3.10"`
has no upper bound, and `onnxruntime` (through `chromadb`) has wheels only up to cp314
(`adk-laptop/07`). Fix: `uv python pin 3.13` (any of 3.11-3.14), then `uv sync`.
`uv python list --only-installed` shows what uv can choose from.
</details>

**C4. `` KeyError: "Context variable not found: `itinerary_validation` in agent 'TravelPlanner'." ``** A
teammate renamed the validator's `output_key` to `"validation"`, or tested `TravelPlanner` on its own.
Explain, and give two fixes.

<details><summary>Answer</summary>

Before the planner's call, ADK fills `{itinerary_validation}` from the session state; nothing has
written that key, and a missing key is an error, not an empty string. Checked by running the planner
alone in a fresh session (`q4-a-whiteboard.log`): exactly this `KeyError`. A renamed `output_key`
leaves the key missing in the same way. Fixes: keep `output_key` and `{placeholder}` names identical
(they are the only contract between the agents, Q4); or make the placeholder optional with a question
mark, `{itinerary_validation?}`: then the instruction goes out as "Using , design a realistic
multi-day travel plan…" with an empty value (`c4-optional-placeholder.log`), which runs but plans from
nothing. Prefer the first.
</details>

**C5. Module 4's `/chat` answers `Internal Server Error`, and the server log ends with
`AttributeError: 'NoneType' object has no attribute 'parts'`.** Is the bug in FastAPI?

<details><summary>Answer</summary>

No: read the first error, not the last. The log first shows the model call failing (in the check it was
`ClientConnectorDNSError: Cannot connect to host generativelanguage.googleapis.com:443`, because the
check container had no internet; on a laptop with the placeholder key expect Google's
`400 … API key not valid`, as `adk-laptop/29` shows for `adk web`). ADK turns a failed model call into an event that counts as
the final response (`event.py:297-302`) but has no content: `final=True content=None
error_code='ClientConnectorDNSError'` (`c5-error-event.log`). The wrapper then reads
`event.content.parts[0].text` (`app/runner.py:46`) and trips over `None` (`b6-a-module4-api.log`:
`main.py` line 31 → `runner.py` line 46). Fix the key first; then make the wrapper honest:

```python
            if event.is_final_response():
                if event.error_code:
                    raise RuntimeError(f"Model call failed: {event.error_code}: {event.error_message}")
                response_text = event.content.parts[0].text
```
</details>

**C6. Cheese Quiz: "I edited the MCP tool in *Build your own MCP Server* and ran that cell again, but
the agent still returns the old facts. The cell even printed `Server thread alive: True`."**

<details><summary>Answer</summary>

The first server is still running in the same Colab runtime and still holds port 8001. Checked with
today's unpinned packages (fastmcp 4.1.1) in one Python process (`c6-fastmcp-rerun.log`): the second run
prints `FastMCP server starting on http://127.0.0.1:8001/mcp` and `Server thread alive: True`, because
the check happens before the new server tries to bind; then `ERROR: [Errno 98] … address already in
use`, and three seconds later the new thread is dead. A FastMCP client (no model) still lists one tool
and gets a random fact from the **old** function, not the edited one. Fix: *Runtime › Restart session*,
then run the setup cells again (Install Packages, Imports, Set Up OpenAI Key) and the cells from the
fun facts on; or run the edited server on another port and change the URL in the next cell. A client is
also a free way to test your server without OpenAI: `async with fastmcp.Client("http://127.0.0.1:8001/mcp")
as c: print(await c.call_tool("<tool name>", {}))`.
</details>

**C7. Cleaning up `6-rag/1-vertex-rag-engine`** *(only if you tried it, with Google Cloud)*. You ran
`setup_corpus.py`, chose `5. Delete corpus`, pasted the name, typed `y`, and got `Cancelled.` Before
that, the script stopped at `Error: GOOGLE_CLOUD_PROJECT environment variable not set.` Explain both,
and what else to check so nothing keeps billing.

<details><summary>Answer</summary>

`load_dotenv()` finds the nearest `.env`; from the module folder that is your root `.env`, where
`GOOGLE_CLOUD_PROJECT` is commented out, so the script exits (lines 29-35;
`m6-c-vertex-rag-import.log`). Put it in the module's `.env` (the module's own `cp .env.example .env`)
or export it. The delete prompt compares `confirm.lower() != "yes"` (line 139): only the whole word
`yes` (any case) deletes, `y` cancels. Checked offline (`m6-d-delete-corpus-menu.log`): `y` →
`Cancelled.`; `yes` → the script reaches `rag.delete_corpus` and, here, stopped at
`DefaultCredentialsError` for want of credentials. The corpus name is the full resource name,
`projects/…/locations/us-central1/ragCorpora/…` (option 2 lists them). Run it from the module folder
with the root environment: `uv run --project ../.. python setup_corpus.py`. The import also warns that
`vertexai.preview.rag` is deprecated (google-cloud-aiplatform 2.5.0).

Then check the console's RAG Engine page. Google's documentation
([deployment modes](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/deployment-modes),
[Spanner mode](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/spanner-mode), both
"last updated 2026-10-15") says Spanner mode is the default, its Basic tier is a
fixed provisioned instance, and only switching the tier to **Unprovisioned** (`UpdateRagEngineConfig`)
deletes that instance and stops its billing, irreversibly; deleting corpora removes your data. Not
run here (no Google Cloud): look at the billing report a day later.
</details>

**C8. `6-rag/2-custom-chromadb-rag`: "`docker compose up -d` says the container is unhealthy, the
README's `curl http://localhost:8000/api/v1/heartbeat` returns an error, and after `docker compose
down` and `up` my documents are gone."** Three questions: is Chroma down, why unhealthy, where did the
data go?

<details><summary>Answer</summary>

Checked against the Chroma image the course pulled as `latest` (`chroma 1.4.4`):

- **Not down:** `/api/v1/heartbeat` → `410 {"error":"Unimplemented","message":"The v1 API is deprecated.
  Please use /v2 apis"}`; `/api/v2/heartbeat` → `200` (`m6-a-heartbeats.log`).
- **Unhealthy forever:** the healthcheck runs `curl -f …/api/v1/heartbeat` inside the container
  (`docker-compose.yml:16`), but the image has no `curl` (`command -v curl` fails, `m6-b-chroma-image.log`),
  and the v1 path would fail anyway. Ignore the status, or drop the healthcheck.
- **Data:** the file mounts its named volume at `/chroma/chroma` and sets `IS_PERSISTENT` /
  `PERSIST_DIRECTORY` (lines 9-14), settings of older images. Today's server writes to `/data` and the
  image declares no volume (`m6-e-chroma-image-config.log`). Started with the module's settings, a
  collection with one record went to `/data` (`chroma.sqlite3` and an index folder) while
  `/chroma/chroma` stayed empty (`m6-f-module-compose-settings.log`); `down` removes the container and
  the data with it. Mount the volume at `/data` instead.

It also publishes port 8000, like llm-rag's Chroma and `adk web` (S10): run one at a time, or move
one. The module's agent needs `sentence-transformers` (PyTorch) and wasn't run here.
</details>

---

## Part D · Think

**D1. Data, action, orchestration.** Sort today's tools into the lecture's three families (slide 51):
`get_book_by_author`, `get_book_by_search_content`, `web_search`, `list_directory`, `read_file`,
`write_file`, `finalize_itinerary`, `send_email`, `research_facts` (`.as_tool`), `researcher_agent`,
`editor_agent`, `ask_head_cheesemonger`. Where do the tutorial's checks sit? And who decides what
`ask_head_cheesemonger` returns?

<details><summary>Answer</summary>

- **Data** (fetch): the two book searches, `web_search`, `list_directory`, `read_file`.
- **Action** (change something): `write_file` (the server offers it; the filter removes it, B8),
  `finalize_itinerary` (a checked plan), `send_email` (saves the letter; "sends" in a real system).
- **Orchestration** (hand work to an agent): `research_facts` and the other Guild tools made with
  `.as_tool`, and the Newsletter's `researcher_agent` and `editor_agent`.

The decisive checks sit on the **action** tools: the approval gate on `finalize_itinerary`, validation
and the receipt on `send_email` (the editor's draft is validated too), and the MCP filter keeps the
filesystem's action tools away entirely. That is the useful rule: the more a tool changes, the more
code should stand between the model and it.

`ask_head_cheesemonger(prompt, default_decision=True)` (Cheese Quiz cell 62, lines 159-162) is
offered to the Guild's orchestrator and returns `default_decision`, an argument **the model writes**:
"In real UI, ask the user. Here we simulate." So the "human decision" is the model answering itself.
Compare the Travel Planner, where only a later human turn can approve (B9).
</details>

**D2. Force the search, or let the model choose?** llm-rag forces a tool call (`ANY`); B2 lets the
model choose (`AUTO`). For each, name a question where it helps and one where it hurts. What would a
Self-RAG-style agent add (slides 10-11)?

<details><summary>Answer</summary>

`ANY` helps whenever the answer must come from your books: "what does the instructor's story say about
the curd?" can't be answered from memory, and forcing makes sure the model looks. It hurts on "Hi! Who
are you?" or "what's 2 + 2?": a paid embedding call and a search for nothing, and ten unrelated chunks
in the prompt. `AUTO` handles greetings, but the model may also skip the search for a question it
*thinks* it knows, and answer from memory: without the system instruction (never sent, Q1) nothing
tells it to prefer the books.

Self-RAG adds explicit steps around that choice: decide whether to retrieve, then grade the retrieved
passages (relevant?), the answer (supported by them?) and its usefulness, and retrieve again if not.
In code that is either more model calls in a loop (B3) with grading prompts, or checks in your own code;
the tutorial has neither. google-genai 1.39.1 also lists a `VALIDATED` mode, "model decides … but will
validate function calls with constrained decoding" (`types.py:504-505`); not tried here.
</details>

**D3. Session state is not memory.** The ADK README calls per-session state "Memory"
(`README.md:140`). What would an agent need to remember *you* next time, in the lecture's sense (slides
40-41)? Use what you saw: the Cheese Quiz's step 5, ADK's sessions file, module 4's new session per
request, and the Travel Planner's `SQLiteSession`.

<details><summary>Answer</summary>

Three things: a store keyed by **user**, not by session; a write step that decides what is worth
keeping (a preference, a fact about you), and a read step that puts it back into the envelope on the
next run. The Cheese Quiz's step 5 shows only the last part: a profile typed into the cell and sent with
every call (cell 42). ADK's state lives in one session: a new session starts `{}` (B4), module 4 even
makes a new session per request (B6), and the Travel Planner's `SQLiteSession("travel-planner")` uses
an in-memory database by default (`db_path=':memory:'`, openai-agents 0.3.2, `b9-travel-gate.log`), so
its history ends with the runtime, and `chat_loop()` starts a fresh one. Sessions do persist in
`adk web` (`baseline/.adk/session.db`, B11), but they are transcripts, not memory.

ADK has a separate memory service for this (`google/adk/memory/`: in-memory, SQLite, Vertex AI Memory
Bank, Vertex AI RAG; and the tools `load_memory` / `preload_memory`), passed to the `Runner` as
`memory_service`; none of the tutorial's code uses it (`d3-adk-memory.log`). Whatever you store, store
deliberately: it is data about a person, and every later prompt carries it.
</details>

**D4. Every hop costs.** The Guild's orchestrator runs with `max_turns=12` (cell 71) and is told to make
"at most 2 total review rounds" (cell 70, line 11). Count the orchestrator's turns on the longest path
its instructions allow, with one tool call per turn. Is 12 enough? How would you enforce "at most 2
reviews" in code?

<details><summary>Answer</summary>

`research_facts`, `vegan_specialist` (vegan topics), `write_quiz`, `review_quiz`, one revision
`write_quiz`, a second `review_quiz`, `ask_head_cheesemonger` (if the reviewer needs an opinion),
`format_quiz_json`, then the final structured answer: 9 model calls, so 12 leaves 3 spare. More if the
model retries a failed tool or ignores the limit, fewer if it calls tools in parallel. `max_turns` counts
only the orchestrator's own calls: each agent-as-tool runs its own `Runner.run` with its own budget,
default 10 (`as_tool(…, max_turns=None)` → `DEFAULT_MAX_TURNS`, openai-agents 0.24.0 `agent.py:617,
755`; `d4-as-tool.log`). So one quiz can make dozens of model calls and several paid web searches, and
the saved run logged three errors on the way (S13).

"At most 2 review rounds" is prose. To enforce it, give the orchestrator a `review_quiz` function tool
of your own that counts its calls in the run's context and returns an error after the second, or take
the order away from the model: a fixed sequence in Python (like ADK's `SequentialAgent`) with a loop of
at most two review rounds (reasoned, not run).
</details>

**D5. Fix the enum, or fix the data?** The enum leaves out two books' authors (S04). Would adding
`"Milk Industry Foundation"` and `"Woman's Institute of Domestic Arts and Sciences"` to the enum
(`agent_tools.py:19-29`) make both books reachable by author?

<details><summary>Answer</summary>

Only one. *Cottage Cheese Recipe Book*'s chunks carry `author: 'Milk Industry Foundation'`, so the
filter works: 10 results, 3,509 characters (`b1-two-tools.log`). The Woman's Institute book's chunks
have **no** author at all, only `{'book': 'Womans Institute Library of Cookery'}`: lecture 5's
file-name slip (`filename.split(".")[0]`, `cli.py:178`) cut the name before it could match
`book_mappings`. Filtering by its author returns 0 results and an empty function response. The model
would then answer from an empty string. Fix the data first (L05's exercise B4: `os.path.splitext`, then
chunk, embed and load again), then the enum. Both books stay reachable through
`get_book_by_search_content` either way.
</details>

**D6. Put the agent behind a web page.** Lecture 18's app reuses this `agent_tools.py` unchanged
(`cheese-app-v2` @ `14f2a14`, `src/vector-db/agent_tools.py`; `d6-cheese-app-v2.log`). If anyone on
the internet can type the question, what can they control, what does each question cost, and what
would you change first?

<details><summary>Answer</summary>

They control only the question. The model turns it into `{name, args}`: `author` is limited to the 9
enum values, `search_content` is free text that is only embedded, never executed, and `n_results=10` is
fixed, so the database can't be steered beyond "which author, what text". Each question costs at least
two Gemini calls and one embedding call (Q1), more with a loop (B3), and there is no limit per user.

First changes: send the system instruction (it exists, `cli.py:40-58`), so off-topic or
prompt-injection questions get the polite redirect it describes; cap the calls per question (a loop with
a turn limit, B3) and per user (rate limits, budget alerts); print or return only `response.text`, with
the empty and the function-call cases handled (C2); and treat retrieved text as data, never as
instructions: the chunks go back as a function response the model reads, so whoever can add a book can
put words in front of the model.
</details>
