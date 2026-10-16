# L07 lecture slides — LLM: Agents II

Source: one deck, `L07a_llm_agents_ii_main` (**49 slides**), titled "Lecture 7A: LLM: Agents II"
(AC215/E115; Pavlos Protopapas and Shivas Jayaram). These are the instructor's lecture slides
(PDF), provided by the student for study; the PDFs are not in this repository; slide numbers are
PDF page numbers. Numbers in parentheses below are slide numbers. I wrote this digest from the
deck's extracted text and from all six contact sheets, and I enlarged slides 9, 10, 13, 16, 17,
21, 22, 23, 35, 36, 39, 41 and 42 to read their diagrams. Everything below is in my own words;
only short titles, terms, code and one-line quotes are quoted. The tutorial side of the lecture is
in [`digest.md`](digest.md).

Read this first:

- **Footer numbers.** The printed footers match the PDF page numbers except on slide 1 (no
  footer) and slide 2 (prints "8", left over from a longer deck). Always cite the PDF page number.
- **"7A".** The title slide says "Lecture 7A" and the file is `L07a`. No 7B deck was provided.
- **How the deck maps onto the tutorial (`dlops-io/agent-harness`).** The deck's seven outline
  sections (Recap, Context Engineering, Agent Harness, Skills, Agent Systems, Evaluation,
  Additional Resources) are the README's seven numbered sections, in the same order. The README
  opens by saying it "brings together the concepts from the lecture", and its first table maps each
  "Lecture concept" to an act. Slide 44 links the repo and the same Colab notebook the digest uses.
  The slides themselves are concept-only. They show no Formaggio shop, no Agent Framework code, no
  Docker and no CLI. Their running example is a different cheese story: a grilled-cheese
  recommendation (14–17) and a `cheese-pairing` skill (27).
- **Where the slides and the tutorial differ** (details under Terms):
  1. **"Layers" means two different things.** On 37 and 39 the layers are the five parts of an
     agent stack (LLM, Tool, Context, Agent Harness, Skills). In the tutorial a "layer" is a named,
     removable harness feature: `Trace()`, `Budget(...)`, `Context(...)`, `CartCheck()`, and so on
     (digest C2). A scene must say which one it means.
  2. **Where workflows live.** The slides place fixed workflow graphs on the autonomy spectrum,
     under Agent Systems (36). The README puts Act 3's ordering workflow under **Agent Harness**
     (§3).
  3. **Agent systems.** The slides teach two multi-agent patterns: a manager that calls agents as
     tools, and peers that hand tasks to each other (33). Act 6 has an outer agent that calls a
     *workflow* as a tool. That is closest to the manager pattern, or the "Hybrid Orchestrators"
     graph on 36. The tutorial has no peer-handoff example.
  4. **Skill scripts.** Slide 27's skill has a `scripts/` folder that the agent runs. The
     tutorial's skills have `references/` and `assets/` only, and its harness removes the SDK's
     `run_skill_script` tool (digest C6).
  5. **Evaluation.** Slide 41's "LLM as judge" has no counterpart in the tutorial. The tutorial
     uses deterministic property checks plus a five-point human review of the prose, and
     `context_evidence.py` says outright that it uses "no model judge". Slide 40's "Trajectory" is
     what the tutorial calls `process.*` checks, or "execution paths".
  6. **MCP** (29) does not appear anywhere in the tutorial.
  7. **Hidden reasoning.** Slide 21's Think and Reason steps happen inside the model. The README
     warns that its logs "describe visible execution, not hidden model reasoning".

## Outline

- 1 · title slide: "Lecture 7A: LLM: Agents II", AC215/E115, the two instructors, a Harvard crest
- 2 · "Logistics / Reminders": about 85% of students have groups; Milestone 1 is due that night
  (09/29, 10 PM); a group sheet link with a QR code
- 3 · "Outline": the seven sections, none highlighted
- Slides 4–10 · **Recap**
  - 4 · outline with "Recap" in bold
  - 5 · "Recap: Agents": only the question "What is an Agent?"
  - 6 · "Recap: Agent Definition": the one-sentence definition
  - 7 · "Recap: What is an Agent?": the agent block diagram (Task / Goal in, Task Completion out)
  - 8 · "Recap: Agent Building Blocks": the four blocks and their parts as a list, beside the same
    diagram
  - 9 · "Motivation": a plain LLM call next to an agent, whose input adds tool definitions
  - 10 · "Motivation": the agent loop, with Memory and Tools feeding back; "How do we manage what
    goes into the LLM?"
- Slides 11–18 · **Context Engineering**
  - 11 · outline with "Context Engineering" in bold
  - 12 · "What is Context Engineering?": the "invisible layer"; four bullets on what instructions do
  - 13 · a nested map of everything that sits in the context
  - 14 · worked example, part 1: the user's question plus four context panels (system prompt,
    current-conversation memory, RAG data, past-conversation memory)
  - 15 · worked example, part 2: tool-call outputs and the structured-output schema
  - 16 · assembly diagram: user prompt → a stack of six context blocks → LLM ("GPT") → response
  - 17 · worked example, part 3: the JSON answer
  - 18 · four definitions: context, prompt engineering, context engineering, and who does it
- Slides 19–24 · **Agent Harness**
  - 19 · outline with "Agent Harness" in bold
  - 20 · "What Is an Agent Harness": definition; the model cannot execute tools; examples
  - 21 · "One Turn": six steps, split between the LLM and the harness
  - 22 · "Action Boundary": who decides what, for five concerns, and when to shift the line
  - 23 · "Harness Engineering": the boundary moves both ways; authority stays with the harness
  - 24 · "Who does Harness Engineering?"
- Slides 25–29 · **Skills**
  - 25 · outline with "Skills" in bold
  - 26 · "Skills": definition and the two problems skills solve
  - 27 · "Anatomy of a Skill": the folder tree and `SKILL.md` of `cheese-pairing`
  - 28 · "Progressive Disclosure": three loading levels and their token cost
  - 29 · "Tools, MCP, & Skills": a comparison table
- Slides 30–37 · **Agent Systems**
  - 30 · outline with "Agent Systems" in bold
  - 31 · "Agent Systems": single vs multiple agent systems, one line each
  - 32 · "Single Agent Systems": four bullets
  - 33 · "Multi Agent Systems": the graph view and two orchestration patterns
  - 34 · "Review: Agent": slide 7's diagram again
  - 35 · "From Traditional to AI Agent Systems": a classic software component mapped onto an agent
  - 36 · "The Autonomy Spectrum": five orchestration graphs placed on a spectrum
  - 37 · "Agent Layers": table of five layers, what each controls and who owns it
- Slides 38–42 · **Evaluation**
  - 38 · outline with "Evaluation" in bold (this copy swaps sections 3 and 4; see the note below)
  - 39 · "From Model to Product": the layers we build between the model and the product
  - 40 · "What to Measure?": outcome, trajectory, cost; what each layer's changes break
  - 41 · "How to evaluate?": three ways to decide pass or fail
  - 42 · "Evaluation Process": a six-step improvement loop
- Slides 43–48 · **Additional Resources**
  - 43 · outline with "Additional Resources" in bold (same swapped order as 38)
  - 44 · "Tutorial: Agent Harness": Colab notebook and GitHub links
  - 45 · "GenAI Building Blocks (GCP)"
  - 46 · "GenAI Building Blocks (AWS)"
  - 47 · "GenAI Building Blocks (Azure)"
  - 48 · "GenAI Frameworks [TODO]": four columns of product names; the title still carries a TODO
- 49 · "THANK YOU", with a cartoon theatre-curtain image

**Outline order slip.** Slides 3, 4, 11, 19, 25 and 30 list Agent Harness third and Skills fourth.
Slides 38 and 43 list Skills third and Agent Harness fourth. The deck itself teaches the harness
first (20–24) and skills second (26–29), and so does the README. Follow the deck order.

## Key ideas

1. **An agent is an LLM, given instructions and tools, that runs on its own until the task is
   done.** It has four building blocks: the LLM core (the reasoning engine), instructions (system
   and user prompts, context, an output schema), tools (data, actions, flows) and memory (user
   sessions, preferences). "Dynamic control" ties them together. (6–8, 34)
2. **The difference between an LLM call and an agent is in the input.** A plain call sends prompts
   and a schema. An agent also sends tool definitions. Its answer may be a request to call tools,
   and the tool outputs and memory then flow back in, so the input grows with every turn. That
   raises the section's driving question: how do we manage what goes into the LLM? (9–10)
3. **Context engineering governs what the model sees, when it sees it, and how it uses it.** It is
   the "invisible layer" that feeds every part of the agent. Without it, even a strong reasoning
   model cannot plan, adapt or remember well. (12)
4. **Context is everything in one LLM call; prompt engineering is only part of it.** Context means
   instructions, user input, history, retrieved evidence, tool definitions and tool results.
   Prompt engineering covers the instructions and examples. Context engineering covers the whole
   lifecycle: what goes in, when, and how it is kept up across turns. The app developer does it,
   and every block the code includes is a decision. (18)
5. **The context has a fixed set of parts.** They are the system prompt, the user prompt, the
   structured-output schema, retrieved information (RAG) and the available tools, plus memory
   split into long-term and short-term. (13, 16)
6. **Each context block puts a different fact into the answer.** In the grilled-cheese example, the
   system prompt sets the persona and the criteria. RAG supplies melting temperatures, and the
   current conversation supplies "cooking for kids, basic stovetop". Past conversations supply
   "shops at Kroger, lactose-sensitive, budget under $6". The tools supply prices, stock and
   lactose figures, and the schema fixes the JSON shape. The final answer stitches these together.
   (14–17)
7. **A harness is the runtime around the model.** It is the loop, the tools, context management
   and the guardrails. The model only writes text or proposes an action. It cannot run a tool
   itself; the runtime does. Claude Code, Codex and Antigravity are all harnesses. (20)
8. **One turn is split between the model and the harness.** The LLM thinks, reasons and plans. The
   harness executes (tools, code, sub-agents), verifies the work (code checks, judges) and decides
   what the user is shown. (21)
9. **The action boundary decides who owns each choice.** For control flow, tools, context and
   memory, verification and sub-agents, the LLM makes the open-ended choices. The harness owns the
   fixed machinery: loop limits, tool registry and validation, compaction, deterministic gates,
   spawn limits. Give the model more room when goals are novel, the model is capable or exploring
   pays off. Give code more control when stakes are high, actions are irreversible, the task is
   predictable, or tokens and audit matter. (22)
10. **The boundary moves over time, in both directions.** Hand work to the model when it gets more
    capable, goals turn out varied, or the code is brittle. Take a decision back into code when it
    keeps repeating, its output is predictable, or cost, latency or audit matter. Through all of
    this, permissions, sandboxing, budgets and checks frame the system, and the harness keeps
    authority throughout. (23)
11. **Harness engineering is not only for platform teams.** The people behind Claude Code, Codex
    and the Agents SDK do it, but so does anyone who has written a loop that calls the model and
    dispatches its tool calls. (24)
12. **A skill is a folder of procedure that an agent finds and loads when needed.** It holds a
    `SKILL.md` plus optional references, templates and scripts. It closes two gaps: expertise
    (your process, style and rules) and context budget (it loads only when relevant). Domain
    experts can write skills, not only developers. (26)
13. **The description decides whether a skill is loaded.** `SKILL.md` starts with front matter (a
    `name` that must match the folder, and a description) followed by the steps. The agent sees
    only the description before choosing, so it is a hint to the model, not a guaranteed trigger.
    Reference files are read on demand; scripts are run, not read. (27)
14. **Progressive disclosure loads skills in three levels.** At startup the agent sees every
    skill's name and description (about 100 tokens each). When a task matches, it loads that
    skill's `SKILL.md` (keep it under about 5k tokens). It reads references and script results
    only as needed. The slide calls this "context engineering, automated", carried out by the
    harness. (28)
15. **Tools, MCP and skills answer different questions.** A tool is an action (the hands, written
    by a software engineer). MCP is connectivity: how capabilities and data are exposed to a
    client (the universal socket, built by a platform or integration engineer). A skill is
    know-how (the training manual, written by a domain expert). (29)
16. **One agent, or a graph of agents.** A single agent is one LLM
    with instructions and tools. It grows by adding tools, its complexity is controlled by the
    number of tools, and it stays easy to evaluate. A multi-agent system is a graph of agents. In
    the manager pattern, one agent calls specialised agents as tools, and the edges are tool calls.
    In the decentralised pattern ("Agent 2 Agent"), peers hand tasks to each other, and the edges
    are handoffs. (31–33)
17. **An agent replaces each part of a classic software component with an adaptive one.** Code
    instructions become an LLM core plus instructions, and rule-based control becomes dynamic
    control. Static decision trees become context-aware decisions, function calls become tool use,
    and predefined workflows become emergent ones. Monitoring becomes self-monitoring, functions
    become tools and state becomes memory. (35)
18. **Autonomy is a spectrum, not a switch.** It runs from predictable rule-based systems, through
    data-driven workflows, ML- and LLM-enhanced tasks, structured output and guided or bounded tool
    selection, to full agent autonomy. The graphs change along the way. First come fixed branches
    and loops, then fixed graphs with ML steps, then fixed graphs with agent nodes. At the far end,
    agents choose paths to a goal. (36)
19. **An agent stack has five layers with different owners.** The LLM decides what is generated
    from the context it gets (LLM provider). The tool layer sets what the agent can actually do
    (software engineer). The context layer sets what the model receives next (AI engineer). The
    agent harness sets how execution proceeds and what is permitted (platform or AI engineer). The
    skills layer sets which procedure is loaded (domain expert). In this class and in small teams,
    one person wears all of these hats. (37)
20. **Everything between the provider's model and the product is ours to change, so it must be
    tested.** Context, harness, tools and skills sit between the model and a product, which has
    users, tasks, policy rules, cost and latency. (39)
21. **Measure three things: outcome, trajectory and cost.** Outcome asks whether the result is
    right. Trajectory asks whether the agent got there sensibly. Cost counts tokens, turns and
    latency. Each layer fails in its own way. A swapped model drifts or changes format, which the
    outcome catches. A tool gets bad arguments or has side effects, which shows in the trajectory.
    A prompt edit fixes one case and breaks three (outcome). A harness loop runs long or skips a
    gate (trajectory, cost). A skill loads wrong or steps get skipped (trajectory). (40)
22. **Pass or fail can be decided by code, by an LLM judge or by a human.** Deterministic checks
    (tests, schema, state assertions) are cheap, rigid and auditable. An LLM judge (a rubric, k
    samples) is flexible but needs calibration. Human review is slow and costly but the gold
    standard, and it is also how you spot-check the judge. Lean as far toward deterministic checks
    as the task allows; the slide calls this the same rule as for the harness. (41)
23. **Improve by a disciplined loop, and keep the test cases.** Six steps: see a real failure;
    capture it as a test case (input, expected result, limits); change one layer only; run the
    suite k times for pass rate and variance; compare with the baseline as a diff, not just a green
    check; then merge or iterate, keeping the traces either way. The suite grows, and the eval set
    becomes the most valuable artifact. (42)
24. **Every major cloud offers the same six-layer GenAI stack.** The layers are UI, orchestration,
    prompts, data, models and infrastructure, and each cloud fills them with its own services
    (Vertex AI, Bedrock/SageMaker, Azure AI Foundry). Shared open pieces include Chroma and
    PostgreSQL. (45–47)

## Diagrams

Colour code used throughout the deck (useful to keep in a re-draw): instructions and prompts are
blue, tools orange, memory green, the LLM a white box with a black outline, and control red/pink.
On 22–23 the LLM is green and the harness purple. On 41 the colours flip meaning (see 41).

- **7 (repeated on 8 and 34) · the agent block.** A large rounded box (purple outline, lilac fill)
  titled "Agent", subtitle "Autonomous Execution". Inside it:
  - top row: "LLM Core" (subtitle "Reasoning Engine") and "Instructions" (subtitle "Prompts,
    Tasks, Guidelines, Goals");
  - middle: a wide red bar, "Dynamic Control";
  - bottom row: "Tools" (orange) and "Memory" (green);
  - footer, in italics: "Self-contained execution unit operating independently".

  Outside, a solid blue pill "Task / Goal" has an arrow into the box, and a dashed pill "Task
  Completion" has an arrow out. On 8 the same box sits beside a bullet list of each block's parts.
  Purpose: the agent as one self-running unit that turns a goal into a finished task.
- **9 · LLM call vs agent.** Two rows.
  - Top row: a dashed "User prompt" → two dotted blue chips, "prompts" and "schema" → a box "LLM" →
    a dashed "Response".
  - Bottom row: the same flow, but the chips and the LLM sit inside a lilac rounded box labelled
    "Agent", and a third chip, "tool defs", is added.

  Purpose: the visible difference is the tool definitions in the input. Re-draw it as one row
  morphing into the other, with "tool defs" sliding in.
- **10 · the agent loop.** The bottom row of 9, with the output now labelled "Response; tools to
  call". A grey line drops from the output and runs back left into an orange "Tools" box. From
  Tools, a dashed "tool outputs" box has an arrow up into the Agent box. A green "Memory" box below
  the Agent also has an arrow up into it. A red caption asks "How do we manage what goes into the
  LLM?" Purpose: the LLM's input now comes from three places (user, memory, tool results), and
  it grows every turn, which motivates context engineering.
- **13 · what sits in the context.** A large grey rounded box labelled "Context", with a tab "LLM
  Core" sitting on its top edge like a lid.
  - Inside is a blue box, "Instructions", holding dotted chips "System prompt", "User prompt" and
    "Structured output", and a solid white box in the middle, "Retrieved Information (RAG)".
  - Overlapping the bottom edge of Instructions are an orange "Available Tools" box and a green
    "Memory" box. Two dotted green chips branch off Memory: "Long-term memory" and "Short-term
    memory".
  - Thin connector lines run from the RAG box down to Available Tools and to Memory. My reading:
    retrieved information arrives through tools or from memory.

  Purpose: one map of every source that ends up in the context the LLM reads.
- **14–15 · the context, panel by panel (worked example).** Monospace text panels, arranged around
  a "User Input" box: "What's the best cheese for a grilled cheese sandwich?"
  - **Prompt Engineering** (14, top left): a system prompt that makes the model a culinary expert
    in cheese and comfort food. It must weigh melting, flavour, availability and technique, and be
    specific.
  - **Memory (Current Conversation)** (14, top right): cooking for kids, so mild flavours; a basic
    stovetop; the user asked about butter vs mayo; a tool `temperature_guide()` already returned
    melting temperatures.
  - **RAG (External Data)** (14, bottom left): melting points and flavours for American (150°F),
    Gruyère (170°F) and Cheddar (varies with age; sharp ones may separate), credited to a "Cheese
    Institute" guide.
  - **Memory (Past Conversation)** (14, bottom right): preferred mild cheddar in a mac-and-cheese
    chat two weeks ago, mentioned lactose sensitivity a month ago, usually shops at Kroger, and
    usually spends under $6.
  - **Tool Call Output** (15): three calls with results. A grocery API returns four Kroger cheeses
    with prices and stock ($3.49–$8.99). A nutrition checker returns lactose per slice. A melting
    simulator at 300°F compares American and mild cheddar.
  - **Structured Output** (15): an instruction to answer in JSON with four keys.

  Purpose: show that context is many separately sourced blocks, not one prompt. A re-draw can
  give each panel its own colour and keep those colours for 17.
- **16 · assembling the context.** A dotted "User prompt" chip on the left, with an arrow into a
  tall white column. The column stacks six dotted chips: "System prompt" (blue), "Long-term memory"
  and "Short-term memory" (green), "External Data" and "API Data" (orange), and "Structured
  output" (blue). An arrow leads from the column to a dashed box "LLM" with an OpenAI logo labelled
  "GPT", and another arrow to a dashed "Response". Purpose: before each call, the developer builds
  this stack. Colour marks the kind of source: instructions, memory or outside data.
- **17 · the answer.** A "User Input" box with the same question. A thick grey L-shaped arrow runs
  down and right into a large "Output" box holding the JSON answer (keys in red, values in blue).
  It recommends Kroger mild cheddar at $3.49 and lists two alternatives, two cooking tips (about
  300°F; mayo on the bread) and a "why" that cites shopping habits, budget and 0.2 g lactose.
  - Purpose: every phrase in the answer can be traced back to a block on 14–15. A strong scene
    draws lines from each phrase to its source panel.
  - My observation, not the slide's: two phrases go beyond the evidence. The answer calls American
    Singles "zero lactose", but the tool said 0.1 g per slice. It also says the kids "already loved"
    mild cheddar, but past memory only records that the user preferred it. This is the same lesson
    as the tutorial's garbled "1,5000¢" (digest C1): fluent prose is not evidence.
- **21 · one turn.** A header strip, "Think → Reason → Plan → Execute → Verify → Response", over two
  cards.
  - The left card, "LLM", holds Think (deliberation; "the grey streamed text in Claude Code"),
    Reason (hypotheses, alternatives, consistency) and Plan (which actions, in what order).
  - The right card, "Harness", holds Execute (dispatches tools, code, sub-agents), Verify (code
    checks, judges) and Response (assembles what the user sees: model output, visible reasoning,
    tool-call details, UI components).

  Purpose: the hand-off point in a turn sits between Plan and Execute. Re-draw it as one arrow of
  six steps with a vertical seam after Plan, coloured green (model) and purple (harness).
- **22 · the action boundary.** Three columns.
  - Headers: a green "LLM" box (probabilistic · adaptive · open-ended) on the left and a purple
    "Harness" box (code · deterministic · auditable) on the right, with a pink double-headed arrow
    between them labelled "who decides?".
  - Five rows. The middle column is a grey pill naming the concern, the left a green cell (the
    model's part) and the right a purple cell (the harness's part):
    - Control flow: the plan, the next step, when to stop | the loop itself, max turns, timeouts,
      stop conditions.
    - Tools: which tool, what arguments, how to react to an error | the tool registry, schemas,
      argument validation, execution, errors.
    - Context & memory: what to retrieve, which skill to load, what to remember | the system
      prompt, "instruction vs evidence lanes", the compaction trigger, what persists and where.
    - Verification: self-critique, revising from a checker's feedback | schema and fact checks,
      tests, deterministic gates.
    - Sub agents: when to delegate, how to brief, how to merge results | spawn limits, context
      isolation, concurrency, per-agent tool scopes.
  - At the bottom, a big green arrow points left ("Move LEFT" when goals are novel, the model is
    capable, speed to market matters, or exploring is worth the tokens). A big purple arrow points
    right ("Move RIGHT" when stakes are high, actions are irreversible, the task is predictable,
    tokens matter, or an audit is required).

  Purpose: a decision table, not a flow. Every row of the tutorial's harness has a cell here (see
  Terms).
- **23 · harness engineering.** A dashed purple frame encloses everything.
  - Top banner: "Set boundaries carefully — permissions · sandboxing · budgets · checks".
  - Below it, the green LLM box and the purple Harness box, with a pink double arrow "who chooses
    the next step?".
  - Two wide arrows. A green one points left: "Move to LLM ← What can the harness stop doing?",
    with reasons. A purple one points right: "Move to Harness → What can the model stop doing?",
    with reasons.
  - Bottom banner, on the frame: "The harness keeps authority at every point of the conversation".

  Purpose: the line between model and code slides both ways over time, but always inside the
  harness's frame. A re-draw can animate a divider sliding left and right inside a fixed border.
- **27 · anatomy of a skill (code figure).** A grey code panel. On top is a folder tree,
  `cheese-pairing/` with `SKILL.md`, `references/pairing_table.md` and `scripts/lookup.py`. Arrows
  annotate each: required front matter plus instructions; docs loaded on demand; code the agent
  RUNS. Below, the `SKILL.md` text: front matter with `name` and `description`, then three numbered
  steps (identify each cheese, run the lookup script, report one safe pairing, one adventurous
  pairing and one serving tip). A bullet under the panel gives the naming rule and says the
  description is a hint, not a trigger. Purpose: what a skill physically is.
- **28 · progressive disclosure (table).** Columns Level / What loads / When / Cost:
  1. Discover: every skill's name and description, at startup, about 100 tokens per skill.
  2. Activate: the chosen `SKILL.md`, when a task matches, under about 5k tokens recommended.
  3. Use resources: references and script results, as needed, costing only what is read or
     returned.

  A cheese emoji note adds that this is context engineering automated, run by the harness, "the two
  sections we saw, combined". Re-draw it as three widening rings, or a staircase of token cost.
- **29 · Tools vs MCP vs Skill (table).** Columns Tool / MCP / Skill; rows Question, Grants,
  Analogy, Authored by:
  - Tool: what operation can be requested? It grants an action ("the hands"; a software engineer).
  - MCP: how are capabilities and data exposed to a client? It grants connectivity ("the universal
    socket"; a platform or integration engineer).
  - Skill: what procedure should guide this task? It grants know-how ("the training manual"; a
    domain expert).

  A cheese emoji summary line closes the slide.
- **35 · traditional component → AI agent.** Two big lilac boxes, with a dotted pink arrow from the
  left one to the right one.
  - Left: "Traditional Component", "Deterministic Execution". It holds a blue "Code Instructions";
    a red panel "Rule-based Control" with six cells (Decision Making, Process Direction, Static
    Decision Trees, Function Call, Predefined Workflows, Monitoring); and at the bottom "Functions"
    (orange) and "State" (green).
  - Right: "AI Agent", "Autonomous Execution". It holds "LLM Core" and "Instructions"; a red panel
    "Dynamic Control" with six cells (Decision Making, Planning, Context Aware Decisions, Tool Use,
    Emergent Workflows, Self Monitoring); and at the bottom "Tools" and "Memory".

  The cells sit in matching positions, so each traditional part has a counterpart. Purpose: an
  agent is the same component skeleton with adaptive parts. A re-draw can morph each cell into its
  partner.
- **36 · the autonomy spectrum.** A "Traditional Component / Deterministic Execution" header box
  sits top left and an "AI Agent / Autonomous Execution" box top right. Five small flow graphs
  start from a dashed "event" box:
  - "Directed Graphs" (top left): the flow splits into "if" and "else" branches. One branch has a
    self-loop labelled "loop"; both reach a blue "end".
  - "Workflow Orchestrators" (bottom left): two parallel paths, one with a loop, merge into "end".
  - "Workflow Orchestrators (with ML)" (top middle): a fixed graph in which two nodes are green ML
    steps, "summarize" and "classify", ending in "end".
  - "Hybrid Orchestrators" (bottom middle): a fixed graph with three green "agent" nodes embedded
    in it, ending in a blue "goal".
  - "Autonomous Orchestrators" (top right): an "agent" node fans out along dotted green edges to
    several nodes and to a second "agent", reaching two "goal" boxes. The dotted edges are paths
    chosen at run time.

  Along the bottom, a pink double-headed arrow spans the slide, labelled left to right: "Rule-based
  Systems" / "Predictable", "Data Driven Workflows", "ML-Enhanced Tasks", "LLM-Enhanced Tasks",
  "Structured Output", "Guided / Bounded Tool Selection", "Full Agent Autonomy". Two details are
  worth keeping in a re-draw: green marks every node where a model decides, and the terminal
  changes from "end" to "goal" once agents appear. The tutorial's Act 3 graph is a workflow
  orchestrator with one model step (`ProposeCart`), and Act 6 is a hybrid.
- **37 · agent layers (table).** Columns Layer / Controls / Primary owner. Rows: LLM, Tool,
  Context, Agent Harness and Skills, with owners LLM provider, software engineer, AI engineer,
  platform/AI engineer and domain expert (see key idea 19). A cheese emoji note says you will wear
  all the hats.
- **39 · from model to product.** Left: a green box "LLM — the provider's". A hollow arrow leads to
  a dashed box, "Agent — the layers we build", which holds four grey tiles in a 2×2 grid: Context
  ("what it sees"), Harness ("loop and limits"), Tools ("what it can do") and Skills ("loaded on
  demand"). Another hollow arrow leads to a blue box "Product" (users · tasks, policy rules, cost ·
  latency). A red banner below asks how we test and evaluate changes to every layer. Purpose: it
  bridges into evaluation; the middle box is what we own.
- **40 · what to measure.** Three green pills across the top: "Outcome" (did it get the right
  result?), "Trajectory" (did it get there sensibly?) and "Cost" (tokens · turns · latency). Below
  them is a table, Layer / What a change here typically breaks / What catches it, with five rows
  (see key idea 21). Re-draw it as a 5 × 3 grid with the catching column lit.
- **41 · who decides pass/fail.** Three header boxes, left to right: a green "Deterministic checks"
  (tests · schema · state assertions), a grey "LLM as judge" (rubric · k samples) and a purple
  "Human review" (spot-check the judge). Under each is a grey pill: cheap · rigid · auditable;
  flexible · needs calibration; slow · costly · gold standard. A grey double-headed arrow below is
  labelled "who decides pass / fail?". A dashed box reads "Move as far left as the task allows —
  same rule as the harness".
  - **Warning for a re-draw:** the left/right direction is mirrored from 22. On 22 the
    deterministic side (the harness) is on the right in purple. Here deterministic checks are on
    the left in green.
  - The shared rule is "use deterministic code wherever the task allows". Put the deterministic
    side in the same place and colour in both scenes.
- **42 · the evaluation loop.** Six rounded boxes in two rows of three, with no arrows drawn:
  - top row: "1. Failure observed" (red: a real user or run broke), "2. Capture test case" (input ·
    expected · limits), "3. Change one layer" (prompt · tool · harness · skill);
  - bottom row: "4. Run the suite k times" (pass rate and variance), "5. Compare to baseline" (a
    diff, not a green check), "6. Merge or iterate" (green: traces kept either way).

  A dashed banner below says the suite grows and the eval set is the most valuable artifact.
  Re-draw it as a closed cycle (6 back to 1), with the test-case pile growing on each lap.
- **45–47 · GenAI building blocks per cloud.** Six horizontal coloured bands, top to bottom: UI UX
  (light blue), Orchestration (teal), Prompts (orange), Data (indigo), Models (pink) and
  Infrastructure (dark grey). Each band holds dark chips with that cloud's services. The UI,
  prompt-layer and open-source chips are the same on all three slides; the managed services
  change. Purpose: a reference stack, not a mechanism.
- **48 · GenAI frameworks.** Four bordered columns of product names: Data & Embeddings, Prompts,
  Orchestration and Low-code Orchestration. A reference list, not a mechanism. The title is marked
  "[TODO]".

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Agent" ("a system where an LLM, given instructions and tools, runs autonomously until a task is done") | 6 | README §1 concept: "instructions + model + tools"; the notebook's rule "the model proposes; the harness decides" (digest C1). |
| "LLM Core", "Reasoning Engine" | 7, 8, 13, 34, 35 | README says "model". The tutorial's model is OpenAI `gpt-5.6-luna` (digest §1); slide 16 also shows a GPT logo. |
| "Instructions" (Prompts, Tasks, Guidelines, Goals) | 7, 8, 12, 13 | Tutorial: `prompts/*.md`. On 12–13 "Instructions" is the umbrella for system prompt, user prompt, structured output and RAG. |
| "Dynamic Control", "Autonomous Execution" vs "Rule-based Control", "Deterministic Execution" | 7, 35, 36 | Not in the README. |
| "Agent Building Blocks": Tools as "Data", "Actions", "Orchestrations (flows)"; Memory as "User sessions", "User preferences" | 8 | Tutorial memory = "customer-scoped preference memory" (SQLite, Act 4) plus session history (digest C5). |
| "prompts", "schema", "tool defs", "tool outputs", "Response; tools to call" | 9, 10 | Not named in the README. |
| "Context Engineering"; "the invisible layer" | 12–18 | README §2 "Context Engineering — choose what the model sees"; concept "context is assembled, selected, and attributed". The tutorial's two modes, `basic` and `enriched`, are not on the slides. |
| "Context" (everything supplied to the LLM call) | 13, 18 | Same idea. The tutorial's context *packet* is labelled "Retrieved context (data, not instructions):" (digest C3). |
| "Prompt Engineering" | 14, 18 | Not a README term. |
| "Retrieved Information (RAG)", "External Data", "API Data" | 13, 14, 16 | The tutorial's "retrieval" is a pre-filtered catalog and saved preferences, not a vector search (digest C3). |
| "Long-term memory" / "Short-term memory"; "Memory (Current Conversation)" / "Memory (Past Conversation)" | 13, 14, 16 | Tutorial: customer memory DB (long-term) vs conversation history (short-term). It also keeps tasks, approvals and audit apart from both, plus a re-attached "capsule" (digest C5); the slides have no such split. |
| "Structured output" | 13, 15, 16 | Tutorial: structured final reply (`TastingReply`), `CartReport`. |
| "Agent Harness"; "runtime" | 19–24 | README §3 "Agent Harness — manage execution and enforce boundaries"; concept "the runtime supplies state, control, limits, and permissions around model calls". In code: the `Harness` class and the SDK's `create_harness_agent`. The slides' examples (Claude Code, Codex, Antigravity) are not in the tutorial. |
| "guardrails" | 20 | README does not use the word; it speaks of validation, approval and governance. |
| "One Turn": "Think", "Reason", "Plan", "Execute", "Verify", "Response" | 21 | Not in the README, which says its logs show "visible execution, not hidden model reasoning". |
| "Action Boundary"; "who decides?" | 22 | README reflection question 2 asks which "action boundaries" the runtime managed. |
| "max turns · timeouts · stop conditions" | 22 | Tutorial: `Budget(model_calls=8, tool_calls=20, seconds=120)`; without it, the SDK's 40-iteration fallback (digest C2). |
| "Tool registry · schemas · argument validation" | 22 | Tutorial: `ToolControl` admission and the always-on `ToolTrace` audit (digest C2). |
| "instruction vs evidence lanes" | 22 | Tutorial: retrieved context goes in as a *user* message labelled "data, not instructions" (digest C3). |
| "compaction trigger" | 22 | Tutorial: the `Compaction()` layer, with SDK thresholds at 50% and 80% of the budget (digest C5). |
| "deterministic gates" | 22 | Tutorial: `CartCheck`, `Store.validate`, the Act 3 workflow graph, approval fingerprints (digest C2, C4). |
| "Sub agents"; "Spawn limits · context isolation · concurrency · per-agent tool scopes" | 21, 22 | Tutorial Act 6: outer and inner proposer agents with separate call counters and one shared time budget (digest C7). |
| "Harness Engineering"; "Move LEFT/RIGHT"; "Move to LLM / Move to Harness"; "authority" | 22–24 | Not README terms. "Authority" matches the README's "authoritative result/outcome" in Act 6. |
| "Skills"; "SKILL.md"; "frontmatter"; `name`, `description` | 26–27 | README §4 "Skills — load reusable guidance when needed". Tutorial skills: `tasting-planning`, `vendor-outreach`, each with `name`/`description` front matter. |
| "references", "templates", "scripts" | 26, 27 | **Differs.** Tutorial folders are `references/` and `assets/` (the templates); there is no `scripts/`, and `run_skill_script` is stripped (digest C6). |
| "expertise gap", "context budget" | 26 | Not README terms. |
| "Progressive Disclosure": "Discover", "Activate", "Use resources" | 28 | README §4 concept: "progressive disclosure of reusable instructions and resources". Tutorial steps: metadata → `load_skill` → `read_skill_resource` (digest C6). |
| "MCP" ("the universal socket"); "connectivity" | 29 | **Not in the tutorial.** |
| "Single Agent System", "Multiple Agent System" | 31–33 | README §5 "Agent Systems — compose a harness and a workflow". |
| "Manager Orchestration Pattern (Agents as tools)"; "Decentralized Orchestration Pattern (Agent 2 Agent)"; "handoffs" | 33 | **Differs.** Act 6 calls a governed *workflow* as a tool (`start_order`), not an agent; no handoff pattern (digest C7). |
| "Directed Graphs", "Workflow Orchestrators", "Workflow Orchestrators (with ML)", "Hybrid Orchestrators", "Autonomous Orchestrators" | 36 | **Placement differs.** The tutorial's "controlled ordering workflow" / "workflow graph" (Act 3) is filed under Agent Harness in the README, not Agent Systems. |
| "Agent Layers": LLM, Tool, Context, Agent Harness, Skills; "Primary owner" | 37, 39 | **Name collision.** Tutorial "layers" = named, removable harness features such as `Trace()`, `Budget(...)`, `Context(...)`, `CartCheck()`, `Planning()`, `Memory()`, `Compaction()`, `Skills(...)` (digest C2, C5, C6). |
| "Outcome", "Trajectory", "Cost" | 40 | Tutorial checks are named `outcome.*` and `process.*` (e.g. `process.manager_authority`); README §6: "outcomes and execution paths". Trajectory = process. |
| "Deterministic checks", "LLM as judge", "Human review", "rubric", "k samples" | 41 | Tutorial: deterministic property checks over traces, and a five-point human review list for prose (README §6 step 4). **No LLM judge.** "k samples/times" = `--repeats N`. |
| "test case", "suite", "baseline", "eval set", "traces" | 42 | Tutorial: golden cases in `data/agent_evaluation_cases.json`, `--evaluate core`, `--repeats`, immutable `--label`, `--compare A B` (improved/regressed/unchanged, confounding changes), SQLite traces (digest C8). |
| "GenAI Building Blocks" (UI UX, Orchestration, Prompts, Data, Models, Infrastructure) | 45–47 | Not in the tutorial, which uses no cloud services (OpenAI only; digest §7). |

Slips on the slides, so a scene does not copy them:

- 2's footer reads 8.
- 38 and 43 swap sections 3 and 4 of the outline.
- 31's two lines have small grammar slips ("Consist of a single agent that execute flows").
- 48's title still says "[TODO]".
- 47 lists "AVM / AKS / ACI" as infrastructure. "AVM" is presumably Azure Virtual Machines, but
  the slide does not say so.
- 17's answer goes beyond its own evidence in two places (see Diagrams, 17).

## Commands and code on the slides

There are no shell commands, Docker, or tutorial code on the deck. The literal code-like items are:

- 14 · a tool already called in the conversation: `temperature_guide()`.
- 15 · tool calls:
  - `grocery_store_api("Kroger", "cheese", user_zipcode="29550")`
  - `nutrition_checker("lactose content", ["american", "cheddar"])`
  - `melting_simulator("grilled_cheese", temperature=300, cheeses=["american", "mild_cheddar"])`
- 15 · the structured-output schema keys: `"top_recommendation"`, `"alternatives"`,
  `"cooking_tips"`, `"why_this_works"`.
- 17 · the JSON answer, whose first value begins
  `"top_recommendation": "Kroger Brand Mild Cheddar ($3.49) - Perfect melting properties for stovetop cooking, …"`.
- 24 · the minimal harness: `while True: model(); dispatch()`.
- 27 · the skill folder tree: `cheese-pairing/`, `SKILL.md`, `references/pairing_table.md`,
  `scripts/lookup.py`.
- 27 · front matter: `name: cheese-pairing` and a `description:` that begins "Expert cheese pairing
  recommendations for wines, beers, and accompaniments."
- 27 · step 2 of the body: `Run scripts/lookup.py <cheese> for the house pairing.`
- 28 · costs: "~100 tokens / skill" (Discover), "< 5k tokens recommended" (Activate).
- 44 · links (see Pointers).

## What the lecture stresses

- **Without context engineering, even the best reasoning model cannot plan, adapt or remember
  well.** (12)
- **Every block of context is a choice the developer makes.** (18)
- **The model cannot execute a tool; the runtime does.** (20)
- **The harness, not the model, decides what the user sees.** (21)
- **Check the work before trusting it.** Verify is its own step, done with code checks or judges.
  (21)
- **Choose the model/code boundary per concern, using stated criteria.** Novelty, capability and
  speed push toward the model. High stakes, irreversibility, predictability, token cost and audit
  push toward code. (22)
- **Set boundaries carefully** (permissions, sandboxing, budgets, checks), **and keep authority in
  the harness at every point.** (23)
- **Revisit the boundary as models improve.** Move work to the model when code gets brittle, and
  move it back when a decision keeps repeating. (23)
- **You are a harness engineer as soon as you write the loop.** (24)
- **A skill's description is a hint, not a deterministic trigger**, and its `name` must match the
  folder. (27)
- **Keep skills cheap to carry**: about 100 tokens of metadata per skill, and a `SKILL.md` under
  about 5k tokens (the slide's authoring guidance). (28)
- **Don't confuse tools, MCP and skills**: hands, reach and guidance. (29)
- **Manage a single agent's complexity through the number of tools.** Single agents stay
  manageable to evaluate. (32)
- **One person wears all the hats** in this class and in small teams. (37)
- **Every layer you change needs testing.** (39)
- **Typical breakages:** a swapped model changes answers and formats; one prompt edit fixes one
  case and breaks three. (40)
- **Prefer deterministic evaluation wherever the task allows**, use LLM judges with calibration,
  and have humans spot-check the judge. (41)
- **Change one layer at a time, run k times, and compare with a baseline**: "a diff, not a green
  check". Keep traces whether you merge or not. (42)
- **The eval set is the most valuable artifact**, and it should grow with every observed failure.
  (42)

## Pointers

- **Course logistics (2).** About 85% of students have groups. Milestone 1 is due "tonight 09/29
  10 PM". Teams fill the group sheet (`https://bit.ly/ac215_2026_groups`, also as a QR code).
- **The tutorial (44).**
  - Colab notebook: `https://colab.research.google.com/drive/1ZYMsbG0gqsbs-6Pcj8WtT3WhEa4f80EZ?usp=sharing`
    (the same notebook the digest read, as `L07_agent_harness.ipynb`).
  - GitHub: `https://github.com/dlops-io/agent-harness`.
- **Quoted sources.** Two definitions are attributed to "Anthropic": the agent harness (20) and
  skills (26). The slides give no link.
- **Products named as examples.** Claude Code (20, 21, 24), Codex (20, 24), Antigravity (20), "the
  Agents SDK" (24).
- **Reference stacks.** GenAI building blocks for GCP, AWS and Azure (45–47) and a framework list
  (48). These are for orientation, with no links. Orchestration options named there include Google
  ADK, OpenAI SDK, LangChain and "Agent Framework" (47; the SDK family the tutorial uses).
- **Recap of the previous lecture.** Slides 5–8 and 34 recap Agents I (the series' L06).
- **Not on the slides.** There are no readings, papers, homework or demos beyond the tutorial
  links. The deck does not mention the README's Docker/CLI path, the Formaggio shop or its six
  acts. The pairing of each section with an act comes from the README's own table (see Read this
  first).

## This video and the slides

**Basis.** The video is not scripted yet. This folder holds only `digest.md` and this file: no `BRIEF.md`, `script.md`, `ASSETS.md` or `assets/terminal/`. The map below therefore uses the hook and the nine chapters planned in [`digest.md`](digest.md) §8, the study guide (`MLOps_Learning/guides/L07-agents-2-harness.md`) and every slide (the extracted text and all six contact sheets, re-read for this section). With no captures yet, "what the tutorial does today" means the repo at `e25dfe9` as verified in `digest.md`, plus the saved Colab outputs (cells 8–24). For this section I re-checked these points in a read-only copy of the repo at `e25dfe9`:
- the README's "Lecture concept" table (README.md:11-21) and its section headings;
- the two README sentences on hidden reasoning (README.md:198, 684) and the one on host-only memory (README.md:488);
- `context_evidence.py:1` ("no model judge") and the `run_skill_script` filter (`skill_support.py:55-62`);
- the two skill folders: `SKILL.md`, `references/`, `assets/`, and no `scripts/`;
- that Act 3's `CartProposer` has no tools and answers only in the `CartProposal` schema (`workflow_runtime.py:44-47`);
- the evaluation check names, all `outcome.*` or `process.*`.

When captures exist, re-check Conflicts 6 and 7 against them first. If a capture and this section disagree, the capture wins.

**Tag form.** `lecture_ref(7, "a–b")` (`explainer/devops.py`) prints "Lecture 7 · slides a–b". The deck's own title is "Lecture 7A"; no 7B deck was provided, so the bare "7" is unambiguous.

### 1. Map: planned chapters ↔ slides

| # | Planned chapter (`digest.md` §8) | Slides on the same ground | Relation |
|---|---|---|---|
| Hook | Two saved answers to one request; one says "1,5000¢" | 21 (Verify: check the work before trusting it) | Tutorial-only evidence. The lecture states the rule; the Colab run (cells 21, 23) supplies the broken thing. |
| 1 | The bare agent (2.5 min) | 5–10 (recap: definition, building blocks, LLM call vs agent, the loop), 20 (the runtime executes tools) | Same concept, and the tutorial applies it: Act 1's bare agent (Colab cell 21). The plan's token counter is slide 10's growing input, measured. |
| 2 | Wrapping the agent (3 min) | 20–24 (harness, one turn, action boundary, harness engineering) | Same concept, and the tutorial applies it: Budget, `@tool` schemas, ToolControl/ToolTrace and CartCheck fill harness cells of slide 22's rows "Control flow", "Tools" and "Verification". Immutable `.add`/`.without` and sticky admission are tutorial-only. "Layer" means something else on 37 and 39 (Conflict 1). |
| 3 | What the model sees (3 min) | 12–18 (context engineering), 22 (row "Context & memory": "instruction vs evidence lanes") | Same concept, and the tutorial applies it: basic vs enriched changes only the injected blocks. The three sieves and the PA/NY toggle are tutorial-only. "RAG" here is a Python filter (Conflict 8). |
| 4 | Rails, not suggestions (3 min) | 22 (rows "Control flow", "Verification"; "Move RIGHT"), 23, 36 (autonomy spectrum) | The tutorial applies the lecture's rule: control flow moves from the model into a fixed graph with one model node. The revise loop capped at 2 is tutorial-only. The README files this workflow elsewhere (Conflict 4). |
| 5 | Approve *this exact* cart (2.5 min) | 22 ("Move RIGHT": stakes high, irreversible, audit required), 23 (permissions · budgets · checks; authority) | The tutorial applies it. Pause/resume, the SHA-256 fingerprint, re-validation at checkout and the active-time clock are tutorial-only; the deck names no human-approval step. |
| 6 | Long tasks without amnesia (3 min) | 8, 13–14, 16 (long- and short-term memory), 22 (row "Context & memory": compaction trigger, what persists and where) | Same concept, refined: the five kinds of state and the re-attached capsule are tutorial-only. Who decides what to remember differs (Conflict 6). |
| 7 | Skills (2 min) | 25–29 (skills, anatomy, progressive disclosure, tools vs MCP vs skills) | Same concept, and the tutorial applies it. The SHA-256 snapshot and path checks are tutorial-only; MCP is lecture-only; skill scripts differ (Conflict 2). |
| 8 | Agent systems (2.5 min) | 30–36 (single vs multi agent, two patterns, autonomy spectrum), 22 (row "Sub agents") | Same concept, different shape: an agent calls a workflow, not another agent (Conflict 3). The two-orders race ("approval ≠ placement") is tutorial-only. |
| 9 | Evidence, not vibes (2.5 min) | 39–42 (model to product, what to measure, who decides pass/fail, the evaluation loop) | Same concept, and the tutorial applies it: golden cases, `--repeats`, immutable labels, `--compare` with confounding changes. No LLM judge (Conflict 5). |
| Recap | The plan's six recap questions | 22 (as a checklist), 40 | Could stand on lecture ground; the plan does not use it yet. |
| — | not in the plan | 1–4, 11, 19, 25, 30, 38, 43 (title, logistics, outline dividers); 34 (repeat of 7); 35 (traditional component → agent); 37 (five-layer stack and owners); 45–48 (GenAI building blocks per cloud, frameworks); 49 | Lecture-only. 37 is worth one beat in ch9 (gap 11). |

### 2. Already in common

| # | Concept | Chapter ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | An agent is a model with instructions and tools that runs until the task is done | ch1 ↔ 6–8 | Yes. README §1's "instructions + model + tools" is slide 8's building blocks minus memory, which arrives in ch6. |
| 2 | The model proposes; the runtime executes | ch1, ch2 ↔ 20 | Yes, exactly. Slide 20's "does not and cannot execute the tool function" is the lecture's form of the notebook's rule, "the model proposes; the harness decides". `preview_order` is that sentence in code. |
| 3 | Tool definitions go in, tool outputs come back, the input grows | ch1 ↔ 9–10 | Yes. The plan measures what slide 10 draws: 1 → 11 conversation messages and 1,942 → 4,540 input tokens over six model calls (Colab cell 23). |
| 4 | The harness is the loop, tools, context management and guardrails around the model | ch2 ↔ 20, 24 | Yes. The SDK's tool loop is slide 24's `while True: model(); dispatch()`, and the tutorial's `Harness` wraps it. The word "layer" clashes (Conflict 1). |
| 5 | Loop limits | ch2 ↔ 22 (row "Control flow": max turns, timeouts, stop conditions) | Yes. `Budget(model_calls=8, tool_calls=20, seconds=120)`, and the SDK's 40-iteration fallback without it. The tutorial is stricter than "max turns": it counts model calls and tool calls separately, and a breach is sticky. |
| 6 | A tool registry with schemas and validated arguments | ch1, ch2 ↔ 22 (row "Tools") | Yes. `@tool` builds the schema from the signature and docstring; `ToolControl` admits each call; `ToolTrace` audits it, fail-closed. |
| 7 | Verify before trusting | hook, ch2, ch4 ↔ 21 (Verify), 22 (row "Verification": deterministic gates) | Yes, sharpened: `CartCheck` reports and "never repairs", and the `validate` node sends feedback instead of fixing the cart. The lecture's Verify also allows judges; the tutorial uses code (Conflict 5). |
| 8 | Context engineering: your code chooses every block | ch3 ↔ 12, 18 | Yes. Act 2 runs slide 18's last bullet as an experiment: prompt, model, tools and message stay fixed, and only the injected blocks change. |
| 9 | Remembered preferences shape the answer | ch3, ch6 ↔ 14, 17 (past-conversation memory) | Yes. The lecture's "shops at Kroger, budget under $6" plays the role of the tutorial's saved "mild cheeses, nonalcoholic pairings" for `shivas`. The tutorial adds the test case `preference-override`, where today's request beats the saved preference. |
| 10 | Instructions and evidence travel in separate lanes | ch3, ch6 ↔ 22 ("instruction vs evidence lanes") | Yes, and the tutorial makes the phrase concrete three times: the context packet as a user-role message labelled "data, not instructions"; the capsule labelled "data, not new instructions"; and quarantined vendor text. Slide 16's single stack does not show the lanes; slide 22 names them. |
| 11 | High-stakes, irreversible actions move into code; the harness keeps authority | ch4, ch5 ↔ 22 ("Move RIGHT"), 23 | Yes. Act 3 is a "Move RIGHT" of control flow, and the approval gate is the "permissions" and "checks" of slide 23's banner. The tutorial goes further: an approval is bound to one exact cart, and checkout re-validates. |
| 12 | Long-term and short-term memory; compaction | ch6 ↔ 13, 16, 22 (compaction trigger; what persists and where) | Yes, refined. The customer memory DB is long-term and the history short-term; tasks, approvals and audit are kept apart from both. Compaction fires at the SDK's 50 % / 80 % thresholds, and the capsule is re-attached. Who chooses what to remember differs (Conflict 6). |
| 13 | Skills load progressively | ch7 ↔ 26–28 | Yes. Discover / Activate / Use resources = metadata at start → `load_skill` → `read_skill_resource`. Slide 28's "the harness executes it" is the `Skills(...)` layer. Scripts differ (Conflict 2). |
| 14 | A skill is know-how, not an action | ch7 ↔ 29 | Yes, exactly. Slide 29's "the hands" vs "the training manual" is the tutorial's misconception box: a tool acts, a skill advises, and reading `SKILL.md` cannot add an email recipient. |
| 15 | A manager agent calls others as tools, each within its own limits | ch8 ↔ 22 (row "Sub agents"), 33 | Partly. Separate call counters, three narrow tools (`start_order(request_id)` …) and one shared time budget are the slide's "spawn limits · per-agent tool scopes". But the callee is a workflow (Conflict 3). |
| 16 | Measure the outcome and the path | ch9 ↔ 40 | Yes. The tutorial's checks are named `outcome.*` and `process.*` (e.g. `process.check_before_action`, `process.manager_authority`). Cost shows up as model calls, tool calls and tokens in the Act 2 comparison table. The plan does not name the triad (gap 4). |
| 17 | Change one thing, run k times, compare with a baseline, keep the traces | ch9 ↔ 42 | Yes, strongly. `--repeats`, `--compare A B`, immutable labels and the SQLite traces are the six steps as commands. `--compare` even flags confounding changes, which enforces "change one layer" in code. |
| 18 | Prefer deterministic checks; humans are the gold standard | ch9 ↔ 41 | Yes. Property checks over traces, plus README §6's five-point human review of the prose. No LLM judge (Conflict 5). |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **The action boundary as the video's spine (22–23).** The plan walks act by act and never shows the one picture that ties the acts together. Slide 22 is that picture: five concerns, the model's part on the left, the harness's part on the right, and stated reasons to move the line. Every act fills harness cells:
   - control flow: Budget and admission (Act 1), the workflow graph (Act 3);
   - tools: `@tool` schemas, ToolControl, ToolTrace;
   - context & memory: the context packet, the capsule, compaction, host-written memory;
   - verification: CartCheck, the `validate` node, re-validation at checkout;
   - sub agents: Act 6's per-agent counters and narrow tools.

   README reflection question 2 already asks which "action boundaries" the runtime managed. **Carry it:** build the table in ch2, light one row per chapter in ch3–ch8, and fill it in as the recap.
2. **The autonomy spectrum (36).** It explains why Act 3 exists. Act 3 is a fixed graph whose one model node has no tools and returns only a `CartProposal`: near "LLM-Enhanced Tasks / Structured Output" on the slide's axis. Acts 1–2 and 4–5 are bounded tool selection. Act 6 mixes both, inside out: the agent is outside and the fixed graph is its tool. **Carry it:** ch4 (place Act 3) and ch8 (place Act 6).
3. **The whole context, built from the tutorial's real blocks (13, 16, 18).** The plan shows the enriched packet but not the whole call. Slide 16's stack can be rebuilt from what Acts 1–2 actually send:
   - system prompt: `prompts/shop_assistant.md` plus the policy JSON;
   - user prompt: the request as JSON;
   - structured output: `AgentReply`;
   - tool definitions: the five tools;
   - retrieved data: the enriched packet;
   - memory: saved preferences.

   Basic is the same stack without the last two. **Carry it:** ch3 opening, with slide 18's definitions as the chapter's last line.
4. **What to measure, and the improvement loop (40, 42).** Outcome, trajectory and cost; the table of what a change in each layer typically breaks; and the six-step cycle that ends with "the eval set is the most valuable artifact". The plan has the commands but not this frame. Slide 40's Context row ("prompt edit fixes one case, breaks three others") is exactly why README §6's live A/B compares per case. **Carry it:** ch9.
5. **One turn, split at the seam (21).** The model thinks, reasons and plans; the harness executes, verifies and assembles the response. In the Act 1 trace, "📤 Requested tools: get_catalog" is where Plan ends and "🔧 Tool call 1" is Execute. "The harness decides what to show the user" is Act 6's app-rendered `TastingReply` and every act's authoritative result block. **Carry it:** ch1 (the seam), ch2 (Verify = CartCheck), ch8 (Response). Mind Conflict 7.
6. **A skill's description is a hint, not a trigger; token costs (27–28).** This explains what the student will see. In `stock-question` no skill loads, and the `tasting-planning` description itself says it is "not simple stock lookups". Because a description is only a hint, the harness adds a code backstop: drafting is refused until `vendor-outreach/assets/email-template.html` has been read (`require_template`). That is a "Move RIGHT" inside the skills chapter. The token figures are about 100 per skill at discovery and under 5k for a `SKILL.md`. **Carry it:** ch7.
7. **Who decides pass or fail (41).** Code, an LLM judge or a human, with the rule "move as far left as the task allows — same rule as the harness". The tutorial picks code plus a human; saying why it skips the LLM judge closes the loop with ch2. **Carry it:** ch9, after gap 4.
8. **"How do we manage what goes into the LLM?" (9–10).** The plan's token counter motivates the answer, but the plan never asks the question. **Carry it:** the last line of ch1, as the bridge to ch3.
9. **Single vs multi agent, and the two patterns (31–33).** A single agent's complexity is managed by its number of tools (32): Act 6's outer assistant gets three narrow tools, not the shop's catalog tools. Manager (agents as tools; edges are tool calls) vs decentralized (peers; edges are handoffs). **Carry it:** ch8 opening.
10. **You are a harness engineer (24).** `while True: model(); dispatch()` never stops. The first thing every harness adds is a stop: Budget, or the SDK's 40-iteration fallback. **Carry it:** ch2 opening.
11. **Tools vs MCP vs skills (29), and the stack with its owners (37, 39).** MCP is not in the tutorial; one sentence saves a student from looking for it. Slide 39's banner (every layer is something we change, so how do we test it?) is the natural opening of ch9, and slide 37's "you will wear all hats" fits the same beat. **Carry it:** ch7 (29, one line) and ch9 (37, 39).

Lecture-only and of low value for this tutorial: slide 35 (traditional component → agent) and slides 45–48 (cloud GenAI stacks). The tutorial uses no cloud service. Slide 47 does list "Agent Framework" among the orchestrators, the SDK family the tutorial uses; one line at most.

### 4. Conflicts

| # | Slides say | Tutorial today (repo `e25dfe9`, saved Colab outputs; no captures yet) | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **"Layers"** (37, 39) are the five parts of an agent stack: LLM, Tool, Context, Agent Harness, Skills. On 39 the Harness is one tile beside Context, Tools and Skills. | A layer is a named, removable harness feature: `Trace()`, `Budget(...)`, `Context(...)`, `CartCheck()`, `Planning()`, `Memory()`, `Compaction()`, `Skills(...)` (`harness.py:62-68`; `acts/act4_harness.py:39-43`; `acts/act5_skills.py:27`). Context and skills sit *inside* the harness here. | Both, with different meanings | "The lecture's layers are the parts of the stack and who owns each. In the code, a layer is a feature you `.add()` to the harness. On screen, 'layer' means the code's sense; the lecture's we'll call the stack." Do not draw slide 39's 2×2 in a code chapter. |
| 2 | **Skill scripts** (26–28). A skill holds instructions, references, templates and scripts; 27's `scripts/lookup.py` is code "the agent RUNS"; level 3 loads "script results". | Both skills have `SKILL.md`, `references/` and `assets/` only. The harness strips the SDK's `run_skill_script` tool, which SDK 1.19 advertises even when no scripts exist (`skill_support.py:55-62`), and refuses reads outside the run's SHA-256 snapshot. | The repo (a deliberate choice) | "Skills can carry scripts, as the lecture shows. This harness takes that tool away on purpose: here a skill advises and never executes." Draw the lecture's tree beside `vendor-outreach/`, with `scripts/` greyed out. |
| 3 | **Multi-agent pattern** (33). A manager agent coordinates specialised agents through tool calls, or peers hand tasks to each other. | Act 6's outer assistant calls a governed *workflow* through `start_order(request_id)`; the workflow's one model node is the `CartProposer`. There is no peer handoff (README §5: "a harness invokes an ordering workflow"). | The repo | "This is the lecture's manager pattern with one change: the tool it calls is a whole workflow, with a model inside one of its nodes." Then place it on slide 36 (gap 2). |
| 4 | **Where workflow graphs are taught** (36). Fixed graphs and orchestrators belong to Agent Systems, on the autonomy spectrum. | The README's lecture table files Act 3 (the workflow) and Act 4 under "3. Agent Harness" (README.md:11-21), and "5. Agent Systems" is the harness calling that workflow. | Both: two filings of one graph | "The README files the workflow under the harness, because Python owns its edges. The lecture files it under agent systems, because it is a way to orchestrate. Same graph." One clause in ch4. |
| 5 | **Judges** (21: Verify uses "code checks, judges"; 41: "LLM as judge", rubric · k samples). | No model judge anywhere: `context_evidence.py:1` says "no model judge or guesses from response wording". Checks are deterministic properties over traces (`outcome.*`, `process.*`), plus README §6's five-point human review of the prose. "k samples" = `--repeats N`. | The repo, consistent with slide 41's own rule | "The lecture lists three judges. This tutorial uses two, code and you, and leaves out the LLM judge on purpose. That is the lecture's own rule: as far left as the task allows." |
| 6 | **Who decides what to remember** (22, row "Context & memory"). The model's cell includes "what is worth remembering"; the harness owns what persists and where. | The model has no memory-write tool. Only the host writes a preference, with `--remember-preference` (README.md:488). | The repo (the decision moved fully into the harness) | "The lecture lets the model suggest what's worth remembering. This harness moves even that to the right: only you, the host, write memory." A live example of slide 23's "Move to Harness". |
| 7 | **Visible reasoning** (21). Think is "the grey streamed text in Claude Code", and the harness's response can show "visible reasoning". | The traces record model inputs and outputs, requested tools and tokens. README.md:198 and 684 say the logs and recorded messages are visible execution, "not hidden model reasoning", and saved Colab cell 23 shows no reasoning text. | The repo and saved outputs | "Think and Reason happen inside the model. In this trace you see only where Plan ends: which tool it asked for." Re-check against the captures when they exist. |
| 8 | **"RAG"** (13: "Retrieved Information (RAG)"; 14: "RAG (External Data)"; 16: "External Data", "API Data"). | Act 2's retrieved context is a Python pre-filter over the 12-cheese catalog, plus one customer's saved preferences: no embeddings and no vector store, unlike L05. The packet is labelled "Retrieved context (data, not instructions):". | The repo | "The lecture's RAG box is any outside data you bring in. Here it's a Python filter, not the vector search from Lecture 5: retrieval just means choosing what to bring." |

Not counted as conflicts:
- Slides 38 and 43 swap Skills and Agent Harness in the outline. The deck and the README both teach the harness first.
- Slide 2's footer reads 8, and slide 48's title still says "[TODO]".
- Slide 41 puts deterministic checks on the left in green, while slide 22 puts the deterministic harness on the right in purple. That is slides against slides; see Proposals.
- Slide 20's "guardrails" are the README's validation, approval and governance: different words, same thing.
- The README's "7. Additional Resources" is a repository map and a reflection; the deck's is the tutorial links and the cloud stacks. Same title, different content, nothing to reconcile.
- Slide 44's Colab and GitHub links are the digest's sources.
- Slide 17's JSON answer overstates two facts relative to its own panels (Diagrams, 17). That is inside the lecture's example, not a disagreement with the tutorial.

### 5. Proposals for the BRIEF and script authors

**General**
- Tag every chapter that stands on lecture ground with a GREY `lecture_ref(7, "a–b")`, using the ranges below. Re-draw every lecture diagram in the series style. Never show slide images, the QR code or the closing cartoon.
- Make slide 22 the **running map** (gap 1): a table with MODEL and HARNESS columns and five rows. Build it in ch2 with the tutorial's mechanism in each harness cell, light the row each chapter is about, and fill it in for the recap. This is the strongest link between lecture and tutorial.
- **Colours.** The lecture's green model and purple harness collide with the series code (GREEN = project-owned and isolated; PURPLE = a tool you install). Proposal:
  - the model in BLUE: remote, "the provider's" on slide 39, and reached over HTTPS to OpenAI;
  - the harness in GREEN: code we own, deterministic, pinned;
  - a human decision in YELLOW (your turn at the prompt), a blocked or rejected step in RED, tokens in GOLD.
  - Keep the deterministic side on the right and GREEN in both ch2 and ch9, even though slide 41 mirrors it, so that "same rule as the harness" reads as the same place on screen.
- **Length.** The plan is about 24 minutes plus the hook, under the series' 25–35. Gaps 1–5 add roughly 4–6 minutes of lecture-backed content without padding.
- **The hook.** Keep the Colab "1,5000¢" as the broken thing, and land slide 21's Verify as the rule it breaks. Do not put slide 17's two over-reaching phrases on screen: pointing at them would read as correcting the instructor, and the tutorial's own saved output makes the same point.
- **Captures.** When they are made, record the Act 1 trace, `--act 5 --fixture --scenario stock-question`, a live `--act 5` (to see whether skills load) and one `--inspect-run`. Then re-check Conflicts 6 and 7 and gap 6.

**Per chapter**
- **Hook · no tag.** The evidence is the tutorial's own. As the Verify rule lands, the tag may show `lecture_ref(7, "21")`.
- **Ch1 · Lecture 7 · slides 6–10.**
  - One line of recap (6), and slide 7's agent block re-drawn small, with Memory dimmed: "memory comes back in chapter 6".
  - Slide 9 as one row morphing into the other: the "tool defs" chip slides in, showing Act 1's five tool names.
  - Slide 10's loop with the measured numbers (messages 1 → 11, input tokens 1,942 → 4,540). End on the lecture's own question, "How do we manage what goes into the LLM?" (gap 8), as the bridge to ch3.
  - Slide 20's sentence over `preview_order`: the model can ask, but it cannot act.
  - Mark slide 21's seam on the ping-pong: the model's "Requested tools" vs the harness's "Tool call" (gap 5; Conflict 7 for what the trace cannot show).
- **Ch2 · Lecture 7 · slides 20–24.**
  - Open with slide 24's one-liner: if you've written this loop, you're a harness engineer. Then ask what it lacks: a stop. Show Budget's 8 / 20 / 120 s and the 40-iteration fallback (gap 10).
  - Build slide 22's table (gap 1). Fill the rows "Control flow" (Budget, admission), "Tools" (`@tool` schema, ToolControl, ToolTrace) and "Verification" (CartCheck); leave the other rows dim.
  - Slide 21's Verify lands on CartCheck's ✅ next to the garbled prose, a callback to the hook.
  - Say "harness layer" for Trace, Budget, Context and CartCheck (Conflict 1).
- **Ch3 · Lecture 7 · slides 12–18.**
  - Rebuild slide 16's stack from the real blocks (gap 3); basic vs enriched is the last two chips toggling.
  - Then split the stack into slide 22's two lanes, the system lane and the user-role DATA lane, and light the row "Context & memory".
  - One clause on "RAG" (Conflict 8).
  - Close on slide 18's last bullet, in our words: every block your code adds is a decision. The plan's ponder question 1 follows.
- **Ch4 · Lecture 7 · slides 22–23, 36.**
  - Slide 22's "Move RIGHT" arrow with its reasons (stakes high, irreversible, predictable, audit required): the cart's route becomes a graph that Python owns.
  - Place Act 3 on slide 36's spectrum: a fixed graph with one model node that returns structured output (gap 2).
  - Row "Verification": the `validate` node gives feedback and never repairs.
  - One clause on where the README files it (Conflict 4).
- **Ch5 · Lecture 7 · slides 22–23.**
  - Slide 23's frame: the "set boundaries carefully" banner and "the harness keeps authority at every point of the conversation". The approval ticket is "permissions" and "checks" made concrete; the active-time stopwatch is "budgets".
  - Say that the fingerprint is the tutorial's own step beyond the slides. The lecture says to put approval in code; the tutorial says exactly what is approved.
- **Ch6 · Lecture 7 · slides 13–16, 22.**
  - Slide 13's two memory chips split into the tutorial's five drawers: tasks, history, memory, approval, audit.
  - Row "Context & memory": the compaction trigger is the 50 % / 80 % thresholds; "what persists and where" is `customer_memory.sqlite` vs history; the evidence lane is the capsule and the quarantined vendor text.
  - Conflict 6, told as a "Move to Harness" example (23).
- **Ch7 · Lecture 7 · slides 26–29.**
  - The lecture's `cheese-pairing/` tree beside `vendor-outreach/` (Conflict 2).
  - Slide 28 as a staircase of token cost, mapped to metadata → `load_skill` → `read_skill_resource`.
  - Gap 6: `stock-question` loads nothing, and `require_template` is the code backstop for a description that is only a hint.
  - Slide 29 in one beat: hands, socket, manual. MCP is not in this tutorial (gap 11).
- **Ch8 · Lecture 7 · slides 31–36.**
  - Slide 33's two patterns as two small graphs (gap 9). Act 6 is the manager with a workflow for a tool (Conflict 3). Place it on slide 36 with the agent outside and the fixed graph inside (gap 2).
  - Row "Sub agents": separate counters (16 outer model calls, 8 per proposer), three narrow tools, one shared 180 s clock.
  - Slide 21's Response: the app renders the `TastingReply` (gap 5).
- **Ch9 · Lecture 7 · slides 39–42.**
  - Open on slide 39's banner (every layer is something we change, so how do we test it?) and slide 37's "you will wear all hats" (gap 11).
  - Map slide 40's three pills: outcome → `outcome.*`; trajectory → `process.*` (e.g. `process.check_before_action`); cost → model calls, tool calls and tokens. Then slide 40's table: the README's live A/B is its Context row ("prompt edit fixes one case, breaks three others"), which is why `--compare` reports per case (gap 4).
  - Slide 41: three judges, two used (Conflict 5). Keep the deterministic side where ch2 put it (gap 7).
  - Slide 42 as a closed cycle, with a command on each step: a golden case → a one-file change (`prompts/shop_assistant_v2.md`) → `--repeats 2` → `--compare A B` (whose confounding flag enforces "change one layer") → an immutable label and the traces. End on "the eval set is the most valuable artifact".
- **Recap.** Keep the plan's six questions, and add two:
  - "For each act, which row of the lecture's action-boundary table did the harness take over, and what did it leave to the model?"
  - "Name the lecture's three things to measure, and one tutorial check for each."

**Terms**
- Use the lecture's words: *agent harness*, *runtime*, *action boundary*, *harness engineering*, *Move LEFT / Move RIGHT*, *authority*, *context engineering*, *instruction vs evidence lanes*, *compaction trigger*, *progressive disclosure* (*Discover / Activate / Use resources*), *expertise gap*, *context budget*, *MCP*, *manager pattern*, *handoff*, *autonomy spectrum*, *hybrid orchestrator*, *outcome / trajectory / cost*, *deterministic checks*, *LLM as judge*, *baseline*, *eval set*.
- Add the tutorial's words where the lecture stops: *harness layer*, *admission*, *sticky failure*, *context packet*, *capsule*, *quarantined*, *approval ticket*, *fingerprint*, *fixture*, *golden case*, *label*, *confounding change*, *authoritative result*.
- Qualify, don't repeat:
  - "layer": the code's sense on screen; the lecture's sense is "the stack";
  - "RAG": here a Python filter;
  - "judges": here code and you;
  - "the model decides what to remember": not in this harness.
