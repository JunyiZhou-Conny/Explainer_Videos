# AC215 · Lecture 18 — APIs and frontend: a FastAPI service, a simple page and a React app (follow-along: cheese-app-v1 + cheese-app-v2)

## 00:00 — Who answered on port 3000?
Here is a request to port 3000, where this app's frontend runs. It asks for two newsletters and gets them. But look who answered: uvicorn, the API's server, and the API listens on port 9000.
Last year's version of this app worked differently. Its page called port 9000 directly, and every answer carried a permission slip: access control allow origin, star.
This year's API sends no such slip at all. So who carried the request from 3000 to 9000, and why did last year's page need permission?
The lecture draws one chat message as six numbered steps: request, forward, map into a container, run a function, respond, show it. We add one step it never draws: three and a half, the courier.
Zoom out, and this is the lecture's blueprint for the whole app, with the same three ports. The lecture calls the app ready, then admits: well, not really, we need to build it. Today we build the right-hand side, on your laptop.
To follow along, clone both repositories, keep Docker running, and free about 10 gigabytes. Your Google key matters only for the chat answers.
The tracker in the corner names the README step, code panels name their file and lines, and a yellow tag, your turn, means pause and run it.

## 01:22 — The blueprint, and your folders
First, where this lecture sits. The course project has its machine learning pipeline; what is still missing is the app: a backend API and a frontend.
The lecture draws the system as a technical architecture, the blueprint, one layer at a time. Developers, users, GitHub and Colab sit outside the cloud, Vertex AI inside, and every arrow is labeled with its protocol and port.
Then come a bucket, a registry of images and a persistent disk. On the right sits a cluster: NGINX in front, the app on 3000, the API on 9000, the vector database on 8000.
Today, that whole right-hand side runs on your laptop.
The lecture's folder rule: one Git folder per app, one folder per service under src, and secrets outside the Git folder. Version 1 even keeps empty folders for the services it does not run; version 2 holds only its three.
Steps 1 and 2: clone both repositories. The READMEs say clone or download; git clone is our spelling. Pause and clone them.
Step 3: next to the clones, create secrets and persistent folder yourself. Left to Docker on Linux, they would belong to root, and the container could not write there. Your ml workflow key goes into secrets.
One thing changed on the day we recorded: the main branch of version 2 moved twice. We follow main as you clone it today. The simple frontend the lecture teaches now sits on a branch called 2025, which we visit at the end.

## 03:04 — v1: a server, an app, a port
A browser sends a request; a server sends a response. A port picks which program gets it: public sites leave the default 80 and 443 out of the address; ours show the port.
In this course, an API means a REST API, built with FastAPI. Every client talks to that one API, and only the API talks to the stores.
Part 1, cheese app version 1. Step 1: go to the API folder; the README's path misses src, so this fails. A small slip: add src.
Step 2: sh docker-shell.sh. It builds the image, then starts a container that removes itself on exit, mounts your code, and publishes port 9000 to 9000. Pause and run it.
Step 3: the README's long uvicorn line. Here, uvicorn is the server: it owns the port and speaks HTTP. FastAPI is the app inside it.
The phrase api dot service colon app is an address: folder api, file service dot py, variable app.
Host 0.0.0.0 means every interface: the container's own loopback, and its network interface, where the tunnel arrives. Reload restarts the app when a file in api changes; the last part passes on extra arguments.
The log agrees: 0.0.0.0, port 9000, a reloader watching api, startup complete.
In service dot py, the app adds CORS middleware, which matters at the very end, and one route: GET slash returns a welcome.
Step 4: open localhost 9000. An extra curl shows the same reply: status 200 from uvicorn, and the welcome. Pause and try it.
That is the lecture's trip: forwarded to the published port, mapped into the container, the function runs, and the JSON comes back.
One kind note: the slide labels the inside of the container localhost 9000. Take it as port 9000 of the container: uvicorn listens on 0.0.0.0.
So, a quick test. If uvicorn listened on 127.0.0.1 instead, would a curl from inside the container work? And your browser on localhost 9000?

## 05:42 — A Python function becomes a URL
Inside, yes: the container's own loopback answers. From the browser, no: the forwarded request arrives on the container's network interface, where nothing listens. That is why the README says 0.0.0.0.
Step 5: the lecture writes a route as a decorated Python function. Add the README's square root function at the end of service dot py, and save. It returns the square root of x squared plus y squared.
In the server's terminal, StatReload sees the change and swaps in a fresh app. You restarted nothing.
Step 6: open square root, with its trailing slash. No arguments, so the defaults 1 and 2 apply: the square root of 5. Pause and try it.
Step 7: add x equals 2 and y equals 10. The query string fills the function's arguments, and back comes the square root of 104.
Two extras. A letter instead of a number bounces off the float type hint with 422.
Without the trailing slash, FastAPI answers 307 and points to the slash version.
The server's log shows each request with its status. 200, 200, 200, 422, 307.
Step 8: open slash docs. FastAPI built this page from your code: x and y appear as numbers, with their defaults, and you can try a call right there.
The type hints became the validation and the documentation. Pause and try one call from the docs page.

## 07:19 — Files for the browser: the simple frontend
Now the other half of version 1: a page. The lecture splits a page into HTML for structure, CSS for style and JavaScript for behavior. In version 1, index dot html links all three.
Step 1: go to the frontend folder. Same slip as before: add src.
Steps 2 and 3: pause, run sh docker-shell.sh, then http-server inside the container. It serves this folder on port 8080, with a one-hour cache. The addresses it prints are inside the container; your laptop uses 8080.
Step 4: open localhost 8080. This is the lecture's first trip: the request reaches http-server, a file comes back, and the browser draws it. Pause and open it.
An extra look at main dot js: the podcasts are sample data, which would normally come from an API. Part 2 adds that second trip.
Step 5: add a paragraph to index dot html. A small note: the README's snippet is an old whole body, and pasting it would drop the page and its script tag. Add only the paragraph.
Step 6: refresh, and the new text appears. Edits to main dot js may need a hard refresh, because http-server lets the browser cache files for an hour.
To clean up, press Control C and type exit in both terminals. The container list is then empty, because both removed themselves.
Docker system prune asks first, so type y for yes; the image list shows what stays.

## 09:13 — v2: four containers, and the cheese books
Now version 2, the real app: four containers on one Docker network. Chroma, the vector database, on 8000; a loader; the API on 9000; and the React frontend on 3000.
The prerequisites: a Google Cloud project with the Vertex AI API, the ml workflow key with the Vertex AI User role, and about 10 gigabytes. With your key, chat and embedding calls bill your project.
One honest note: our recording's key file is well-formed but belongs to no account. Everything that does not call Google works exactly as for you; the first Google call fails, and we show where.
Last setup step: put your project ID into both docker-shell scripts. Ours shows a placeholder.
The lecture's first step: make sure the vector database is running. Step 1: change into src, vector db, and run docker-shell.sh. Pause and run them.
The script creates the network, builds the loader, and Compose starts Chroma, publishing 8000 and keeping its data in a folder on your laptop.
Step 2, inside the container: download and load the cheese books. Eleven files, one finished line per book, 14,356 chunks in all. Pause while yours loads.
These are the RAG lecture's chunks and embeddings, downloaded, not recomputed.
Step 3: chat. The first Google call, embedding the question, fails here: invalid grant, account not found. With your key, an answer from the books appears instead.
A small note: chat always asks its own fixed question, how is cheese made; there is no place to type yours. To ask another, edit that line in cli dot py.
Step 4: exit. Chroma keeps running on 8000, as an extra docker ps shows, and the network's phone book now turns its name into an address.

## 11:16 — Start the API: alive, then ready
Backend APIs. In a new terminal, from the cheese app v2 folder: step 1, change into src, api service, and run docker-shell.sh. The first build takes a while, because of TensorFlow, so pause and start it.
The banner offers two commands: API server and pytest.
This script checks first: if the container already runs, it just opens a shell in it. Otherwise it mounts secrets without write access, mounts your persistent folder, publishes 9000, and joins the network.
Step 2: API server. It is almost the same uvicorn line as before, pointing at api dot service colon app. Pause and start it.
Application startup complete arrives at once. Only after it do TensorFlow's lines appear, from a background thread that loads the cheese classifier.
That is the design: the API answers right away while the model loads. Two probes say how far along it is: healthz and readyz.
Step 3: healthz says 200: the process is alive. Readyz says 503, CNN model is loading.
An extra look: the model is downloaded once into your persistent folder, and every start reuses it.
Another extra: the version 1 habits fail. Slash and slash docs answer 404; everything the browser calls is under slash api, and only the probes stay at the root.
So, a quick test. Healthz says 200 and readyz says 503. Do you restart the container, or wait?
Wait: about nine seconds later, readyz says 200: the model is loaded and Chroma answers. A restart would only start the loading over. Kubernetes, which you meet in lectures 19 and 22, can use exactly these two probes: restart on liveness, send traffic on readiness.

## 13:39 — Screens decide the routes
Which routes does the API need? The lecture starts from the screens: newsletters, podcasts, and a chat that takes a photo. Each screen needs data, and each kind of data becomes a group of routes.
In service dot py, newsletters and podcasts get a router each under slash api. Then one function stamps out three chat routers: Ask, Identify and Cheese books. The lecture shows six groups; agent chat has no router in this repository.
The lecture also shows three places an agent can sit, with or without an MCP service. This repository has none.
And the slide's one-file route is the idea. The repository puts the same function in a router, mounted at slash api, newsletters.
Demo route: add the README's function after get status, and save. The server reloads by itself.
This loads the model again, and readyz is back to 200 shortly after.
Then open slash api, square root: the square root of 5 again. With x equals 3 and y equals 4, it answers five point zero. Pause and try both.
API docs: they moved to slash api, docs. An extra listing shows all 25 operations: the leaves of this tree.
In the docs, pause and try get newsletters with a limit of 2. Two newsletters come back as JSON, newest first: the lecture's example, now real. An unknown ID gets 404, newsletter not found.
Review the code: the README's table maps each file. Service dot py builds the app, settings dot py holds every setting, the routers hold the routes, and one utils file per chat mode does the work.

## 15:28 — A chat is a file, not a memory
The lecture's chat handler says: use Gemini to generate text. In the repository, one route starts a chat and another continues it. The real path names the mode: slash api, llm, chats.
How does the API remember a conversation? It does not: with every message, the browser sends a session ID, one random UUID per browser. The API opens that session's chat file, adds your message and the reply, saves, and forgets.
Two extras: no session ID, or an empty message, gets 422.
Identify's photo step works fully offline. We send the repository's own blue cheese photo, and the CNN guesses parmigiano, at 58 percent. A follow-up question would go to Gemini.
An extra listing shows it on disk: one JSON file per chat under your session, and the photo in the mode's images folder.
Ask mode calls Gemini, and here it stops: Internal Server Error, status 500. The API's terminal shows why: the same invalid grant, account not found. With your key, Gemini's answer has this shape.
A small note: the README's table covers Gemini 403 and 404, reported as 502. A key Google cannot sign in with fails earlier, as a plain 500, so check the API's terminal first.
Two more README notes. Each message rebuilds the conversation from the saved file, so any copy of the API can answer. And routes written with plain def run in threads, so one slow answer does not block the rest.
Last, the tests: in a second terminal, in the same folder, docker-shell.sh again opens a shell in the running container. Run pytest: 26 passed. Pause and run it.
Keep this container running. The API is ready, but nobody can use it from a browser yet. In part 2 the browser talks to port 3000, so how does that reach 9000?

## 17:46 — Why a framework: React with Vite
Part 2: the frontend. The API is up on port 9000; now a page that uses it.
The lecture starts with one HTML page per feature. Each carries its own header, script and style; nothing is shared, and every click loads a whole page: slow.
The fix is a single-page app built from components, with a framework. The lecture names the common ones and picks React.
In React, a component is a function that returns markup, written in JSX. The app is one shell: a header defined only once, a footer, and in between a block that changes with each page.
Today's repository uses React with Vite, a development server and build tool, plus React Router. In main dot jsx, a route table maps each address to a page, with a star that catches everything else.
In App dot jsx, the header and footer are written once, and between them sits the outlet, the window where the current page appears.
React setup, in a new terminal from the cheese app v2 folder: step 1, change into src, frontend react, and run docker-shell.sh. It mounts your code, keeps node modules in a named volume, publishes 3000 to port 5173, and joins the network. Pause and run it.
The banner shows Node and npm. Your first run installs the dependencies into the volume; ours was already up to date.
Step 2: npm run dev. Vite is ready and prints two addresses on 5173; both are inside the container, so on your laptop, use 3000. Pause and start it.
Step 3: open localhost 3000. The HTML is almost empty: one div called root and a script, main dot jsx. The whole app is one page and its JavaScript.
An extra check: every address, even one that does not exist, returns the same HTML. The browser picks the page, not the server.

## 19:55 — One origin: the Vite proxy
Now the hook's answer. In the lecture, the page's JavaScript calls the API. Here, every call in api dot js goes to a relative path starting with slash api, with the session ID from local storage.
And vite dot config dot js holds the courier: a proxy rule that forwards slash api to cheese app API service, port 9000, by container name.
So the browser only ever talks to localhost 3000. Vite, in the frontend container, carries each slash api request across the network. That is why uvicorn answered on 3000.
An origin is the scheme, the host and the port. The page and its API calls share one origin, so the browser has nothing to object to, and the API needs no permission slip.
So, a quick test. Could the page's JavaScript call the API by its container name, port 9000, directly?
No. The JavaScript runs in your browser, on the laptop, and the laptop's DNS knows no container names. Only code inside the network can use them: the Vite proxy, nginx, the API.
An extra experiment: unplug the API from the network for one request. The browser gets 502 with an empty body: the README's troubleshooting row for pages that load empty.
Review the app: home, podcasts and newsletters load through the API, and the Recent tab keeps your chats across a reload. In chat, Identify works through the proxy; Ask, and Cheese books with its Tolminc question, get the same 500. Pause and click through.
The README's code table names the files we just saw; pause to match each one. Then, in a second terminal in the same folder, docker-shell.sh again opens a shell in the running container; run npm run check: a lint, a format check and a production build. That build is what production serves.

## 22:11 — Production: nginx instead of Vite
In production, Vite does not run, so who serves the files and forwards slash api? Nginx does. Today's README dropped this section on the recording day, but its files are still in main, so we run the earlier README's commands, marked extra.
The production Dockerfile has two stages. The first builds the app with Node. The second starts from nginx and copies in only the built files.
The nginx template has the same rule as Vite: slash api goes to the API container. Any other page address gets index dot html, so the router can choose the page; only a missing asset is a real 404.
Stop the dev server with Control C and exit, then build the production image, tagged prod. Its first stage runs the same Vite build you just checked.
Run it on the network, publishing 8080 to port 80. Open localhost 8080: the server is now nginx, slash api still reaches the API, and a deep link still gets the page.
Compare the sizes: 331 megabytes for the dev image, about 95 for production. No Node, no Vite: just files and one proxy rule.
The lecture's production slide: only the outside changes. In lecture 20, NGINX goes in front on a cloud machine, on port 80; the API's code and port stay the same.
As an extra, stop it, stop the API too, and start the production container again. It will not start. So, a quick test: why would a page server care whether the API is up?
It exits at once: host not found in upstream. Nginx looks up the proxy target's name when it starts, and the API is gone. Start the API first.

## 24:11 — One command, then clean up
Instead of three terminals, one command. Step 1: put your project ID into the compose file in src. It appears twice.
The file names the same four services. The loader first checks whether the books are already in Chroma, and loads them only if not.
Step 2: stop whatever still runs, then docker compose down in src, vector db. Compose warns about two unset variables; the shell scripts set them, so this is harmless.
Step 3: change into src, and docker compose up with build. Pause and run it.
Two warnings: the network and the volume already exist, made by the shell scripts. They are warnings, not errors. Then four containers are created.
Chroma, uvicorn and Vite start together, and the loader exits with 0: it found the books already loaded.
Step 4: open localhost 3000 and the API docs. A small slip: the README prints port 900; use 9000.
Step 5: Control C, then docker compose down removes all four containers.
Docker cleanup: compose down in vector db finds nothing left. Docker system prune asks first, then deletes the network and about four and a half gigabytes of build cache.
Prune keeps every tagged image, including the API's image of over 4 gigabytes, and the node modules volume. Remove those by name if you need the disk.

## 25:49 — Tutorial 24 lives on branch 2025
Now Tutorial 24, the lecture's simple frontend. Main dropped it on the recording day; branch 2025 keeps it, with last year's API, which serves it. Branch 2025 builds its own big images: if your disk is tight, remove main's images first.
Git switch 2025 refuses at first: your edits to four files would be overwritten. An extra stash puts them aside.
An extra log shows last year's commit, with frontend simple. Its vector db script wants a second key name, so copy your key under it, and set your project ID again.
Vector DB steps 1 to 3, from the folder above cheese app v2, as the 2025 README spells them, end in the same load: 14,356 chunks. Its Chroma image is tagged latest and still works. Leave with exit; Chroma keeps running.
Backend steps 1, 2 and 4, in a new terminal from the folder that holds both clones: change into the API folder, sh docker-shell.sh, and uvicorn server. Pause and start it.
Two differences from main: the reloader is WatchFiles, and the model loads before application startup complete, so start-up waits, with no readiness probe.
Then verify localhost 9000: welcome to AC215. A small note: the demo route and the routers the 2025 README asks you to enable are already in the code, except RAG and agent. Don't paste them again, or the route is duplicated.
Also, last year's Gemini model is retired: even with a key, its chat fails until the model and region are updated; main uses a current one.
And what matters next: CORS middleware that allows every origin, the permission slip main no longer needs.

## 27:55 — Last year's pages: CORS and the preflight
Tutorial 24, step 1: change into cheese app v2, src, frontend simple. Steps 2 and 3: sh docker-shell.sh, then http-server on 8080. Pause and start it.
Home page: open index dot html. The landing page links to two more pages: newsletters and chat.
Newsletter feature: open newsletters dot html. Its script names the API: localhost 9000. This is the lecture's second trip: the page came from 8080, and its JavaScript calls 9000 itself.
Same laptop, different port, so a different origin. Now the browser checks every answer: did the server allow this origin?
An extra curl sends what the browser sends. The API answers with access control allow origin, star: permission granted.
First comes 307, then 200: the paths differ by one slash, an extra round trip.
Chat feature: open chat dot html and ask how cheese is made. Now the browser adds a step the lecture never draws: step zero, the preflight.
A JSON post with a custom header makes the browser ask first, with an OPTIONS request. The answer allows any origin, these methods and these two headers, for 600 seconds.
The log: OPTIONS 200, then the post bounces with 307 and ends in 500, the same Gemini error. That 500 carries the permission header too, so the browser shows the real error.
So CORS is the browser's rule about the server's permission; curl and the docs page never meet it.
So, a quick test. Last year's page needed CORS, and this year's React app does not. What changed: the API, the browser, or the origin it calls?
The origin. The React page calls its own origin, and a proxy forwards: nothing to permit. The API then dropped the middleware, because nothing needed it.
To stop, Control C and exit in both terminals. As extras, stop last year's Chroma, discard the branch's edits and switch to main; git stash pop restores yours.

## 30:26 — Tear down, recap, and what's next
Before you go, a cleanup checklist, all done once already. Exit every container, compose down, back to main, prune after checking its list; then remove the node modules volume and big images by name. Your key stays in secrets.
Here is the whole trip, with the hook answered: the browser talks only to 3000. Inside, Vite in development or nginx in production carries slash api by name to uvicorn on 9000, where a router runs the function. The JSON comes back the same way: one origin, no permission needed.
Back to the lecture's blueprint. Your four boxes rise into the cluster. NGINX in front, the registry and the persistent disk are still dashed: the next lectures build them.
For your project, the lecture asks you to draw your solution and technical architecture, and points to a crash course and a template repository.
Test yourself, pausing on each. One: trace a newsletters request on main. Which container does the browser talk to, and where does port 9000 come in?
Two: what do api dot service colon app, host 0.0.0.0 and reload each do, and why does square root without a slash answer 307?
Three: healthz and readyz. What does each one check in this API?
Four: where does a chat stay between two messages, and why can any copy of the API answer it?
Five: which file decides where slash api goes in development, which in production, and why did last year's API need CORS while main's does not?
