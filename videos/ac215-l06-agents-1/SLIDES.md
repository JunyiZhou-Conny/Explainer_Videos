# L06 lecture slides — Lecture 6: LLM: Agents I

Source: one deck, `L06_llm_agents_i` (56 slides), titled "Lecture 6: LLM: Agents I", by Pavlos
Protopapas and Shivas Jayaram (AC215/E115). This is the instructor's lecture slides (PDF), provided
by the student for study; the PDFs are not in this repository; slide numbers are PDF page numbers.
I wrote this digest from the deck's extracted text and all seven contact sheets. I also enlarged
slides 7, 10–14, 18, 28–33, 35–49 and 51–53 to read their diagrams and screenshots. Everything
below is in my own words. I quote only short terms, titles and single lines. The tutorial side of
the lecture is in [`digest.md`](digest.md) (cited below as "digest C2", "digest E12", and so on).

Read this first:

- **Slide numbers and footers agree.** Every slide except the title slide prints its PDF page
  number as its footer, so a slide number here is also what a viewer sees on the slide.
- **The outline slide comes back at each section**, with the current section in bold: slides 2
  (nothing bold), 3, 15, 19, 23, 50 and 54. Slide 19 is a **different, eight-item outline**. It
  inserts "Context Engineering", "Agent Systems" and "Additional Resources", and renumbers "Tools,
  MCP" as item 6. None of those three sections is in this deck; slide 23 returns to the six-item
  list. Context engineering and agent systems are the topics of L07 (Agents II), so slide 19 was
  probably carried over from a longer version of the deck. That is my inference; the slide does
  not say so.
- **The deck has no code.** It has no shell commands, no Python and no framework names (no ADK,
  OpenAI Agents SDK or Microsoft Agent Framework). It teaches with box diagrams and annotated
  screenshots of the Claude app. So these things are taught **only in the tutorials**: how
  function calling works (the model writes the call, your code runs it, digest C2), the agent
  loop and its stop rule (digest C3), framework runtime objects (digest C6), and harness guards
  such as approval gates and receipts (digest C8). The word "Harness" appears in the deck only
  as part of a notebook title (slide 55).
- **How the deck maps onto the tutorials** (the links are on slide 55):
  - Slides 4–5 (plain LLM) and 16–18 (Reasoning LLM) → the Cheese Quiz's "Base LLM" and
    "Reasoning LLM" sections (cells 18–25).
  - Slide 13 (Agentic RAG: an LLM chooses the retrieval technique) → `llm-rag --agent`, where
    Gemini chooses between "search one author's book" and "search all books" (digest C2).
  - Slides 20–22 (travel planner motivation) → the Travel Planner notebook and ADK's
    `1-baseline` travel pipeline.
  - Slides 25–41 (definition and anatomy) → the Cheese Quiz "Agent" section (cells 27–31); the
    Travel Planner notebook's cell 6 repeats the definition on slide 26 word for word.
  - Slides 44–49 (sub-agents) → the Cheese Quiz Guild, the Newsletter's sub-agents and ADK's
    `sub_agents` (digest C7).
  - Slides 51–53 (tools, MCP) → Cheese Quiz cells 45–59 and ADK `3-mcp-tools` (digest C5).
- **Where the slides and the tutorials disagree, or say it differently** (details under Terms):
  1. "Memory" is cross-session on the slides. The ADK README uses the word for per-session state
     (digest E12).
  2. The `llm-rag` "Cheese Expert Agent" is a fixed two-call pipeline. It does not "run until
     the task is done", which is the slide-26 definition (digest C3).
  3. The MCP picture shows one "MCP" junction box between the agent and every server. In the
     protocol and in the tutorial code, each server is a separate connection over a transport
     (stdio or HTTP). The slides do not mention transports.
  4. "Reasoning" means three things: a multi-call orchestration system (slides 16–18), the
     Cheese Quiz's hand-coded five-step chain, and Claude's "Effort" setting and thought panel
     (slides 31–33).
  5. The motivation trip is Paris, with weather and flight-delay replanning (slide 20). The
     Travel Planner notebook plans Seattle → California from a mock catalog, and has no weather
     or delay tool.

## Outline

- Slide 1 · title slide: "Lecture 6: LLM: Agents I", course tag AC215/E115, both instructors,
  Harvard shield
- Slide 2 · outline: Recap; Reasoning Models; Motivation; Agents; Tools, MCP; Tutorials (no
  item bold)
- Slides 3–14 · **Recap** (from a plain LLM to agentic RAG)
  - 3 · outline, "Recap" bold
  - 4 · "Recap: LLM": question → LLM → response
  - 5 · the same with "How is brie cheese made?" and a generic multi-step answer
  - 6 · "Recap: Naive RAG": question + retrieved context → LLM → response
  - 7 · "Recap: Naive RAG": the full retrieval loop (embedding model, vector DB, chunks) with a
    grounded but partial answer
  - 8 · "Recap: Naive RAG" compressed to four boxes: question → Retrieval → LLM → Response
  - 9 · "Recap: Advanced RAG": pre-retrieval and post-retrieval stages plus "Optimizations"
  - 10 · "Recap: Self RAG": a retrieval decision and a self-critique box
  - 11 · "Recap: Self RAG": the full decision flowchart (Retrieve? Relevant? Supported? Useful?)
  - 12 · "Recap: Corrective RAG": document evaluation, query rewrite, web-search fallback
  - 13 · "Recap: Agentic RAG": an LLM in front of a menu of seven RAG techniques
  - 14 · "Recap: Agentic RAG": the menu abstracted to Planning & Reasoning, Task Decomposition,
    Tool Use
- Slides 15–18 · **Reasoning Models**
  - 15 · outline, "Reasoning Models" bold
  - 16 · "Reasoning LLM": the reasoning engine as four stacked layers
  - 17 · the same four layers, each with a one-line purpose
  - 18 · a four-column catalogue of techniques per layer
- Slides 19–22 · **Motivation**
  - 19 · outline, "Motivation" bold (the eight-item variant, see above)
  - 20 · "Motivation: Travel Planner": the Paris prompt and three requirements
  - 21 · the same slide faded, with "Can RAGs or LLMs alone achieve this?" and two verdict boxes
  - 22 · what LLMs and RAG lack: interaction with the world, tools, autonomy
- Slides 23–49 · **Agents**
  - 23 · outline, "Agents" bold
  - 24 · divider: "What is an Agent?"
  - 25 · "Agent Definition": three industry definitions (OpenAI, Anthropic, Google)
  - 26 · "Agent Definition": the course's one-line definition
  - 27 · "What is an Agent?": the agent anatomy diagram
  - 28–33 · "Agent Example: Claude" (first example, a normal chat)
    - 28 · the query box and the model chip
    - 29 · the model's answer
    - 30 · the "+" menu: skills, connectors, plugins, research, web search
    - 31 · the model menu and the "Effort" levels
    - 32 · 30 and 31 combined; banner "Agent ≈ LLM + Reasoning + Instructions + Tools"
    - 33 · the answer with its "Thought process" panel; same banner
  - 34 · "What is an Agent?": the anatomy diagram again
  - 35–40 · "How an Agent works?", one component per slide
    - 35 · Step 1: LLM Core
    - 36 · Step 2: Instructions
    - 37 · Step 3: Decision Maker / Dynamic Control
    - 38 · Step 4: Planner / Dynamic Control
    - 39 · Step 5: Tools
    - 40 · Step 6: Memory
  - 41 · "Agent: Building Blocks": the configurable parts, as a list and a diagram
  - 42–49 · "Agent Example: Claude" (second example, Research mode with sub-agents)
    - 42 · the query with the Research and thinking toggles
    - 43 · the reasoning: research instructions say to launch a research task
    - 44 · the "Lead Researcher" card (a sub-agent)
    - 45 · the card expanded into two sub-agent steps
    - 46 · the research plan (planner sub-agent)
    - 47 · the gathered sources and findings (web search sub-agent)
    - 48 · the list of web search queries (tool use)
    - 49 · the final report; banner "Agent ≈ LLM + Reasoning + Tools + Deep Research"
- Slides 50–53 · **Tools, MCP**
  - 50 · outline, "Tools, MCP" bold
  - 51 · "Tools": definition and three tool families
  - 52 · "Tools": one agent wired to ten external systems; "Do you see a problem?"
  - 53 · "Model Context Protocol (MCP)": the same wiring through MCP
- Slides 54–55 · **Tutorials**
  - 54 · outline, "Tutorials" bold
  - 55 · "Tutorial: Agents": three Colab notebooks and two GitHub repos
- Slide 56 · closing "THANK YOU" with a cartoon stage-curtain picture

## Key ideas

1. **A plain LLM answers from what it learned in training.** The question goes in and an answer
   comes out, with nothing fetched. (4–5)
2. **Naive RAG adds retrieved context to the prompt.** The question is embedded, the vector DB
   returns matching chunks, and the chunks and the question go to the LLM together. The answer is
   tied to what was retrieved. On slide 7 it even admits that the retrieved text does not cover
   the whole process. (6–8)
3. **Advanced RAG optimises around retrieval.** It adds a stage before retrieval and a stage
   after it, both driven by "Optimizations". (9)
4. **Self RAG lets the model decide and check itself.** The model first decides whether to
   retrieve at all. Then it critiques its work on three questions: are the passages relevant, is
   the answer supported by them, is it useful? Without retrieval it answers directly and only the
   usefulness check applies. (10–11)
5. **Corrective RAG grades what was retrieved.** If the documents are poor, it rewrites the query
   and falls back to web search before generating. (12)
6. **Agentic RAG is the bridge to agents.** An LLM is placed in front of all those techniques and
   chooses which to use. Abstracted, that choosing is planning and reasoning, task decomposition,
   and tool use. (13–14)
7. **A "Reasoning LLM" is a reasoning engine built from several LLM calls in four layers.**
   Frameworks structure the thinking (chain of thought, problem decomposition, tree or graph of
   thought). Inference strategies generate and check candidate reasoning (parallel decoding,
   majority voting, rationale verification). Feedback loops iterate towards a stable, correct
   answer (self-consistency, self-refinement, verification). A response generator turns the
   result into a user-friendly answer (summary, formatting, confidence, fallbacks). (16–18)
8. **The motivating task needs more than text.** A five-day Paris trip means finding flights and
   hotels within budget, suggesting activities that fit your preferences, and replanning when
   the weather turns or a flight is delayed. An LLM can draft an itinerary but cannot make
   decisions as things change. RAG can only fetch and summarise information. (20–21)
9. **Three things are missing:** contact with live systems (weather, maps, booking), tools that
   call APIs to actually book, and the autonomy to decide and act alone. The lecture's goal is a
   system that can "interact, adapt, and act". (22)
10. **Definitions converge.** OpenAI, Anthropic and Google all describe a *system* that acts
    independently towards a goal and directs its own process and tool use. The course's own
    definition: an LLM, given instructions and tools, that runs autonomously until the task is
    done. (25–26)
11. **Anatomy of an agent.** A task or goal goes in and task completion comes out. Inside one
    self-contained unit sit an LLM core (the reasoning engine), instructions, dynamic control,
    tools and memory. (27, 34)
12. **You can see the parts in a real product.** In the Claude app, the model picker is the LLM.
    The effort level is the reasoning. Skills, connectors, research and web search are the
    instructions and tools. The slides sum this up as LLM + reasoning + instructions + tools.
    (28–33)
13. **The agent decides whether to use a tool.** On slide 33, with web search switched on, the
    model reasons that brie-making is stable, well-known knowledge and answers without searching.
    On slide 43, in Research mode, its instructions tell it to launch a research task for almost
    every query, so it does. The same question takes a different path under different
    instructions. (The slides show both screenshots; the contrast is my reading.) (30, 33, 43)
14. **Step 1, the LLM core,** sets the agent's cognitive ceiling. You choose the model (GPT,
    Claude, Gemini, …), its parameters (temperature, top-p, max tokens) and the response format.
    (35)
15. **Step 2, instructions,** are the prompt that shapes the core into a specialist. They define
    identity and role, guidelines and constraints, goals and success criteria, and output formats.
    (36)
16. **Step 3, the decision maker:** the LLM core plus the prompt "becomes" the decision maker. It
    weighs user intent, the tools and resources available, constraints and guardrails, and
    context from memory. (37)
17. **Step 4, the planner,** works out *how* to reach the goal. It breaks the task into steps,
    orders them, finds dependencies and anticipates obstacles. Because the plan is generated, the
    agent can take paths that the instructions never spelled out ("emergent workflows"). (38)
18. **Step 5, tools,** connect the agent to the outside world and turn a conversational system
    into an action-oriented one. They work through function calling (APIs, databases,
    calculations, code execution). The agent must pick the right tool for each step, format the
    inputs and interpret the outputs. (39)
19. **Step 6, memory,** gives persistence: session history, user preferences, learned strategies.
    It provides continuity and personalisation across sessions and lets the agent monitor itself
    over time. (40)
20. **The building blocks you configure are four:** the LLM core; instructions (system and user
    prompts, context, output schema); tools (data, actions, orchestrations/flows); memory (user
    sessions, user preferences). On slide 41's diagram, dynamic control is greyed out and missing
    from the list. It is not a part you build: it emerges from the core plus the prompt, as slide
    37 says. (41, 37)
21. **Deep research is a multi-agent system.** A lead researcher agent reasons about the query and
    first creates a plan (a planner sub-agent decides this is a "depth-first" query that needs
    about 3–4 parallel sub-agents). Then web-search sub-agents run many searches (255 sources in
    the example), and the results are synthesised into a cited report. The slide's summary: LLM +
    reasoning + tools + deep research. (42–49)
22. **Tools are functions with defined schemas that the agent calls on its own.** There are three
    families: data tools (search, APIs), action tools (execute, modify) and orchestration tools
    (handoffs, delegation to other agents). (51)
23. **Without a standard, every tool is a custom integration.** Email speaks SMTP/IMAP, calendars
    CalDAV, databases SQL, and Drive, Maps, Slack and WhatsApp each have their own API. So each
    tool is wired separately, and swapping one is a lot of work. (52)
24. **MCP is one standard protocol between agents and tools.** The agent becomes an MCP host with
    MCP clients. Each external system is wrapped by an MCP server. That gives one integration
    pattern for every tool, easy swapping and no custom adapters. (53)

## Diagrams

The Recap slides (4–14) share one visual grammar, useful for a re-draw:

* the user's question is a rounded, blue-outlined pill with a speech-bubble icon, on the left;
* the LLM is a small dashed square labelled "LLM", with an OpenAI-style logo and "GPT" inside;
* every other stage is a small dashed rectangle;
* light-grey arrows run left to right, and the response box is on the far right.

Diagram by diagram:

- **4–5 · Recap: LLM.** Three items on one line: the question pill → the LLM square → a dashed
  "Response" box. Slide 5 puts the brie question in the pill and a large dashed "Answer" box on
  the right, holding a generic step-by-step recipe. Purpose: the baseline. One call, no outside
  information.
- **6 · Naive RAG, concept.** Question pill → two stacked dashed boxes joined by a "+" ("User
  question" over "Retrieve Relevant Context") → LLM → "Response using the relevant context".
  Purpose: RAG = question plus retrieved context.
- **7 · Naive RAG, mechanism.** A counter-clockwise loop:
  1. the question pill (top left), with an arrow down to a dashed "Embedding Model" box;
  2. an arrow down to a short multicoloured strip (the query vector);
  3. an arrow right to "Vector DB" (a database-cylinder icon in a dashed box);
  4. an arrow right to four small document icons, then a "+" and a dashed box repeating the
     question;
  5. an arrow up to the LLM (top right);
  6. an arrow left to a dashed "Answer" box (top centre);
  7. an arrow left back to the user.

  The answer is grounded but incomplete: it says the provided text does not describe the full
  process, then gives size and weight facts from the retrieved passages. Purpose: retrieval
  limits the answer to what came back. Slide 5's fuller but unsourced answer is the contrast
  (my reading).
- **8 · Naive RAG, compressed.** Four boxes in a row: question → "Retrieval" → LLM → "Response".
  This strip is the template that slides 9–14 modify. A scene can keep the strip fixed and insert
  or replace the middle boxes.
- **9 · Advanced RAG.** The strip becomes question → "Pre-Retrieval" → "Retrieval" →
  "Post-Retrieval" → LLM → "Response". A wide dashed "Optimizations" box sits under the three
  retrieval stages and sends one up-arrow into each. Purpose: retrieval itself is tuned before
  and after the search.
- **10 · Self RAG, overview.** Question → "Retrieval Decision" → "Retrieval" → LLM → "Response".
  Under the first two stages, a dashed box "Self-Reflection & Critique" with the three
  criteria in brackets ("Relevant | Supported | Useful") sends up-arrows into both. Purpose: the
  model's own judgement steers retrieval.
- **11 · Self RAG, flowchart.** Grey solid boxes are LLM calls, dashed boxes are outputs and
  diamonds are decisions. Only the "Yes" branches are labelled; the "No" outcomes of Relevant,
  Supported and Useful are not drawn.
  - Start: the question pill (top left) → LLM → the diamond "Retrieve".
  - "No" path (right): LLM → "Response" → up to an LLM call → diamond "Useful" → "Yes" → LLM →
    "Final Response" (top right).
  - "Yes" path (down): "Retrieval" → LLM → diamond "Relevant" → "Yes" → LLM → "Response" → up
    to an LLM call → diamond "Supported" → "Yes" → left into the same LLM call that feeds
    "Useful".

  Purpose: three checks in order (relevance of the passages, support for the answer, usefulness
  to the user), each made by an LLM call.
- **12 · Corrective RAG.** Main line: question → "Retrieval" → "Document Eval" → LLM →
  "Response". A side path drops from "Document Eval" to "Query Rewrite", runs diagonally to "Web
  Search", and rises into the LLM. The branches are not labelled. Purpose: if the retrieved
  documents fail evaluation, rewrite the query and search the web instead.
- **13 · Agentic RAG, the menu.** Question → LLM → a vertical column of seven separate dashed
  boxes → a second LLM → "Response". The boxes, top to bottom: Retrieval Decision, Pre-Retrieval,
  Retrieval, Query Rewrite, Post-Retrieval, Document Eval, Web Search. One arrow enters the column
  and one leaves it. Purpose: the techniques of slides 9–12 become options that the first LLM
  chooses among. A re-draw can animate the earlier boxes flying into the column.
- **14 · Agentic RAG, abstracted.** The same frame. The column is replaced by one dashed
  container with three coloured bars: green "Planning & Reasoning", blue "Task Decomposition" and
  pink "Tool Use". Purpose: name the capabilities that the Agents section builds on.
- **16–17 · Reasoning engine.** A large dashed container titled "Reasoning Engine", subtitled
  "Multi-LLM Orchestration System". Inside are four stacked colour bars, each with an emoji
  icon: blue "Frameworks" (brain), purple "Inference Strategies" (light bulb), orange "Feedback &
  Iteration Loops" (loop arrows) and green "Response Generator" (speech bubble). On slide 16 the
  question pill feeds the container and a "Response" box leaves it. Slide 17 drops the question
  and response, and puts a one-line purpose box beside each bar. The bars have **no arrows
  between them**: it is a layered stack, not a pipeline. Purpose: reasoning as a system of many
  LLM calls.
- **18 · Technique catalogue.** Four columns, coloured like the bars on 16, each a list of small
  dashed pills:
  - Frameworks: CoT, problem decomposition, ToT, GoT, self-refinement;
  - Inference Strategies: parallel decoding, sequential processing, majority voting/ensembles,
    rationale verification, backward chaining, iterative prompting;
  - Feedback & Iteration Loops: self-consistency, decomposition, self-refinement and
    verification loops, dynamic scaling, bootstrapping loop;
  - Response Generator: summary generation, answer formatting, UI adaptation, confidence
    scoring, multi-modal output, error detection & fallback.

  Purpose: a map, not a mechanism. The Cheese Quiz's "Reasoning LLM" uses one path through it:
  decomposition → sequential sub-answers → verification → summary.
- **20–21 · Travel planner (callout layout, a natural hook).** Slide 20: the user's prompt in a
  green box; three numbered requirements with colour-coded keywords (blue for things to find or
  react to: flights, hotels, the Louvre, weather, flight delay; green for the user's constraints:
  budget, preferences, adjusting plans); a blue goal box at the bottom (a seamless,
  taken-care-of trip). Slide 21 fades all of this. A red banner asks whether RAG or an LLM alone
  can do it, and two green verdict boxes answer: LLMs can draft but cannot decide dynamically;
  RAGs can only retrieve and summarise. Purpose: show the gap before defining agents.
- **27 / 34 · What is an Agent? (the anatomy diagram).**
  - Layout: a filled blue button "Task / Goal" on the left → a large rounded box with a purple
    outline and a light-purple fill → a dashed light-blue box "Task Completion" on the right.
  - The big box's header reads "Agent", subtitle "Autonomous Execution". Its footer, in italics:
    a self-contained execution unit operating independently.
  - Inside, top row: "LLM Core" (subtitle "Reasoning Engine", white with a black outline) and
    "Instructions" (subtitle "Prompts, Tasks, Guidelines, Goals", blue).
  - Middle: a full-width red bar, "Dynamic Control".
  - Bottom row: "Tools" (orange) and "Memory" (green).
  - There are no arrows inside the box: the slide shows the parts, and slides 35–40 show how
    they connect.

  Purpose: the master picture. Slides 35–40 and 41 reuse its colours.
- **28–33 · Claude, first example (annotated screenshots).** Dark-theme screenshots of the
  Claude app, with coloured tag call-outs:
  - "User Query" (blue) on the message box ("How is brie cheese made?");
  - "LLM" (orange) on the model chip;
  - "Instructions & Tools" (red) on the "+" menu (Skills, Add connector, Add plugins, Research,
    Web search, with Web search ticked);
  - "Reasoning" (red) on the "Effort" row of the model menu;
  - "LLM Response" (green) on the answer;
  - "Reasoning Process" (purple) on the collapsible "Thought process" panel.

  Slide 32 combines the menus, and slides 32–33 carry a blue banner with the formula. A
  re-draw should use a generic chat mock-up with the same colour-coded tags rather than the real
  app UI. The menus are product details that change: slides 28–33 show a "Chat/Cowork" toggle
  and "Fable 5"/"Opus 5" models, while slide 42 shows "Claude Sonnet 4". Purpose: map the
  abstract parts onto something students have used.
- **35–40 · How an Agent works? (build-up).** Each slide puts bullets on the left and, on the
  right, a rounded purple box titled "AI Agent" that gains one icon per step. A tiny thumbnail
  of the slide-27 diagram (top right) marks which block the step is about: LLM Core, then
  Instructions, Dynamic Control twice, Tools, Memory.
  - 35: a neural-network icon "LLM Core" (top left).
  - 36: a person icon "The Prompt" (top right), with an arrow pointing left into the LLM Core.
  - 37: a short line down from LLM Core, labelled "becomes" in red, to a head-with-brain icon
    "Decision Maker" (centre).
  - 38: a checklist icon "Planner" (right), with a curved arrow from Decision Maker to Planner
    and another back (a plan–decide cycle).
  - 39: a wrench icon "Tools" (bottom left), with two curved arrows between Decision Maker and
    Tools (call out, result back).
  - 40: a database-cylinder icon "Memory" (bottom centre), with two curved arrows between
    Decision Maker and Memory (write, read).

  The final picture is a hub with the Decision Maker in the centre and three two-way spokes
  (Planner, Tools, Memory), fed from above by LLM Core + Prompt. Purpose: dynamic control is the
  LLM, steered by the prompt, cycling through planning, tool calls and memory. This is the
  slide-side picture of the agent loop that the tutorial frameworks run (digest C3).
- **41 · Building blocks.** On the left a bullet list (four blocks, each with two or three
  sub-items). On the right the slide-27 box without Task/Goal and Task Completion, with
  **"Dynamic Control" greyed out**. Purpose: the four parts you configure, against the one that
  emerges.
- **42–49 · Claude Research, second example (annotated screenshots).**
  - 42: the message box, with a red tag "Research + Reason" on the Research and thinking
    toggles and "LLM" on the "Claude Sonnet 4" chip.
  - 43: the thought panel ("Reasoning Process"). It cites research instructions that say to use
    a research-launching tool except for greetings and trivial questions, and decides this
    question needs it.
  - 44: a one-line strategy summary ("Reasoning Process"), then a card "Lead Researcher" (tag
    "Sub Agent") reading research complete, 255 sources, about six minutes.
  - 45: the card (tag "Researcher Agent"), with an orange L-shaped arrow to its expanded step
    list: "Research plan created" (tag "Sub Agent 1"), "Gathered 255 sources" (tag "Sub Agent
    2"), then a final "research report" line.
  - 46: the plan expanded (tag "Research Planner Agent"): assessment, query type ("depth-first"),
    a plan to deploy about 3–4 sub-agents (tag "Instructions for more Sub Agents"), then parallel
    execution and synthesis.
  - 47: the sources expanded (tag "Web Search Agent"): top domains with counts (23 + 17 + 14 + 5
    + 196 others = 255), then four findings, each with its own source count.
  - 48: the query list (tag "Web Search Tool Use"): ten distinct search strings about brie
    production, ageing, microbiology and chemistry, each returning 10 results.
  - 49: the chat with a report document card on the left, and the opened report with inline
    citation chips on the right (tag "Final Agent Response"); the banner gives the formula.

  For a re-draw, the structure is a tree: lead agent → planner sub-agent → several parallel
  search sub-agents (each issuing many tool calls) → a synthesis step → a document. Purpose:
  agents can create and direct other agents.
- **51 · Tools taxonomy.** At the top, a purple "Agent" box containing an orange "Tools" pill.
  Below it, three cards: red "Data Tools" (database icon; "Search, APIs"), green "Action Tools"
  (lightning icon; "Execute, Modify") and blue "Orchestration" (cycle icon; "Handoffs,
  Delegation"). Purpose: what kinds of things tools do.
- **52 · The integration problem.**
  - Left: a purple "Agent" box containing an orange "Tools" box with four pills, Tool 1–4.
  - About ten thin grey curves fan out from the Tools box to a column of ten rows. Each row has a
    grey protocol label and then a service with its icon: SMTP/IMAP → Email, CalDAV → Calendar,
    REST → Search, SQL/NoSQL → Database, REST → API, File I/O → Filesystem, Drive API → Google
    Drive, Maps API → Maps, Slack API → Slack, WhatsApp API → WhatsApp.
  - Under the agent, in red: "Do you see a problem?" and two bullets (each tool has a different
    integration or protocol; swapping tools takes a lot of work).

  Purpose: N different hand-built connections.
- **53 · MCP.**
  - The agent box now contains an orange "MCP Host" with four "MCP Client" pills (1–4).
  - A single line runs from the host to one orange dashed box "MCP".
  - From there the curves fan out to ten orange dashed "MCP Server" boxes. Each server sits in
    front of the same protocol label and service as on slide 52.
  - Five bullets underneath list the benefits.

  Purpose: one standard plug in place of N custom ones. A scene can animate slide 52 into 53
  (the curves collapse into one trunk; a server adapter clicks onto each row). **Caution:** the
  "MCP" box is a drawing shorthand for the shared protocol, not a broker process. Each MCP
  client keeps its own connection to one server. In the tutorials, each server is connected
  separately: a remote server over HTTP in the Cheese Quiz, and an `npx` child process over
  stdio in ADK `3-mcp-tools` (digest C5). Label any trunk "same protocol", not "server".

Not diagrams: 1, 2, 3, 15, 19, 23, 50, 54 (title and outlines), 22 (a text list), 24 (a
question), 25–26 (quoted definitions), 55 (links), 56 (closing picture).

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Agent" (definition) | 25–26 | Slide 26 matches the Travel Planner notebook's cell 6 word for word. The Cheese Quiz (cells 8, 28) says "a component" instead of "a system", and "to accomplish tasks" instead of "until a task is done". The `llm-rag` README calls its agent an "AI Agent (Cheese Expert Agent)". That agent is a fixed two-call pipeline: a forced tool call, then the answer, with no loop (digest C3). By the slides it sits nearer to Agentic RAG (13) than to the anatomy on 27–40. |
| "Autonomous Execution"; "self-contained execution unit" | 25, 27, 34, 41 | Google's definition on 25 uses the same phrase as Google's ADK documentation (the slide gives no source). The tutorial READMEs do not use it. |
| "Task / Goal", "Task Completion" | 27, 34 | No tutorial term. In the Newsletter notebook, "completion" is proved by a receipt, not stated by the model (digest C8). |
| "LLM Core" / "Reasoning Engine" | 27, 35, 41 | In code this is just `model=` (`gpt-4o`, `gpt-5.6-luna`, `gemini-3.1-flash-lite`, ADK's `GEMINI_MODEL`). **"Reasoning Engine" has two uses in the deck**: the LLM core here, and the multi-LLM system on 16–17. |
| "Instructions" (Prompts, Tasks, Guidelines, Goals); "The Prompt" | 27, 36–41 | ADK: `instruction=`. OpenAI Agents SDK and Microsoft Agent Framework: `instructions=`. The Cheese Quiz calls the system-prompt step "Prompt Engineering" (cell 36). |
| "Dynamic Control"; "Decision Maker"; "Planner"; "becomes" | 27, 37–40, 41 | No tutorial term. In code this is the agent loop that the framework runs: ADK's `Runner`, OpenAI's `Runner.run` with `max_turns`, Microsoft's `max_iterations` (digest C3). The Cheese Quiz frames it as "who controls the workflow" (cell 7; digest C1). |
| "Tools"; "function calling"; "functions with defined schemas" | 39, 51 | `llm-rag`: `FunctionDeclaration`, and the README says "function calling". OpenAI SDK: `@function_tool`. Microsoft: `@tool`. ADK: plain functions in `tools=[...]` (digest C5). The slides never say who runs the function. In the tutorial, the model only writes the call and your code runs it (digest C2). |
| "Data Tools" (Search, APIs), "Action Tools" (Execute, Modify), "Orchestration" (Handoffs, Delegation) | 51 | Tutorial examples: `llm-rag`'s two search tools are data tools. The Travel Planner's `finalize_itinerary` is a gated action tool (digest C8). Orchestration = agents-as-tools: `.as_tool` in the Cheese Quiz, and the researcher/editor `@tool`s in the Newsletter (digest C7). **"Handoffs" are not used**: the Cheese Quiz sets `handoff_description` on each specialist but composes them only as tools. |
| "Memory" (session history, user preferences, learned strategies; continuity across sessions) | 40–41 | **Conflicts with the ADK README**, which defines "Memory" as per-session state and says separate sessions do not share it (`llm-agent-google-adk/README.md:140`; digest E12). In ADK, per-session data is *state*. The Cheese Quiz's short-term vs long-term memory (cells 35, 41–42) matches the slides. The Travel Planner's `SQLiteSession` is in-memory and lasts one runtime. |
| "System & User Prompts", "Contexts", "Output Schema" | 41 | The Cheese Quiz's "Managing LLM Inputs" (cells 33–44) builds exactly these layers. Output schema is its step 7 (`json_schema`, strict), and `output_type=` in the Travel Planner and the Guild. "Context Engineering" appears in the deck only on the slide-19 outline. |
| "Orchestrations (flows)" | 41 | ADK workflow agents (`SequentialAgent` in `1-baseline`), and custom routing in `5-custom-agent` (digest C7). |
| "Reasoning LLM"; "Multi-LLM Orchestration System"; "Frameworks", "Inference Strategies", "Feedback & Iteration Loops", "Response Generator" | 16–18 | The Cheese Quiz's "Reasoning LLM" (cells 22–25) is one hand-coded instance: analyse → decompose → answer each → verify → synthesise, 11 `gpt-4o` calls. Its notebook map calls it "a manually orchestrated reasoning workflow". |
| "Reasoning" / "Reasoning Process" | 31–33, 42–44 | Here it means the model's own thinking: Claude's "Effort" setting and its "Thought process" panel. That is not a multi-call system like 16–18. The tutorial's only trace of it is Gemini's `thought_signature` in `llm-rag/out.txt` (digest C2). |
| "Naive RAG", "Advanced RAG", "Self RAG", "Corrective RAG", "Agentic RAG" | 6–14 | The L05 slides wrote "Naïve RAG" and "Self-RAG"; this deck writes "Naive" and "Self RAG". The `llm-rag` README calls its L05 part "RAG" and its L06 part "Agents", and never says "agentic RAG". ADK has a `6-rag` module. |
| "Retrieval Decision", "Pre-Retrieval", "Post-Retrieval", "Optimizations", "Self-Reflection & Critique", "Relevant / Supported / Useful", "Document Eval", "Query Rewrite", "Web Search" | 9–14 | The L05 slides used the reflection-token names IsREL / IsSUP / IsUSE. This deck uses plain words. None of these steps exists as code in the tutorials. |
| "Planning & Reasoning", "Task Decomposition", "Tool Use" | 14 | — |
| "Sub Agent", "Researcher Agent", "Research Planner Agent", "Web Search Agent", "Web Search Tool Use", "Deep Research" | 44–49 | ADK: `sub_agents=[...]`. The Newsletter's "Define Sub Agents" (cell 19). The Cheese Quiz's "Guild" specialists (digest C7). |
| "Agent ≈ LLM + Reasoning + Instructions + Tools"; "Agent ≈ LLM + Reasoning + Tools + Deep Research" | 32–33; 49 | The second version drops "Instructions". |
| "Model Context Protocol (MCP)"; "MCP Host", "MCP Client", "MCP Server" | 53 | ADK's `3-mcp-tools/README.md:130` gives the same one-line meaning (a standard way to connect agents to external tools and data). Tutorial code: OpenAI SDK `MCPServerStreamableHttp` (a client-side object named after the server it talks to), a FastMCP server, and ADK's `MCPToolset` with `StdioConnectionParams`. **Transports (stdio, streamable HTTP, SSE) and `tool_filter` are tutorial-only.** |
| "Travel Planner" | 20–22 | Notebook 2 (Seattle → California, mock catalog, Python-checked budget, human approval) and ADK `1-baseline` (a three-agent travel pipeline). Neither has a weather or delay tool: the notebook's tools are city, flight, hotel, restaurant and attraction search, plus finalize. |
| "Harness" | 55 | Appears only in the Notebook 3 title, "Cheese Newsletter - Harness". The deck never defines it. It becomes the main topic in L07 (`dlops-io/agent-harness`). |
| "Context Engineering", "Agent Systems", "Additional Resources" | 19 | Listed on the slide-19 outline only. These sections are not in this deck. |

Slips on the slides, so a scene does not copy them: slide 39 says "Format and interest tool
inputs" (meaning *interpret*); slide 51 says "agents can invoked"; slide 52 labels a pill "Toolt
4"; slide 36 has "Guideline & Constraints" (singular). "Reasoning Engine" names two different
things (27/35 and 16–17).

## Commands and code on the slides

There are no shell commands, no Python, no configuration and no framework APIs in the deck. The
only literal, code-like items are:

- 32, 33 · `Agent ≈ LLM + Reasoning + Instructions + Tools`
- 49 · `Agent ≈ LLM + Reasoning + Tools + Deep Research`
- 35 · model parameters named: `temperature`, `top-p`, `max tokens`
- 31 · Claude effort levels: `Low`, `Medium`, `High` (default), `Extra`, `Max`; models listed:
  Fable 5, Opus 5, Sonnet 5, Haiku 4.5 (42 shows "Claude Sonnet 4")
- 30, 32 · Claude "+" menu items: `Skills`, `Add connector` (`Browse connectors`, `Add custom
  connector`), `Add plugins`, `Research`, `Web search`
- 43 · a tool name visible in the thought panel: `launch_extended_search_task`
- 52, 53 · protocol labels: `SMTP/IMAP`, `CalDAV`, `REST`, `SQL/NoSQL`, `File I/O`, `Drive API`,
  `Maps API`, `Slack API`, `WhatsApp API`
- 55 · URLs (listed under Pointers)

## What the lecture stresses

- **LLMs and RAG cannot act.** They have no live connection to the world, no tools that make
  changes, and no autonomy. The banner question "Can RAGs or LLMs alone achieve this?" is the
  turning point of the lecture. (21–22)
- **An agent runs until the task is done**, not for a fixed number of steps. (26)
- **Choosing the LLM core is a design decision**: which model, which sampling parameters, which
  response format. (35)
- **Instructions must state success criteria and constraints**, not only a role. (36)
- **Guardrails are part of the decision.** The decision maker weighs "Constraints & guardrails"
  along with intent, tools and memory. (37)
- **Planning brings flexibility at a price.** The planner can create paths that the
  instructions never covered. The slide frames this as a strength for novel problems (38). The
  tutorials' harness notebooks show the other side: Python owns the arithmetic, approvals and
  the definition of success, because the model may take unexpected paths (digest C8). Pairing
  the two is my suggestion, not the slide's.
- **Tool use has three duties**: pick the right tool, format its inputs, interpret its outputs.
  (39)
- **Memory is what makes interactions continuous**, across sessions as well as within one. (40)
- **Dynamic control is not a component you build.** It is greyed out among the building blocks
  (41), and the LLM core "becomes" the decision maker (37).
- **The model should not search when it does not need to.** The first Claude example skips web
  search for a stable topic (33). In Research mode, the instructions explicitly exempt greetings
  and trivial questions (43). (This echoes the L05 Self-RAG point that unnecessary retrieval
  hurts.)
- **Higher reasoning effort is a trade-off**: more thorough answers, but slower and costlier (the
  effort menu's help text). (31)
- **"Do you see a problem?"**: point-to-point tool integrations do not scale, and swapping a
  tool is expensive. MCP's benefits are listed against exactly that. (52–53)
- **Check, don't trust**: the Self RAG checks (relevant, supported, useful) and Corrective RAG's
  document evaluation are framed as the way to catch bad retrieval and unsupported answers.
  (10–12)

## Pointers

- **Tutorials (slide 55)**, the same links as the course site's "Lecture 6" entry
  (`2026-AC215/tutorials_demo.md:83-98`):
  - Notebook 1 (Cheese Quiz):
    https://colab.research.google.com/drive/14UKW-Z7kFPuCwVqyUFcLxeA1KF70fwfm?usp=sharing
  - GitHub: https://github.com/dlops-io/llm-rag?tab=readme-ov-file#agents
  - GitHub: https://github.com/dlops-io/llm-agent-google-adk
  - Notebook 2 (Travel Planner):
    https://colab.research.google.com/drive/1I_jJEHJsVkGxNoSC1c4wEoVF2QL6vCVY?usp=sharing
  - Notebook 3 (Cheese Newsletter - Harness):
    https://colab.research.google.com/drive/1nnHrJ4Si3tpgUQl6HqlcwxKymV1-ecPv?usp=sharing
- **Quoted definitions (slide 25)** are attributed only to "OpenAI", "Anthropic" and "Google",
  with no link or title. The wording matches OpenAI's *A practical guide to building agents*,
  Anthropic's *Building effective agents* (the slide paraphrases it slightly) and the "Agents"
  page of Google's ADK documentation. That identification is mine.
- **Live demos (slides 28–33, 42–49)**: the Claude app in normal chat and in Research mode. A
  viewer can reproduce the idea in any assistant with web search and a research mode, but the
  menus will look different.
- **Recap of L05 (slides 4–14)**: Naive, Advanced and Self RAG were taught in L05 (see
  `../ac215-l05-rag/SLIDES.md`). Corrective RAG was only a name ("CRAG") on L05's landscape map
  (A11), and Agentic RAG was not in L05; both get diagrams here for the first time.
- **Sections promised but not in this deck (slide 19)**: Context Engineering, Agent Systems,
  Additional Resources. Look for them in L07 (Agents II).
- **No homework, milestone, reading list or logistics** appear anywhere in this deck.
