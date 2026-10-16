# L18 lecture slides — APIs and Frontend

Source: two decks for one lecture. `L18a_apis_and_frontend_apis` (47 slides) is titled "Lecture 18:
APIs", and `L18b_frontend` (42 slides) is titled "Lecture 18: Frontend". Both are by AC215/E115,
Pavlos Protopapas and Shivas Jayaram, 89 slides in all. These are the instructor's lecture slides
(PDF), provided by the student for study; the PDFs are not in this repository; slide numbers are PDF
page numbers. In this file **A*n*** means slide *n* of the APIs deck (`L18a`) and **B*n*** means
slide *n* of the Frontend deck (`L18b`). This digest was written from both decks' extracted text and
from every contact sheet, with enlarged tiles for A4, A11, A14, A17–A19, A24, A28, A30–A32, A42,
B5, B17, B24 and B27. Everything below is paraphrased; only short titles, terms, URLs and single
code lines are quoted. The tutorial side of the lecture is in [`digest.md`](digest.md).

## Outline

**Deck A — "Lecture 18: APIs" (47 slides).** It has three numbered sections (A2). Divider slides
repeat the outline with the current section in bold.

- Slide A1 · title slide
- Slide A2 · outline (Recap; Technical Architecture Review; APIs)
- Slides A3–A5 · **1. Recap**
  - A3 · section divider
  - A4 · "Recap: Cheese App Status": the POC → Prototype → MVP roadmap, with "Build Cheese App"
    marked as the current step
  - A5 · "Recap: Cheese App Development": the ML pipeline (ticked) and the App Dev pair
    (Backend API, Frontend) on GCP
- Slides A6–A22 · **2. Technical Architecture Review**
  - A6 · section divider
  - A7 · what a technical architecture is and what it is for
  - A8–A18 · "Building a Technical Architecture": the diagram is assembled one layer per slide
  - A19 · "Technical Architecture": the finished diagram
  - A20 · the same diagram behind a smiley: "App is ready!"
  - A21 · the punchline: "Well not really, we need to build it"
  - A22 · "Technical Architecture Building Blocks (Comparison)": GCP vs AWS vs Azure product names
- Slides A23–A46 · **3. APIs**
  - A23 · section divider
  - A24 · "Review: Microservice Architecture", now with an MCP Service and Agents added
  - A25 · "Review: What is HTTP?"
  - A26 · "Review: What is a port?"
  - A27 · "What is an API": API → Web API → REST API, built with FastAPI
  - A28 · "APIs": in this course "API" means REST API, the connector between clients and back ends
  - A29 · "Review: Screenflow & Wireframes": the three Cheese App screens
  - A30–A32 · "API Design Patterns": three ways to wire users, agents, an API service and an MCP
    service to the same back ends
  - A33 · "API & MCP": the two side by side
  - A34–A41 · "How does an API work": one request to `localhost:9000/newsletters`, built up step
    by step on a local machine
  - A42 · "How does an API work (In Production)": the same request against a domain on a GCP
    server
  - A43 · "Setup & Code Organization": the repository folder layout and the secrets folder
  - A44 · "Tutorial: APIs": the API service and its six route groups
  - A45 · "Tutorial: APIs": the steps and the tutorial link
  - A46 · "Tutorial: Building Solution Architecture": a group exercise for the project
- Slide A47 · closing "THANK YOU"

**Deck B — "Lecture 18: Frontend" (42 slides).** It has five numbered sections (B2). Section 2
is called "Frontend (Simple)" on B2–B3 and "App Frontend (Simple)" from B15 on.

- Slide B1 · title slide
- Slide B2 · outline (Recap; Frontend (Simple); Frontend Frameworks; Frontend App (React); App
  Building Crash Course)
- Slides B3–B14 · **1. Recap**
  - B3 · section divider
  - B4 · "Recap: Cheese App Status" (the A4 roadmap, with only "Build Cheese App" marked)
  - B5 · "Recap: Cheese App Development" (the A5 picture, now with Backend API ticked too)
  - B6 · "Recap: Screenflow & Wireframes" (= A29)
  - B7–B14 · "Recap: How does an API work" (= A34–A41, one for one)
- Slides B15–B28 · **2. App Frontend (Simple)**
  - B15 · section divider
  - B16 · "App Frontend": what HTML, CSS and JavaScript each do
  - B17 · "App Frontend": a tiny annotated HTML page and how it renders
  - B18–B23 · "How does the App work": the browser fetches `newsletters.html` from the
    frontend container on port 8080 and renders it
  - B24–B26 · "How does the App work": the page's JavaScript then calls the API on port 9000 and
    draws the newsletters
  - B27 · "How does the App work (Chat)": the same round trip for a chat message, numbered 1–6
  - B28 · "Tutorial: Frontend Simple": the tutorial link
- Slides B29–B33 · **3. Frontend Frameworks**
  - B29 · section divider
  - B30 · one HTML page per feature
  - B31 · the problems that causes
  - B32 · the fix: a single-page app built from components, using a framework
  - B33 · the common frameworks (React highlighted)
- Slides B34–B38 · **4. Frontend App (React)**
  - B34 · section divider
  - B35 · "React": components and JSX
  - B36 · "React App": the Header / Content / Footer layout
  - B37 · "React App": the header is defined once, the content block is swapped per page
  - B38 · "Tutorial: Frontend React": the tutorial link
- Slides B39–B41 · **5. App Building Crash Course**
  - B39 · section divider
  - B40 · "Tutorial: App Building Crash Course": a GitHub repo
  - B41 · "Tutorial: App Building Template": a GitHub repo
- Slide B42 · closing "THANK YOU"

## Key ideas

1. **The project has moved from the ML pipeline to the app.** On the roadmap, the current step is
   "Build Cheese App" in the MVP phase. The tail of "Design Cheese App" is also boxed in A4 (the app's
   design is revisited), but not in B4. The four pipeline components (collector, processor, training,
   deploy, plus a vector DB) are ticked. What remains is "App Dev": a Backend API and a Frontend
   running on GCP Compute Engine. Between the two decks the Backend API also gets its tick, so the
   APIs lecture comes first and the frontend builds on it. (A4, A5, B4, B5)
2. **A technical architecture is the system's blueprint.** It shows the whole path from
   development to deployment and how the components, i.e. the containers, talk to each other. Its
   job is to help a team design the app, see the big picture and onboard new members. (A7)
3. **Three kinds of people touch the system through different tools.** Developers build app
   components from an IDE or CLI, always inside containers. Data scientists explore data and
   models in Colab or JupyterHub notebooks, build ML tasks in an IDE (also containerized) and use
   LLMs. Users only have a browser: they upload images, see predictions and chat. (A8–A10)
4. **The architecture is built up one layer at a time.** First come source control (GitHub),
   notebooks (Colab), a Vertex AI pipeline of tasks plus Gemini, and the app. Then a GCP boundary
   is drawn, every arrow gets a protocol and port, and a GCS bucket for "Data & Models" appears.
   The app becomes "Single Compute Instance/ Kubernetes Cluster". Google Artifact Registry
   holds one image per component, and Vertex AI runs the pipeline containers from it. A GCE
   persistent volume is attached over NFS. Finally the cluster is filled with an NGINX container
   in front of the frontend ("Cheese App"), API service and vector DB containers. (A11–A19)
5. **Drawing the architecture is not building it.** The finished diagram earns an "App is
   ready!" smiley, immediately followed by "Well not really, we need to build it". The
   right-hand side (the cluster) is what the coming lectures build. (A20, A21)
6. **The same building blocks exist on every cloud.** Container registry, object storage, ML
   platform, hosted LLMs, persistent storage, virtual machines and managed Kubernetes each have a
   GCP, an AWS and an Azure product. The architecture transfers, only the product names change.
   (A22)
7. **A microservice back end puts one API service in front of many modules.** Browser, mobile
   and edge-device apps all speak REST/JSON to a single API service. The API service fans out to
   modules, and each module owns its own store (database, cloud store, models). The new element is
   an MCP service that gives AI agents the same reach into those modules. (A24)
8. **HTTP is request and response, and ports tell traffic apart.** A client asks, a server
   answers, and the content can be anything from text to video. HTTPS is the encrypted version.
   A port is the endpoint where a network connection starts or ends. The lecture's examples are
   22 (SSH), 25 (SMTP), 80 (HTTP) and 443 (HTTPS). (A25, A26)
9. **"API" in this course means a REST API.** An API is an application programming interface. A
   Web API is one reached over HTTP/S. A REST API is a Web API that sticks to the HTTP methods
   GET, POST, PUT and DELETE. The course builds them with FastAPI. Such an API is the one
   connector between all client types and the server's cloud stores, databases and models.
   (A27, A28)
10. **The screens decide the APIs.** The wireframes show three screens: a newsletter list, a
    podcast list with a player, and a chat that accepts a cheese photo ("What type of cheese is
    this?" → "Brie"). Each screen needs data from the API. (A29, B6)
11. **There are three ways to put agents next to an API.** (a) The browser calls the API
    service. The API service hands work to an agent, and the agent reaches the back ends through
    an MCP service. (b) The same, but the agent calls the back ends directly, with no MCP layer.
    (c) The agent itself is the client, in a desktop or mobile app with no browser. It calls the
    API service and the MCP service side by side. In all three, the same four back ends sit on the
    right: Newsletters, Podcasts, Image Model and Cheese KB. (A30–A32)
12. **API and MCP are parallel standards for different callers.** REST APIs are for
    applications, are reached over HTTP/S and are built with FastAPI. MCP (Model Context
    Protocol) is a universal standard for agent-to-tool communication. Remote MCP servers are
    reached with SSE (Server-Sent Events) over HTTP/S and are built with FastMCP. (A33)
13. **A request to a containerized API passes through four hops.** The browser asks for
    `http://localhost:9000/newsletters`. The host machine forwards port 9000 to the Docker
    service, `cheese-app-api-service`. Port 9000 on the host is mapped to port 9000 inside the
    container. There FastAPI, started from `api-service/api/service.py`, has a function
    registered for `/newsletters`. That function reads JSON files and returns a list of objects,
    which travels back and appears in the browser as JSON. (A34–A41, B7–B14)
14. **In production only the outside of that path changes.** The URL becomes a domain
    (`https://formaggio.me/api/newsletters`) and HTTPS reaches the server's public IP on 443. The
    host forwards to port 80 of the Docker service, which is mapped to 9000 inside the container.
    The FastAPI code and its port do not change. (A42)
15. **One repository, one folder per service, secrets outside Git.** The application root is
    the GitHub root. Under `src/` each service has its own folder: API service, data collector,
    data processor, model training, model deploy, ML workflow, two frontends, vector DB, Postgres
    DB. A `secrets` folder with the service-account key sits next to the repository, never in it.
    (A43)
16. **The tutorial's API service has six route groups:** Newsletters, Podcasts, LLM Chat, LLM +
    CNN Chat, RAG Chat and Agent Chat. Building them takes two steps: make sure the vector
    database is running, then expose the data through the API. (A44, A45)
17. **A web page is three languages.** HTML gives structure and content, CSS gives style, and
    JavaScript, the one programming language the browser runs, gives behavior. B17 maps each
    part of a small page to what you see: the title in the tab, the background style, the body
    text and a script. (B16, B17)
18. **A simple frontend is two separate round trips from the browser.** First the browser gets
    `newsletters.html` from the frontend container. `http-server` there serves the file on port
    8080, and the browser renders it. Then the JavaScript in that page runs *in the browser* and
    sends its own request to the API on port 9000. When the list comes back, the JavaScript draws
    the newsletter grid. A chat message follows the same path, numbered 1–6 on B27: request,
    host forwarding, port mapping, FastAPI handler (Gemini generates the text), response, display.
    (B18–B27)
19. **One HTML page per feature does not scale.** With `index.html`, `newsletters.html`,
    `podcasts.html` and `chat.html`, every page carries its own HTML, JavaScript and CSS, so
    nothing is shared, and every page loads separately, which is slow. The fix is a single-page app
    that manages HTML, JavaScript and CSS as components, built with a frontend framework: Angular
    (Google), React (Facebook), Vue or Svelte. The course uses React. (B30–B33)
20. **React: everything is a component, written in JSX.** JSX extends JavaScript and works like
    a template language with the full power of JavaScript. A React app is laid out as Header,
    Content and Footer. The header is written once and reused on every page; only the content
    block changes from page to page. (B35–B37)
21. **Next come your own app and architecture.** Two dlops-io repos, an app-building crash course
    and an app-building template, are the starting point for the project's app. A group exercise
    asks each team to describe its project's Process, Execution and State, and to draw a Solution
    Architecture and a Technical Architecture. (A46, B40, B41)

## Diagrams

- **A4 (= B4) · project roadmap (Gantt-style).** A wide light-blue arrow runs left to right with
  three phase labels, "POC", "Prototype" and "MVP". Dashed vertical lines mark the phase
  boundaries. Below it are staggered horizontal bars:
  - "Design Cheese App": from the start to the end of Prototype.
  - "Data Collection" and "Setup Experiment Tracking": early POC.
  - "Build Baseline Models": late POC.
  - "Build Better Models" and "ML Workflow": stacked in Prototype.
  - "Build Cheese App": all of MVP.
  - "Deployment, Scaling & Automation": from mid-Prototype to the end.

  A red dashed rectangle surrounds "Build Cheese App" (the you-are-here marker). In A4 only, a
  second red dashed box frames a short extra slice at the end of the "Design Cheese App" bar,
  where Prototype turns into MVP. Purpose: place the lecture on the project timeline.
- **A5 (= B5) · Cheese App development on GCP.** Two dotted panels sit side by side.
  - Left, "ML Pipeline": four tiles in a row joined by small blue double arrows. "Data
    Collector" (red, download icon), "Data Processor" (blue, gears), "Model Training" (yellow,
    light bulb) and "Model Deploy" (green). A "Vector DB" tile (orange, database icon) sits
    under Model Deploy. A green check sits on the panel's corner.
  - Right, "App Dev": "Backend API" (purple, gear icon) and "Frontend" (teal, phone icon). There
    is no check in A5. In B5 a green check sits on Backend API.

  Grey double arrows connect both panels down to a dashed "Google Cloud Platform" strip holding
  "Cloud Storage", "Vertex AI" and "Compute Engine". Purpose: progress tracker. The pipeline is
  done, and L18 builds the right panel (the API first, then the frontend).
- **A8–A19 · the technical architecture, built up layer by layer.** Every slide keeps the
  previous one and adds a layer, so a scene can animate it the same way. The final layout (A19):
  - **Top band (pink).** On the left, "Developers / Data Scientists" with an "IDE/ CLI" box, three
    small dashed green "Containers" squares and a "Browser" box. On the right, "Users" with a
    "Browser".
  - **Left column.** "Source Control" holds GitHub. A down arrow runs from the developers'
    containers into it.
  - **Centre left.** "Colab" holds "Notebooks" (yellow). Below it, "GCS Bucket" holds "Data &
    Models" (grey, cloud icon).
  - **Centre.** "Vertex AI" (blue panel) holds a vertical chain of tasks and a white "Gemini"
    box at the bottom.
  - **Right.** "Single Compute Instance/ Kubernetes Cluster" (grey-green panel).
  - **Bottom left.** "Google Artifact Registry" (lilac) lists "Data Collector Image", "Data
    Processor Image", "⋮", "API Service Image" and "Cheese App Image".
  - **Bottom right.** "GCE Persistent Volume" holds "Persistent Disk".
  - A dotted outline labelled **GCP** wraps Vertex AI, the cluster, the GCS bucket, Artifact
    Registry and the persistent volume. It steps around Colab and GitHub, which stay outside.

  The build order:
  - A8: only the two pink bands.
  - A9: adds the IDE/CLI, the containers and the two browsers.
  - A10: adds three text columns describing developers, data scientists and users.
  - A11: adds GitHub, Colab Notebooks, Vertex AI with "Task 1"–"Task 4" plus Gemini, and an "App"
    panel showing a chat-screen thumbnail. Hollow double arrows join the developer browser to
    Colab and to Vertex AI, and the users' browser to the App.
  - A12: draws the GCP boundary.
  - A13: labels the arrows. Developer browser ↔ Colab "HTTPS 443", developer browser ↔ Vertex AI
    "HTTPS 443", users ↔ App "HTTP/HTTPS 80".
  - A14: adds the GCS bucket, with Notebooks ↔ bucket, bucket ↔ Vertex AI and Notebooks ↔
    Vertex AI, each "HTTPS 443".
  - A15: renames "App" to "Single Compute Instance/ Kubernetes Cluster" (now empty) and empties
    Vertex AI down to Gemini.
  - A16: adds Artifact Registry, with a second down arrow from the developers' containers into it.
  - A17: refills Vertex AI with "Data Collector", "Data Processor", "Model Training" and "Model
    Deploy". A pipe from Artifact Registry runs along the bottom up into Vertex AI ("HTTPS 443"):
    Vertex AI pulls the pipeline images.
  - A18: adds the persistent volume, joined to the cluster by a short double arrow "NFS".
  - A19: fills the cluster. An "NGINX Container" sits at the top. An "API Service Container"
    feeds it on "HTTP 9000" and a "Cheese App Container" feeds it on "HTTP 3000". A "Vector DB
    Container" connects to the API service on "HTTP 8000". New "HTTPS 443" links run Vertex AI ↔
    cluster (Gemini and models), GCS bucket ↔ cluster (a long double arrow under Vertex AI), and
    the Artifact Registry pipe now also rises into the cluster (it pulls the app images).

  Purpose: one picture of where every L1–L17 piece lives and how traffic flows, with ports on
  every edge. It also previews later lectures: NGINX, a VM or Kubernetes, Artifact Registry and
  persistent disks.
- **A20, A21 · the punchline overlay.** A big red smiley covers the cluster, captioned "App is
  ready!" (A20). A21 adds "Well not really, we need to build it". Purpose: honesty about scope.
  The cluster side is still to be built.
- **A22 · comparison table** (a table, not a mechanism). Seven rows of building blocks, one
  column each for GCP, AWS and Azure. The names are listed under *Terms* below.
- **A24 · microservice architecture.**
  - Left: three client icons, "Browser Apps", "Mobile Apps" and "Edge Device Apps". Their
    "REST / JSON" lines merge into one bus.
  - Centre: the bus points to "API Service" (gold, large). Above it, "Storefront UI" (blue) sends
    "HTML" back to the browser apps.
  - Bottom left: "Agents" (red robot icon) connects with a red arrow to "MCP Service" (red,
    dashed border, the new element).
  - Right: the API service and the MCP service both feed one vertical bus to four modules, each
    with a double arrow to its own store. "Catalog Module" (green) → Database, "Reviews Module"
    (orange) → Cloud Store, "Orders Module" (red) → Database, "Recommendation Module" (purple) →
    Models.

  Purpose: the API (or MCP) layer is a single front door. Clients and agents never touch a
  module's store directly.
- **A25 · HTTP request/response.** A laptop on the left and a server rack on the right, joined
  by a loop of two arrows: "HTTP Request" on top (laptop → server) and "HTTP Response" below
  (server → laptop).
- **A28 · REST as the connector.** Browser, mobile and edge-device apps on the left, each with a
  "REST / JSON" line, merge into one line that crosses a dashed vertical divider (client side |
  server side) to a "Server" icon. The server fans out to "Cloud Stores", "Databases" and
  "Models". Purpose: every client speaks the same REST/JSON to one server, and the server alone
  talks to storage and models.
- **A29 (= B6) · screen-flow wireframes.** Three greyscale phone-style screens, each headed
  "Cheese App" with a hamburger icon:
  - Newsletters: a welcome blurb and a card, "Exploring Alpine Cheeses".
  - Podcasts: a welcome blurb and an episode card, "Episode 1 Halloumi [EN]", with a play button.
  - Chat: a user bubble with a cheese photo and "What type of cheese is this?", a bot bubble
    "Brie", and an input "How can I help you?" with a camera icon and a send arrow.

  Purpose: the API routes needed follow from these screens.
- **A30–A32 · API design patterns.** Grey line drawings. On the right, the same four rounded
  boxes are joined by one vertical bus: "Newsletters", "Podcasts", "Image Model" and "Cheese KB".
  "API Service" and "MCP Service" are drawn as dotted boxes, meaning a role rather than a
  concrete server.
  - A30: "Users" (people icon) → "Browser" → "API Service" → bus. A line drops from the API
    service to "Agents" (robot icon), and the agents → "MCP Service" → bus.
  - A31: the same, but the MCP service is gone. The agents' line runs straight into the bus.
  - A32: the browser is gone. Users → "Agents" inside a dotted frame labelled "Desktop / Mobile".
    From the agents, one line goes over the top to the API service and another to the MCP service.
    Both services connect to the bus.

  Purpose: show where an agent can sit (behind the API, or as the client) and what MCP adds (a
  standard tool interface instead of hard-wired calls).
- **A34–A41 (= B7–B14) · "How does an API work", step by step.** The layout is fixed. On the
  left, a browser window labelled "Browser" with the address `http://localhost:9000/newsletters`.
  On the right, a laptop outline labelled "Local computer / Server" holding a blue "Container"
  box. A dashed vertical line separates the two sides. Red arrows and red notes are added one per
  slide:
  - A34: a red arrow to the right, "HTTP request made to localhost". The laptop is labelled
    `localhost:9000` and the container `cheese-app-api-service:9000`.
  - A35: + "Host machine forwards request to port 9000 of docker services".
  - A36: + "Port 9000 is mapped to 9000 inside the container".
  - A37: a `localhost:9000` tag appears inside the container.
  - A38: the container shows a file path `api-service` / `-api` / `-service.py`, with the note
    "FastAPI is running on port 9000 serving /newsletters".
  - A39: a dotted code panel opens next to the container with the route function (see *Commands
    and code*).
  - A40: a red arrow back to the left: "/newsletters was requested so the results of the
    /newsletters will be sent back to browser. In this case is a list of objects".
  - A41: the browser fills with a JSON array of two newsletter objects (fields `id`, `dts`,
    `title`, `excerpt`, `detail`, `readTime`, `category`, `image`, e.g. "Spanish Cheese Journey",
    "The Art of Blue Cheese").

  Purpose: make the port-forwarding chain from browser → host → Docker → container → function
  concrete.
- **A42 · the same chain in production.** The layout is the same, with the right side labelled
  "GCP Server". The address is `https://formaggio.me/api/newsletters` and the arrow reads "HTTPS
  request made to server". The laptop is labelled `12.12.12234.34:443` and the notes say the host
  forwards "to port 80 of docker services". The container is `cheese-app-api-service:80` and
  "Port 80 is mapped to 9000 inside the container". FastAPI still runs on 9000. The browser
  already shows the JSON. Purpose: only the outer address and ports change between laptop and
  cloud. (The IP is a placeholder: 12234 is not a valid octet.)
- **A43 · code organization tree.** A dotted box holds a monospace tree. An arrow labelled
  "Github root" (blue) points to `/application-root-folder`, and an arrow labelled "Secrets
  (outside git folder)" (red) points to `/secrets`. Purpose: the repository layout convention.
- **A44 · the tutorial API's route groups.** A gold "API Service" box on the left. A bracket
  of arrows fans out to six coloured boxes: "Newsletters" (green), "Podcasts" (orange), "LLM Chat"
  (red), "LLM + CNN Chat" (teal), "RAG Chat" (blue) and "Agent Chat" (purple). Purpose: one
  service, one router per feature.
- **B17 · anatomy of an HTML page.** On the left, a code box with a minimal page (doctype, head
  with title and an inline style, body text, a script). Red arrows run from four parts of the code
  to labels on the right: the `<title>` → "Browser Title", the `<style>` → "Page Style", the body
  text → "Web page details", the `<script>` → "Web page scripts (Javascript)". Below the labels, a
  browser screenshot at `localhost:8080/index-simple.html` shows the rendered result, the tab
  title "🧀 Formaggio" and the text "Formaggio.me is here!".
- **B18–B23 · fetching the page from the frontend container.** The same browser / laptop layout
  as A34, now with the address `http://localhost:8080/newsletters.html`. Each slide adds one note:
  - B18: "HTTP request made to localhost". The laptop is `localhost:8080` and the container
    `cheese-app-frontend-simple:8080`.
  - B19: + "Host machine forwards request to port 8080 of docker services".
  - B20: + "Port 8080 is mapped to 8080 inside the container". The file path `frontend-simple` /
    `-newsletters.html` appears with "http-server is running on port 8080 serving
    /newsletters.html".
  - B21: a dotted panel shows the file's skeleton, `<!DOCTYPE html> <html> … </html>`.
  - B22: a return arrow, "the content of the /newsletters.html will be sent back to browser. The
    HTML is sent back to the browser".
  - B23: the browser shows the rendered page (a dark header bar with navigation and an empty
    body), noted "Browser renders the HTML content received from the server".
- **B24–B26 · the page's JavaScript calls the API.**
  - B24: inside the browser, "Javascript in the Browser is executed", with a dotted code panel
    (an axios base URL and a GET, see below) hanging off the browser. A red arrow labelled "HTTP
    request made to http://localhost:9000/newsletters" goes to a laptop whose container is
    blank. The frontend container is no longer drawn: the call starts in the browser, not in
    the 8080 container.
  - B25: the right side fills in with the full A40 API chain (9000 forwarding, port mapping,
    FastAPI, route code) and the return arrow "a list of objects".
  - B26: the code panel is gone. The browser shows newsletter cards with cheese photos, noted
    "Javascript displays the newsletters data in the html page."
- **B27 · the chat round trip, numbered.** The browser is at `http://localhost:8080/chat.html`
  and shows a dark chat UI with a long bot answer. Six pink numbered circles mark the order:
  - 1: the request arrow, "HTTP request made to http://localhost:9000/chat".
  - 2: "Host machine forwards request to port 9000 of docker services" at `localhost:9000`.
  - 3: "Port 9000 is mapped to 9000 inside the container".
  - 4: "FastAPI is running on port 9000 serving /chat", with a code panel showing a POST handler
    whose comments say it chats with an LLM, RAG or agent and uses Gemini to generate text.
  - 5: the return arrow, "/chat was requested so the results of the /chat will be sent back to
    browser. In this case it is the chat details".
  - 6: "Javascript displays the chat details in the html page."

  Purpose: the chat feature is the same mechanism as newsletters, only with a POST and an LLM
  inside.
- **B36 · React page layout.** Three stacked blocks: a black "Header" bar, a large grey
  "Content" area, and a light "Footer" bar.
- **B37 · reuse in a React app.** Three screenshots of the real Cheese App side by side: the home
  hero ("Formaggio.me is here!"), the newsletters grid, and the "Cheese Assistant" chat. Red
  arrows from the label "Header defined only once" at the top point to all three header bars.
  Red arrows from "Content block switched for each page" at the bottom point to the three bodies.
  Purpose: a component (the header) is written once, and pages differ only in the content
  component.
- Not diagrams: A1/B1 and A47/B42 (title and closing slides), the outline and divider slides
  (A2, A3, A6, A23, B2, B3, B15, B29, B34, B39), and the bullet-only slides A7, A10 (text part),
  A26, A27, A33, A45, A46, B16, B28, B30–B33, B35, B38, B40 and B41.

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Cheese App", "Formaggio.me", `formaggio.me` | A4, A5, A29, A42, B17 | The README title is "Cheese App - APIs & Frontend". The digest calls the app "Formaggio.me". |
| "Technical Architecture", "Building a Technical Architecture", "Blueprint of the system" | A7–A21, A46 | Not in the README. The v1 README shows a "container architecture" image instead. |
| "Solution Architecture"; "Process, Execution, State" | A46 | Project-milestone vocabulary. It does not appear in the tutorials. |
| "Developers / Data Scientists", "Users", "IDE/ CLI", "Containers" | A8–A19 | The roles behind the diagram. |
| "Source Control", "Colab", "Notebooks", "Vertex AI", "Gemini", "Task 1"–"Task 4" | A11–A19 | Earlier lectures' pieces (L05–L15). |
| "GCS Bucket" / "Data & Models" | A14–A21 | The v2 API passes `GCS_BUCKET_NAME` but never reads it. Newsletters and podcasts are served from local folders (`news-letters/`, `podcasts/`), a stand-in for a bucket (digest §2, §5). |
| "Single Compute Instance/ Kubernetes Cluster", "NGINX Container", "Google Artifact Registry", "GCE Persistent Volume", "Persistent Disk", "NFS" | A15–A21 | None of these are in the L18 tutorials. They arrive with cheese-app-v3 in L20 (VM + NGINX, Artifact Registry) and L22 (Kubernetes). |
| "API Service Container" / "API Service Image" / "API Service" | A16, A19, A24, A30–A32, A44 | The README folder is `src/api-service`; the image and container are `cheese-app-api-service`. |
| "Cheese App Container" / "Cheese App Image" (port 3000) | A16, A19 | This is the React frontend, `src/frontend-react`, on port 3000. v3 calls it `frontend`. |
| "Vector DB Container" (port 8000), "Vector DB" | A5, A19 | The README's "Vector DB for RAG Setup": ChromaDB as container `cheese-app-vector-db` on 8000. |
| "Container Registry", "Object Storage", "AI / ML Platform", "LLMs", "Persistent Storage", "Virtual Machines", "Kubernetes Service" | A22 | GCP: Google Artifact Registry, Google Cloud Storage, Vertex AI, Vertex AI LLMs, GCE Persistent Volume, Compute Instance, Google Kubernetes Engine. AWS: Elastic Container Registry, S3 Bucket, Amazon SageMaker, Bedrock LLMs, Elastic Block Store, EC2 Instance, Elastic Kubernetes Service. Azure: Azure Container Registry, Azure Blob Storage, Azure Machine Learning, Azure OpenAI Service, Azure Disk Storage, Azure Virtual Machine, Azure Kubernetes Service. |
| "Microservice Architecture", "Storefront UI", "Catalog Module", "Reviews Module", "Orders Module", "Recommendation Module" | A24 | A generic shop example from an earlier lecture. It is not the Cheese App. |
| "MCP Service", "MCP" (Model Context Protocol), "Remote MCPs", "SSE (Server-Sent Events)", "FastMCP", "Agents" | A24, A30–A33 | The v2 API declares `fastmcp` as a dependency (`cheese-app-v2/src/api-service/pyproject.toml:10`), but no code under `api/` uses it. There is no MCP server in L18. Its "agent" chat router is a GET-only stub, commented out in `service.py` (digest §4 B5). |
| "API", "Web API", "REST API", "REST / JSON" | A27, A28, A33 | Same meaning as in the READMEs: v1 builds "our REST API" with "The FastAPI framework", and v2 a "FastAPI-based REST API service". |
| "FastAPI" | A27, A33, A38–A42 | The same framework. The slides never name the server that runs it (uvicorn), the `/docs` page, or routers. |
| "Port", "HTTP", "HTTPS", "HyperText Transfer Protocol", "Port 22 = SSH" … "Port 443 = HTTPS" | A25, A26 | Not explained in the README. The digest assumes ports from L02/L04. |
| "Host machine forwards request to port 9000 of docker services"; "Port 9000 is mapped to 9000 inside the container" | A35–A42, B8–B14, B19–B27 | The README/digest call this publishing a port, `-p 9000:9000` (`-p HOST:CONTAINER`). "docker services" means the running container. |
| `localhost:9000` *inside* the container | A37–A42 | It stands for port 9000 in the container. The digest stresses that the server must listen on `0.0.0.0`, because the container's own `localhost` is not reachable from the host (digest §3.3). |
| "Newsletters", "Podcasts", "LLM Chat", "LLM + CNN Chat", "RAG Chat", "Agent Chat" | A44 | Router prefixes `/newsletters`, `/podcasts`, `/llm`, `/llm-cnn`, `/llm-rag`, `/llm-agent`. In v2, RAG and Agent are commented out (digest §5). |
| "Image Model", "Cheese KB" | A30–A32 | The CNN behind `/llm-cnn` (downloaded at start-up) and the RAG knowledge base (Chroma collection `recursive-split-collection`). |
| "Screenflow & Wireframes" | A29, B6 | Design artifacts from earlier milestones. |
| "Setup & Code Organization", `/application-root-folder`, "Github root", "Secrets (outside git folder)" | A43 | Matches the v1 README title "Cheese App - Setup & Code Organization". The slide's key file is `data-service.json`. v2 instead expects `ml-workflow.json` (API) and `llm-service-account.json` (vector-db CLI). The slide's tree (with `ml-workflow`, `frontend-react`, `postgres-db`) is an idealized layout. v1's `src/` has no `ml-workflow`, `frontend-react` or `postgres-db`, v2's `src/` has only `api-service`, `frontend-simple`, `frontend-react` and `vector-db`, and no repo has a Postgres DB. |
| "App Frontend", "HTML", "CSS" ("Cascading style sheets"), "Javascript" | B16, B17 | — |
| "Frontend (Simple)" / "App Frontend (Simple)", `frontend-simple`, `cheese-app-frontend-simple:8080` | B2, B15, B18–B28 | README "Tutorial (24): Simple Frontend App". The image and container are named `cheese-app-frontend-simple` in the script. |
| "http-server" | B20–B23 | The same Node static server as in the README. |
| "single page app", "components", "Frontend Frameworks", Angular / React / Vue / Svelte | B32, B33 | The README never says "single-page app". |
| "React", "Component", "JSX", "Frontend App (React)" | B34–B38 | The README's "Tutorial (25): React Frontend Setup" is a **Next.js** (App Router) project, and the slides never say Next.js. B37's "Header defined only once" is `src/app/layout.jsx` wrapping every page in `<Header />` / `<Footer />`. |
| "App Building Crash Course", "App Building Template" | B39–B41 | Not in the digest. These are separate dlops-io repos. |

The slides never use these tutorial words: `uvicorn`, `--reload`, `/docs` (Swagger/OpenAPI),
`APIRouter` / `include_router` / prefix, CORS and preflight, Docker network and container DNS
(`cheese-app-network`), `X-Session-ID`, the `/persistent` chat history, Docker Compose, Next.js,
`DataService`, `NEXT_PUBLIC_BASE_API_URL`, `docker-shell.sh`. A video that follows the slides
has to introduce them itself, from the digest.

## Commands and code on the slides

The slides contain **no shell commands** (no `docker`, `sh docker-shell.sh`, `uvicorn` or `npm`).
The code consists of short illustrative snippets.

- A39–A42, B12–B14, B25–B26 (the API handler, in a dotted panel):
  - `@app.get("/newsletters")`
  - `def get_newsletters():`
  - `# Fetch newsletters`
  - `news_letters = []`
  - `... # Read data from json files`
  - `return news_letters`

  In v2 the real route is `@router.get("/")` in `api/routers/newsletter.py`, mounted with
  `prefix="/newsletters"`.
- B27 (the chat handler):
  - `@app.post("/chats")`
  - `def start_chat_with_llm():`
  - `# Chat with LLM / RAG / Agent`
  - `... # Use Gemini to generate text`
  - `return chat`

  The slide's arrows and notes say `/chat`, but the code says `/chats`. In v2 the route is
  `POST /llm/chats` (router prefix `/llm`), and `/llm-cnn/chats` and `/llm-rag/chats` work the
  same way.
- B24–B25 (browser JavaScript, in a dotted panel):
  - `// API URL`
  - `axios.defaults.baseURL = 'http://localhost:9000/';`
  - `// Call the API`
  - `axios.get('/newsletters)` (the closing quote is missing on the slide)
  - `.then((response) => {`
  - `newsletters = response.data;`
  - `// Build the grid`

  The repo's `newsletters-main.js` keeps the base URL in a `DataService` object and calls
  `` axios.get(`${this.baseURL}/newsletters?limit=${limit}`) ``.
- B17 (an HTML page; the repo's `frontend-simple/index-simple.html` is this page without the
  style and script):
  - `<!DOCTYPE html>`
  - `<title>🧀 Formaggio</title>`
  - `<style>body{background-color: #efefef;}</style>`
  - `🧀 Formaggio.me is here!`
  - `var input_file = document.getElementById("input_file");`
- B21–B23: `<!DOCTYPE html>` `<html>` `...` `</html>` (the served file, abbreviated).
- A43 (the folder tree):
  - `/application-root-folder`, then `/src` with `/api-service`, `/data-collector`,
    `/data-processor`, `/model-training`, `/model-deploy`, `/ml-workflow`, `/frontend-simple`,
    `/frontend-react`, `/vector-db` and `/postgres-db`
  - `/secrets` with `- data-service.json`
- Addresses on the slides:
  - `http://localhost:9000/newsletters`, `localhost:9000`, `cheese-app-api-service:9000` (A34–A41,
    B7–B14, B25–B26)
  - `https://formaggio.me/api/newsletters`, `12.12.12234.34:443`, `cheese-app-api-service:80`
    (A42)
  - `http://localhost:8080/newsletters.html`, `localhost:8080`, `cheese-app-frontend-simple:8080`
    (B18–B26)
  - `http://localhost:8080/chat.html`, `http://localhost:9000/chat` (B27)
  - `localhost:8080/index-simple.html` (B17, screenshot)
- Port labels in the architecture (A13–A21): `HTTPS 443`, `HTTP/HTTPS 80`, `HTTP 3000`,
  `HTTP 9000`, `HTTP 8000`, `NFS`.
- The JSON in the browser (A41, A42, B14) has the fields `"id"`, `"dts"`, `"title"`,
  `"excerpt"`, `"detail"`, `"readTime"`, `"category"` and `"image"`. These match the repo's
  `news-letters/*.json`, except that the slide uses ids `"1"`/`"2"` where the files use UUIDs.

## What the lecture stresses

- **Draw the architecture before you build, and keep it current.** It is the blueprint that lets
  a team see the big picture and onboard people (A7). The deck spends 14 slides building one
  (A8–A21).
- **Label every connection with protocol and port.** From A13 on, every arrow carries one
  ("HTTPS 443", "HTTP/HTTPS 80", "HTTP 9000", "HTTP 3000", "HTTP 8000", "NFS"). Port numbers are
  how traffic is told apart (A26). One loose label: A13–A21 put the users' traffic on
  "HTTP/HTTPS 80", while A26 assigns HTTPS to 443 and A42 shows HTTPS arriving on 443.
- **All development is containerized,** for developers and for data scientists' ML tasks alike
  (A10). Every component becomes an image in Artifact Registry (A16).
- **Do not overclaim.** "App is ready!" → "Well not really, we need to build it" (A20, A21).
- **Cloud-agnostic thinking.** The same seven building blocks exist on GCP, AWS and Azure (A22).
- **Use one front door.** All clients reach modules through an API (REST/JSON), and agents through
  MCP. Nothing talks to a module's store directly (A24, A28).
- **Design trade-off: where the agent sits** (A30–A32). Behind the API with an MCP tool layer,
  behind the API calling tools directly, or as the client itself on desktop or mobile. MCP's
  value is a *universal standard* for agent–tool communication (A33).
- **Follow the request hop by hop.** The deck spends eight slides (A34–A41) and repeats them as
  B7–B14 to trace browser → host → port forward → port mapping → container → FastAPI function →
  response. The production slide (A42) shows that the inner part never changes.
- **Secrets stay outside the Git folder** (A43, highlighted in red).
- **The vector database must be running before the API** (A45, first step).
- **The browser, not the frontend container, calls the API.** The simple frontend's container
  only serves HTML. The JavaScript that calls port 9000 runs in the browser (B23–B26). B24 drops
  the frontend container from the picture to make that point.
- **Separate pages do not scale.** No reuse across pages, and every page reloads, which is "Slow"
  (B31, B32). The answer is a single-page app built from components with a framework (B32, B33).
- **Define shared UI once.** The header is written once, and only the content block changes per
  page (B37).
- **Inconsistencies to watch for when re-drawing:**
  - B27 says `/chat` but its code uses `/chats`.
  - B24's JS is missing a quote.
  - A42's IP is not a valid address, and it uses an `/api/` path prefix, while the course's later
    NGINX config routes `/api-service/` (`cheese-app-v3/src/deployment/nginx-conf/nginx/nginx.conf:35`).
  - A43's key file name and folder list do not match the repos (see *Terms*).

## Pointers

- A45: tutorial "Cheese App APIs", `https://github.com/dlops-io/cheese-app-v2#setup-environments`.
  The pinned v2 README (`14f2a14`) has no such anchor. Its sections are "Tutorial (23):
  Environment Setup" (`#tutorial-23-environment-setup`), "Vector DB for RAG Setup" and "Backend
  APIs" (`#tutorial-23-backend-apis`). "Setup Environments" is a heading in the **v1** README.
  The link therefore opens the top of the v2 README.
- B28: tutorial "Frontend Simple", `https://github.com/dlops-io/cheese-app-v2#frontend-app-simple`.
  This anchor is also stale. The v2 heading is "Tutorial (24): Simple Frontend App"
  (`#tutorial-24-simple-frontend-app`). v1 has "Frontend App (Simple) Container".
- B38: tutorial "Frontend React", `https://github.com/dlops-io/cheese-app-v2#frontend-app-react`.
  The v2 heading is "Tutorial (25): React Frontend Setup" (`#tutorial-25-react-frontend-setup`).
- B40: `https://github.com/dlops-io/app-building-crashcourse` ("Tutorial: App Building Crash
  Course").
- B41: `https://github.com/dlops-io/app-building-template` ("Tutorial: App Building Template").
  Neither repo is covered by the digest, and this session could not check them.
- A46: group exercise "Building Solution Architecture". Open the shared Google Slides deck
  (`https://docs.google.com/presentation/d/1O1j-zcud3vTnD_dZpNPSddYpM8eoMRJ9Cds2wWzjEuU/edit?usp=sharing`),
  duplicate its slides 2–4 to the end, add your group name, identify Process, Execution and State
  for your project, and draft its Solution Architecture and Technical Architecture slides.
- A43 matches the cheese-app-v1 tutorial ("Setup & Code Organization"). The course site also lists
  v1 for L18 (digest header), but the slides link only v2.
- A4, A5, B4, B5: the project roadmap. Building the app is the current milestone, and deployment,
  scaling and automation (L20–L23) follow. A15–A19 preview that deployment: a VM or Kubernetes
  cluster behind NGINX, images pulled from Artifact Registry.
- The slides list no readings, demos or homework beyond these.
