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
