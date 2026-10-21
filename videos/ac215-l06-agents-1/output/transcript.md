# AC215 · Lecture 6 — LLM: Agents I (follow-along: llm-rag, llm-agent-google-adk)

## 00:00 — Who searched your database?
Here's a question for a cheese expert: describe where cheese making is important in the instructor's book. In the staff's recorded run, these two lines print before the answer: a function called get book by author, and its arguments.
Ten passages came back, all from one book, filtered by author. But Gemini runs in Google's data center, where localhost means nothing. So who searched your database, and who chose the book?
The lecture asks a bigger version: plan five days in Paris, and replan if it rains or a flight is late. A model can draft a plan, and RAG can fetch facts, but neither can act.
What's missing: live systems, tools that act, and the autonomy to decide.
Today we climb toward that in three steps. By hand, with L-L-M rag's agent; with a framework, Google's Agent Development Kit; and with a harness, in Colab notebooks.
The tracker, top left, shows the step; the gray tag, top right, names the lecture slides. Pause at each yellow your-turn tag, and run the command.
You'll need the database and key from lecture 5, Docker, uv, Node, and two more keys: one from Google AI Studio, one from OpenAI, with billing on.
We recorded on October 18, 2026, without keys. Docker, Chroma, uv, the ADK web server and two MCP servers ran for real; every model call stopped unsent, or was refused. Model answers are the staff's saved outputs.
On screen we hide the instructor's name; your terminal shows it. Every command is in the study guide, in the MLOps Learning repo.

## 01:55 — Who holds the steering wheel?
First the ideas, in the Cheese Quiz. Save a copy in Drive, then add your OpenAI key in the Secrets panel, under the name shown, with notebook access on.
The install cell installs two packages, unpinned, and hides all output: if imports fail later, rerun it without that redirect. Then download the quiz files, and pause to run the setup.
Now the notebook asks one question three ways, with the same model each time: what's the best cheese for a grilled cheese sandwich? Lane 1, the base LLM: one call to GPT-4o, one answer, in under 3 seconds.
Lane 2, the reasoning LLM: Python methods run in a fixed order. Analyze, split into 4 sub-questions, answer and verify each, then combine. That's 11 calls and 39 seconds, and its token total is only an estimate.
The lecture calls a multi-call system like this a reasoning engine. Here your Python orders the calls, so it's a reasoning workflow, not a reasoning model.
Lane 3, the agent: the same model, plus instructions and a web search tool that OpenAI hosts. Its answer reports two searches, and it stopped on its own after 13 seconds. It also reports one tool used, but that counts tools configured, not calls.
The lecture defines an agent as an LLM, given instructions and tools, that runs on its own until the task is done. Of its five blocks, one decides the next step: dynamic control, the steering wheel.
So an agent isn't a smarter model: the model was the same in all three lanes. What changed is who steers, and the tools. Every call is paid; pause, and run the three lanes.

## 03:49 — Everything the model knows is in the envelope
Next section: managing the model's inputs. LLMs are stateless functions. Every call is a fresh envelope, and the model knows only what's inside.
The notebook keeps the model and question fixed, and changes the inputs each step. A system prompt, retrieved documents, earlier turns, a profile from past sessions, a tool's output, an output schema.
Watch the top pick change: cheddar, American, then mild cheeses for kids, then Havarti. Then a mild cheddar from Whole Foods, and finally the same pick as strict JSON.
Step 4 shows what memory really is. The earlier turns aren't remembered: the code sends them again, every time. Memory is paper you put back in the envelope.
The lecture groups these sheets into two building blocks: instructions and memory. Next lecture names the craft: context engineering.
Now look closely at the code of step 2. Can you spot the slip?
The system prompt goes in with the role user, and the question with the role system.
Swap those two roles before comparing; from step 3 on, they're right. Pause, and run the seven steps.
And notice step 6: the code pasted a tool's output into the envelope. But how does a model ask for a tool?

## 05:13 — A menu of two tools
In lecture 5, RAG was a straight line: question, retrieval, model, response. The lecture's recap makes retrieval smarter: steps around the search, whether to retrieve at all, grading, rewriting, and web search.
Agentic RAG puts a model in front of that menu, and lets it choose.
L-L-M rag's agents section is agentic RAG with a menu of two. Its README says: let the L-L-M decide how to retrieve. Search one author's book, or search all books.
Here's the first menu item, written by hand: a name, which the model will write back, and a description; with the parameter descriptions, the only documentation the model sees. Parameters come as a JSON schema.
The author must be one of 9 names in an enum. The search text's description even coaches the model: expand the search term to a sentence or two. And both fields are required.
Now the real function. Two more arguments, the collection and an embedding function, aren't in the schema: your code supplies them. The model controls only the author and the search text.
The lecture says a tool-using agent must pick the right tool, format its inputs, and interpret its outputs. Here the model picks and formats only by writing; your code runs the tool.
Here are the 11 books in the collection, beside the 9 names in the enum.
Two books. The cottage cheese recipe book, 178 chunks, has an author who isn't on the list. The Woman's Institute book, 1,505 chunks, has no author at all: a file name slip in lecture 5.
Both stay reachable by the search across all books. Now the stage: Gemini in Google's cloud, two containers on your laptop, and a boundary between.
The model never gets your database, only a menu. Call 1 returns an order: a function name and arguments. Your code runs it; call 2 sends back the result.

## 07:32 — Back in the container: the agent needs an index
Lecture 5 ended on one command; today we run it. Starting fresh? Clone L-L-M rag, and put the service account key in a secrets folder beside it; otherwise, go to your folder.
Step 1: cd L-L-M rag. Step 2: edit docker-shell.sh, and set GCP project to your own project ID; we used a placeholder. Pause, and do both.
Step 3: sh docker-shell.sh. Compose starts Chroma first. The pull message after it looks like an error but is harmless: there's no such image online, so Compose builds it.
After about 40 seconds of building, the banner prints. Python 3.12.15 and uv 0.13.1, at the time of recording. After the at sign comes the container's ID, new every run; pause, and get to this prompt.
An extra check from a second terminal: docker ps. Chroma publishes port 8000; remember that port for part 2.
Now the agents section, step 1: python cli.py, dash dash agent, chunk type char split. On a fresh clone it fails at once: the collection does not exist. That's line 429, before any call to Gemini.
The agent needs the index from lecture 5. Kept that database? It's in the docker volumes folder; if you chunked before September 22, pull and rebuild it. Otherwise, chunk, embed and load again.
We had no key, so the staff's committed embeddings stood in for the embed step.
Then the load step: python cli.py, dash dash load, chunk type char split. 11 books, 8,248 chunks; the instructor's story is just 24 of them. An extra get command confirms the collection answers; pause, and load yours.

## 09:36 — Call 1: the model writes the call
After the collection lookup, the agent function builds the user's turn: the question, with the role user. Then comes the first call to Gemini.
Three settings: temperature zero, the menu as tools, and a tool config with mode any. The lecture lists temperature as a design choice. Zero keeps the tool choice nearly repeatable.
An extra one-liner shows what mode any becomes: the enum value ANY. The model must answer with a function call.
In the lecture, a good agent may decide not to search at all; Self-RAG starts with that decision. Ours can't: on call 1, mode any forces a tool call. It chooses which search, never whether.
What does Gemini actually receive? An extra script runs the same code, but prints the request instead of sending it. One envelope: the question, both declarations with the enum, mode ANY, temperature zero.
And no system instruction: as in lecture 5, cli.py defines one and never sends it.
Now step 1 again, with the collection loaded. The lookup passes and the question prints, but the first model call needs your key: default credentials error, file not found.
Here's what the staff saw. The model's whole answer is a function call: get book by author, with the instructor as author, and the search text, cheese making importance location.
Four words, though the description asked for a sentence or two. There's also an ID, and a thought signature; we'll meet it again.
The SDK ran nothing; it only has declarations. So far, one paid call. Pause here, and run step 1 with your key.

## 11:21 — Call 2: your code ran it, the model answers
Back in your Python, a dispatcher matches each call's name, runs the real function with the model's arguments, and wraps the result as a function response.
Without a key, an extra script feeds the staff's recorded call through the tutorial's own dispatcher, against our collection.
One stand-in: without Google we can't embed the search text, so a stored chunk's vector stands in, and the 10 chunks may differ from a real query's.
Out come 10 passages from today's story, about Mara and Anja. Joined into one string of 3,509 characters, they're stapled to the call as its response.
Call 2 sends three things: the question, the model's own turn, unchanged, and your function responses. The tools go along again, but no tool config: the mode is back to automatic.
Inside, the model's turn carries its thought signature: Gemini's thinking models sign their turn, and want it back exactly as sent. Resending the turn unchanged keeps the seal.
The staff's answer? An Alpine valley, its caves, and transhumance, the seasonal movement of livestock. The two calls used 247 and 1,269 tokens.
So, who searched your database? Gemini wrote the call and chose the book; your Python ran it, on your laptop. That's two model calls and one embedding call per question, all paid.
But today's book never says transhumance, nor three other words from this run: the commit that added this output also rewrote the book. The staff's index was built from the old text.
Your run on today's book draws on passages like these: Mara, the curd, the wheels. An index answers from what was loaded.
One small slip: the README promises the response, but line 478 prints the whole response object. Print response dot text for just the answer.
Step 2 links to the course's hosted Cheese Agent Tool, up at the time of recording; try it in Chrome.

## 13:29 — From two calls to a loop
The lecture's agent runs until the task is done. L-L-M rag's agent ran one lap: a forced tool call, then an answer. The README calls it an agent; by the lecture's definition, it's the smallest piece of one.
Here's a question about that one lap.
It prints a response whose only part is a function call, with no text, and the program ends. Nothing runs that call; a loop would run it, and ask again.
The lecture draws the agent as a hub: the core and its instructions become a decision maker, with spokes to a planner, tools, and memory. Unroll the spoke to the tools into a loop.
What ends the loop? The stop rule: a reply with no function call is the final response. The model decides it's done by answering in plain text.
In code you see the loop from outside: the ADK Runner streams events, this wrapper keeps the final response, and the loop runs inside the library.
You also cap it, in case it never stops: 12 turns in the Cheese Quiz Guild, 16 iterations in the newsletter. Hitting the Agents SDK cap ends the run with an error.
The lecture's building blocks gray out dynamic control. You configure the model, instructions, tools and memory; the loop is the block a framework writes for you.
Before part 2, tear down. Type exit; an extra docker ps then shows Chroma still up, on port 8000. Then docker compose down: two harmless warnings, and it stops.
Your index stays on disk, and part 2 also needs port 8000. Pause and tear down. In part 2, a framework runs this loop for us.

## 15:24 — ADK: clone, configure, and a sync that fails
Part 2: frameworks own the loop. No Docker this time: Google's Agent Development Kit runs in a uv environment on your laptop. Open a new terminal where you keep your clones.
Step 1: clone; the README writes a placeholder for the address. The next line says cd google ADK tutorial, but no such folder exists.
A small slip: the folder is named after the repo. Type cd L-L-M agent google ADK instead.
An extra ls shows six numbered module folders, but no lock file: the repo ignores it, so everyone resolves fresh versions.
Next, copy dot env dot example to dot env. An extra grep shows a placeholder Google API key, and the model, Gemini 2.5 Flash.
Then create a key in Google AI Studio, and paste it into dot env, after Google API key equals.
Also change the model line. Choosing the LLM core is the lecture's first design decision, and here it's one line: a current model, like Gemini 3.1 Flash-Lite.
Google lists the code's fallback, Gemini 2.0 Flash, as shut down, and limits 2.5 Flash to earlier users. Keep everything in this root file: only the nearest dot env is loaded. Pause, and set up yours.
The project file wants Python 3.10 or newer and ADK 1.8 or newer, with no upper bound. It also lists Chroma and sentence transformers.
One more fact: this laptop has no Python at all.
Then install: uv sync. As in lecture 1, with no Python around, uv downloads the newest: CPython 3.15.0, at the time of recording.
It resolves 189 packages, then fails. O-N-N-X runtime, which Chroma pulls in, has wheels only up to Python 3.14.
So this step fails whenever uv picks 3.15: on a fresh laptop, or where uv already has 3.15, even beside an older Python. The fix, with an extra command: uv python pin 3.13.
Then uv sync again: CPython 3.13 this time, and it installs, ADK 2.12.0 included. PyTorch makes it big: about 1.6 gigabytes, plus about 3 gigabytes for CUDA on a Linux PC.
An extra check, uv run ADK dash dash version, says 2.12.0, at the time of recording. Pause, and get your sync to succeed.

## 18:19 — adk web and the folder names
Running agents, step 1, from the repository root: uv run ADK web. First, version 2.12 asks a question the README doesn't mention: may Google collect usage data?
The text says telemetry is off by default, but the capital Y means pressing enter answers yes. Answer as you like; change it later with uv run ADK telemetry disable.
Then the server starts, on port 8000. Step 2: open localhost 8000 in your browser; an extra curl shows the redirect to the dev UI.
The agent dropdown lists 7 entries, nested ones included. Pick 1 baseline, as its README says, and the page refuses: agent names must be valid Python identifiers.
Why? Each folder name becomes the app's name, and an identifier holds only letters, digits and underscores, never starting with a digit. The name 1 baseline breaks both rules.
An older version, 1.27.5, lists only the four folders. But picking one still fails, as an invalid app name. So a version pin doesn't help; we undid ours.
What works is renaming, which isn't in the README either. Stop the server with control C, then drop each leading number, and turn hyphens into underscores.
Start the web server again, and pick baseline. The log says it loaded the root dot env file, and found the root agent in baseline dot agent.
Two more slips: the quick start passes a file where a folder is expected, and the module READMEs drop the word web, so it only prints help.
And if L-L-M rag's Chroma still holds port 8000, they clash; the web server stopped: address already in use. Run docker compose down first, or add dash dash port 8080. Pause, and get the dev UI open on baseline.

## 20:22 — Runner, session, state: the shared whiteboard
Baseline holds three LLM agents, each with a model, an instruction, and an output key. In the lecture's blocks: the LLM core, the instructions, and no tools at all.
A sequential agent runs them in order: validator, planner, summarizer. An extra request shows the tree the UI loads, with the model from your root dot env; check yours.
Another extra request creates a session: an empty state, and no events yet. Think of the state as a shared whiteboard.
Once you add your key, the Runner does this. The validator's reply goes into the state, under its output key; before the planner runs, its instruction's placeholder is filled from that cell.
The summarizer reads the plan the same way. The agents never call each other: the session carries the data, in its state and its history of events. A parallel agent fills its cells at once.
The lecture's planner needs live systems; this pipeline has no tools, so its prices are the model's guesses. A later notebook gets prices from tools and sums from Python.
The ADK README calls this memory. The code calls it session state, and it lasts one session; the lecture's memory remembers you next time, which none of today's runs does.
Without a real key, a trip request gets an internal server error. The server log says why: API key not valid. The placeholder reached Google, and was refused.
With your key, look for three replies in order, and three new entries in the State tab; the session is a file in the agent's folder. Each request is three model calls: pause, and plan a trip.

## 22:11 — Tools you didn't write: MCP
The lecture sorts tools into three families. Data tools fetch, like our book searches; action tools change something, like finalizing a trip or sending email; orchestration tools hand work to another agent.
Now wire one agent to ten services, each with its own protocol. The lecture asks: do you see a problem?
Every tool becomes a custom integration. MCP, the Model Context Protocol, makes it one pattern: a host with clients, and an MCP server for each service.
The lecture's MCP box is a shared protocol, not a program you run. In code, each server is its own plug, and the tutorial has three.
Plug 1 is in the ADK module on MCP. Install Node.
The agent's toolset starts a filesystem server with npx, as a child process, talking over standard input and output.
An extra script asks that toolset for its tools, with no model involved. The server offers 14, including write and edit, and the filter lets three through. With your key, ask the agent to list files.
Plug 2 is back in the Cheese Quiz. After a first tool written as a plain function, the notebook connects to a remote MCP server by URL, passed as MCP servers, not tools.
Extra curl commands talk to that server. A browser's plain request gets 406: the server is up, but speaks MCP, not web pages. Then initialize, list tools, call: one tool, one cheese fact per call.
Plug 3 is optional: the notebook runs its own FastMCP server, in a thread, on port 8001. A small slip: the comment above says 8000, and so does an older saved output.
Notice who does the talking: your client process. MCP gives the model no network access; it still only writes calls. Pause, and run the MCP cells.

## 24:31 — Many agents: who plans the order?
In the lecture, deep research is a tree of agents: a lead agent, a planner, parallel web searchers, and a synthesis into a report. The tutorial builds trees like it: the Cheese Quiz Guild, and the newsletter.
The lecture's planner raises the question that sorts them: who plans the order? First answer: the code. The sequential agent is an assembly line, its order fixed in Python.
Second answer: the model. In the Guild, each specialist becomes a tool: a whole agent behind one function. An orchestrator decides which to call.
Its instructions say: follow the assembly line strictly, at most 2 review rounds. That's a rule in prose; no code enforces it, except a cap of 12 turns.
The staff's saved run logged three errors getting a response, and still produced a quiz; the log doesn't say which calls failed. Every hop adds cost, time, and a way to fail; pause, and run the Guild.
Third answer: Python, reading the model's label. In this custom agent, a classifier writes one word into the state, and plain if statements pick the handler.
The else branch: clarification. The comparison is exact; lowercase the label first, or ask for structured output. The exercises try both.
The lecture also lists handoffs among the orchestration tools. These tutorials use agents as tools; lecture 7 sketches handoffs.

## 26:15 — The harness: only a human says yes
The Travel Planner notebook rehearses the lecture's trip. Copy it, add your key, and install its pinned agents package. Paris shrinks to a mock catalog: 3 cities, 6 hotels, 5 search tools and a finalize tool, booking nothing.
In the staff's saved run, turn 1 asks which California city. Turn 2 runs five searches and offers options. In turn 3 the user picks, the model calls finalize, and the reply shows the exact plan and asks for a yes.
That's the gate. A finalize call from the model can only propose: if the plan isn't the approved one, the code stores it as pending, and returns needs confirmation.
Approval lives in a separate function, apply confirmation: only an explicit yes copies pending to approved.
Because apply confirmation runs on the human's message, before the agent starts. Inside turn 3, nothing is approved, so every retry gets the same stamp.
Turn 4: the human types yes. The stamp flips to approved, finalize runs, and Python builds the budget line by line: 2,690 of the 6,000 dollars. The notebook's own test checks Python's number.
What the user sees comes from checked state, not the model's prose. An itinerary that skipped the check raises an error, a hard guardrail; a dollar amount in the model's prose only prints a warning, a soft one.
The lecture puts success criteria in the instructions, and guardrails in the decision maker. This notebook keeps both in code the model can't talk its way past, on the action tool. Every turn is paid; pause, and run the four turns.

## 28:12 — The harness: success is a receipt
The last notebook writes a cheese newsletter per reader, with Microsoft's Agent Framework, pinned. In the users cell, put in yourself and a friend, and keep two entries. Email is preview only; nothing is sent.
The orchestrator gets three tools: a researcher with web search, an editor, and send email. At most 16 iterations, one tool call at a time.
In the staff's saved run, the first city took four editor calls; the code validates every draft and hands any errors back as the tool's result. Then send email saved the HTML. That run had four readers; today's list makes two.
Now the harness. When the orchestrator stops, Python ignores its words and checks two things: is there a receipt from send email, and is that file on disk? If not, the run fails; success is a receipt, not a claim.
Compare a rule that lives only in the prompt. The editor is told: no embedded URLs. The saved preview has one anyway, because no code checks for it; a note is not a check.
The lecture's Self-RAG and Corrective RAG grade their retrieval for the same reason: don't trust, check. Next lecture calls this outer layer the harness. Web search is billed per call; pause, and run the demo.

## 29:33 — Tear down, recap, and what's next
Tear down: control C stops the web server. An extra git status shows the renamed folders and your Python pin; dot env, the virtual environment and the lock file are ignored.
The sessions in the agent's dot ADK folder aren't ignored, so don't commit them, and delete the 1.6 gigabyte virtual environment when you're done.
In each notebook, disconnect and delete the runtime. Keep the service account key beside L-L-M rag, never inside, and delete or cap the other two keys when the course ends.
Here's the lecture's anatomy, filled with today's code. Gemini and OpenAI models as the core; prompts and output types as instructions; tools by hand, decorated, or over MCP; history and session state as memory.
Dynamic control is the framework's loop, or two calls by hand. The lecture's formula, LLM plus reasoning, instructions and tools, gains two pieces: a loop the framework runs, and checks that your own code enforces.
Test yourself. One: who runs the function, and what goes back in call 2? Two: what does mode any change, and why only on call 1?
Three: what ends an agent loop, what cap do frameworks add, and which block is that? Four: how does the summarizer get the plan without a message?
Five: what decides that a harness run succeeded, and why not the model's word? Answers and every command are in the exercises and the study guide. Next lecture: the harness itself.
