# AC215 · Lecture 7 — LLM: Agents II (follow-along: agent-harness)

## 00:00 — Which sentence would you trust?
A customer wants cheese for a tasting: 12 guests in Pennsylvania, a 150 dollar budget, no nuts, a French cheese, and one with a funk rating of 4 or more. Here are two answers from the same model and tools.
The first proposes 1,050 grams for 5,600 cents. The second, 1,200 grams for 6,400 cents, within a budget with the comma in the wrong place: a malformed number.
Which of these would you let charge a customer's card? And what would have to be true first?
The second run printed more. Code checked the cart itself: 1,200 grams, 64 dollars, shop rules satisfied, no order placed. The cart was valid; only the sentence was garbled. Nothing checked the first answer's final cart.
The course notebook says it in one line: the model proposes; the harness decides. The harness is the code around the model: the loop, its limits, its context and its checks. Today we sort every line of output into these two columns.
Lecture 7 and the README share seven sections, in order. The tutorial runs six acts in a fictional cheese shop, where nothing is really bought, shipped or emailed.
The tracker, top left, shows the README step; the gray tag, top right, shows the lecture slides. When a tag says your turn, pause and run the command.
One honest limit: we recorded this on October 20, 2026, without an OpenAI key. Everything offline ran for real; live commands ran until OpenAI refused the placeholder key. Live answers come from the staff's saved Colab run and the README.
The only cost is OpenAI tokens. Customer IDs are masked on screen, and every command is in the study guide.

## 02:00 — One container, no ports
Your laptop holds the clone, with an empty secrets folder beside it. One container mounts both, your key goes in as an environment variable, no port is published, and the app's only call out is HTTPS to OpenAI.
Two extras first: git clone, since the README assumes a copy, then change into the agent-harness folder, where every setup command runs. A listing shows no docs folder; that matters later.
Step 1 makes the secrets folder, one level up. Nothing reads it today, so no service account. Pause and run it.
Step 2 exports your key. Replace the placeholder with your own, or skip this line offline. We typed it as written; act 1 shows what that does.
Step 3, bash docker-shell.sh, builds the image and starts the container. Ours took 38 seconds, with the base image already on the machine; your first build also pulls it, so expect a minute or more.
The Dockerfile installs from the lockfile before it copies the code: the layer trick from lecture 2.
The banner says the environment is activated before the script activates it: a harmless slip. After the at sign comes the container ID.
From here on, every command runs inside the container. Pause, run steps 2 and 3, and wait for this prompt.
Three extras from a second terminal. Docker ps: no ports. Docker images: 1.77 gigabytes, since the framework installs every integration.
Docker inspect shows your key in the container's configuration; treat a real key as sensitive.
Step 4 is for a container already running when you changed the key: the script then only runs docker exec, which doesn't bring the new key.
If that's you, shell in from a second terminal and type the README's three lines: the key goes in hidden, and out of your history. Keep working in that shell. Pause here.

## 04:09 — Verify offline, and the Colab road
Now verify, offline, inside the container. Step 1 checks the SDK and prints the installed versions, at the time of recording: Python 3.13.16, agent framework 1.19.0, and every feature true.
Step 2 runs the tests: 281 of them, in about 100 seconds, ending in OK. They use scripted model responses, so they test the machinery, not the model.
Step 3 shows the logs: deliberate failures, like an injected audit outage, and an approval-identity warning we'll meet in act 4. Trust the last line.
The model check prints the default without calling it: GPT 5.6 Luna, at the time of recording. A model flag beats an environment variable, which beats this default; if your account can't use it, set either.
The README's notebook section has two more test commands. They run in the container too: 9 notebook tests and 12 chat view tests, both OK.
There's a second road: the course Colab. Save a copy to your Drive, add your key as a secret named OpenAI API key, allow notebook access, and run the setup cells.
The Colab setup installs the seven pinned packages, not the lockfile, so their dependencies can drift; for identical versions, use Docker.
Every recorded answer in this video comes from this notebook's saved run. Pause, and verify your setup either way.

## 05:47 — Act 1: an agent, measured
Act 1 starts from the lecture's recap: an agent is a model with instructions and tools, running until the task is done.
In code, the function build agent makes one framework agent: the shop instructions, five tools, and a structured reply format.
The model can only ask for a tool; the harness runs it. And none of these five can place an order: the preview order tool records an unvalidated proposal, with order placed set to false.
Step 1: python cli.py, dash dash act 1, dash dash scenario standard. You see the ask, call 1 and five tools; then the call fails with error 401: the placeholder key. Fix it in this shell with the three read lines from setup step 4. The failed run is still recorded.
Here's what a key gets you, from the staff's saved run. The model asks for the catalog; the harness runs it, and the result goes back in: two more messages.
Every round splits at the same seam. The model's plan ends at requested tools; the harness executes at tool call. The trace shows requests and results, not hidden reasoning.
Then stock, price, pairings and preview. On call 6 the model answers without asking for a tool, and the loop stops. Messages grew from 1 to 11, input from 1,942 to 4,540 tokens: about 21,000 billed input tokens, for one answer.
Step 2 adds dash dash show JSON, to see the exact message: a short note, plus the confirmed request as JSON, where null means not provided. Pause and run both, with your key.
The input grows with every call. That's the lecture's question: how do we manage what goes into the model?

## 07:42 — Act 1: wrap it in a harness
The lecture says it plainly: if you've written a loop that calls a model and runs its tool calls, you're a harness engineer. And a bare loop has no stop.
Step 3 is a notebook cell, for Colab or Jupyter, that wraps build agent in a harness. It adds Trace, Budget with 8 model calls, 20 tool calls and 120 seconds, basic Context, and Cart Check. The CLI builds exactly this.
The inner ring never comes off: call admission, the tool audit and the shop rules. Four harness layers slide on around it, one feature each.
Budget is a turnstile. Each model call is admitted and counted; a ninth fails with maximum of 8 model calls reached, and the lock stays shut.
Without Budget, only the framework's fallback is left: 40 loop iterations, no call limits, no overall time budget.
Cart Check is the lecture's verify step. Back to the hook: it checked the items, not the prose, so the garbled budget still passed. It reports, and never repairs.
Now the two columns become the lecture's action boundary: five concerns, the model's part on the left, the harness's on the right.
Act 1 fills three rows. Move right when stakes are high, or an action can't be undone.
Something to ponder. Take harness without trace, and run that copy. Is a tool call still counted and audited? And does the original harness still trace?
Yes, and yes. Admission and the audit are the inner ring. And the add and without methods never change a harness: each returns a new configuration, so the original keeps all four layers.
Step 4 runs the missing details scenario. With a key, look for a question back, not invented details; Cart Check should report no cart. Pause and run it.

## 09:50 — Act 2: same agent, different context
Act 2 changes what the model sees: the lecture's invisible layer. Here is one model call as the lecture's stack: system prompt and shop policies, the request, the reply format, five tools, and two slots, for retrieved data and saved preferences.
Basic mode, the one act 1 used, sends the first four and leaves the slots empty; enriched fills them.
Step 1, dash dash compare, uses the personalized scenario, where today's request leaves out the second customer's saved taste: mild cheeses and nonalcoholic pairings. The basic run starts and stops at the 401, so enriched never starts.
With a key, it prints a side-by-side table and a verdict, which may be a tie or a regression.
Steps 2 to 4 are optional single runs. Even without a key, there's a real difference: basic sends 1 conversation message, enriched sends 2; the extra one is the context packet.
Step 4, the override run, asks for funk 4 or more, and today's request must win over the saved taste.
The README says each act 2 command also prints a harness policy check. A small slip: dash dash compare doesn't. This extra call does: the same raw-milk cart fails for Pennsylvania and passes for New York, under a fictional rule.
Step 5 is an act 3 command the README puts here; part 2 explains it.
Step 6 repeats both cases in both modes, 3 times: 12 live runs. Without a key it stops after 3 errors, but the report still writes in step 7, and the label is used up: with your key, choose a new one.
The page linked here belongs in the docs folder we saw missing, so use the README checkpoints. Pause here if you have a key.

## 11:49 — Act 2: sieves and lanes
The README prints inspect the context first after the live runs. Without a key, start here: dash dash preview context, offline. Both modes share instructions, message and tools; only the packets differ.
Basic has no sources. Enriched has three, each with a trust label: the confirmed request, shop data, and saved preferences.
Twelve cheeses fall through three sieves: enough stock, no raw milk to Pennsylvania, no nut allergens. Munster has no stock, Brie and Comté fail the shipping rule, and two nut cheeses fail the allergy check. Seven survive.
The lecture's retrieved information is any outside data; here it's a Python filter, not the vector search from lecture 5.
And where does it go? Into a user message headed retrieved context, data, not instructions, so it cannot pose as a system rule. That's the lecture's two lanes: instructions in the system lane, evidence in the user lane.
Something to ponder. The enriched packet already removed Comté. Can the model still put Comté in its cart? And does anything in act 2 stop it?
Yes: the get catalog tool still returns all twelve, and in act 2 Cart Check only reports. Selection narrows, but validation decides: the act 3 workflow blocks it.
Step 9 is the optional baseline, in both modes. For standard, the saved preferences repeat the request, so little may change. Pause and run steps 8 and 9.
So selecting candidates helps, but validation decides, and today's request outranks saved preferences. In part 2, the harness takes the cart's route out of the model's hands.

## 13:51 — Act 3: rails, not suggestions
Part 2 picks up at the container prompt; if you closed it, rerun the setup and set your key. Remember the move-right arrow: when stakes are high, actions can't be undone, the task is predictable, or you need an audit, give control to code.
Act 3 does exactly that. The order route is a graph, and Python owns its edges. Confirm, propose, validate, and back to propose only if the report fails, at most twice; then pairings, manager review when required, revalidate and place. Only one node belongs to the model: propose cart, with no tools.
The README files this under the harness; on the lecture's autonomy spectrum, it sits near structured output: a fixed graph with one model step.
Step 1: act 3, scenario standard. With a key, the model proposes quantities; code does the rest: transitions, pricing, validation, placement. Success is a receipt.
Steps 2 and 3 are the shipping lesson, with a customer's own cart: Comté, Bûcheron and Époisses, to Pennsylvania. Before, the model only records the cart; the harness checks it and stops. After, the revise loop opens, and the live model may fix it.
As an extra, dash dash fixture runs the same path offline, with a script in the model's seat. Attempt 1 has raw-milk Comté, and the rail sends it back; attempt 2 swaps in Taleggio: valid, 50 dollars 10.
One trap: with fixtures, the blocked scenario proposes the same cart three times and ends unresolved, not blocked, so in Colab keep fixtures off for this lesson. Pause and run steps 1 to 3.

## 15:41 — Act 3: approve this exact cart
Step 4 is scripted, so approval is predictable: 60 guests in New York, a valid cart at 220 dollars 80, above the 200 dollar threshold.
The workflow pauses, and you are the manager: the host answers, never the agent. Type approve.
What did you approve? A fingerprint: the SHA-256 hash, taken over the request, the items, the subtotal, the policy and the product attributes. Stock is left out on purpose: it's rechecked, not approved.
At checkout the cart is validated and hashed again. The approval counts only if the decision is approve, and the ticket matches this checkout and this fingerprint. Change one line, and the hashes differ.
Your thinking time doesn't count against the budget.
And as an extra, type decline instead: the workflow ends, with no order.
Something to ponder. The manager approves. Before checkout runs, another order takes most of the Mimolette. What does checkout do, and why doesn't the approval protect this order?
Checkout revalidates, finds a stock violation, and blocks. Stock isn't in the fingerprint: an approval authorizes a decision; it doesn't reserve anything. Act 6 shows this for real.
Step 5: Munster has 0 grams, so attempt 1 fails. One bounded revision swaps in Époisses, and the order places at 50 dollars 10, with zero model calls.
Step 6 is the notebook cell. Its trace and budget layers can come off; validation, approval and revalidation are graph and checkout rules, so they stay.
So an approval binds this exact cart, and checkout revalidates after the pause. Pause and run steps 4 and 5; the cell is for Colab.

## 17:44 — Act 4: a planner with five drawers
Act 4 is a planner for a longer task: a 40-guest event in New York. The lecture splits memory into long-term and short-term; here that's saved memory and history, plus tasks, approvals and the audit: five kinds of state.
The README asks which of these can authorize an action. Only one: the approval drawer.
Step 1: act 4. Before any model call, the harness prints the first customer's saved memory. Then the planner's tools: assess the event, read the vendor document, draft and save a vendor email, and the to-do tools. No tool writes memory.
With a key, look for the brief: 1,000 grams each of Comté and Mimolette, and 1,200 of Époisses. The shop has only 900 grams of Époisses: 300 short. A finished task is not an approval, and shop stock is not vendor availability.
Saving the email has approval mode always require, so the framework pauses before the save runs. Act 3 paused a whole workflow; this pauses one tool.
The output after you approve comes from a scripted extra run. The review shows the vendor address and a body written by code, nut allergy included. Then: status saved, email transmitted no, and the file path.
Then comes the approval-identity warning you saw in the tests: the README predicts it, and it's harmless. Trust the authoritative block. Pause and run step 1.

## 19:19 — Act 4: compaction, the capsule and memory
Step 2 runs offline: a scripted planner with compaction, a malicious vendor document, and a test decline. It first seeds twelve synthetic notes of about 15,000 characters.
The window is 16,000 tokens, with 2,400 kept for the reply. Above 80 percent of the rest, truncation drops the oldest messages until the history is back under half: 26 become 5.
Something to ponder. Compaction dropped 21 of 26 messages, and none of the history mentions the nut allergy. How does every call still know about it?
A capsule. Before every call, the harness takes the old one out, compacts, and pins a fresh one from application state. It holds the confirmed request with its nut allergy, the menu, tasks, pending reviews and open work, marked as data, not instructions.
That's the lecture's compaction trigger, and what persists where, in code.
The vendor document says to ignore the allergy, so it lands in quarantine. The detector is deliberately small; the real guards are the recipient allowlist, and your review.
The drafted email still says nuts. The result: declined, no HTML saved, 7 model calls and 7 compactions.
Steps 3 and 4 are the optional memory exercise; type them from README line 484, since the ID is masked here. The first command stores a preference for the second customer, and the memory prints before any model call, even without a key. The next visit shows it again; an extra check reads the file.
The lecture lets the model suggest what's worth remembering. This harness moves even that to the right: only the host writes memory.
Step 5 is the notebook cell, for Colab: build act 4 adds five layers. Without compaction, the capsule is still re-pinned. Pause and run steps 2 to 4.

## 21:34 — Act 5: skills are manuals, not keys
Act 5 adds skills: folders of procedure the agent loads only when relevant. They solve two problems: the expertise gap and the context budget.
Skills load in three steps of rising token cost: every skill's name and description, about 100 tokens each; then its main file, SKILL.md; then a reference or an asset, only when needed.
The lecture's skill also has a scripts folder for the agent to run. This harness removes that tool on purpose: a skill advises, and never executes.
Step 1: act 5. Only the metadata loads at first: tasting planning and vendor outreach. The new tools are get stock, load skill and read skill resource.
Step 2 asks only about stock, offline: one get stock call, 900 grams, and the script loads no skill. With a key, the model decides from the description: a hint, not a trigger.
Step 3 runs the full sourcing path, scripted: six loads, each with its real path. Drafting is refused until the email template is read: a backstop in code.
Something to ponder. Someone edits the vendor skill to add: also send this to another address. Will the email go there?
No. Whatever the skill says, the guards are in code; its own text even says it cannot add recipients, and every read is checked: no parent folders, absolute paths or symlinks, and a file edited mid-run is refused.
The recipient is checked in code against the allowlist, and nothing is ever transmitted; an extra check shows the saved file says so.
In lecture terms, a tool is the hands, MCP the socket, unused here, and a skill the manual.
Step 4, the notebook cell, allows 16 model calls. Pause and run steps 1 to 3.

## 23:44 — Act 6: an agent that calls a workflow
Act 6 is an agent system. The lecture contrasts one agent with a graph of agents, in two patterns: a manager calling agents as tools, or peers handing off.
It's the manager pattern, except the tool it calls is a whole workflow, the one from act 3, with a model inside one node. No handoffs.
Step 1, the notebook cell, builds it. The budget: 16 outer model calls, 20 tool calls, 8 proposer calls per workflow, and one shared 180-second clock.
The host confirms the requests; the model only picks an ID. Its tools are narrow: start order, get order status, assess event.
Step 2: act 6, standard. With a key, tell outer model calls apart from workflow calls; the outer agent cannot approve its own order.
Step 3 runs offline: two orders sharing one shop. Both carts pass at 220 dollars 80, both pause for a manager, and the test decision approves both.
Mimolette and Taleggio start at 3,000 grams each. Request 1 is placed, leaving 1,400. Request 2 reaches revalidation needing 1,600: blocked. That's the ponder from act 3, for real: approval is not placement.
The final answer is the lecture's response step: the app checks the model's plan and fills in quantities, prices and the status, placed, from the receipt. The blocked order says invalid or unauthorized; the stock lines below give the reason.
On the autonomy spectrum it's a hybrid, inside out: the agent outside, the fixed graph as its tool. Pause and run steps 2 and 3.

## 25:33 — Evaluation: the trace is the evidence
Everything between the provider's model and the product is ours: context, harness, tools and skills. So all of it must be tested.
The lecture measures three things: outcome, trajectory and cost. Here they're the outcome and process checks, plus calls and tokens.
Evaluation step 1 lists the runs. Every run so far is in one SQLite database, including the failed live ones, with status error.
Dash dash inspect run takes a run ID: typed literally, it fails, because it's a template. Paste a real one; we use the manager approval run.
The events read in order: approval requested with the fingerprint, approval decided by a human, policy decision allow, order placed, run finished. The evidence for order placed is an event, not the prose.
As an extra, inspect the first failed run: model failed, with the 401. A failure is evidence too.
Evaluation step 2 starts offline: the act 2 evaluation, scripted, two repeats, labeled context fixture 1. All 4 runs pass, but scripted runs test the machinery, not the model.
Then read the report back, and export the HTML scorecard, to its default path or one you choose.
Open it from the outputs folder on your laptop.
The last command is a template for a database copied from Colab: typed literally, it fails. Labels are immutable: reuse one, and the batch stops. Pause and run evaluation steps 1 and 2.

## 27:16 — Evaluation: one change, k runs, a diff
Evaluation step 3 compares two configurations. The lecture warns that a prompt edit can fix one case and break three, so compare per case.
The lecture's improvement loop: see a failure, capture a test case, change one layer, run the suite k times, compare with the baseline, then merge or iterate.
Batch A runs enriched mode on two cases, twice: 4 live runs. Without a key: 0 of 4, with 3 errors and 1 missing. If one fails, fix the key and rerun both with new labels.
Copy the prompt file and edit the copy on your laptop: one deliberate change, keeping the confirmed constraint rules.
Our extra appends a line asking for a price and an action status; diff shows just that line.
Batch B runs the same cases and settings, with dash dash prompt file pointing at the copy.
Then compare, offline. Changed configuration: prompt. Confounding changes: none. Change code, data or the model, and it says so: the lecture's change-one-layer rule, checked in code.
Compare flags a run only when pass or fail flips; here every run errored both times.
As an extra, comparing two scripted batches reports all four runs unchanged, because fixtures ignore the prompt.
Evaluation step 4 asks what the checks establish. They check properties, like cart validity and approval order; the prose needs your review, with the README's five questions.
The lecture lists three judges: code, a model and a human. This tutorial uses two: code, and you. Lean toward code as far as the task allows, as in the harness.
Report one difference, its evidence, and one limit. And keep your cases: the eval set is the most valuable artifact. Pause and run evaluation step 3.

## 29:17 — Tear down, recap, and what's next
The repository map of section 7 ends with python cli.py, dash dash help: every option in one place.
Traces and live memory stay in SQLite. Inventory, orders, tickets and pending workflows last for one process; tasks and history, for one session.
Now tear down; these steps are extras. Type exit in each container shell; it was started with dash dash rm, so nothing is left in docker ps dash a.
The outputs folder stays on your laptop. Its trace database holds your prompts and outputs, keys redacted; delete it when you're done.
Docker image remove frees most of those 1.77 gigabytes; the base image stays. Then close the terminal that held your key, keep it out of files, commits and your shell history, and watch your usage. In Colab, delete the runtime. Pause, and tear down.
Here is the action boundary, filled in: budgets and the graph; schemas, the audit and approval on save; the packet, the capsule and host-written memory; Cart Check and revalidation; narrow tools and separate counters.
The model proposes, on the left. On the right, the harness decides, and where it matters, so do you.
The README ends with five reflection questions. Pick one run you did, and answer them.
Test yourself. What survives harness without trace? Why does retrieved context arrive as data? What is an approval bound to? Which state can authorize an action? And what does a passing fixture batch establish? Pause and try them; answers are in the exercises.
Next, lecture 8 fine-tunes models on Google's Agent Platform, formerly Vertex AI. Lecture 9 tests code with pytest; these 281 tests use unittest, and are a good model.
