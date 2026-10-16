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

## This video and the slides

**Basis.** The video is not scripted yet. This folder holds only `digest.md` and this file: no
`BRIEF.md`, `script.md`, `ASSETS.md` or `assets/terminal/`. The map below therefore uses the hook
and the ten chapters planned in [`digest.md`](digest.md) §8, the study guide
(`MLOps_Learning/guides/L10-cloud-connect-cheese-app-v0.md`) and every slide (the extracted text
and all seven contact sheets, re-read for this section). With no L10 captures, "what the tutorial
does today" means the repo at `cb6fb94` as verified in `digest.md`. Three neighbouring episodes
have captures or verified digests on the ground the slides' examples come from, and I used them:
- **L04** (`../ac215-l04-flexible-workflow-ports/assets/terminal/port-laptop/`), the Containers II
  commands the networking section retells: `11-run-gateway.txt` (`-p 127.0.0.1:8090:9100` …
  `toy-gateway`), `16-ps.txt` and `21-x-ps-all-addresses.txt` (`127.0.0.1:8090->9100/tcp`, and
  `0.0.0.0:8091->9100/tcp` without the prefix), `28-network-inspect.txt` (`toynet`
  172.19.0.0/16, processor .2, gateway .3), `29-x-dns.txt` (`nameserver 127.0.0.11`, Docker's
  embedded DNS) and `14-send.txt` (outbound ports 55620, then 55634).
- **L05** (`../ac215-l05-rag/assets/terminal/`): the same Chroma Compose service as here, shown by
  `docker ps` as `0.0.0.0:8000->8000/tcp` (`laptop/08-x-docker-ps.txt`) and resolved by name to
  172.19.0.2 (`cli-container/04-x-chroma-by-name.txt`); the missing-key failure
  `DefaultCredentialsError: File /secrets/llm-service-account.json was not found.`
  (`cli-container/20-embed-char-split.txt`).
- **L03** (`../ac215-l03-mega-pipeline/digest.md` §2, `ASSETS.md`): the Mega Pipeline the GCS
  section retells, with its real bucket, key and image names.

When L10 captures exist, re-check Conflicts 2 and 4 first (the 403 with only a storage role; the
PORTS column for the three services). If a capture and this section disagree, the capture wins.

**Tag form.** `lecture_ref(10, "a–b")` (`explainer/devops.py`) prints "Lecture 10 · slides a–b".
The title slide says "Lecture 10"; the deck never names the repo (slide 52 is an empty "Tutorial"
divider), and the course site maps L10 to `cheese-app-v0`.

**Who covers what.** The deck is the theory behind the tutorial's plumbing: networking (3–11)
behind ch6, authentication (12–38) behind ch2–ch5, GCS (39–45) behind ch8. Its Drive section
(46–51) has no counterpart. The other way round, the slides never mention CORS, ADC by name,
`0.0.0.0`, Vertex AI, the browser as the integrator, or RAG, so ch7 and most of ch4 stand on
tutorial ground.

### 1. Map: planned chapters ↔ slides

| # | Planned chapter (`digest.md` §8) | Slides on the same ground | Relation |
|---|---|---|---|
| Hook | Three phone calls from the browser; who checks that it's you, and how does a page find a database inside a container? (0:45) | 4 (three puzzles pinned on commands you already typed), 11 (the question flips to "who's allowed in?"), 13 | Same concept: both open on questions about a setup that already works and end on who is allowed in. The cheese questions are tutorial-only. |
| 1 | The map: one laptop, three containers, one cloud (2 min) | 5–6 (anything with an address is a "house"; one machine, several addresses), 11 (laptop vs cloud), 53 | The tutorial applies it: three containers on two Docker networks, a browser on the host, Google's API in the cloud. The three-box topology is tutorial-only. |
| 2 | Who are you? Service accounts and keys (3 min) | 12–13 (why authentication), 24–25 (an identity for code), 31 (choosing the tool), 32–38 (console steps), 37 (the key warnings) | Same concept; the tutorial applies it with `llm-service-account`. Conflicts 1, 2, 5. Slides 14–23 (factors, API keys, OAuth) are not used yet (gaps 4, 5). |
| 3 | Two filesystems, one folder: the `secrets/` portal (2.5 min) | 38 (the key goes into `secrets/`), 42 (`-v` mount plus the env var) | Same concept; the tutorial applies it at a different depth (Conflict 3). |
| 4 | ADC: from key file to Bearer token (3 min) | 42 (the env var points the library at the key; `storage.Client()` reads it), 19–23 (access tokens), 27–28 (the default account on a VM), 29–30 (short-lived tokens) | Mostly tutorial-only: the slides never say ADC and never show the key-to-token exchange. The lecture's identities fill ADC's three places (gaps 1, 2). |
| 5 | IAM: may this identity do this, here? (2.5 min) | 26 (authentication vs authorization, roles, least privilege), 35 (granting a role), 42 (authentication, then IAM checks the role), 45 | Same concept; the tutorial applies it (`roles/aiplatform.user` on `GCP_PROJECT`). Conflict 2. |
| 6 | Ports, `0.0.0.0` and names: one server, two addresses (3.5 min) | 4–10 (IP, ports, ranges, the tunnel, Docker DNS) | Same concept; the tutorial applies it with three published ports and two networks. `0.0.0.0` and "the browser is on no Docker network" are tutorial-only. Conflict 4. |
| 7 | The browser is the integrator: following one chat question (3.5 min) | 11, 13 (who's allowed in; the unprotected AI endpoint), as framing only | Tutorial-only: origins, CORS and preflights are not on the slides. Gap 3 links them. |
| 8 | What survives? Volumes now, buckets next (2 min) | 39–45 (object storage, flat key space, `storage.Client()`, `gcloud storage`, permissions) | Same concept for the bucket half. v0 never calls GCS, so the tutorial applies it only in E7; bind-mounted volumes are tutorial-only. Conflict 6. |
| 9 | Run it end to end (with the two fixes) (3 min) | 32–38 (the console walkthrough), 52 (the empty "Tutorial" divider) | Tutorial-only apart from the console steps. |
| 10 | Recap and debugging flowchart (1.5 min) | 53 (summary), 26, 31, 42 | Could stand on lecture ground. The plan's flowchart sorts errors into layers; 26 and 42 give the authentication / authorization split it rests on. |
| — | not in the plan | 14–16 (factors, MFA, passwordless), 17–18 (API keys), 19–23 (OAuth user consent), 27–30 (default service accounts, Workload Identity Federation), 46–51 (Google Drive); 1–3, 12, 39, 46, 52 (title and dividers); 54–55 (film still, thank-you) | Lecture-only. 14–31 are worth one-beat bridges (gaps 1, 2, 4, 5); Drive and the images add little here. |

### 2. Already in common

| # | Concept | Chapter ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | Start from commands that already work and ask what they hide | hook, ch6 ↔ 4 | Yes. The lecture pins three questions on `8090:9100`, `localhost` and `processor`. This app has the same three: `3200:3000`, `localhost:9000` and `llm-rag-chromadb:8000` (Proposals, ch6). |
| 2 | Anything with an address is a "house", a container included; `localhost` always means "this machine, itself" | ch1, ch6 ↔ 5–6, 9 | Yes. The plan's misconception that `localhost` inside a container is the laptop (§3.5, E5c, recap Q3) is slide 5's rule seen from inside the container. |
| 3 | The IP picks the machine, the port picks the service, and the server listens on a fixed port | ch6 ↔ 7 | Yes. Each of the three services listens on one fixed port (3000, 9000, 8000). |
| 4 | `-p HOST:CONTAINER` is a tunnel: the host number is yours, the container number is where the app listens | ch6 ↔ 9 | Yes, closely. The plan's door animation, where the outside number morphs into the inside number (§3.5), is slide 9's bridge with `3200 → 3000` in place of `8090 → 9100`. The `next dev` misconception (opening 3000) is this split. |
| 5 | On a shared network, containers dial each other by name; Docker DNS returns the current IP; Compose sets the network up | ch6 ↔ 10 | Yes. `CHROMADB_HOST = "llm-rag-chromadb"` (`cli.py:30`) and Compose's `llm-rag-network` are this. The tutorial adds two limits the slide doesn't draw: a name resolves only inside its own network (E5, ponder #3), and the browser is on none (gotcha 9). |
| 6 | A service account is an identity for code, with no human and no login screen | ch2 ↔ 24–25 | Yes. The plan's "hotel key card cut for a robot" (§3.1) matches the lecture's own robot wording (47, 49). |
| 7 | IAM & Admin → Service accounts → create → grant a role → KEYS → Add key → JSON → move the file into `secrets/` | ch2, ch9 ↔ 32–38 | Yes: the README's seven steps (`README.md:48-56`) follow the slides' step text almost line for line. Only the account name and the roles differ (Conflicts 1, 2). |
| 8 | Mount the key folder with `-v` and point `GOOGLE_APPLICATION_CREDENTIALS` at the in-container path; no password in code | ch3, ch4 ↔ 42–43 | Yes. Slide 42's two callouts (the key mounted in with `-v`; the env var pointing the library at it) are the plan's portal and its label. The depth differs (Conflict 3). |
| 9 | Authentication first, then authorization: prove who you are, then IAM checks the role | ch4, ch5 ↔ 26, 42 | Yes, in the same order. The tutorial turns it into a diagnostic the slides don't give: `DefaultCredentialsError` is an authentication failure, a 403 an authorization failure (§3.3, E3). |
| 10 | Least privilege | ch5 ↔ 26, 45, 53 | Yes. The digest applies it to the README's Storage Admin grant (§3.3, E6); slide 45 goes one step finer (Storage Object Admin rather than Storage Admin). |
| 11 | Long-lived keys are the thing to protect | ch2, ch3 ↔ 29, 37–38 | Yes. The tutorial's key hygiene (outside every repo, gotcha 14; list and delete keys at teardown) answers the console's own warnings on slide 37: keys are a risk if leaked, and Google disables keys it finds in public repositories. |
| 12 | GCS is object storage: buckets of objects in a flat key space, where "folders" are prefixes | ch8 ↔ 40–41, 43 | Yes. The digest's misconception "a bucket is a filesystem" (§3.7) is slide 41. The plan's "a folder on Google's disks that any authorised machine can see" is slide 40's one durable store every container can reach. |
| 13 | `storage.Client()` with no key path; upload, download, list by prefix | ch8 ↔ 42–43 | Yes. E7's code makes slide 43's calls against your own bucket; Excerpt 12 (L08) is the upload half. |
| 14 | `gcloud storage` is the current CLI | ch8, E7 ↔ 44 | Yes. Every suggested command in the digest uses `gcloud storage`, none uses `gsutil`. |
| 15 | Storage costs money; delete what you don't need | ch9 teardown ↔ 45 | Yes. The teardown's `gcloud storage rm -r gs://YOUR_BUCKET` and the key deletion follow the same rule. |
| 16 | A reachable address with an open port invites strangers; AI endpoints need protecting | hook, ch7 ↔ 11, 13 | Partly. The hook's "who checks that it's you?" is about the call to Google, which is protected (key, IAM). The lecture's open endpoint is the other side: the app's own API on `:9000`, which checks nobody (gap 3). |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **ADC's three places are the lecture's identities (19–31).** The plan's ch4 animates ADC as a
   lookup order. The lecture supplies who sits in each place:
   - the file named by `GOOGLE_APPLICATION_CREDENTIALS` → a service-account key (24–25, 32–38):
     this tutorial;
   - the gcloud user file from `gcloud auth application-default login` → you, signed in through
     an OAuth 2.0 consent screen (19–23): gotcha 13's fallback when an organization blocks key
     creation;
   - the metadata server → the service account attached to the VM, Cloud Run service or pod; the
     default account of 27–28 is the quick-start version (L13–L15, and GKE's Workload Identity in
     L22–L23).

   Slide 31's four-way rule then reads as "which place gets filled, wherever this code runs".
   Outside the slides and the course repos: a federation credential (29–30) also enters through
   `GOOGLE_APPLICATION_CREDENTIALS`, as a config file of type `external_account` instead of a key.
   **Carry it:** ch4, as labels on the three slots; one line in ch10.
2. **What travels is a short-lived OAuth 2.0 access token (19–23, 29–30).** The lecture shows
   tokens only for users (a one-time code traded for an access token, 22–23) and for outside
   workloads (a short-lived token, 30). The tutorial's service account makes the same trade without
   a person: google-auth signs a JWT with the private key, posts it to the OAuth token endpoint
   `https://oauth2.googleapis.com/token` and gets an access token for about an hour (digest §3.2).
   The consent screen and the code drop out because nobody is there to consent; the token at the
   end is the same kind, and the private key never leaves the laptop. **Carry it:** ch4, in the
   plan's passport-and-visa animation, as one added line: "the same token desk the lecture's OAuth
   diagram ends at, minus the person".
3. **Slide 13's unprotected AI endpoint is running on your laptop (11, 13).** `api-service` on port
   9000 has no login, accepts every origin (`allow_origins=["*"]`, `service.py:17`), and every call
   spends your project's Vertex AI budget through your key. It is published as `-p 9000:9000`,
   which binds all of the laptop's addresses: the L04 capture shows `-p 8091:9100` as
   `0.0.0.0:8091->9100/tcp`, and the L05 capture shows this very Chroma line as
   `0.0.0.0:8000->8000/tcp`. Slide 11's laptop column says the router keeps the world out; it
   keeps out the internet, not other devices on the same Wi-Fi, which can reach
   `<your laptop's IP>:9000` unless the laptop's firewall stops them (not yet captured with a
   second device). port_toy guarded against this with `-p 127.0.0.1:8090:9100` (Conflict 4).
   *(extra)* `-p 127.0.0.1:9000:9000` and `127.0.0.1:8000:8000` keep the app working from your own
   browser. CORS is not this protection: browsers enforce it, and a neighbour's `curl` ignores it
   (§3.6). **Carry it:** ch6 (the publish form and the PORTS column) and the last beat of ch7:
   "CORS decides which page may read the answer; nothing here decides who may call."
4. **Why a service account, by slide 31's rule (17–18, 19–23, 31).** The plan's ch2 says software
   needs its own identity, not why it isn't an API key or OAuth. Walk the rule for this app: it
   isn't a metered public call (an API key; outside the repo, Gemini can also be called with an
   API key through Google AI Studio); it doesn't act for a consenting user (OAuth); it is code
   calling Vertex AI in your project, so a service account, whose roles and bill live in
   `GCP_PROJECT`. The rule's last line (outside GCP → federation) is where a laptop doesn't fit
   cleanly (Conflict 5). **Carry it:** ch2, right after the ID card is minted.
5. **A key file is one factor that works from anywhere (14–16, 37).** Console sign-in asks for
   two different factors (15–16). The JSON key is a single "something you have": whoever holds a
   copy is the account, from any machine, with no second step, until someone deletes the key.
   That is the reason for `secrets/` outside the repo (gotcha 14), for slide 37's warnings and for
   federation (29). **Carry it:** ch2, one sentence while the `private_key` field glows red.
6. **The port number line (7–8).** The plan never says why the course picks 3200, 8000 and 9000:
   they sit in the registered range, the one slide 8 marks "pick yours here". The browser's end of
   each call is a random outbound port the OS picks (7); the L04 page displayed it (55620, then
   55634). See the note on the dynamic range under Conflicts. **Carry it:** ch6, ten seconds on a
   0–65535 line.
7. **GCS ground rules for E7 (45).** Bucket names share one worldwide namespace, so
   `gs://YOUR_BUCKET` needs a prefix (`ac215-…`); keep the bucket private and reach it through the
   service account; Storage Object Admin covers E7's reads and writes; delete the bucket
   afterwards. **Carry it:** ch8, as a four-item card before E7 is suggested.
8. **Slide 11's cloud column is where this app was, and where it goes.** The `deployment/` folder
   deleted in `2bc29dd` served this frontend publicly at `ac215-llm-rag.dlops.io`: a public DNS
   name with TLS, and nginx in front routing traffic to the containers, the role slide 11 gives
   the load balancer. The app's home page still draws that hosted picture (`ArchitectureDiagram.jsx`,
   erratum 8). **Carry it:** ch10, one closing line toward L14 and L20–L23; or ch1, to explain why
   the home page's diagram isn't what you run.
9. **One identity, many Google services (47–51).** The Drive section is lecture-only, but its
   closing idea transfers: the same JSON key reaches another service once that service grants the
   account access (on Drive, by sharing a folder with the account's email). Here the same
   `llm-service-account` reaches Vertex AI now and GCS once it holds a storage role (E6, E7); L08
   used one key for both. **Carry it:** ch5, one optional line.

Lecture-only and of low value here: MFA beyond gap 5 (15–16), the drawn OAuth flows and their
numbering (20–22), the Drive API details (48, 51), the film still (54) and the curtain (55).

### 4. Conflicts

| # | Slides say | Tutorial today (repo `cb6fb94`; neighbouring captures where named) | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **The account is `data-service-account`, its key `data-service-account.json`** (33–34, 38, 42, 51; the screenshots show yet another name, `2025_ac215_Tutorial58`). | `llm-service-account` and `llm-service-account.json` (`README.md:46-67`). Both scripts hard-code `GOOGLE_APPLICATION_CREDENTIALS="/secrets/llm-service-account.json"` (`api-service/docker-shell.sh:10`, `llm-rag/docker-shell.sh:8`). With any other file name the first Gemini call fails with `DefaultCredentialsError: File /secrets/llm-service-account.json was not found.` (captured in L05, `cli-container/20`). | The README, for this tutorial. `data-service-account` is next week's name (L11, `data-labeling`). | "The lecture's demo account is named for next week's data work. The clicks are identical; for this app, call it `llm-service-account`, because that's the file the scripts look for." Use that name in the mock console. |
| 2 | **One storage role.** The step text says Storage Admin (35–36); the screenshot's dropdown and slides 42 and 45 say Storage Object Admin, and 45 recommends it. No other role appears. | Two roles: Storage Admin and Gemini Enterprise Agent Platform User (formerly Vertex AI User, `roles/aiplatform.user`) (`README.md:51-52`). v0 needs only the second: every call goes to Vertex AI, and no file imports `google.cloud.storage` (erratum 2). An account set up from the slides alone would get a 403 `PERMISSION_DENIED` on the first embedding (gotcha 3b). | The README for the Vertex AI role; slide 45 for storage, which v0 doesn't use at all. | "The lecture's account only reads and writes a bucket, so it gets one storage role. This app calls Gemini, so it needs the Agent Platform User role; that's the one that matters. The Storage Admin grant is there for reuse with L08's bucket, and by the lecture's own rule Storage Object Admin would do." In ch5's grid, show both role tokens and grey out the storage one. |
| 3 | **Mount `"$PWD/../secrets"`**, one level up (42). | Two levels up: `SECRETS_DIR=$(pwd)/../../secrets/` (`api-service/docker-shell.sh:8`) and `../../secrets:/secrets` (`llm-rag/docker-compose.yml:11`), both landing on `AC215/secrets`. The slide's line run from `api-service/` would mount `cheese-app-v0/secrets`, which Docker silently creates empty (gotcha 2). | The tutorial's scripts. Each is right for where its script sits. | "Same portal, different stairs: the number of `../` is how far the script sits below your course folder. Here it's two." The plan's path-walk (§3.4) shows it; one line can note the one-level form of flatter repos such as L11's `../secrets`. |
| 4 | **The Containers II command is `docker run -p 8090:9100 gateway-img`** (4; 9 and 11 also write `-p 8090:9100`), and on a laptop "your router keeps the world out" (11). | port_toy published on loopback only: `-p 127.0.0.1:8090:9100` … `toy-gateway`, which `docker ps` shows as `127.0.0.1:8090->9100/tcp`; without the prefix the same image showed `0.0.0.0:8091->9100/tcp` (L04 `port-laptop/11`, `16`, `21`). cheese-app-v0 publishes with no prefix (`-p 9000:9000`, `-p 3200:3000`, Compose `8000:8000`); the same Chroma line appears as `0.0.0.0:8000->8000/tcp` in L05 `laptop/08`. | The captures. The slide shortens the command and renames the image. | "The slide shortens what you typed in Containers II: it was `-p 127.0.0.1:8090:9100`, and that first part decides which of the laptop's addresses get the door. Without it, as in this app, the door faces your Wi-Fi too." Then gap 3. |
| 5 | **Code running outside GCP should use Workload Identity Federation** (31); the console's banner prefers federation to keys (37); federation leaves no key to copy, store or leak (29–30). | A container on your laptop, which is outside GCP, authenticates with a downloaded, long-lived JSON key (`README.md:54-56`). Later the course keeps doing so in CI: L23's GitHub Actions pass a JSON key from a repository secret (`ac215-l23-final-cicd/digest.md` C6). Only GKE pods (L22–L23) get keyless identities, through GKE's Workload Identity. | Both, each in its own scope. Federation needs an outside identity provider Google can verify, such as GitHub's OIDC token on slide 30; a laptop has none. For local work a key file, or your own login (ADC's second place, gotcha 13), is what works. | "By the lecture's rule a laptop is 'outside GCP', and Google would rather you used federation. Federation needs another system to vouch for your code, the way GitHub vouches for its Actions; your laptop has nobody to vouch for it. So for local work the course hands you a key, and you treat it like a password." |
| 6 | **The Mega Pipeline example:** bucket `gs://ac215-mega-pipeline`, image `transcribe-audio`, key `data-service-account.json` mounted at `/secrets` with `-v` and named with `-e` (40–44). | L03 as students ran it: bucket `mega-pipeline-bucket`, image `transcribe_audio`, one shared key from Canvas (`mega-pipeline.json`) copied into each component's `secrets/` and named by a relative `ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json` in the Dockerfile; the run command mounts only the code (`docker run --rm -ti -v "$(pwd):/app" transcribe_audio`; L03 `digest.md` §2, captures `transcribe_audio/01`, `22-g1-key-in-image`). | L03's repo for what you ran in L03. The slide's `/secrets` mount is the course's later convention, the one cheese-app-v0 follows. | "The lecture retells the Mega Pipeline in this week's conventions: the key outside the code, mounted in at `/secrets`. In L03 the key sat inside each folder, which is how it could end up baked into the image." If ch8 shows a bucket, label it `gs://YOUR_BUCKET`, not either course bucket. |

Not counted as conflicts:
- **Addresses on the diagrams** (5, 7, 10): `app-net` 172.18.0.x with the gateway at .2 and the
  processor at .3. In the L04 capture `toynet` was 172.19.0.0/16, with the processor at .2 (started
  first) and the gateway at .3; in L05 `llm-rag-chromadb` resolved to 172.19.0.2. These are
  examples, and the difference makes slide 10's point (addresses change, names don't). Say so when
  the video shows real addresses.
- **The dynamic range** (8: 49152–65535, picked by the OS). That is the registry's range; a Linux
  kernel defaults to 32768–60999 (`net.ipv4.ip_local_port_range`), and containers run Linux. The
  L04 capture's 55620 and 55634 fit both. Say "a high, throw-away port the OS picks".
- **"Viewer / Editor / Admin"** (26). Google Cloud's basic roles are Viewer, Editor and Owner;
  "Admin" belongs to predefined roles such as Storage Admin, and the tutorial uses predefined roles.
  Show the ladder as the idea, then the real role names.
- **Where the bridge sits** (9). The slide draws the Docker bridge inside the laptop's own
  namespace. On Docker Desktop (Mac, Windows) containers and the bridge live in a Linux VM, and
  Docker Desktop forwards the laptop's port into it. The tunnel picture holds; `-p` hides the
  extra hop.
- **No ADC and no token exchange on the slides.** Slide 42 says the library reads the key, not how
  it finds it or what it sends. Absence, not disagreement (gaps 1, 2).
- **Slide 51's explicit `from_service_account_file(…, scopes=[SCOPE])`** for Drive, vs the
  tutorial's ADC: two services, one key, both valid.
- **Slide-internal slips** (the OAuth step numbers on 20 and 22, the API-key titles on 21–22,
  `out-01` vs `output-01` on 41 and 43, the account name in the screenshots): see *What the
  lecture stresses*.

### 5. Proposals for the BRIEF and script authors

**General**
- Tag ch1–ch6, ch8 and ch10 with a GREY `lecture_ref(10, "a–b")`, using the ranges below; ch7 and
  ch9 stand on tutorial ground (ch9 tags only its console beat). Re-draw lecture diagrams in the
  series style. Never show the console screenshots (32–38), the hand-drawn images (18, 20–22) or
  the film still (54).
- **The running picture** is slide 5's houses, scaled to this app: the laptop as a GREY house with
  its own loopback; three TEAL houses inside it on two network streets (`llm-rag-network`,
  `cheese-app-network`); Google as a BLUE building across a public street. Each chapter adds to it:
  doors with two numbers (ch6), the badge and the key (ch2–ch4), the IAM gate at Google's door
  (ch5), the browser walking between doors (ch7), a bucket beside the building (ch8).
- **Colours.** Keep the series': laptop GREY, containers TEAL, Google BLUE, the Vertex AI bill
  GOLD, failures RED. The key is project-owned, so GREEN, turning RED when it lands inside a repo
  or a neighbour reaches the open door. Draw Docker networks as TEAL streets, not the slides' green
  panels; the slides' blue public panel happens to match the series' BLUE cloud.
- **Length.** The plan is about 26 minutes, inside the series' 25–35. Gaps 1–5 add 3–4 minutes,
  mostly in ch2 and ch4; ch6 can take slide 4's hook structure without growing.
- **Captures to make first** (none exist): the 403 with only a storage role (Conflict 2); `docker
  ps` with the three services' PORTS (Conflict 4); `docker network inspect` of both networks for
  real addresses; `getent hosts llm-rag-chromadb` from the CLI container, and its failure from the
  API container (E5); the `google.auth.default()` one-liner (E4) for ch4; *(extra)* the stack with
  `127.0.0.1:` prefixes and a request from a second device with and without them (gap 3).

**Per chapter**
- **Hook · `lecture_ref(10, "11–13")` on the last line.** Keep the three phone calls. End on slide
  11's flip in one sentence: once anything can knock, the question becomes who's allowed in. The
  video then gives two answers: Google checks your key (ch2–ch5); nobody checks callers of your own
  API (gap 3).
- **Ch1 · Lecture 10 · slides 5–6, 11.** Build the house picture. Show slide 6's rule on this app:
  the API container has one address on `cheese-app-network`, Chroma one on `llm-rag-network`, the
  laptop its loopback plus its Wi-Fi address. Use slide 11's right column only for Google's side:
  a public building with a guarded door.
- **Ch2 · Lecture 10 · slides 24–25, 31–38.**
  - Slide 31's rule walked for this app (gap 4), ending on Conflict 5's honest line.
  - The ID card with the account's email: slide 25's server-to-server arrow with a badge clipped
    on.
  - A simplified mock console for 32–38 with `llm-service-account` and both roles (Conflicts 1, 2),
    and slide 37's two warnings as console banners in our own words.
  - Gap 5's sentence while `private_key` glows red.
- **Ch3 · Lecture 10 · slides 38, 42.** The plan's path-walk, then one line on the one-level form
  (Conflict 3). Slide 42's two callouts become two labels on the plan's tube: "the key, mounted in"
  on the `-v` line, "the env var that points the library at it" on `GOOGLE_APPLICATION_CREDENTIALS`.
- **Ch4 · Lecture 10 · slides 19–30, 42.** Open on slide 42's bottom chain (client → reads the key
  → authentication → IAM → allowed) with `genai.Client(vertexai=True, …)` in place of
  `storage.Client()`, then open the "reads the key" box into the plan's ADC animation. Label the
  three slots with the lecture's identities (gap 1), then the token trade (gap 2). The JWT and
  `token_uri` are tutorial-only; tag only the slot labels and the token beat.
- **Ch5 · Lecture 10 · slides 26, 35, 42, 45.** Slide 26's split becomes the plan's two-layer
  error map; least privilege becomes the grid's rule; Conflict 2's two role tokens; slide 45's
  Object Admin vs Admin as one line pointing to E6 and E7. Gap 9 optional.
- **Ch6 · Lecture 10 · slides 4–10.** Open with slide 4's device on this app's own commands:
  - `-p 3200:3000` → "two numbers, why?" (9: the host number is yours, the container number is
    where `next dev` listens);
  - `NEXT_PUBLIC_BASE_API_URL=http://localhost:9000` → "which machine is that?" (5: the browser's,
    because the JavaScript runs there; E8);
  - `CHROMADB_HOST = "llm-rag-chromadb"` → "a name, where's the address?" (10: Docker DNS, inside
    `llm-rag-network` only).

  Then the plan's two arrows into Chroma, the number line (gap 6), and the PORTS column with
  `0.0.0.0` vs `127.0.0.1` (Conflict 4, gap 3). `0.0.0.0` shows up twice, which is worth one
  sentence: uvicorn listens on all of the container's interfaces so the tunnel can reach it, and
  Docker publishes on all of the laptop's interfaces unless you write `127.0.0.1:`.
- **Ch7 · no tag, or `lecture_ref(10, "13")` on the last beat.** CORS is tutorial-only. Close on
  gap 3: CORS answers "which page may read this?", not "who's allowed in?".
- **Ch8 · Lecture 10 · slides 40–45.** The plan's bucket icon becomes slide 41's melt (folder tree
  → flat keys), then slide 43's loop (download → transform → upload) as one beat, then slide 45's
  rules as the E7 card (gap 7). Labels as in Conflict 6.
- **Ch9 · `lecture_ref(10, "32–38")` on the console step only.**
- **Ch10 · Lecture 10 · slides 26, 31, 53.** Keep the flowchart. Add slide 31's rule read as ADC's
  places (gap 1) and the cloud column (gap 8). Add two recap questions:
  - "A classmate reads slide 31 and says your laptop should use federation. What would federation
    need that a laptop doesn't have?" (An outside identity provider Google trusts, such as
    GitHub's OIDC token for its Actions.)
  - "`docker ps` shows `0.0.0.0:9000->9000/tcp`. Who besides you can call your API, what does each
    call cost, and what one change narrows it?" (Anyone who can reach your laptop's address on port
    9000; each call bills your Vertex AI project; `-p 127.0.0.1:9000:9000`.)

**Terms**
- Use the lecture's words: *house* and *street address* for an IP, *door* for a port, *inbound
  (listening) port*, *outbound port*, *registered* and *dynamic* ranges, *port publishing* / *the
  tunnel*, *HOST : CONTAINER*, *network namespace*, *Docker bridge*, *Docker DNS* ("the phone
  book"), *service account* ("an identity for code"), *server-to-server*, *authentication* vs
  *authorization (IAM)*, *roles*, *least privilege*, *default service account*, *Workload
  Identity Federation*, *short-lived token*, *access token*, *scopes*, *object storage*, *bucket*,
  *object*, *key prefix*, *flat key space*.
- Add the tutorial's where the lecture stops: *Application Default Credentials (ADC)*, *JWT*,
  *token endpoint*, *Bearer token*, *principal*, `GCP_PROJECT`, *bind mount*, `0.0.0.0` ("all
  interfaces"), *user-defined network*, *published port*, *origin*, *CORS*, *preflight*.
- Qualify, don't repeat:
  - "`-p 8090:9100`": add `127.0.0.1:` when you mean "this machine only";
  - "`data-service-account`": `llm-service-account` in this tutorial;
  - "Storage Admin": the Agent Platform User role is the one this app needs;
  - "outside GCP → federation": when something can vouch for the code;
  - "Viewer / Editor / Admin": the basic roles are Viewer, Editor and Owner;
  - "49152–65535": a high port the OS picks.
