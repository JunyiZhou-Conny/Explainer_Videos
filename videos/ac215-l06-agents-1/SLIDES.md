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
    "Reasoning LLM" sections (cells 18–26).
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
  diamonds are decisions. Retrieve has a labelled "No" and "Yes"; the other three diamonds have
  only a "Yes" branch, so the "No" outcomes of Relevant, Supported and Useful are not drawn.
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
- **41 · Building blocks.** On the left a bullet list (four blocks: LLM Core with no sub-items,
  the other three with two or three each). On the right the slide-27 box without Task/Goal and Task Completion, with
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
| "Reasoning LLM"; "Multi-LLM Orchestration System"; "Frameworks", "Inference Strategies", "Feedback & Iteration Loops", "Response Generator" | 16–18 | The Cheese Quiz's "Reasoning LLM" (cells 22–26) is one hand-coded instance: analyse → decompose → answer each → verify → synthesise, 11 `gpt-4o` calls. Its notebook map calls it "a manually orchestrated reasoning workflow". |
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

## This video and the slides

**Basis.** The video is not scripted yet. This folder holds only `digest.md` and this file: there is
no `BRIEF.md`, `script.md`, `video.yaml`, `ASSETS.md` or `assets/terminal/`. So the map below uses
the ten planned chapters in [`digest.md`](digest.md) §8 and the study guide
(`MLOps_Learning/guides/L06-agents-1.md`). With no captures yet, "what the tutorial does today"
means the two repos at `e17a39f` and `f89faa7` and the notebooks' saved outputs, as verified in
`digest.md`. For this section I re-read all seven contact sheets and the deck's text, and enlarged
the two thought panels (slides 33 and 43). I also re-checked these at the source:
- **llm-rag (`e17a39f`).** The README's Agents section: its one-line intro, "let the LLM decide how
  to retrieve" (`README.md:244`); the name "AI Agent (Cheese Expert Agent)" (`:246`); its flow
  diagram, which has one LLM box before the retrieval and one after, like slide 13
  (`images/llm-rag-flow-3.png`). In `cli.py`, `agent()` makes exactly two `generate_content` calls
  (`:441`, `:465`), forces the first with `mode="any"` (`:449`), and has no loop.
- **ADK (`f89faa7`).** The README's definition of "Memory" (`README.md:140`). `1-baseline/agent.py`:
  three `LlmAgent`s joined by `output_key`, with no tools. MCP's one-line meaning
  (`3-mcp-tools/README.md:130`).
- **The notebooks.**
  - Cheese Quiz: cells 8 (its definition of an agent), 17 (its question), 24 (the `ReasoningLLM`
    docstring), 41–42 (short- and long-term memory) and 64–66 (`handoff_description`).
  - Travel Planner: cells 4 (mock tools; a real planner would call real APIs), 6 (slide 26's
    definition), 12 and 14 (three cities, five search tools).
  - Newsletter: cell 22 (the "no embedded URLs" rule) and the saved preview in cell 30, which
    contains a URL anyway.

When captures exist, re-check Conflicts 1, 2, 4 and 5 against them. If they disagree, the captures
win.

### 1. Map: planned chapters ↔ slides

| # | Planned chapter (`digest.md` §8) | Slides on the same ground | Relation |
|---|---|---|---|
| 1 | Who holds the steering wheel? (2.5 min) | 4–5 (plain LLM), 16–18 (Reasoning LLM), 26 (definition), 27 (anatomy, "Dynamic Control") | Same concept, and the tutorial applies it. The Cheese Quiz's three runs (base LLM, reasoning workflow, agent) follow the deck's own order: Recap → Reasoning Models → Agents. The hook (Gemini never touched `localhost`) is tutorial-only. Slides 20–22 would fit right after it (gap 3). |
| 2 | Everything the model knows is in the envelope (2.5 min) | 41 (Instructions: system & user prompts, contexts, output schema; Memory: user sessions, preferences), 36 (output formats), 40 (memory) | Partly the same concept. Slide 41's words name five of the Cheese Quiz's seven steps (user and system prompt, short- and long-term memory as sessions and preferences, the output schema); RAG documents and tool outputs can only hide under its vague "Contexts". Slide 19 promises a "Context Engineering" section that this deck does not have; it is L07's slides 11–18. The swapped roles in Step 2 (E1) are tutorial-only. |
| 3 | Function calling, frame by frame (4 min) | 13–14 (Agentic RAG), 39 (tools work through function calling), 51 (functions with defined schemas) | Same concept, and the tutorial applies it. Slide 13 is llm-rag's agent in outline: one LLM picks from a menu, a second LLM answers. Who runs the function, the hand-written JSON schema with its `enum`, and `mode="any"` are tutorial-only. Conflict 2. |
| 4 | Run it on your laptop (3.5 min) | 13 (two LLMs around the menu), 7 (the retrieval the tool performs) | The tutorial applies it. Docker, reading the trace, the `thought_signature` and the stale `out.txt` are tutorial-only. |
| 5 | From two calls to a loop (3 min) | 26 ("until a task is done"), 37–40 (the decision maker's two-way spokes), 41 (dynamic control greyed out) | Same concept. The slides draw the cycle but give no stop rule and no turn cap. `is_final_response()`, `max_turns` and `max_iterations` are tutorial-only. Conflict 1. |
| 6 | ADK: a framework that owns the loop (4.5 min) | 35–36, 40–41 (the blocks you configure); 20–22 (the travel theme of `1-baseline`) | Mixed. `LlmAgent(model=…, instruction=…, tools=…)` is slide 41 in code. Runner, Session, State, Event, `output_key`, `{key}`, `adk web` and the version pin are tutorial-only. Conflicts 3 and 5. |
| 7 | Tools you didn't write: MCP (2.5 min) | 51–53 | Same concept, and the tutorial applies it. Transports, `mcp_servers=` and `tool_filter` are tutorial-only. Conflict 4. |
| 8 | Many agents (2.5 min) | 44–49 (Claude Research: a lead agent, a planner, web-search sub-agents), 51 (orchestration tools: handoffs, delegation), 41 ("Orchestrations (flows)"), 38 (planner) | Same concept, and the tutorial applies it. The deck shows a product; the tutorial builds three composition patterns. Handoffs are lecture-only. |
| 9 | The harness: code decides what "done" means (3 min) | 36 ("Goals & success criteria"), 37 ("Constraints & guardrails"), 27 ("Task Completion"), 20–22 (the travel planner), 55 (the notebook title "Cheese Newsletter - Harness") | Mostly tutorial-only. The deck never defines a harness; L07 does (its slides 20–23). It names what the notebooks enforce, but leaves it to the agent: the instructions state it, the decision maker weighs it (Conflict 7). Conflict 5. |
| 10 | Recap + cleanup (1 min) | 41 (building blocks), 32–33 and 49 (the formula) | The recap could stand on lecture ground, but the plan does not use it yet. Cleanup is tutorial-only. |
| — | content not used by the plan | 1–3, 15, 19, 23–24, 50, 54–56 (title, outlines, dividers, links, close); 6, 8–12 (the RAG ladder); 20–22 (motivation); 25 (three industry definitions); 28–34, 42–43 (the first Claude demo, the anatomy repeat, the research toggle and its thought panel) | Lecture-only, unless gaps 2, 3, 7 and 8 bring them in. 20–22, 32–33 and 55 also appear in rows 6, 9 and 10 above: those chapters share their ground (the travel theme, the formula, the notebook title), but the plan does not use what these slides say. |

### 2. Already in common

| # | Concept | Chapter ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | A plain LLM: one call, nothing fetched | ch1 ↔ 4–5 | Yes. The Cheese Quiz's `BaseLLM` is slide 4's three boxes. Its question is a different cheese question (the best cheese for a grilled cheese sandwich, cell 17), not slide 5's brie. |
| 2 | A reasoning system built from several LLM calls | ch1 ↔ 16–18 | Yes, and the plan sharpens it. The notebook's docstring calls `ReasoningLLM` a reasoning framework of orchestrated calls, which is slides 16–17's "Multi-LLM Orchestration System". Slide 16's stack has no arrows, so it does not say who orders the calls. The plan answers: your Python, which makes it a workflow, not an agent. The word "reasoning" needs care (Conflict 6). |
| 3 | What an agent is: an LLM with instructions and tools that runs on its own | ch1 ↔ 26 | Yes. The Travel Planner (cell 6) uses slide 26's sentence word for word. The Cheese Quiz (cell 8) says "a component" for "a system" and drops "until a task is done". The plan's point (same model; a different loop and different tools) is slide 26 read closely. |
| 4 | Agentic RAG: an LLM chooses how to retrieve | ch3, ch4 ↔ 13–14 | Yes. The README introduces the section the same way (`README.md:244`), and its flow diagram, like slide 13, has one LLM before the retrieval and one after. llm-rag's menu has two entries, slide 13's has seven. Its first entry, "Retrieval Decision", is the one llm-rag takes away (Conflict 2). |
| 5 | Tools are functions with schemas; the agent picks the right one, formats its inputs, interprets its outputs | ch3, ch7 ↔ 39, 51 | Yes, read with slide 26's "system". The slides say agents invoke tools and never say who executes them. The plan's split (the model writes the call, your code makes it) is more precise and does not contradict them, as long as "agent" means the whole system and not the model. The three duties map onto llm-rag: the function name, the arguments (`search_content`, which its description asks the model to expand into a sentence or two; the recorded run sent four words, `out.txt:23`), and call 2. |
| 6 | The agent loop | ch5 ↔ 37–40 | Yes. Slide 40's final picture, a decision maker with two-way spokes to planner, tools and memory, is the loop drawn as a hub. ADK's `while True` is the same loop in code. The plan adds what the slides leave out: the model ends the loop by answering in plain text, and you cap it. |
| 7 | Dynamic control is not a part you write | ch5, ch6 ↔ 37, 41 | Yes. Slide 41 greys it out among the building blocks. In the tutorial it is the framework's loop: ADK's `Runner`, the Agents SDK's `Runner.run`, Microsoft Agent Framework's run with `max_iterations`. |
| 8 | Instructions turn the core into a specialist: role, constraints, output format | ch2, ch6 ↔ 36, 41 | Yes. ADK's `instruction=`, the Agents SDK's `instructions=`, the Cheese Quiz's system prompt. The output schema is Step 7's strict JSON schema and `output_type=`. |
| 9 | Short- and long-term memory | ch2 ↔ 40–41 | Yes for the Cheese Quiz: prior turns (cell 41), then a profile "from past sessions" written into the notebook as a dict (cell 42). Not for the ADK README's use of the word (Conflict 3). |
| 10 | MCP: one protocol between agents and tools; host, clients, servers | ch7 ↔ 52–53 | Yes. `3-mcp-tools/README.md:130` gives the same one-line meaning, and the plan's "USB hub" is slide 53's point. Draw it with one plug per server (Conflict 4). |
| 11 | An agent that directs sub-agents | ch8 ↔ 44–49, 51 | Yes. The Guild's and the Newsletter's orchestrators delegate the way slide 45's lead researcher does. The plan adds a caution the slides do not make (each hop adds cost and failure points; each saved Guild run logged three errors). It complements slide 47's 255 sources rather than contradicting it. |
| 12 | A travel planner as the worked example | ch6, ch9 ↔ 20–22 | The same task at a much smaller scope (Conflict 5). |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **The agent's anatomy as a map of the code (27, 34–41).** The plan never shows the lecture's
   master picture, yet every object the student types belongs to one of its blocks:
   - LLM core: `model=` (`gemini-3.1-flash-lite`, `gpt-4o`, `gpt-5.6-luna`, ADK's `GEMINI_MODEL`);
   - instructions: `instruction=` / `instructions=`, the system prompt, `output_type=`;
   - tools: `FunctionDeclaration`, `@function_tool`, `@tool`, `MCPToolset`, `.as_tool`;
   - memory: the message history, `SQLiteSession`, ADK's session state;
   - dynamic control: the framework's loop, the one block nobody writes (slide 41 greys it out).

   With this map, three frameworks stop looking like three things to learn. **Carry it in** ch1
   (introduce it), ch5 (dynamic control becomes the loop), ch6 (label ADK's constructor) and ch10
   (the recap card).
2. **Agentic RAG, and the choice not to retrieve (8, 10, 13–14, 33, 43).** llm-rag's
   `--agent` is slide 13 with a two-item menu, and the plan never says so. The lecture also
   shows the choice llm-rag takes away. Self RAG's first box decides *whether* to retrieve (10).
   Claude skips web search for a stable topic (33), while in Research mode its instructions push it
   to search for almost everything (43). Exercise 2 (remove `tool_config`) is the tutorial's version
   of that choice. **Carry it in** ch3 (L05's RAG boxes fly into slide 13's column, which shrinks to
   llm-rag's two tools) and ch4 (one sentence on Exercise 2).
3. **Why agents: what an LLM and RAG lack (20–22).** The plan's hook is a good puzzle, but the plan
   never says why we need agents. The lecture's answer is three missing things: contact with live
   systems, tools that act, and the autonomy to adapt. It sets them against a trip-planning task,
   which the Travel Planner notebook then rehearses. **Carry it in** ch1, 20–30 seconds after the
   hook, and again in ch9 to open the Travel Planner.
4. **Three families of tools (51).** Data tools fetch: llm-rag's two searches, `web_search`, the
   filesystem server's `read_file`. Action tools change something: `finalize_itinerary`,
   `send_email`. Orchestration tools hand work to other agents: `.as_tool`, the Newsletter's
   researcher and editor. The sorting explains the harness: the decisive gates in the last two notebooks
   sit on the action tools (approval on `finalize_itinerary`; validation and the receipt on
   `send_email`, though the editor's draft is validated too). **Carry it in** ch7 (sort the tools before MCP) and ch9 (the gates).
5. **The LLM core is a design decision (35).** The lecture names three choices: the model, the
   sampling parameters, the response format. The tutorial makes each one concrete:
   `temperature=0` on llm-rag's first call for a repeatable tool choice (the second call keeps the
   default), the strict JSON schema in Step 7, and `GEMINI_MODEL`, a model choice that broke because
   the defaults were retired (G2). **Carry it in** ch3 (`temperature=0`) and ch6 (the `.env` fix).
6. **The planner, and who plans (38).** The lecture's planner creates paths the instructions never
   spelled out. The tutorial's three multi-agent patterns differ in exactly that. In
   `SequentialAgent` the code fixes the order; the Guild's orchestrator plans from its instructions;
   `conditional_agent.py` lets Python route on the model's label. **Carry it in** ch8, as a "who
   plans the order?" axis. (L07 slide 36 returns to this as the autonomy spectrum.)
7. **Deep research as a tree of agents (42–49), and the formula (32–33, 49).** Students know chat
   apps. The research example (a lead agent, a planner, parallel web-search agents, a synthesis)
   has the same shape as the Newsletter (orchestrator, researcher with web search, editor). The
   formula "LLM + Reasoning + Instructions + Tools" gives the video a one-line summary. **Carry it
   in** ch8 (the tree beside the Guild and the Newsletter) and ch10.
8. **Check, don't trust (10–12).** Self RAG's three checks (relevant, supported, useful) and
   Corrective RAG's document grading are the lecture's early form of what the harness does in code:
   `validate_newsletter`, sources taken only from search citations, `check_itinerary`. The link is
   mine, not the slides'. **Carry it in** ch9, in one sentence.

### 4. Conflicts

| # | Slides say | Tutorial today (repos at `e17a39f` and `f89faa7`; notebooks and their saved outputs) | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **An agent runs until the task is done** (26), cycling through planner, tools and memory (37–40). | The README calls llm-rag's `--agent` an "AI Agent (Cheese Expert Agent)" (`README.md:246`). The code makes two calls and stops (`cli.py:441`, `:465`). If the second answer asked for another tool, the program would print the request and end (`cli.py:478`; digest C3). By the lecture's own diagrams it is Agentic RAG (13), one step before an agent. | Both describe their own object; the code decides what `--agent` does. | "The README calls this an agent. By the lecture's definition it runs one lap: a single tool call, then the answer. That is the smallest piece of an agent, and the next chapter adds the loop." Never call `--agent` an agent loop. |
| 2 | **The agent decides whether to retrieve.** Self RAG starts with a retrieval decision (10–11); the agentic-RAG menu lists it (13); Claude answers the brie question without searching (33). | `mode="any"` (`cli.py:449`) forces a function call, so llm-rag always retrieves. It chooses only *which* search. (The L05 cross-reference makes the same point: `../ac215-l05-rag/SLIDES.md`, Common 17.) | The code. | "In the lecture, a good agent may decide not to search at all. Ours can't: `mode="any"` makes it call a tool every time. It chooses which search, never whether. Exercise 2 hands the choice back." |
| 3 | **Memory persists across sessions** (40): history, preferences, learned strategies; "User sessions" and "User preferences" (41). | The ADK README uses "Memory" for per-session state and says separate sessions do not share it (`README.md:140`). In ADK's API that is *state*; memory is a separate, cross-session service (digest E12). The Travel Planner's `SQLiteSession` lives in RAM and ends with the runtime, and `chat_loop()` starts fresh. The Cheese Quiz's long-term memory is a dict written into the notebook (cell 42). | The slides' meaning, which is also ADK's API. | "The ADK README says 'memory' for what ADK's code calls session state. In the lecture's sense, remembering you next week, none of today's runs keeps memory. The Cheese Quiz shows the idea by pasting a stored profile into the prompt." |
| 4 | **One "MCP" box** sits between the host and ten servers (53). No transport is named. | Each server is its own connection: a remote server over streamable HTTP (Cheese Quiz cell 54), a FastMCP server in a thread on `127.0.0.1:8001` (cells 57–59), and an `npx` child process over stdio (`3-mcp-tools/agent.py:20-29`, with `tool_filter`). The SDK's client-side object is named after the server it talks to (`MCPServerStreamableHttp`). | The protocol and the code; the slide's box is shorthand. | "The lecture's 'MCP' box is the shared protocol, not a program you run. In code each server is its own plug: a URL, a thread, or a child process." Label any shared trunk "same protocol". |
| 5 | **The travel planner** books a five-day Paris trip within budget, suggests activities, and replans for bad weather or a delayed flight, through live systems and booking APIs (20–22). | The Travel Planner notebook goes from Seattle to San Francisco or Los Angeles, using a mock catalog: 3 cities, 6 hotels, prices in cents (cells 12, 14). It has five search tools and a gated finalize, no weather or delay tool, and books nothing. The notebook itself says a real planner would call real APIs (cell 4). ADK's `1-baseline` is three `LlmAgent`s in a fixed `SequentialAgent` with no tools at all, so its costs are the model's own estimates. | The notebooks and the code. | "The lecture's Paris trip is the goal. The notebook is a small, safe rehearsal: a mock catalog instead of live bookings, and a human 'yes' before anything is final. Weather and delays would be two more tools in the same pattern." For `1-baseline`: "a pipeline of three agents, not the lecture's planner. It has no tools, so its prices are guesses." |
| 6 | **"Reasoning" names three things**: a section called "Reasoning Models" (2) whose slides describe a multi-call "Reasoning Engine" (16–18); the model's own thinking, Claude's "Effort" setting and "Thought process" panel (31–33, 43); and the LLM core's subtitle, "Reasoning Engine" (27, 35). | The Cheese Quiz's `ReasoningLLM` is 11 calls of the same `gpt-4o`, ordered by Python (cell 24). Gemini 3.1 Flash-Lite thinks inside a single call: its `thought_signature` (`out.txt:28`) must be sent back unchanged (`cli.py:465-477`). | Names only; both kinds exist. | Say which one each time: "a reasoning workflow (many calls, ordered by your code)" or "the model's own thinking (inside one call)". Do not call the Cheese Quiz's chain a reasoning model. |
| 7 | **Success and guardrails live in the agent.** The instructions define "Goals & success criteria" (36); the decision maker weighs "Constraints & guardrails" (37); "Task Completion" comes out of the agent box (27). | In the last two notebooks, code decides. Python prices the trip, and only a later human "yes" approves a proposal (Travel Planner cells 15, 18). Success is a receipt for a file on disk (Newsletter cell 18). A rule left to the prompt slips: the editor is told not to embed URLs (cell 22), yet the saved preview contains one (cell 30). | Both, at different levels: the slides say what you tell the agent, the notebooks what code enforces. L07 slides 20–23 make this the main topic. | "The lecture lists success criteria among the instructions: that's where you tell the agent what 'done' means. These notebooks add where you check it, in code the model cannot talk its way past. Next lecture calls that the harness." |

Not counted as conflicts:
- The slides never say who executes a tool (39, 51); the tutorial does. That is an omission the
  video should fill, not a contradiction (Common 5).
- Slide 51 lists "Handoffs" under orchestration, and no tutorial uses one. The Cheese Quiz sets
  `handoff_description` on its specialists (cells 64–66) but calls them only as tools. L07 slide 33
  has the peer-handoff pattern.
- The recap diagrams draw every LLM as GPT, and the demos use Claude; the tutorial uses Gemini and
  OpenAI models. Slide 35 makes the model a choice, so this is not a disagreement.
- The model names in the Claude screenshots differ between 28–33 and 42. These are product details.
- Slide typos: 39 "interest" (for *interpret*), 51 "can invoked", 52 "Toolt 4".

### 5. Proposals for the BRIEF and script authors

**General**
- Tag each chapter that stands on lecture ground with one GREY `lecture_ref(6, "a–b")`, using the
  ranges below. Re-draw lecture diagrams in the series style. Never show slide images or the Claude
  screenshots; for the Claude examples, use a generic chat mock-up.
- Make the slide-27 anatomy the video's **running map** (gap 1). Build it in ch1 and light one block
  per chapter: instructions in ch2, tools in ch3 and ch7, dynamic control in ch5, all five in ch6,
  the whole box multiplied in ch8. In ch10, fill it with the tutorial's objects.
  - Do not copy the slide's colours. Its red "Dynamic Control" and green "Memory" would read as
    "error" and "project-owned" in the series palette.
  - Colour each block by **where it runs**, which is also the video's thesis. The model is BLUE: it
    runs in Google's or OpenAI's cloud. Your code is GREY on the laptop and TEAL inside the llm-rag
    container: the tools you wrote, the loop, the session. The hosted `web_search` and the remote
    MCP server are BLUE. The dashed trust boundary of the C2 animation separates BLUE from
    GREY/TEAL. Colab code runs on a Google VM, which the series table (`docs/AC215_SERIES.md`)
    colours BLUE, not GREY; in the notebook chapters, let the dashed boundary, not the colour,
    separate your code from the model. YELLOW marks the block in focus; RED stays for errors.
- The plan runs about 29 minutes. Gaps 1–4 add about 2.5 minutes and keep it inside 25–35.
- When captures are made, record a `--agent` run on today's book, the `adk web` event view for
  `1-baseline` and `3-mcp-tools`, and Travel Planner turns 3–4. Then re-check Conflicts 1, 2, 4
  and 5 against them.

**Per chapter**
- **Ch1 · Lecture 6 · slides 20–22, then 16–18, then 26–27.**
  - After the hook, spend 20–30 seconds on the lecture's motivation: the Paris request, the question
    whether RAG or an LLM alone can do it, and the three missing things (gap 3).
  - Lane 1 is slide 4. Lane 2 is slide 16's stack, turned into the Cheese Quiz's five boxes and
    labelled with the slide-18 techniques they use: problem decomposition, sequential processing, a
    verification loop, summary generation. Say who orders them: your Python (Conflict 6).
  - Close on slide 26's sentence and slide 27's box, with "Dynamic Control" in YELLOW: that block
    is the steering wheel.
- **Ch2 · Lecture 6 · slide 41.** Label the envelope's sheets with slide 41's words: system and user
  prompts, contexts, output schema, user sessions, user preferences. Add one sentence: the lecture
  lists these as parts of the instructions and the memory, and the next lecture names the craft,
  context engineering (L07 slides 11–18).
- **Ch3 · Lecture 6 · slides 13–14, 39.**
  - Start from slide 8's strip (L05's RAG). The boxes of slides 9–12 fly into slide 13's column,
    and the column shrinks to llm-rag's two tools. The first LLM becomes call 1, the second call 2.
    Show the README's flow diagram for one beat: it has the same two LLM boxes.
  - Leave "Retrieval Decision" in the column, then grey it out when `mode="any"` appears
    (Conflict 2, gap 2).
  - Caption the C2 animation with slide 39's three duties: pick the tool (the name), format the
    inputs (the arguments), interpret the output (call 2).
  - Give slide 35's `temperature` as the reason call 1 sets `0` (gap 5).
- **Ch4 · Lecture 6 · slide 13.** Keep slide 13's frame small in a corner as the timeline: call 1 →
  your Python → call 2. After the run, one sentence: "The lecture's Claude chose not to search.
  Exercise 2 lets ours choose too."
- **Ch5 · Lecture 6 · slides 37–41.**
  - Build slides 35–40's hub: the LLM core and the prompt become the decision maker, with two-way
    spokes to planner, tools and memory. Then turn the tools spoke into the circular track with the
    turn counter.
  - Answer slide 26's "until a task is done": done means the model answers without a tool call,
    and your cap stops it anyway.
  - Show slide 41's greyed-out block: the loop is the part the framework writes. Place Conflict 1
    here: "llm-rag ran one lap."
- **Ch6 · Lecture 6 · slides 35–36, 40–41.**
  - Label `LlmAgent(model=…, instruction=…, tools=…)` with the block names. The Runner is dynamic
    control; session state is memory within one session (Conflict 3).
  - At the `.env` fix: "The lecture's first design decision, choosing the model, is this one line.
    And the default broke." (gap 5)
  - Call `1-baseline` a pipeline of three agents with no tools, not the lecture's planner
    (Conflict 5).
- **Ch7 · Lecture 6 · slides 51–53.**
  - Open with slide 51's three families and sort the tutorial's tools into them (gap 4).
  - Use slide 52's "Do you see a problem?" as a five-second pause. Then animate 52 into 53, label
    the trunk "same protocol", and split it into the three real plugs: a URL, a thread on `:8001`,
    an `npx` child process (Conflict 4). `tool_filter` is the tutorial's addition.
- **Ch8 · Lecture 6 · slides 44–49, 38.**
  - Draw slides 44–48's research tree as a generic diagram (lead agent → planner → parallel
    searchers → synthesis → report), beside the Guild and the Newsletter (gap 7).
  - Put the three patterns on slide 38's question, who plans the order (gap 6): the code
    (`SequentialAgent`), the model (the Guild's orchestrator), or Python reading the model's label
    (`conditional_agent.py`).
  - One line on handoffs: slide 51 lists them, but the tutorials use agents as tools. L07 shows the
    other pattern.
- **Ch9 · Lecture 6 · slides 20–22, 36–37.**
  - Open on the lecture's Paris planner shrinking to the notebook's three-city catalog
    (Conflict 5).
  - Show slide 36's "success criteria" and slide 37's "guardrails" as notes pinned to the prompt.
    Then the harness puts a copy of each in code: `check_itinerary`, the approval gate, the
    receipt. The URL rule that slipped shows that a note in the prompt is not a check (Conflict 7).
  - Note that the gates sit on the action tools (gap 4). Self RAG's "supported" check is an early
    form of the same idea (gap 8).
  - End on the bridge: the next lecture calls this the harness (L07 slides 20–23).
- **Ch10 · Lecture 6 · slide 41.**
  - Recap card: slide 41's blocks, each filled with its tutorial object (gap 1).
  - Close on the lecture's formula with the tutorial's two additions: LLM + instructions + tools,
    plus a loop the framework runs and checks your code enforces.
  - Add two recap questions to the plan's six:
    - "Map `LlmAgent(model=, instruction=, tools=)` and the Runner onto the lecture's five blocks.
      Which block does nobody write by hand?"
    - "Sort `get_book_by_author`, `finalize_itinerary` and `research_facts` into the lecture's
      three tool families. Which family does the harness gate, and why?"

**Terms**
- Use the lecture's words: *agent* (slide 26's sentence), *LLM core*, *instructions*, *dynamic
  control* / *decision maker*, *planner*, *tools*, *memory*, *building blocks*, *task completion*,
  *agentic RAG*, *retrieval decision*, *function calling*, *data / action / orchestration tools*,
  *MCP host, client, server*, *sub-agent*, *deep research*.
- Add the tutorial's words where the lecture stops: *function declaration*, *function call* and
  *function response*, *forced tool call* (`mode="any"`), *agent loop*, *stop rule*
  (`is_final_response()`), *turn cap* (`max_turns`, `max_iterations`), *Runner*, *session*,
  *state*, `output_key`, *transport* (stdio, streamable HTTP), `tool_filter`, *agents as tools*,
  *workflow agent*, *harness*, *approval gate*, *receipt*.
- Qualify, don't repeat:
  - "agents invoke tools": the model asks, your code runs;
  - "memory": cross-session memory, or per-session state;
  - "reasoning": a workflow of calls, or the model's own thinking;
  - the "MCP" box: one protocol, one connection per server;
  - "agent" for `--agent`: one tool call, no loop.
