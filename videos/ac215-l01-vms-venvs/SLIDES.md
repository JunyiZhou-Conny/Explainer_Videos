# L01 lecture slides — Virtual Environments and Virtual Machines

**Provenance.** Two decks:

- `L01_virtual_environments_and_vms`, 75 slides: "Lecture 1: Virtual Environments and Virtual Machines", AC215/E115, Pavlos Protopapas, SEAS/Harvard.
- `L01a_course_intro`, 18 slides: "MLOps & LLMOps: Production AI Systems", the course introduction. It was apparently made for a recorded video, since its agenda slide is titled "What is in this video".

These are the instructor's lecture slides (PDF), provided by the student for study; the PDFs are not in this repository; slide numbers are PDF page numbers.

- Plain numbers ("slide 36") refer to the main deck. Intro-deck slides are written "intro 13".
- The main deck's printed page numbers match the PDF pages. The intro deck's printed numbers do not: slides 2–5 all print "2" and slides 6–9 all print "3". Use the numbers given here.
- Everything below is a digest in our own words. It was made from the extracted slide text and from reading every slide image: all nine contact sheets of the main deck, both sheets of the intro deck, and enlarged single-page renders of the diagram and screenshot slides. Those renders are small (40 dpi), so tiny screenshot text is marked as uncertain where it matters.

The tutorial side is documented in [`digest.md`](digest.md). Below, "tutorial", "README" and "repo" mean `dlops-io/simple-translate` at `62f821b`, sections *Installing App on VM Manually* (Step 1 of 4) and *Installing App on VM using UV* (Step 2 of 4), as recorded there.

## Outline

The main deck's agenda is a slide titled "Outline" with three items: Motivation, Virtual Machines, Virtual Environments. It appears plain on slide 2 and again on slide 3 with "Motivation" in bold. It is not reused after that. Instead:

- a grey "TRANSITION" slide (18) splits the motivation section in two;
- a "Tools" slide with three tiles (Virtual Machines, Virtual Environments, Containers) works as a section divider. It appears first with all three tiles (33), then with only the VM tile lit (34), then with only the virtual-environment tile lit (49). The Containers tile is always greyed out, with the note that containers come next week.

**Main deck (`L01_virtual_environments_and_vms`)**

- **Slide 1 · title.**
- **Slides 2–3 · agenda** (3 marks Motivation as current).
- **Slides 4–17 · 1. Motivation, part 1: from prototype to MLOps.**
  - 4: enterprise AI statistics, framed as "The AI Paradox".
  - 5–6: the classroom data-science workflow (one developer) vs the real world (teams, clusters, apps).
  - 7: six key challenges of real-world production.
  - 8: the six challenges as coordination problems, which MLOps answers.
  - 9: DevOps and MLOps defined.
  - 10: MLOps tasks in three columns.
  - 11–16: the MLOps tech stack, filled one column per slide: empty headers (11), Data (12), Models (13), Development (14), Operations (15), and the four roles underneath (16).
  - 17: "Our Stack", the tools this course uses.
- **Slides 18–32 · 1. Motivation, part 2: the deep-learning flow and the Formaggio app.**
  - 18: transition slide, "Motivation: Deep Learning Flow".
  - 19: the five-step flow ending in "Best Model" and "Now What ?".
  - 20–22: Formaggio, the reference project (20); what it is (21); its functional requirements, beside a meme collage (22).
  - 23–25: the Cheese App's data (23), models (24) and the choice of the best model (25).
  - 26–27: the steps from model to app (26); how the pieces connect (27).
  - 28–30: environment challenges for one developer (28), multiple developers (29), and multiple developers plus automation (30).
  - 31: the six challenges again, now applied to Formaggio.
  - 32: three solution principles.
- **Slides 33–48 · 2. Virtual Machines.**
  - 33: the three tools; 34: the VM tile lit.
  - 35: what the team needs, answered by "Virtual Machines!".
  - 36: what a VM is, with a stack diagram.
  - 37: advantages and virtualization software; 38: limitations.
  - 39–48: the VM tutorial:
    - why a translation app (39);
    - the steps and the README link (40);
    - the Google Cloud homepage (41);
    - advice for creating the account (42);
    - the console click path: navigation menu (43), Compute Engine → VM instances (44), Create instance (45), defaults (46), SSH (47);
    - the SSH terminal with the `git clone` line (48).
- **Slides 49–72 · 3. Virtual Environments.**
  - 49: the tools slide with the virtual-environment tile lit.
  - 50: definition, a directory with three components.
  - 51–54: the story of Maggie and John: a single base install (51), a separate environment for the new course (52), sharing it with a configuration file (53), and receiving an updated environment back (54).
  - 55: why use them; 56: pros and cons.
  - 57: five tools; 58: "We Will Be Using UV".
  - 59–60: venv. 61–62: conda. 63–64: pipenv.
  - 65–70: uv: what it is (65), the three questions it answers (66), the basic workflow (67), two key files and a key directory (68), the simple-translate example (69), and what to do after the first time (70).
  - 71: further readings.
  - 72: the virtual-environment tutorial and its link.
- **Slide 73 · summary.** Virtual environments vs virtual machines as two stacks.
- **Slides 74–75 · closing.** Logistics (74). "THANK YOU" with a cartoon still captioned "Pavlos" (75).

**Intro deck (`L01a_course_intro`)**

- **Intro 1 · title.** "MLOps & LLMOps: Production AI Systems".
- **Intro 2–5 · agenda, built up one item per slide.** Title only (2); "About me" (3); plus "Why take this course in the era of generative AI?" (4); retitled "What is in this video", plus "What the course is about, and what you need coming in" (5).
- **Intro 6–9 · About me.** Role and PhD (6), research areas (7), teaching (8), hobbies and a link to the staff page (9).
- **Intro 10–14 · Why take this course in the era of generative AI?** The question (10), what the course expects of you (11), what it assesses (12), why the steps matter (13), the cycling-coach analogy (14).
- **Intro 15–18 · What the course is about, and what you need.** The goal (15), the logistics video and syllabus (16), how you are assessed: quizzes and milestones (17), "Is This Course For You?" (18).

## Key ideas

1. **In enterprise AI, ambition outpaces execution.**
   - The opening figures (credited to McKinsey 2023, IDC and VentureBeat) set rising AI use against slow deployment: over two-thirds of companies need between 8 and 90+ days to ship a single model.
   - Few companies have an enterprise-wide AI strategy, and more than 80% of generative-AI initiatives show no tangible effect on EBIT, because pilots rarely scale.

   *Slide 4.*
2. **Course projects are one-person prototypes; real ML is a team on clusters.**
   - In the classroom (the CS1090 series), one developer on one computer goes from Data to Models to Results such as reports and dashboards.
   - In the real world, teams of five or more distribute data work and training across cloud clusters, reuse pre-trained models and ensembles, and ship an app.

   *Slides 5–6.*
3. **Scaling up raises six challenges.** They are team integration (onboarding), environment setup, code collaboration, sharing large datasets and models, pipeline automation, and production discrepancies (the "it works on my machine" problem). The cure is to standardise infrastructure through automation, containers and operations, which stops "environmental drift". *Slides 7, 31.*
4. **The six are really one coordination problem, and MLOps is the operating model that answers it.** Going from an individual prototype to many people, environments and tools creates coordination problems. Operational practices that connect data, models, software and infrastructure fix them. *Slide 8.*
5. **DevOps unites development and operations; MLOps adds model development to that union.**
   - MLOps work falls into three columns.
   - ML/DL: data, model selection, training, distillation and compression.
   - Application development: model-serving APIs, web, mobile and edge apps, automation scripts.
   - Operations: servers, uptime, CI/CD, continuous data collection, model and data monitoring and versioning, workflow management.

   *Slides 9–10.*
6. **The tool landscape has four columns, each owned by a role.**
   - Data belongs to data engineers, Models to data scientists, Development to software engineers and Operations to systems engineers.
   - The course's own stack runs from AI/ML through Development to Operations: data stores and DVC, TensorFlow/PyTorch, Colab and Vertex AI, W&B; FastAPI, FastMCP, LLM APIs, React/Next.js, VS Code or Cursor; GitHub, Docker, GCP, GitHub Actions, Pulumi and Kubernetes.

   *Slides 11–17.*
7. **A "best model" is where this course begins.** The familiar flow (collect data, explore data, explore models, train, evaluate, with a hyperparameter-tuning loop between training and evaluation) ends in a best model and the question "Now What ?". The best model is picked on several criteria (accuracy, memory, execution time), not accuracy alone. *Slides 19, 24–25.*
8. **Formaggio is the semester's running example.** The teaching team builds a cheese app: photograph a cheese to identify it, then ask where it comes from, how it is made, what to drink with it and where to buy it. Each week connects one part of it to the topic, and students apply the same steps to their own project. *Slides 20–22.*
9. **Turning the model into an app takes five steps:** expose the model as an API, build a frontend, wire the API into the app, deploy to a cloud provider, and go live (formaggio.me). The pieces start life in different tools: a Python script for data collection, Colab for modelling, and an IDE for the API and the app. *Slides 26–27.*
10. **Every stage runs in a different environment, and each extra person multiplies the mismatch.**
    - Even one developer has four setups: data collection on a Mac (uv, plus a Mac install of Chromium), modelling in Colab's Linux environment, the API on the Mac, and deployment on a Linux server.
    - Add developers on Mac and Windows, and automated retraining on the server, and the combinations multiply.

    *Slides 28–30.*
11. **The solution has three parts:** isolate development in environments that can be shared, develop on a common OS whatever each developer's host OS is, and track what software is installed. The tools are virtual machines and virtual environments (this lecture) and containers (next week). *Slides 32–34, 49.*
12. **A VM is a whole computer made of software, run by a hypervisor.**
    - It imitates hardware such as CPUs and disks, and the hypervisor creates and runs VMs on the physical machine.
    - The machine's own OS is the "host"; each VM runs a "guest" OS, guests can differ from each other, and hardware is the only limit on how many run.
    - VMs answer the team's needs: the same OS for everyone, the same software, and machines that are easy to create and throw away.

    *Slides 35–36.*
13. **VMs trade weight for isolation.**
    - Pros: a computer within a computer, software inside can't harm the real machine, one machine can run many OSs, and every cloud rents servers as VMs.
    - Cons: they depend on the host's hardware, are large and hard to move, cost CPU and memory overhead, run slower than the host, start slowly, and may lack the host's graphics.

    *Slides 37–38.*
14. **The first app is simple-translate,** a small Python tool built on Google Translate. It is motivated by the cheese app's need to speak to cheese lovers in many countries, and it is the foundation for later work. To run it on a Google Cloud VM, you create an instance, SSH in, install git and Python, clone the repo and run the script. *Slides 39–48.*
15. **A virtual environment is just a directory** that gives one Python setup its own libraries. It holds a site-packages folder for third-party libraries, symlinks to system executables, and scripts that make your code use this environment's interpreter and packages. *Slide 50.*
16. **The story of Maggie and John shows why.**
    - Installing everything into one base Anaconda works for a single course.
    - A new course gets its own named environment, and `which python` now points inside it.
    - Maggie shares that environment by sending a configuration file, so John can rebuild it.
    - When John adds a library (taken from another of his environments), he sends back code plus an updated file, so Maggie can replicate his result.

    *Slides 51–54.*
17. **Virtual environments make work reproducible and shareable, but they are not full isolation.**
    - Pros: separate "sandboxes" you can switch between, explicit dependencies, reproducible results, easier teamwork, and an exact environment for a given OS and hardware.
    - Cons: setup can be complex, isolation is incomplete, and behaviour may differ across operating systems.

    *Slides 55–56.*
18. **There are five tools, and the course standardises on uv.** venv is Python's built-in, conda is the data-science package and environment manager, pipenv adds production features on top of venv, mamba is a faster C++ conda, and uv is a very fast installer and resolver written in Rust. uv is the course's primary tool and is presented as the new industry benchmark. *Slides 57–58.*
19. **The older tools record an environment by exporting a list; pipenv adds a manifest and a lock.**
    - venv and conda save the environment to a file (`pip freeze`, `conda env export`) and rebuild from it.
    - pipenv splits the record into a human-readable Pipfile (packages, version constraints and a dev section) and a machine-generated Pipfile.lock (exact packages and their dependencies).

    *Slides 59–64.*
20. **uv answers three questions with two files and a directory.**
    - The questions: which packages the project needs, which exact versions, and where they are installed.
    - `pyproject.toml` says what the project needs: human-edited constraints, with dev dependencies under `[dependency-groups.dev]`. `uv.lock` records the exact versions chosen. `.venv/` is the installed environment.
    - uv replaces pip and pip-tools and manages the environment itself.

    *Slides 65–66, 68.*
21. **uv has two workflows.**
    - Starting a project: `uv init --bare`, then `uv add` to record and install packages, then `uv run`.
    - Joining a project that already has `pyproject.toml` and `uv.lock`: `uv sync` builds `.venv/` with the exact locked versions, without adding anything again.
    - Code runs either after activating `.venv` or through `uv run`.

    *Slides 67, 69–70.*
22. **A venv isolates libraries on one shared Python and OS; a VM isolates a whole OS on a hypervisor.** *Slide 73.*
23. **Learn the steps, even with AI.**
    - The course expects you to be able to build the whole system without generative AI: slower, but knowing every step and how the pieces fit.
    - Fully autonomous agents still go wrong expensively, while a human guiding them step by step gets the gains. AI multiplies your expertise; it doesn't replace it.
    - The analogy: you can't coach a sport you've never played, like a cycling coach who knows the numbers but has never felt a long climb.

    *Intro 10–11, 13–14.*
24. **The goal is to design, build and deploy a complete AI system, end to end.** A model is only half the journey; the other half is a reliable, scalable, usable system, across the full ML lifecycle, with a strong emphasis on LLMs. Assessment covers understanding (quizzes), engineering, working systems, and communication. *Intro 12, 15, 17.*

## Diagrams

- **Slide 5 · the prototype workflow.**
  - Three coloured headers left to right, joined by arrows: Data (blue, database icon), Models (green, light-bulb icon) and Results (red, report icon).
  - Under each, a single stack rises with an up-arrow: icon, laptop, one person.
  - Bullets: collection, exploration and preparation for Data; exploration, experimentation, training and evaluation for Models; blogs, reports, presentations and BI dashboards for Results.
  - A brace along the bottom labels it one developer on one computer, with projects of one to three people.
  - For: the "before" picture.
- **Slide 6 · the real-world workflow.**
  - The same three headers, but the last is Apps (red).
  - Under Data and Models, branching trees replace the single stacks: one node fans out to several machines (laptops, server racks) with several people at the leaves.
  - Data adds "Recombine". Models adds pre-trained models and comparing or ensembling.
  - Apps lists deployed examples with their icons: Siri / Alexa, FaceApp, Socratic.
  - The bottom brace reads: a team of developers on single or multi-node clusters on a cloud platform, with teams of five or more.
  - For: the "after" picture. Re-draw slides 5 and 6 as one stack that fans out into a tree.
- **Slide 8 · from prototype to operational practices.**
  - Four boxes in a row with arrows: Individual Prototype (one developer, local, manual, isolated code) → Multiple Teams & Tools (5+ people, varied environments, pipelines, apps) → Coordination Challenges (environmental drift, asset sharing, integration, environment setup) → Operational Practices (the last box, outlined in blue).
  - A callout below defines MLOps as the model connecting data, models, software and infrastructure.
  - For: framing MLOps as the answer to a coordination problem.
- **Slides 11–16 · the tech-stack board.**
  - Four rounded column headers: Data (blue), Models (green), Development (orange), Operations (red). Each slide fills one more column with tool names and logos, in the order listed under Terms.
  - Slide 16 adds a long double-headed arrow under all four columns and four colour-matched role boxes beneath them: Data Engineers, Data Scientists, Software Engineers, Systems Engineers.
  - For: one column per role. Re-draw as columns that fill in turn, then the role labels sliding up underneath.
- **Slide 17 · "Our Stack".**
  - Three tall coloured panels, AI / ML (blue), Development (green) and Operations (red), joined by grey arrows from left to right. Each has a header with a down-arrow, then category labels with tools: Data, Framework, ML Tasks and Tracking; APIs & Tools, LLM APIs, Frontend and IDE; Source Control, Containerization, Cloud Provider, CI/CD and Scaling.
  - For: the course's own toolchain as a pipeline.
- **Slide 19 · the deep-learning flow** (repeated in pieces on 23–25).
  - A hand-drawn staircase of numbered boxes descending left to right, each with a coloured circle and a curved arrow to the next: 1 Data Collection (blue), 2 Data Exploration (green), 3 Model Exploration (yellow), 4 Model Training (red).
  - From 4, a red arrow climbs to 5 Model Evaluation (purple). A purple arrow labelled "Hyperparameters tuning" curls back from 5 toward 4, forming a loop.
  - From 5, an arrow goes up to a brown "Best Model" box with a light bulb, and from there an orange arrow up to "NOW WHAT ?" in red hand lettering.
  - For: everything students already know ends in a model, and the course starts at the question mark.
  - Slide 23 shows only steps 1–2, slide 24 steps 3–5, and slide 25 the Best Model box with an up-arrow from a results table.
- **Slide 25 · choosing the best model.**
  - A seven-row experiment table with columns trainable_parameters, execution_time, loss, accuracy, model_size, learning_rate, batch_size, epochs, optimizer and name. The rows are MobileNetV2 variants (TF-Hub and plain, with the base trainable or frozen) and custom 4-block, 2-block and VGG-style networks.
  - A red arrow runs from the caption (selection uses several criteria) to the second row, as we read it: about 82 thousand trainable parameters and 90.30% accuracy, against the top row's 2.3 million parameters and 90.91% (both rows list a 10 MB model).
  - For: picking the best model is a trade-off, not the top accuracy.
- **Slide 27 · how the app is assembled.** Left to right:
  - "Data Collection": a grid of cheese photos over a maroon "Python Script" box.
  - A purple arrow to a Colab notebook screenshot over a gold "Colab" box. Four labels stack above it: Data Exploration, Model Exploration, Model Training, Model Evaluation.
  - An orange arrow to a group sitting on a wide blue "IDE / Code Editor" box: a red "Best Model" box, a green "Rest API" box, and a sketch of a cheese wheel labelled with a prediction ("Type: Brie (93.54%)").
  - A green arrow up from Rest API to a browser window titled "Cheese App", showing a brie photo and its predicted type.
  - For: the parts of the app, and which tool each part is born in.
- **Slides 28–30 · the environment map.**
  - Slide 28 redraws slide 27 in one row:
    - a red "Development" brace spans Python Script → Colab → Rest API + Best Model on the IDE;
    - a green arrow leads to the Cheese App under a green "Deployment" brace.
  - Under each stage are two or three environment lines:
    - Python script: Python via uv, Chromium as a Mac install, OS Mac;
    - Colab: Colab's provided Python, OS Linux;
    - API: Python via uv, OS Mac;
    - deployment: Python via uv, OS Linux.
  - Blue braces below group the development stages under one person icon ("One developer, Using a Macbook") and the deployment stage under "Server".
  - Slide 29 replaces the single person with pairs of blue and green person icons under each stage (a crowd under the API) and the caption "Multiple developers, Using Mac and Windows OS".
  - Slide 30 keeps only the Deployment column, bracketed as "Server" (Python via uv, OS Linux):
    - the Cheese App at the top, Model Training in the middle, the photo grid and Python Script at the bottom;
    - curved arrows form a loop: grey arrows run down from the app to training and to the data, a purple arrow goes from the data up to training, and a red arrow joins training and the app.
    - The arrowheads are tiny at 40 dpi, so the loop reading is ours: the deployed app feeds new data back, and the model is retrained and redeployed on the server.
    - The extracted text of slide 30 also carries the development labels widened to "Mac, Windows" (for example, a Windows install of Chromium next to the Mac one), which the render does not show. They are probably hidden or animated objects.
  - For: the "it works on my machine" problem drawn as a grid of stages × environments × people. Re-draw as a row of stages whose environment labels multiply as people are added.
- **Slides 33, 34, 49 · the three tools.**
  - Three square tiles with icons: Virtual Machines (server icon), Virtual Environments (stacked-layers icon), Containers (blocks icon, greyed, with the note that it comes next week).
  - On slide 34 only the VM tile is lit, and the virtual-environment tile carries a "later" note. On slide 49 only the virtual-environment tile is lit.
  - For: a section map.
- **Slide 36 · what a VM is.**
  - A stack, bottom up:
    - "Infrastructure" (dark bar);
    - "Operating System" (grey);
    - "Hypervisor" (light grey);
    - three tall dashed boxes, blue, green and red, each labelled "VM". Each holds, bottom up, a big "OS" block, a "Bins/lib" bar and an "App1/2/3" bar.
  - The caption is "Virtualization".
  - For: every VM carries its own OS, managed by the hypervisor on the host.
  - Precision note for a re-draw: a hypervisor sitting on a host OS is the laptop arrangement (VirtualBox, VMware, Parallels on slide 37). A cloud VM such as a Compute Engine instance runs on a hypervisor built into the provider's host machines. The student sees only the guest, and the slide does not draw this difference.
- **Slides 41–48 · the console click path** (screenshots with red arrows).
  - 41: the Google Cloud homepage, with an arrow at "Console" (top right).
  - 42: two cards: an email you control, and keeping the account personal.
  - 43: the console welcome page, with an arrow at the navigation menu (top left).
  - 44: the menu open, with arrows at Compute Engine and its "VM instances" entry.
  - 45: an empty VM instances list, with an arrow at "CREATE INSTANCE".
  - 46: the create-instance form, where the instruction is to keep all defaults. The visible sections include machine series and type, boot disk and identity/API access, with a monthly cost estimate on the right. The values are unreadable at 40 dpi: plausibly an e2 machine type and a Debian image (uncertain).
  - 47: the instance list with one running instance (green check, a us-central1 zone, internal and external IPs), with an arrow at "SSH" in the Connect column.
  - 48: the browser SSH window showing a Debian login banner and a prompt, with the clone command under it. The banner's kernel version looks like an older Debian release (uncertain at 40 dpi), so the screenshot probably predates today's default images.
  - For: the path to a running VM. Re-draw as a five-step breadcrumb rather than screenshots.
- **Slides 51–54 · Maggie and John's environments.**
  - 51: Maggie's machine:
    - a grey "Operating System" bar, a blue "bins" bar on it, and three blue tiles lib1, lib2, lib3;
    - beside it, `which python` resolves to the base Anaconda Python.
  - 52: a second stack appears on the same OS bar, green, bottom up: "env_ac215", "bins", then only lib1 and lib2. `which python` now resolves inside `envs/env_ac215`.
  - 53: Maggie's green stack gets a dashed outline, and a dashed arrow carries it to John's OS bar, where an identical green env_AC215 (lib1, lib2) appears. Maggie's blue base install is not copied.
  - 54: John has a second, red stack, env_ai4 (lib3b, lib2, lib3).
    - A dashed arrow moves its lib3b into his env_AC215, which becomes lib1, lib2, lib3b.
    - A dashed arrow then carries John's env_AC215 back to Maggie, whose env_AC215 gains a third tile in a dashed box. That tile is labelled "lib3" on Maggie's side and "lib3b" on John's; it is the same library.
  - For: an environment is a named, portable set of libraries that can be sent between machines through a configuration file.
  - Re-draw as stacks of library blocks that copy across between two machines.
- **Slides 63 and 65 · manifest vs lock** (speech-bubble annotations, no drawing).
  - On slide 63, one bubble says the packages under `[dev-packages]` in the Pipfile are development-only. Another, pointing at "Pipfile & Pipfile.lock", contrasts the human-readable Pipfile (packages and version constraints) with the Pipfile.lock (exact packages and their dependencies, described as not human-readable).
  - Slide 65 repeats the pattern for uv: dev dependencies go under `[dependency-groups.dev]`, `pyproject.toml` holds the constraints and `uv.lock` the exact resolution.
  - For: the manifest/lock split. Re-draw as two documents, a short list of wishes and a long fully pinned list, joined by a "resolve" arrow.
- **Slides 68–70 · the two files and the directory** (a text layout, not a drawing).
  - `pyproject.toml`, `uv.lock` and `.venv/` stacked in green code type, each with a short role: what the project needs, the exact versions chosen, the installed environment.
  - Slide 70 shows the second-time case: only the two files are present, and `uv sync` produces the directory.
  - For: which artefacts uv owns. Re-draw as two files feeding a directory.
- **Slide 73 · virtual environments vs virtual machines.**
  - Two stacks side by side, both starting with "Infrastructure" (dark) and "Operating System" (grey).
  - Left, "Virtual Environments": a dark-blue "Python" bar (yellow text) and three short dashed boxes (blue, green, red), each an App over "Libs", labelled "Venv".
  - Right, "Virtualization": the slide-36 stack, with "Hypervisor" and three tall VM boxes, each holding an OS, "Bins/lib" and an App.
  - For: what each unit of isolation carries. A venv carries only libraries on a shared Python and OS; a VM carries a whole OS. The box heights make the difference visible.
  - L02's slide 10 adds a third, container column to this same drawing.
- **The intro deck has no mechanism diagrams.**
  - Its visuals are a portrait (intro 6–8), a list of teaching cards (8), a cheese-board photo (9) and three text cards: Autonomous Fails, Directed Execution, The Expertise Gap (13).
  - Intro 14 has a pencil sketch of a cyclist climbing.
  - Intro 16–17 show cards for the logistics video and the syllabus, and for quizzes and milestones.

## Terms the lecture uses

- **"MLOps"**, **"DevOps"** (9); **"Ops"** (deployment operations, 7); "Operational Practices", "coordination problems" (8).
- **"environmental drift"** (7–8); **"it works on my machine"** (7, 31); "Production Discrepancies", "Team Integration", "Environment Setup", "Code Collaboration", "Sharing Assets", "Pipeline Automation" (7, 31); "Individual Playgrounds to Enterprise Infrastructure" (7).
- **"Data Science Series"** (CS1090 A/B), "Prototype Workflow", "Real World" (5–6).
- **Tech stack** (12–16):
  - Data: Spark, Hadoop, Kafka, BigQuery, Airflow, Vertex AI Pipelines, DVC, Postgres, Neo4j, Chroma.
  - Models: PyTorch, TensorFlow, Hugging Face, Scikit-learn, MLflow, Weights & Biases, XGBoost, ONNX.
  - Development: VS Code, Jupyter, Git, GitHub, Docker, Conda, pip / poetry.
  - Operations: AWS, GCP, Kubernetes, Ansible, Jenkins, GitHub Actions, Cloud Functions, Pulumi.
  - Roles: "Data Engineers", "Data Scientists", "Software Engineers", "Systems Engineers" (16).
- **"Our Stack"** (17): Chroma, PostgreSQL, DVC, Label Studio, TensorFlow, PyTorch, Google Colab, Vertex AI, W&B, FastAPI, FastMCP, OpenAI, Gemini, React, NextJS, VS Code, Cursor, GitHub, Docker, Google Cloud Platform, GitHub Actions, Pulumi, Kubernetes.
- **"Deep Learning Flow"**, **"Best Model"**, **"Now What ?"**, "Hyperparameters tuning" (19, 24–26).
- **"Formaggio"** / **"Formaggio.me"**, the reference project, and **"Cheese App"** (20–30).
  - The example cheeses pictured are Parmigiano, Ricotta, Feta and Brie (20–21).
  - The data slide's four labels are brie, parmigiano, gouda and gruyere (23).
  - None of this appears in the L01 README, whose app is the **"Simple Translate App"**. The lecture writes it **"Simple-Translate App"** and "simple-translate" (39–40, 72).
- **"Rest API"**, "Python Script", "Colab", "IDE / Code Editor" (27–29); "Development" vs **"Deployment"**, "Server" (28–30).
- **"Virtual Machine"**, **"Hypervisor"**, **"host"** and **"guest"** OS, **"Virtualization"**, "Infrastructure", "Bins/lib" (36, 73).
  - The README never says hypervisor, host or guest. Our `digest.md` uses "hypervisor" too (§3.1).
- **"VirtualBox"**, **"VMWare"**, **"Parallels"** (37).
- **"Virtual Machine Instance"** / **"VM Instance"**, **"compute engine and VM instances"**, **"CREATE INSTANCE"**, "ssh" (40, 44–47, 72).
  - The README says "Create a VM Instance from GCP" and "SSH into your newly created instance", so the terms match.
  - The lecture's step "Install Required Dependencies: git, Python" (40, 72) is two README steps, `sudo apt install git` and `sudo apt install python3-pip`. The README also has a third, `sudo pip3 install --break-system-packages …`.
  - The lecture's "Download and Execute the Simple-Translate Python Script" is the README's "Clone App Repo" plus the `python3 cli.py` runs.
- **"virtual environment"** as an "isolated Python setting" that is a **directory** of components (50):
  - **"`site_packages/`"**, written with an underscore. The real folder is `site-packages`, under `lib/pythonX.Y/` (`digest.md` §3.3).
  - **"Symlinks"** to system executables. In our digest this is `bin/python` → the real interpreter.
  - **"Scripts"**. In our digest these are `activate` and friends.
  - The slide does not name `pyvenv.cfg`, which our digest uses to explain how Python knows it is in a venv.
- **"sandboxes"** (55); **"layer of abstraction"** (52); **"configuration file"** / "configurations file" (53–54, 60).
  - The README never says "configuration file". In the uv world, that role is played by `pyproject.toml` plus `uv.lock`.
- **Environment names** "env_ac215" (52) and "env_AC215" (53–54), with the case changing between slides, and "env_ai4" (54).
- **"Reproducible Research"**, **"Explicit Dependencies"**, "Enhanced Engineering Collaboration", "Setup Challenges", **"Lack of Isolation"**, "OS Compatibility Issues" (56).
- **Tool names** (57): "venv (python3)", "conda", "pipenv", "mamba", "uv"; "Anaconda" (51, 61); "pew" (60); **"YAML (YAML Ain't Markup Language)"** (62).
- **"Pipfile"**, **"Pipfile.lock"**, **"[dev-packages]"**, "development vs. production environments" (63).
  - The repo's `pipenv` branch uses these files (`digest.md` §3.7, Part C). The `main` README doesn't.
- **"Drop-in replacement for pip and pip-tools"**, "Built-in virtual environment management", **"[dependency-groups.dev]"** (65).
  - Our digest describes uv as one tool replacing five (venv, pip, pip-tools, pyenv, pipx).
  - It also notes that a uv venv contains no `pip`, which matters if "drop-in" is read literally (`digest.md` §3.7, E3).
- **"project environment"**, "clean project workflow" (66); **"The Two Key Files and a Key Directory"** (68).
  - The lecture says `uv.lock` is "not human readable" (65). It is plain TOML text: readable, but generated and not meant to be edited by hand. The same goes for `Pipfile.lock`, which is JSON (63).
  - The README calls the lock a "lock file" that "pins exact versions". The lecture says "exact versions selected" (68), which is the same idea.
- **"MLOps & LLMOps: Production AI Systems"** (intro 1); **"Milestone Evaluations"**, **"MS2–MS4"**, "TF meetings", "Quizzes", "DCE students", "Edstem" (intro 17); "Directed Execution", "The Expertise Gap" (intro 13); "play the sport" (intro 14, 18).

## Commands and code on the slides

VM tutorial (slide 48, under the SSH screenshot):

```
git clone https://github.com/dlops-io/simple-translate.git
```

Maggie's interpreter before and after creating an environment (slides 51–52):

```
$ which python
/c/Users/maggie/Anaconda3/python                       (slide 51)
/c/Users/maggie/Anaconda3/envs/env_ac215/python        (slide 52)
```

venv (slide 60):

```
python3 -m venv your_env_name
source your_env_name/bin/activate
pip install package_name==version
pip list
deactivate
pip freeze > requirements.txt
pip install -r requirements.txt
```

To remove an environment, slide 60 says to delete its directory. A side note says venv cannot list environments by itself, and suggests the separately installed `pew`.

conda (slide 62):

```
conda env list
conda create --name your_env_name python=3.7
conda activate your_env_name
conda install package_name=version
conda deactivate
conda env export > my_environment.yml
conda env create -f environment.yml
```

The environment folder lands at `/Users/your_username/[opt]/anaconda3/envs/your_env_name`. Note that the slide exports to `my_environment.yml` but recreates from `environment.yml`.

pipenv (slide 64):

```
pip install pipenv
pipenv install
pipenv shell
pipenv install numpy
pipenv sync
exit
```

uv, the basic workflow (slide 67):

```
uv init --bare
uv add <package-name>
uv run <command>
source .venv/bin/activate      # way 1: activate, then
python cli.py
uv run python cli.py           # way 2: no activation
```

The two key files and the key directory (slide 68): `pyproject.toml`, `uv.lock`, `.venv/`.

uv for simple-translate (slide 69):

```
uv init --bare
uv add googletrans==4.0.2 art
uv run python cli.py
```

What that creates (slide 69):

```
pyproject.toml        # project dependencies
uv.lock               # exact versions
.venv/                # installed environment
```

After the first time (slide 70):

```
uv sync
uv run python cli.py
```

Configuration keys named on the slides: `[dev-packages]` in the Pipfile (63) and `[dependency-groups.dev]` in pyproject.toml (65).

**How these compare with the README.**

- The README's walkthrough commands never appear on the slides:
  - `sudo apt-get update`, `sudo apt install git`, `sudo apt install python3-pip`;
  - `sudo pip3 install --break-system-packages googletrans==4.0.2 art`;
  - `curl -LsSf https://astral.sh/uv/install.sh | sh`, `source $HOME/.local/bin/env`;
  - `python3 cli.py -t … -s … -d …`.
- The README's Part B is slide 70's path, with activation as on slide 67: `uv sync`, then `source .venv/bin/activate`, then `python cli.py`.
- Slide 69's `uv init --bare` is for starting a project from scratch. Run inside the cloned repo, it stops with "Project is already initialized" because `pyproject.toml` already exists (checked with uv 0.11.32).
- `uv init --bare` writes no `description` or `readme` lines (checked with uv 0.11.32). The repo's `pyproject.toml` has both, so it came from a plain `uv init` (`digest.md` E12). Its dependency lines, `googletrans==4.0.2` and `art>=6.5`, are what slide 69's `uv add` produces.
- The intro deck has no commands.

## What the lecture stresses

- **The model is half the journey.**
  - The question after "Best Model" is "Now What ?" (19, 25–26).
  - Intro 15 makes the same point: the other half is a reliable, scalable, usable system.
- **Production problems are coordination problems, not six separate bugs** (8). Standardising infrastructure through automation, containers and Ops is called "absolutely essential" against environmental drift (7).
- **"It works on my machine" is the headline failure** (7, 31). Slides 28–30 show where it comes from: each stage and each person runs a different OS and Python setup.
- **The three requirements:** shareable isolated environments, a common OS whatever the host OS, and tracked installs (32). Every tool in L01–L02 is measured against them.
- **Choose a model on several criteria, not accuracy alone:** memory, execution time and other metrics (25).
- **Use a personal cloud account.** Register with any email you control, and don't tie it to a university or employer domain (42).
- **In the VM tutorial, select all defaults** (46).
  - The README gives no VM settings either (`digest.md` E9).
  - Our digest suggests e2-small and warns that the image decides whether uv downloads a Python.
- **VMs are not free lunch.** The lecture lists hardware dependence, large size, overhead, slower performance, slow start-up and weaker graphics (38). These become the motivation for containers in L02 (slides 5–7 there).
- **Virtual environments don't isolate completely, and may not carry across operating systems** (56). Our digest says the same: a venv isolates Python packages only, not system libraries or the OS (`digest.md` §3.3).
- **Share the environment as a file, not as instructions.** Maggie and John exchange a configuration file, and the receiver rebuilds from it (53–54). The same lesson recurs in `pip freeze` / `-r` (60), `conda env export` / `create -f` (62), `pipenv sync` (64) and `uv sync` (70).
- **Keep the human-edited manifest separate from the generated lock,** and keep dev dependencies separate from production ones (63, 65, 68).
- **This course uses uv** as its primary environment and package manager, to standardise development (58).
- **Once a project is set up, don't re-add libraries; run `uv sync`,** which installs the exact versions from `uv.lock` (70).
  - This conflicts with the repo: at `62f821b` it commits no `uv.lock` (`digest.md` E1). A fresh clone's first `uv sync` therefore resolves anew and writes a new lock, instead of installing a locked set.
  - In the same spirit, `requires-python = ">=3.13"` is a constraint, not a pin, so uv may download a Python (`digest.md` E6).
- **You don't need to activate.** `uv run` runs code inside the project environment (67, 69).
- **Removing a venv is just deleting its folder** (60).
- **Intro deck:**
  - You must be able to build the system without generative AI, slower but knowing every step; AI helps you build faster, and the course makes sure you understand what you build (intro 11).
  - Autonomous agents are not ready, guided agents are, and AI multiplies existing expertise (intro 13).
  - You can't coach a sport you never played (intro 14).
  - Quizzes are in person only for on-campus students, with no online option and no make-ups; DCE students take them online (intro 17).
  - The syllabus is the "ultimate source of truth" (intro 16).
  - "Decision time" on whether the course is for you (intro 18).
- **What the slides leave out that the README covers.** None of these appear on the slides; they are README-only, and our video teaches them from the README and the captures:
  - PEP 668 and `--break-system-packages`;
  - installing pip for the system Python;
  - installing uv and putting it on `PATH`;
  - what activation changes;
  - deleting the VM to stop charges, which the README repeats after both walkthroughs.

## Pointers

- **Formaggio, the reference project:** linked on slides 20–21, the latter with a "Project Summary" link whose target is not in the extracted text. Live site: `http://formaggio.me` (26).
- **VM tutorial (slide 40, with a QR code):** `https://github.com/dlops-io/simple-translate#installing-app-on-vm-manually`, link text "Installing App on VM Manually".
- **Google Cloud (slide 41):** `https://cloud.google.com`.
- **Virtual-environment tutorial (slide 72, with a QR code):** `https://github.com/dlops-io/simple-translate?tab=readme-ov-file#installing-app-on-vm-using-uv-t2`.
  - The `-t2` anchor matches no heading of the README at `62f821b`.
  - Slide 40's anchor lacks the emoji-derived prefix of the real heading anchor (`#%EF%B8%8F-installing-app-on-vm-manually`, as the course site encodes it; `digest.md` header and E8).
  - Both links probably open the README at the top.
- **Further readings on uv (slide 71):**
  - official docs, `https://docs.astral.sh/uv/`;
  - a SaaS Pegasus deep dive, `https://www.saaspegasus.com/guides/uv-deep-dive/`;
  - a Medium article, "UV vs PIP", `https://medium.com/@sumakbn/uv-vs-pip-revolutionizing-python-package-management-576915e90f7e`;
  - a DataCamp tutorial, `https://www.datacamp.com/tutorial/python-uv`.
- **Forward references:**
  - Containers are covered "next week" (33–34, 49): L02 Containers I.
  - The slide-17 stack previews later lectures: DVC and Label Studio (data versioning and labelling), Vertex AI, FastAPI and FastMCP, React/Next.js, GitHub Actions, Pulumi and Kubernetes.
  - Slide 39 calls simple-translate the foundation for later implementation, deployment and production work.
- **Logistics (slide 74):** three links, "Survey", "Make project groups" and "Setup & Installations". Their targets are not in the extracted text.
  - L02's slide 2 repeats the survey and the team form (see `../ac215-l02-containers-1/SLIDES.md`).
  - "Setup & Installations" is presumably Tutorial 0, `dlops-io/ac215-setup`, which the README names as a prerequisite.
- **Course staff (intro 9):** `https://harvard-iacs.github.io/2026-AC215/staff/`.
- **Course logistics (intro 16):** a pre-recorded logistics video and the course syllabus. Questions go to the community forum or office hours.
- **Assessment (intro 17):**
  - Quizzes: short (20–30 min), in class, theory plus short coding tasks, on recent material. A test quiz is on Ed, `https://edstem.org/`.
  - Milestone evaluations: end-to-end ML pipelines judged on quality, scalability and reliability. For MS2–MS4, each team gives a 15-minute presentation in the weekly TF meeting.
  - Milestone guidelines are on Ed: `https://edstem.org/us/courses/97373/lessons/180730/slides/1062993`.
- **No homework or milestone deadline** appears in either deck.
