# L10 lecture slides — Connecting to the Cloud: Networking, Authentication & Storage

Source: one deck, `L10_connecting_to_the_cloud_3_` (55 slides), titled "Lecture 10: Connecting to
the Cloud: Networking, Authentication & Storage" (AC215/E115, Pavlos Protopapas, SEAS/Harvard).
These are the instructor's lecture slides (PDF), provided by the student for study; the PDFs are
not in this repository; slide numbers are PDF page numbers. I wrote this digest from the deck's
extracted text and from all seven contact sheets, and enlarged slides 9, 18, 20, 21, 22, 30, 32,
34–38, 40, 42, 47 and 48 to read their diagrams, screenshots and arrows. Everything below is in my
own words. Only short titles, terms, URLs and single code lines are quoted. The tutorial side of
the lecture is in [`digest.md`](digest.md).

Four notes for anyone citing the deck:

- **The printed footer numbers are not the slide numbers.** The deck was cut from a longer one.
  Its footers run 1, 3, 9–21, 21, 22–27, (none), 28–56, 62, 59, 61: slides 15 and 16 both print
  21, slide 23 has no footer, and the last three slides are out of order. Always cite the PDF page
  numbers used here.
- **The deck never names its tutorial repo.** The "Tutorial" section (slide 52) is a divider with
  nothing after it but the summary. The course site maps L10 to `cheese-app-v0` (see
  `digest.md`), which the slides do not mention.
- **How the deck maps onto this episode.** The networking section (slides 3–11) revisits the
  gateway → processor app of Containers II (`port_toy`, ports 8090 / 9100 / 9200), which in the
  tutorial becomes three published ports and two Docker networks (`digest.md` §3.5). The
  authentication section (slides 12–38) is the theory behind the tutorial's service-account key
  (§3.1–3.3), but its walkthrough creates `data-service-account`, not the tutorial's
  `llm-service-account`. The GCS section (slides 39–45) uses the L03 Mega Pipeline as its example;
  `cheese-app-v0` never calls GCS (`digest.md` §3.7, exercise E7). The Drive section (slides
  46–51) has no counterpart in the tutorial at all. In the other direction, the slides never
  mention CORS, ADC by name, `0.0.0.0`, Vertex AI or RAG, which the tutorial depends on.
- **The L03 deck previewed this lecture.** Its slide 23 listed the same five auth methods, and its
  slide 70 announced "Connecting to the Cloud" (see
  [`../ac215-l03-mega-pipeline/SLIDES.md`](../ac215-l03-mega-pipeline/SLIDES.md)).

## Outline

The deck has five sections (slide 2). Each section opens with a divider that repeats the outline
with the current section in bold. Slide 2 is the plain agenda (nothing bold); slide 3 doubles as
the divider for section 1.

- Slide 1 · title slide (red AC215/E115 badge, Harvard shield)
- Slide 2 · outline: Networking & Ports; Security and authentication (detour); Google Cloud
  Storage; Connecting to Google Drive; Tutorial
- Slides 3–11 · **1. Networking & Ports**
  - 3 · divider
  - 4 · "Networking & Ports — What Was All That?": three questions about commands from Containers II
  - 5 · "What Is a Network? (IP = a Street Address)": four flavors of IP
  - 6 · the same, with a callout that one machine can hold several IPs
  - 7 · "What Is a Port? (a Door of the House)": inbound vs outbound port on one connection
  - 8 · the same title: the three port ranges (table)
  - 9 · "Port Publishing, Revisited (the Tunnel)"
  - 10 · "Service-to-Service by Name, Revisited": Docker DNS
  - 11 · "Why This Matters for the Cloud": laptop vs cloud table, "who's allowed in?"
- Slides 12–38 · **2. Security and authentication (detour)**
  - 12 · divider
  - 13 · "Why Authentication Matters in MLOps"
  - 14 · "How Authentication Works: 3 Categories (Factors)"
  - 15 · "MFA, Biometrics, and Passwordless"
  - 16 · "Authentication in Google Cloud": console sign-in, second step, VM access
  - 17 · "API Keys: Basic Way to Call an API": definition and example
  - 18 · same title: hand-drawn "API Key Simple Usage" diagram
  - 19 · "OAuth 2.0: User Consent for Access": definition and example
  - 20 · same title (with a stray closing quote): hand-drawn "Oaath 2.0 Flow" diagram, steps
    numbered 1, 3, 6, 9
  - 21 · titled "API Keys…" by mistake: a chat screenshot joking that the AI drawing tool
    "forgot how to count" (the step numbers on slide 20)
  - 22 · titled "API Keys…" by mistake: redrawn "OAuth 2.0 Authorization Code Flow" diagram
  - 23 · "OAuth 2.0 Authorization Code Flow": the five steps as a clean numbered list (no footer)
  - 24 · "Service Accounts: Identities for Code": definition and example
  - 25 · same title: server-to-server diagram
  - 26 · "Authentication vs. Authorization (IAM roles)"
  - 27 · "Default Service Accounts: Quick Start, Not for Production": definition and warning
  - 28 · same title: VM hub diagram
  - 29 · "Workload Identity Federation: Secure Access from Outside GCP": definition and example
  - 30 · same title: GitHub Actions token-exchange diagram
  - 31 · "Choosing the Right GCP Auth Tool": four-way decision rule
  - 32–38 · "Setup GCP Service Account", Steps 1–5 with console screenshots
    - 32 · Step 1: find "Service accounts" under "IAM & Admin"
    - 33 · Step 2: create `data-service-account` (empty service-account list)
    - 34 · Step 2: the "Create service account" form
    - 35 · Step 3: grant a Cloud Storage role (the role dropdown)
    - 36 · Step 3: the service-account list with the new account
    - 37 · Step 4: KEYS tab → "Add key" → "Create new key", JSON
    - 38 · Step 5: the key-type dialog and the downloaded key; copy it into `secrets/`
- Slides 39–45 · **3. Google Cloud Storage**
  - 39 · divider
  - 40 · "What is Google Cloud Storage?": one shared bucket for all pipeline stages
  - 41 · "Buckets & Objects": folder tree vs flat key space
  - 42 · "How a Container Connects to GCS": mounted key, env var, auth → IAM check
  - 43 · "Reading & Writing Objects": Python client code and the per-stage loop
  - 44 · "Same Thing From the CLI": `gcloud storage cp` / `ls`
  - 45 · "Permissions & Gotchas"
- Slides 46–51 · **4. Connecting to Google Drive**
  - 46 · divider
  - 47 · "Why Connect to Google Drive?": the human-filled shared folder, two ways to read it
  - 48 · "Drive API Basics": install, client, file IDs, scopes
  - 49 · "Two Ways to Authenticate to Drive": OAuth vs service account table
  - 50 · "Service-Account Access Pattern": four-step recipe and access-flow diagram
  - 51 · "Listing & Downloading": annotated Python code
- Slide 52 · **5. Tutorial** · divider only; no tutorial slides follow
- Slide 53 · "Summary: Connecting to the Cloud": five bullets, one per topic
- Slide 54 · image only: a film still captioned "Delete! Delete! Delete!" (no text, no context)
- Slide 55 · "THANK YOU" over a cartoon stage curtain

## Key ideas

1. **Revisit what you already typed.** The networking section opens on three puzzles from
   Containers II: why `-p` takes two numbers, which machine `localhost` is, and how a bare name
   like `processor` becomes an address. It promises to answer them in order and end on the real
   question, who is allowed in. (Slide 4)
2. **An IP address is a street address, and a "house" is anything that has one, including a
   container.** There are four flavors: private addresses on a Docker network (`172.18.0.x`),
   private addresses on home Wi-Fi (`192.168.1.x`), public internet addresses, and the loopback
   address `127.0.0.1` (`localhost`), which every machine has and which always means "this
   machine". One machine can hold several addresses at once: a laptop is both loopback and its
   Wi-Fi address; a container gets one per Docker network it joins; a cloud server has a private
   address and optionally a public one. (Slides 5–6)
3. **A port is a door: the IP picks the machine, the port picks the service.** A full address is
   `IP:port`. On one connection the server's inbound (listening) port is fixed, and it is the
   number you publish; the client's outbound port is chosen at random, and the reply comes back to
   that same random port. (Slide 7)
4. **Port numbers fall into three ranges.** 0–1023 are well-known system ports (22 SSH, 80 HTTP,
   443 HTTPS); 1024–49151 are registered ports, where you pick yours (9200, 8080, 3000, 5432);
   49152–65535 are dynamic ports the OS hands out for outbound connections. (Slide 8)
5. **`-p HOST:CONTAINER` is a tunnel.** A container's ports live in its own network namespace and
   are sealed off from the laptop until published. The Docker bridge, a router rather than a
   machine, forwards the host port you pick (8090) to the port the app listens on inside (9100).
   (Slide 9)
6. **Containers find each other by name through Docker DNS.** On a shared network each service
   name is a hostname; Docker's DNS, the "phone book", returns the container's current IP. IPs
   change when a container restarts, the name does not, so always dial the name. Compose sets
   this up automatically ("Networking for Free"). (Slide 10)
7. **The cloud uses the same ideas on a public street.** A laptop service has a private address
   and the home router keeps the world out; a cloud service has a public IP and a DNS name, a
   firewall that must open the port (closed by default), and a load balancer that routes traffic
   in. Once anyone can knock, the question flips from "how do I reach it?" to "who's allowed in?"
   (Slide 11)
8. **An open AI endpoint is a liability.** An unprotected public endpoint invites runaway LLM bills
   and data leaks or misuse. Authentication and access management are the first defense: only
   authorized users and services should reach your AI. (Slide 13)
9. **Authentication rests on three factors, and MFA means two different ones.** Something you
   know (password, PIN; security questions are weak), something you have (authenticator app,
   hardware key, phone, certificate), something you are (fingerprint, face, iris, voice).
   Password + authenticator app is know + have; a passkey unlocked by a fingerprint is have + are,
   so it is MFA with no password at all. Google Cloud applies this to console sign-in (password
   plus a second step, or a passkey) and to VMs (SSH keys or certificates: the client proves it
   holds a private key). (Slides 14–16)
10. **An API key identifies the calling program, not the person.** A program sends a small secret
    string with each request; the service uses it both to let the caller in and to meter it (the
    example: a hosted translation model limited to 1,000 calls per day per token). It reveals
    little about the user. (Slides 17–18)
11. **OAuth 2.0 lets a user grant an app access without handing over a password.** The user
    approves the requested scopes on a consent screen ("Sign in with Google"); the app receives a
    temporary token for that user's data. In the authorization-code flow the app asks for access,
    the user signs in and approves, Google redirects back with a one-time code, the app trades the
    code (with its client secret) for an access token, and the token goes with each API call.
    (Slides 19–23)
12. **A service account is an identity for code.** It is for server-to-server traffic with no human
    and no login screen: the program proves who it is and receives the permissions granted to
    that identity (the example: a script that uploads into a GCS bucket). (Slides 24–25)
13. **Authentication proves who you are; authorization (IAM) decides what you may do.** IAM roles
    and policies bundle permissions (the slide's tiers: Viewer read-only, Editor read and write,
    Admin full control). The best practice is least privilege: grant each account only what it
    needs. (Slide 26)
14. **Default service accounts are a convenience, not a production setup.** GCP attaches a generic
    service account to some resources, such as new VMs, so code there can reach Cloud Storage or
    a database in the same project without setup. In production, replace it with a dedicated
    account that has only the permissions it needs. (Slides 27–28)
15. **Workload Identity Federation lets outside workloads in without a key file.** A workload
    outside GCP (GitHub Actions, AWS, Azure, on-prem) presents its own identity token; Google
    verifies it and returns a short-lived access token. Nothing long-lived is copied, stored or
    leaked (the example: GitHub Actions deploying to Cloud Run). (Slides 29–30)
16. **Choose the auth tool by who is acting and where.** Public API calls with tracking and limits
    → API key. An app acting for a consenting user → OAuth 2.0. A program inside GCP → service
    account. A program outside GCP → Workload Identity Federation. (Slide 31)
17. **Creating a service account takes five console steps.** Open IAM & Admin → Service accounts,
    create `data-service-account`, grant it a Cloud Storage role, create a JSON key from the KEYS
    tab, and move the downloaded file into the `secrets` folder as `data-service-account.json`.
    (Slides 32–38)
18. **GCS is object storage: one durable store every container can reach.** Objects live in
    buckets, addressed globally as `gs://<bucket>/<path>/<object>`. In the Mega Pipeline every
    stage (transcribe, generate, translate) reads from and writes to one shared bucket. (Slide 40)
19. **The folders in a bucket are an illusion.** GCS keeps a flat key space: each object is data
    plus metadata under a full name such as `audio/input-01.mp3`. What looks like a folder is a
    shared name prefix, and listing a "folder" is listing by prefix. (Slides 41, 43)
20. **A container reaches GCS through a mounted key and an environment variable.** `docker run`
    mounts the host's `secrets` folder at `/secrets` with `-v` and sets
    `GOOGLE_APPLICATION_CREDENTIALS` to the key's path inside the container. `storage.Client()`
    reads that key (authentication), and IAM then checks the account's role, such as Storage Object
    Admin (authorization). No password appears in the code. (Slides 42–43)
21. **Every pipeline stage runs the same loop: download the input object, transform it, upload the
    output object.** The Python client and `gcloud storage cp` / `ls` do the same three things;
    `gsutil` still works but `gcloud storage` is the current command. (Slides 43–44)
22. **Four storage rules.** Grant Storage Object Admin (objects only) rather than Storage Admin
    (which also controls buckets); keep data buckets private and reach them through the service
    account; bucket names share one worldwide namespace, so prefix them (`ac215-…`); storage and
    egress cost money, so delete what you no longer need. (Slide 45)
23. **Drive is where human-supplied data lands, and there are two ways for code to read it.**
    People drop files into a shared folder in the browser. An app can read it via the Drive API as
    a logged-in user (OAuth: it sees whatever that user can see) or as a robot (service account:
    it sees only what has been shared with it). Automation → service account plus a shared folder;
    a user's own data → OAuth. (Slides 47, 49)
24. **A service account's empty Drive is the safety feature.** It starts with no files and sees one
    only after someone shares it with the account's email. Share the folder as Viewer, then build
    the Drive client with the same JSON key you already use for GCS: one identity across many
    Google services, no new secret, no user login. (Slides 49–50)
25. **Drive API essentials.** Install `google-api-python-client` (there is no
    `google-cloud-drive` package), build a `drive` v3 client, address everything by file ID (the
    tail of a share link; a folder is a file too), and request the narrowest scope: read-only for
    pipelines. Listing is a query on the parent folder that skips trashed files; downloading
    fetches the raw bytes and writes them to disk. The course's own `tools/drive_pdf.py` works
    this way. (Slides 48, 51)
26. **Summary.** IPs identify machines and ports identify services; Docker publishes HOST:CONTAINER
    and resolves names. OAuth acts for users, service accounts identify code, federation gives
    outside workloads short-lived tokens. Authentication proves identity, IAM limits actions.
    Buckets hold objects by key. Drive is read by file ID with the smallest scope. (Slide 53)

## Diagrams

- **Slide 4 · three questions on two commands.** Two command lines in gray monospace:
  `$ docker run -p 8090:9100 gateway-img` with `→ http://localhost:8090` below it, and
  `GET http://processor:9200`. Curved connectors tie three highlighted questions to the exact
  tokens: "Two numbers — why?" (blue, upper left) → the `8090:9100` pair; "Which machine is that?"
  (yellow) → `localhost`; "A name — where's the address?" (green) → `processor`. A dark-blue box
  at the bottom left promises the build-up: network, then port, ending on who is allowed in.
  Purpose: the section's hook. A re-draw: show the two commands, then pin three question marks to
  `8090:9100`, `localhost` and `processor`; each is resolved by a later scene.
- **Slide 5 · four flavors of IP.** Four rounded panels in a 2×2 grid, each holding house icons
  with an address under each:
  - Top left, green, "Private IP — a Docker network", subtitle `app-net · 172.18.0.x`: gateway
    `172.18.0.2`, processor `172.18.0.3`.
  - Top right, blue, "Public IP — the open internet": `google.com` `142.250.4.100`,
    `your-app.com` `34.120.10.5`.
  - Bottom left, green, "Private IP — your home Wi-Fi", subtitle `home Wi-Fi · 192.168.1.x`:
    MacBook `.10`, iPad `.11`, iPhone `.12`.
  - Bottom right, no panel, "Loopback — every machine has one": one house labelled localhost
    `127.0.0.1`, with a note that every house above has its own loopback, always meaning "this
    machine, itself".

  Purpose: a house is anything with an address, including a container; private, public and
  loopback addresses differ in who can reach them. Green marks the private networks, blue the
  public one.
- **Slide 6 · several addresses per machine.** Slide 5 with a dark-blue callout laid over the
  middle: one machine or container can hold several IPs at once (laptop: `127.0.0.1` plus its
  Wi-Fi IP; container: one per Docker network; cloud server: private plus optional public). A
  re-draw: highlight the same laptop in the Wi-Fi panel and the loopback panel at once.
- **Slide 7 · one connection, two doors.** Left: a blue door icon labelled `:9200`, "a service
  listens here = its inbound port". Right, a light-blue panel headed "one connection — out to the
  service, then the reply comes back": the gateway house (`172.18.0.2 : 51844`, "client · random,
  outbound") and the processor house (`172.18.0.3 : 9200`, "server · listening, inbound"). A blue
  arrow left → right is labelled "request → to :9200"; a gray arrow right → left is labelled
  "reply returns to :51844". A footer band defines the inbound port (blue, fixed, the number you
  publish) and the outbound port (red, random). The random port number is colored red wherever it
  appears. Purpose: a port picks a service on a machine; a connection has a fixed server end and
  a throw-away client end. A re-draw: two houses with doors, a packet going out of door 51844 into
  door 9200 and the reply returning through the same two doors.
- **Slide 8 · port ranges (table).** Three rows, columns "Port range / What it is / Examples":
  0–1023 well-known system (22 SSH, 80 HTTP, 443 HTTPS); 1024–49151 registered, "pick yours here"
  (9200, 8080, 3000, 5432); 49152–65535 dynamic / ephemeral, outbound (`:51844`, chosen by the
  OS). A re-draw: a 0–65535 number line cut into three colored bands with the example ports
  dropped onto it; 51844 lands in the dynamic band, which links back to slide 7.
- **Slide 9 · the tunnel.** One large teal panel labelled "your laptop — the host machine network
  namespace". Inside it, left to right with gray arrows: a white box "your browser"
  `localhost:8090` ("on this same machine") → a gray box "Docker bridge", "a router, not a
  machine", `:8090 → :9100`, "forwards the host port in" → a white box nested at the right,
  "container · its own network namespace", holding the gateway house at `172.18.0.2 : 9100`.
  Bullets: the container's ports live in its own namespace (Containers I) and are sealed off until
  published; the two numbers are HOST (blue, you pick) : CONTAINER (where the app listens).
  Purpose: what `-p 8090:9100` actually builds. A re-draw: a laptop outline containing a smaller
  sealed box; `-p` drills a tunnel through the box wall, and the number changes from 8090 to 9100
  as the request passes the bridge.
- **Slide 10 · dial the name, DNS returns the address.** Left to right: the gateway house
  (`172.18.0.2 : 51844`, client) → arrow labelled `http://processor:9200`, "you dial the name" →
  a phone-book icon "Docker DNS", "the phone book" → arrow labelled `172.18.0.3 : 9200`, "DNS
  returns the current IP" → the processor house (`172.18.0.3 : 9200`, server). Bullets: name =
  hostname; IPs change on restart, names are stable; Compose wires it for you. Purpose: name
  resolution between containers. A re-draw: restart the processor so its IP changes, show the
  phone-book entry update while the gateway keeps dialing the same name.
- **Slide 11 · laptop vs cloud (table).** A laptop icon heads one column, a cloud icon the other.
  Rows: Address (localhost / private IP vs a public IP + a DNS name); Who can reach it (not on the
  internet, the router keeps the world out vs on the internet, a firewall must open the port,
  closed by default); Getting traffic in (publish the port, `-p 8090:9100`, vs a load balancer
  out front). A dark-blue banner: public address + open port = anyone can knock; the question
  flips to "who's allowed in?" → Authentication. Purpose: the bridge from networking to auth. A
  re-draw: the slide-9 laptop is moved onto a public street; a firewall gate and a load balancer
  appear in front; strangers start knocking.
- **Slide 14 · three factors (cards).** Three cards with colored top bars and icons: blue / brain,
  "FACTOR 1 Something You Know"; green / phone, "FACTOR 2 Something You Have"; purple / DNA,
  "FACTOR 3 Something You Are". Each lists examples; "(weak)" after security questions is red.
  Layout rather than mechanism, but it is the vocabulary for slide 15's MFA combinations (two
  different cards = MFA).
- **Slide 18 · API key simple usage (hand-drawn).** Top: a stick-figure "Client" → a browser
  window "Client App" → an oval "Service/API". Below a horizontal line, a vertical timeline:
  "1. Make API Request + [Your_API_KEY_HERE]" → "2. Return Data"; a key icon labelled "API Key"
  connects to a check box "OK!". Purpose: the key rides along with the request and the service
  checks it before returning data. A re-draw: one request envelope with a key stapled to it; the
  service checks the key against its list (and a call counter), then returns data.
- **Slides 20–22 · OAuth 2.0 flow (hand-drawn, three versions).**
  - Slide 20, headed "Oaath 2.0 Flow": a "User" stick figure → a "Client App" window, with the
    label "Request access + client_id" between the app and a cloud with a padlock,
    "Authorization Server / API". On a vertical
    timeline below: "1. Wants to access data"; a speech bubble "Gimme data!"; "3. Login + Consent
    screen"; "Authorization Code"; "6. Authorization code + Refresh Token"; "9. Use Access Token
    for data / Protected Data". The step numbers jump 1, 3, 6, 9.
  - Slide 21: a chat screenshot showing the slide-20 picture, with the comments that it has only
    steps 1, 3, 6 and 9 and that the AI model "forgot how to count". It is a joke, not content.
  - Slide 22, a cleaner sequence diagram headed "OAuth 2.0 Authorization Code Flow": User →
    Client App (lifeline) and "Authorization Server/API" (lifeline, cloud with padlock). Between
    them, a label with a short arrow pointing at the app: "Requests authorization (client_id,
    redirect_uri, scope)".
    Then "1. Wants to access protected data" under the user; "5. Login + Consent Screen"
    (app → server); "4. Approves access" (server → app); "6. Exchanges Authorization Code (and
    client_secret) for Access Token and Refresh Token" (app → server); "8. Sends Access Token with
    request for protected resources" (app → server, database icon). An "Authorization Code" card
    icon sits on the left. The numbers are still out of sequence (1, 5, 4, 6, 8).

  Purpose: user consent without sharing a password. **For a re-draw, use slide 23's five steps,
  not the drawn numbering:** (1) the app asks for access (client ID, redirect URI, scopes); (2) the
  user signs in with Google and approves the scopes; (3) Google redirects back to the app with an
  authorization code; (4) the app exchanges the code plus its client secret for an access token
  (and a refresh token); (5) the app calls the API with the access token. Three lifelines: user's
  browser, app, Google. The password only ever travels between the user and Google.
- **Slide 25 · server-to-server.** A server-tower icon "Application Server" → a long arrow labelled
  "Automated interaction" → a cloud outline "Cloud Service (Database, API, …)". Under the arrow, a
  stick figure struck through in red, "no user involved". Purpose: a service account is the
  identity in a loop with no human. A re-draw: the same arrow, with an ID badge (the account's
  email) clipped to the server.
- **Slide 28 · default service account on a VM.** A central box "VM" with four satellites: a
  person-badge icon "Default service account" (arrow into the VM), a gear "Created & attached
  automatically" (arrow into the VM), and plain lines out to a cloud "Cloud Storage" and a
  cylinder "Database". Purpose: the VM gets an identity without anyone asking, and that identity
  can already reach project resources. A re-draw: a VM appears and a badge drops onto it on its
  own; then the badge is swapped for a narrower custom one ("not for production").
- **Slide 30 · Workload Identity Federation.** Top left: a GitHub icon, "GitHub Actions (external
  workload)". Top right: a cloud labelled "GCP", "Google STS / Workload Identity Provider". Arrow
  left → right with a handshake icon, "GitHub OIDC token / token exchange request". Arrow back
  right → left, "short-lived token". Then a diagonal arrow labelled "Access" from GitHub Actions
  down to "Cloud resources (GCS, DB, …)" (cloud plus cylinder). Purpose: trade an identity token
  the outside system already has for a short-lived Google token; no key file exists. A re-draw:
  GitHub hands its own badge to a Google desk, receives a ticket with a short timer, and uses the
  ticket on the bucket; contrast with a JSON key file being copied around (struck through).
- **Slides 32–38 · console walkthrough (screenshots).** Each is a Google Cloud console screenshot
  with red boxes:
  - 32: the left nav, "IAM & Admin" and its "Service Accounts" entry.
  - 33: the empty "Service accounts for project" list and the "+ Create service account" button.
  - 34: the "Create service account" form (name, ID, the generated email, description). The
    screenshot's account is called `2025_ac215_Tutorial58`, not `data-service-account`.
  - 35: the "Permissions (optional)" step with the role dropdown, which shows **Storage Object
    Admin**, although the step text says "Storage Admin".
  - 36: the list again, now with the new account (status Enabled, "No keys").
  - 37: the KEYS tab, two console banners (keys are a security risk if compromised, and Google
    recommends Workload Identity Federation instead; Google automatically disables keys found in
    public repositories), and the "Add key" menu with "Create new key".
  - 38: the key-type dialog (JSON, "Recommended", vs P12) and the "Private key saved to your
    computer" notice warning that the file grants access to your cloud resources.

  Purpose: the click path. A scene author should re-create these as a simplified mock console;
  the two banners on slide 37 are worth keeping because they make the slide-29 point in Google's
  own words.
- **Slide 40 · one shared bucket.** Three gray stage boxes stacked on the left, "transcribe",
  "generate", "translate". Blue arrows run between each box and a rounded blue box on the right,
  `gs://ac215-mega-pipeline`, "one shared bucket"; one arrow is labelled "read + write". Purpose:
  the stages never call each other; the bucket is the hand-off. A re-draw: three stage boxes
  orbiting one bucket, each pulling an object in and pushing a new one out.
- **Slide 41 · folder tree vs flat key space.** Left, "How you picture it — a folder tree": a
  panel titled `ac215-mega-pipeline` with two manila folders, `audio/` (holding `input-01.mp3`,
  `input-02.mp3`) and `text/` (holding `out-01.txt`); caption "Folders really contain files — a
  hierarchy you open." A gray arrow → right, "What GCS actually keeps — a flat key space": the same
  bucket name above three side-by-side cards, each "OBJECT: data + metadata", with the full keys
  under them (`audio/input-01.mp3`, `audio/input-02.mp3`, `text/out-01.txt`); caption "An
  object's name points to its data and metadata." Purpose: there are no directories, only names
  with slashes. A re-draw: the folder tree melts into a flat row of labelled objects; the
  `audio/` folder name slides into each object's key as a prefix.
- **Slide 42 · from `docker run` to an allowed request.** Top: the `docker run` command (see
  *Commands*) with three callouts: the `-v` line is "The Service Account JSON key, mounted in with
  `-v`"; the `GOOGLE_APPLICATION_CREDENTIALS` line is the "env var pointing the library at that
  key"; a blue note names `google-cloud-storage` as the client library (next slide). Bottom,
  "What happens when the container runs", a left-to-right chain: `storage.Client()` → "reads the
  JSON key" / "authentication" → a yellow box "Service account (the mounted key)" → "IAM checks the
  role" / "authorization" → a green box "Storage Object Admin ✓ request allowed". Purpose: the two
  checks, who you are then what you may do, in the order they happen. A re-draw: the host
  `secrets/` folder appears inside the container at `/secrets`; the env var label points at the
  file; the client picks the key up, shows it to Google, and an IAM gate checks the role before
  the bucket opens.
- **Slide 43 · read, write, list, and the loop.** Python code in the middle with callouts: on the
  client line, "Authenticates with the mounted key — no password in code"; on the upload pair,
  "Upload a local file up to the bucket"; on the download pair, "Download an object back down to
  a local file"; on `list_blobs(... prefix="audio/")`, "List objects under a key prefix — like
  opening a folder". Bottom: three boxes, blue "download / input object" → gray "transform / run
  the model" → green "upload / output object", under "Every stage runs the same loop". Purpose:
  the generic shape of every pipeline stage. A re-draw: one stage box pulls an object from the
  bucket, a gear turns, and a new object goes back under a different prefix.
- **Slide 44 · the same from the CLI.** Three `gcloud storage` commands with callouts: upload
  (local file → bucket), download (bucket → local file), list (a bucket or prefix). A dark-blue
  speech bubble: `gsutil cp / ls` still works; `gcloud storage` is the modern command. Purpose:
  the CLI mirror of slide 43.
- **Slide 47 · two robots reading one human folder.** Left: "TA / human", "drops files in the
  browser", "no code — before auth" → "adds" → a manila folder `ac215-dataset/`, "shared Drive
  folder". From the right, two boxes connect to the folder through one bracket labelled "read via
  Drive API": a blue box "OAuth — as a logged-in user" ("your app acts for a person — sees what
  they can see") and a yellow box "Service account — as a robot" ("no human in the loop — reads
  only the shared folder"). Purpose: the same fork as the auth section, applied to Drive. A
  re-draw: a person drops files in; two readers approach, one wearing the user's badge and seeing
  all of the user's files, one wearing a robot badge and seeing only this folder.
- **Slide 48 · four setup steps (quadrants).** Four panels with numbered headings: (1) enable the
  API and install `google-api-python-client` (green check) — a grayed-out
  `pip install google-cloud-drive` with a red ✗ "(no such package)"; (2) build the client with one
  import and `build("drive", "v3", credentials=creds)`; (3) every file and folder is addressed by
  an ID, the tail of a share link, shown with the ID part in red (`1AbC…Xy`, `1Zz…Qw`); (4) scopes
  as least privilege: `.../auth/drive.readonly` vs `.../auth/drive`, with the suffix in red.
  Purpose: a checklist rather than a mechanism; quadrant 3 (link → ID) and quadrant 4 (scope
  width) are worth animating.
- **Slide 49 · OAuth vs service account (table).** Columns "OAuth 2.0" and "Service account";
  rows Who acts (a logged-in user vs your code, no human), Sees (that user's own files vs only
  files shared with its email), Best for (user-facing apps vs pipelines, CI, automation). Bullets:
  the account's empty Drive is the safety feature; the decision rule.
- **Slide 50 · service-account access flow.** Left: the four-step recipe and a dark-blue banner
  ("Same key as GCS — no user login, no new secret. One identity, many Google services."). Right,
  "how access flows", top to bottom: a blue box "Shared Drive folder", "a human shares it" →
  arrow "shared with the SA's email (Viewer)" → a yellow box "Service account",
  `id-…@…gserviceaccount.com` → arrow "authenticates with the same JSON key" → a gray box
  "Container reads the files". Purpose: access is granted by sharing to the account's email, not
  by any login. A re-draw: a human drags the folder onto an email address; the badge with that
  email lights up; a container holding the same JSON key used for GCS reads the folder.
- **Slide 51 · annotated Drive code.** About a dozen lines of Python (see *Commands*) with four
  callouts: green "Read-only — we only pull files, never change them" on the scope line; "Same key
  — the secret you already mount, nothing new" on the credentials line; yellow "List — ask for one
  folder's files, skip the trash" on the query; blue "Download — grab the raw bytes, then save to
  disk" on `get_media`. A dark-blue banner points to the course's own `tools/drive_pdf.py`.

## Terms the lecture uses

Tutorial comparisons refer to the `cheese-app-v0` README as quoted in [`digest.md`](digest.md),
plus the neighbouring repos named there.

| Lecture term | Slides | Note on the tutorial README |
|---|---|---|
| "Containers I", "Containers II" | 4, 9 | The lecture's names for earlier lectures (L02 and L03/L04 in this series). |
| "IP = a Street Address", "house" | 5–6 | Not in the README. |
| "Private IP", "Public IP", "Loopback", `localhost` | 5–6 | The README just uses `localhost:<port>` URLs; `digest.md` adds `0.0.0.0`, which the slides never mention. |
| `app-net` (`172.18.0.x`) | 5 | The tutorial's networks are `cheese-app-network` and `llm-rag-network`; `port_toy` uses `toynet`. |
| "port", "a Door of the House"; "full address = IP : port" | 7 | Same meaning. |
| "Inbound (listening) port", "Outbound port"; "client · random, outbound", "server · listening, inbound" | 7, 10 | Not in the README. `port_toy`'s README calls the client side the "ephemeral source port". |
| "Well-known · system", "Registered", "Dynamic · ephemeral" | 8 | Not in the README. |
| "Port Publishing", "the Tunnel", "HOST : CONTAINER" | 9 | Same mechanism. The tutorial's scripts publish `3200:3000`, `9000:9000` and `8000:8000`. |
| "host machine network namespace", "its own network namespace" | 9 | `digest.md` says "each container has its own network namespace, so its own `localhost`". |
| "Docker bridge" ("a router, not a machine") | 9 | Not in the README; the tutorial creates user-defined bridge networks without calling them that. |
| "Docker DNS" ("the phone book"); "Name = hostname" | 10 | The tutorial relies on it (`llm-rag-chromadb:8000`); `digest.md` says "Docker's built-in DNS". |
| "Networking for Free" | 10 | The L04 deck's slide title for Compose's automatic network. |
| "firewall" (closed by default), "load balancer", "public IP + a DNS name" | 11 | Not in L10's tutorial; they arrive with the deployment lectures. |
| "authentication & access management" | 13 | Not in the README. |
| "Factors": "Something You Know / Have / Are"; "MFA", "Biometrics", "Passwordless", "passkey" | 14–15 | Not in the README. |
| "API Key", "token" | 17–18 | Not used in the tutorial. |
| "OAuth 2.0"; "Sign in with Google"; "temporary token"; "scopes"; "authorization code"; "access token", "refresh token"; `client_id`, `redirect_uri`, `client_secret`; "Authorization Server/API"; "Client App"; "consent screen" | 19–23 | The tutorial does not use OAuth for users. `digest.md` §3.2 describes the service-account token exchange at `oauth2.googleapis.com/token`, which the slides do not show. |
| "Service Account", "identity for your code", "server-to-server" | 24–25 | Same concept; the README's account is `llm-service-account`. |
| "Authentication" vs "Authorization (IAM)"; "roles & policies"; Viewer / Editor / Admin | 26 | `digest.md` §3.3 frames IAM as principal × role × resource; the slides do not use "principal". |
| "least privilege" | 26, 45, 48, 53 | `digest.md` exercise E6 applies it to the README's Storage Admin grant. |
| "Default Service Account", "starter identity" | 27–28 | Not in the README. |
| "Workload Identity Federation"; "GitHub OIDC token"; "token exchange"; "Google STS / Workload Identity Provider"; "short-lived token" | 29–30 | Not in L10's tutorial (CI/CD lectures later). |
| "Setup GCP Service Account" | 32–38 | Same title as the README section (`#setup-gcp-service-account`), same click path ("IAM & Admin" → "Service accounts", KEYS tab, "ADD Key (Create New Key)", JSON). |
| `data-service-account`, `data-service-account.json` | 33–34, 38, 42, 51 | **Differs.** The README creates `llm-service-account` / `llm-service-account.json`. `data-service-account` is the L11 (`data-labeling`) name. |
| "Storage Admin" (step text) vs "Storage Object Admin" (screenshot, slides 42, 45) | 35–36, 42, 45 | **Differs.** The README grants Storage Admin plus "Gemini Enterprise Agent Platform User" (formerly "Vertex AI User"); the slides grant only a storage role, and slide 45 recommends Storage Object Admin. |
| "secrets folder" | 38, 42 | Same convention. The slide mounts `$PWD/../secrets` (one level up); the README's scripts mount `../../secrets` (two levels up). |
| "Object storage", "bucket", "object", "blob", "key", "flat key space", "metadata", `gs://` | 40–41, 43 | Not in the README (v0 never calls GCS); `digest.md` §3.7 uses the same words. |
| "google-cloud-storage — the client library" | 42 | Listed in `api-service/Pipfile` but never imported (`digest.md` E6). |
| `GOOGLE_APPLICATION_CREDENTIALS`, "env var pointing the library at that key" | 42 | Same variable in the README's scripts. `digest.md` calls the lookup **Application Default Credentials (ADC)**; the slides never say ADC. |
| "key prefix" | 43 | `digest.md`: "GCS 'folders' are just name prefixes". |
| "egress" | 45 | Not in the README. |
| `gcloud storage` vs `gsutil` | 44 | The README uses neither; `digest.md`'s suggested commands use `gcloud storage`. |
| "Drive API", "file ID" (slide 50 writes `fileId`; the slide-48 heading's text layer reads "fieId", presumably the same word), "scope", `drive.readonly`, "shared Drive folder", "the SA's email" | 47–51 | Nothing about Drive in the tutorial. |
| `ac215-mega-pipeline` bucket, `transcribe-audio` image | 40–44 | The L03 example; the `mega-pipeline` README's bucket is `mega-pipeline-bucket` and its key is `mega-pipeline.json`. |

## Commands and code on the slides

Verbatim, one physical line each, as printed. A trailing `\` means the slide continues the
command on the next line. Lines separated by "·" are separate lines on the slide.

| Slide | Command / code | Note |
|---|---|---|
| 4 | `$ docker run -p 8090:9100 gateway-img` | from Containers II |
| 4 | `→ http://localhost:8090` · `GET http://processor:9200` | the two addresses in question |
| 9 | `-p 8090:9100` · `:8090 → :9100` | the tunnel |
| 10 | `http://processor:9200` → `172.18.0.3 : 9200` | name → current IP |
| 11 | `-p 8090:9100` | laptop column |
| 22 | `(client_id, redirect_uri, scope)` | the authorization request |
| 38 | `data-service-account.json` | the key's file name in `secrets/` |
| 40 | `gs://<bucket>/<path>/<object>` · `gs://ac215-mega-pipeline` | the address format |
| 41 | `audio/input-01.mp3` · `audio/input-02.mp3` · `text/out-01.txt` | object keys |
| 42 | `$ docker run --rm -ti \` | |
| 42 | `-v "$PWD/../secrets":/secrets \` | mounts the key folder |
| 42 | `-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/data-service-account.json \` | the slide wraps this across three lines |
| 42 | `transcribe-audio` | the image |
| 42 | `storage.Client()` | starts the chain |
| 43 | `from google.cloud import storage` | |
| 43 | `client = storage.Client()` | |
| 43 | `bucket = client.bucket("ac215-mega-pipeline")` | |
| 43 | `blob = bucket.blob("audio/input-01.mp3")` · `blob.upload_from_filename("input-01.mp3")` | upload |
| 43 | `blob = bucket.blob("text/output-01.txt")` · `blob.download_to_filename("output-01.txt")` | download; slide 41 calls the object `text/out-01.txt` |
| 43 | `for b in client.list_blobs("ac215-mega-pipeline", prefix="audio/"):` · `print(b.name)` | list by prefix |
| 44 | `$ gcloud storage cp input-01.mp3 \` · `gs://ac215-mega-pipeline/audio/` | upload |
| 44 | `$ gcloud storage cp \` · `gs://ac215-mega-pipeline/text/output-01.txt .` | download |
| 44 | `$ gcloud storage ls \` · `gs://ac215-mega-pipeline/audio/` | list |
| 44 | `gsutil cp / ls` | the older equivalent |
| 48 | `$ pip install google-api-python-client` | ✓ |
| 48 | `$ pip install google-cloud-drive` | ✗ "(no such package)" |
| 48 | `from googleapiclient.discovery import build` | |
| 48 | `drive = build("drive", "v3", credentials=creds)` | |
| 48 | `drive.google.com/file/d/1AbC…Xy/view` · `drive.google.com/drive/folders/1Zz…Qw` | the ID is the tail |
| 48 | `.../auth/drive.readonly` · `.../auth/drive` | read-only vs read-write scope |
| 50 | `id-…@…gserviceaccount.com` | the account email to share with |
| 51 | `from googleapiclient.discovery import build` · `from google.oauth2 import service_account` | |
| 51 | `SCOPE = "https://www.googleapis.com/auth/drive.readonly"` | |
| 51 | `creds = service_account.Credentials.from_service_account_file(` · `"/secrets/data-service-account.json", scopes=[SCOPE])` | the same key as GCS |
| 51 | `drive = build("drive", "v3", credentials=creds)` | |
| 51 | `q = "'<FOLDER_ID>' in parents and trashed=false"` | the list query |
| 51 | `res = drive.files().list(q=q, fields="files(id,name)").execute()` | |
| 51 | `for f in res["files"]:` · `print(f["name"], f["id"])` | |
| 51 | `data = drive.files().get_media(fileId="<FILE_ID>").execute()` | download bytes |
| 51 | `open("local.pdf", "wb").write(data)` | save to disk |
| 51 | `tools/drive_pdf.py` | the course's own tool |

## What the lecture stresses

**Networking**
- Always address another container by its service name, never by its IP: IPs change on restart.
  (Slide 10)
- A container's port is unreachable from the laptop until you publish it, and the host number is
  yours to choose while the container number is wherever the app listens. (Slide 9)
- In the cloud the firewall is closed by default; once a public address has an open port, anyone
  can knock, so the real question becomes who is allowed in. (Slide 11)

**Authentication and IAM**
- An open LLM endpoint means runaway bills and leaked data; authentication and access management
  come first. (Slide 13)
- Security questions are a weak factor (marked red). MFA needs two *different* factors. (Slides
  14–15)
- An API key says little about who the user is; it is for tracking and limits. (Slide 17)
- With OAuth the app never sees or stores the user's password. (Slide 19)
- Least privilege, the lecture's most repeated rule: grant each account only what it needs.
  (Slides 26, 45, 48, 53)
- Default service accounts are for testing; replace them in production (⚠ warning). (Slide 27)
- Workload Identity Federation removes downloaded keys from the picture entirely; no key to copy,
  store or leak. (Slides 29–30) The console says the same on slide 37: keys are a risk if
  compromised, Google recommends federation instead, and Google disables keys found in public
  repositories. Slide 38's notice says to store the downloaded key securely.
- The key goes into the `secrets` folder under a fixed name, `data-service-account.json`. (Slide
  38)

**Storage**
- Prefer Storage Object Admin to Storage Admin. Never make a data bucket public. Bucket names are
  global, so prefix them. Storage and egress cost money, so delete what you do not need. (Slide 45)
  Slide 54's "Delete! Delete! Delete!" image, which has no text of its own, may echo that last
  rule; the deck does not say.
- Credentials come from the mounted key, never from a password in the code. (Slides 42–43)
- `gsutil` still works, but `gcloud storage` is the current command. (Slide 44)

**Drive**
- There is no `google-cloud-drive` package; install `google-api-python-client`. (Slide 48)
- Use the read-only scope for pipelines; request full `drive` only if you must write. (Slides 48,
  51)
- A service account's empty Drive is a feature: it sees only what is explicitly shared with it,
  as Viewer. (Slides 49–50)
- Reuse the GCS key for Drive rather than creating a new secret. (Slides 50–51)

**Slide-internal inconsistencies (for scene authors)**
- Slides 35–36 say "Storage Admin", but slide 35's screenshot selects Storage Object Admin, and
  slides 42 and 45 use and recommend Storage Object Admin. Follow slide 45.
- Slides 33–34 say `data-service-account`, but the screenshots create `2025_ac215_Tutorial58`.
- The OAuth drawings number their steps 1, 3, 6, 9 (slide 20) and 1, 5, 4, 6, 8 (slide 22);
  slide 21 jokes about it. Slides 21 and 22 carry the API-key title. Use slide 23's order.
- Slide 41 names the text object `text/out-01.txt`; slide 43's code uses `text/output-01.txt`.

## Pointers

- **Back-references:** "Containers II" for the `-p 8090:9100`, `gateway-img` and
  `processor:9200` examples (slide 4; the `port_toy` app, L03/L04 in this series), and
  "Containers I" for network namespaces (slide 9; L02).
- **Section hand-off:** slide 11 ends with "→ Authentication (next)".
- **GCP Console** is linked in Step 1 (slide 32). Slide 37's banners link Google's
  service-account key best practices and Workload Identity Federation (screenshot only).
- **Client libraries:** `google-cloud-storage` (slide 42, "Next Slide"), `google-api-python-client`
  (slide 48).
- **Course tooling:** `tools/drive_pdf.py`, the course's own script that pulls lecture PDFs from
  Drive, offered as real code to read (slide 51). The slide gives no repository or link.
- **Example datasets named:** the bucket `gs://ac215-mega-pipeline` (slides 40–44) and the shared
  Drive folder `ac215-dataset/` (slide 47).
- **Tutorial:** the outline lists it as section 5 (slides 2, 52), but no tutorial slide, repo name
  or link follows. The course site pairs L10 with `cheese-app-v0` (`digest.md`).
- No readings, homework or milestone notes appear in this deck.
