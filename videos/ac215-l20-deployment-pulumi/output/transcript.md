# AC215 · Lecture 20 — Deployment: by hand, then Pulumi to a single VM (follow-along: cheese-app-v3)

## 00:00 — One container stops, the site goes dark
We stopped one container, the frontend, and restarted the web server in front of it. The API container is still up, and so is the vector database.
Yet the whole site answers nothing, the address of the API included.
Today's puzzle: the API is running, so why is its address dead too? We answer it once we have built this by hand.
Here is the goal, the lecture's picture of deployment: the containers from your laptop move to one virtual machine in Google Cloud, with port 80 the only door. We build it twice: by hand, then as code.
On the course roadmap, the marker has moved to deployment, scaling and automation. Everything so far ran on your own computer. Users need a server.
You need cheese app version 3 with your secrets folder beside it, a Google Cloud project with billing, and a Docker Hub account. This costs real money, so each part ends by deleting everything.
The tracker in the corner names the README step, code panels name their file and lines, and a yellow tag, your turn, means pause and run it.
One honest note: our recording machine has no Google account and no Docker Hub login. What runs on a machine you own is real; every cloud step stops at its first honest error, and we say what yours prints.

## 01:24 — From your laptop to one VM
Let's draw the goal properly. A browser sends a request to port 80, where nginx passes pages to the frontend on port 3000 and data calls to the API on 9000. The API asks the vector database on 8000.
The slide draws its arrowheads the other way; we draw requests the way they travel. The slide shows four containers. There is a fifth: a loader that fills the vector database once and then leaves.
The lecture splits the manual route into four stages: push the images, set up the VM, deploy the containers, and put a web server in front. That is our map for part 1.
The README starts with a check, not a command: your containers run locally. The vector database is up, the API shows its docs on port 9000, and the frontend its home page on 3000.
A small note: on this code, slash status is a better API check than the docs page. It answers version three point zero, so you know which code runs.
If you followed lecture 18 lately, it now teaches a refactored version 2; here you run version 3, with this repository's scripts.
We follow main, the branch the course site links; on recording day it was this November 2025 commit. READMEs change; git log shows which one you have.

## 02:50 — Images to Docker Hub
Stage 1: push the images. Create an access token in your Docker Hub account settings; it is a password for scripts, so never show it.
Typed exactly as the README prints it, the login fails: syntax error near unexpected token newline. Angle brackets are redirections to the shell, so replace the whole placeholder, brackets included.
Better: the flag password standard in keeps the token out of your shell history.
Now the Docker Hub script, one in each service folder. Line 11 sets the user name to dlops, the course account: change it to yours.
Line 27 creates and selects a new BuildKit builder; the script builds, then builds again to push. The API script builds for A M D 64 and ARM 64; the frontend script, A M D 64 only.
Inside frontend react, outside any docker shell, run it. It prints dlops, creates the builder, and builds: compiled successfully. The warning says this build stays in the builder cache.
Then the push: access denied. We are not dlops, and not logged in; with your name and login, this is where it says pushed.
Run the same script in api service and vector db; we did not capture those two-platform builds. Those two build for two chip types, one of them emulated: expect a long api service build, and on Linux register Q E M U first. Pause, run all three, and check Docker Hub.
Skip this stage and part 1 still works, using the public dlops images, which are a little older than the code. If you pushed yours, replace dlops with your user name in the VM commands.

## 04:37 — A VM with Docker, folders and a network
Stage 2: set up the VM. In the console, create a VM instance with the defaults, except machine type N 2 D, a 50 gigabyte disk, and HTTP and HTTPS allowed.
Those two ticks add network tags, http server and https server; the default firewall opens 80 and 443 only to VMs with them. The VM now bills while it runs, its disk while it exists.
Pause, create yours, and SSH in with the SSH button in the VM instances list. Our VM is a stand-in we can capture end to end: a fresh Debian 12 machine without Docker. Every command is the same on yours.
Install Docker with the official script: download it with curl, run it with sudo. It adds the Docker repository for bookworm and installs the engine, buildx and compose.
Then check it with sudo docker, dash dash version. Pause here and install Docker on your VM.
Next, create folders: persistent folder, secrets and conf nginx, writable by anyone. The README lists these six commands twice: run them once, from your home directory.
An extra check: the folders belong to root, but anyone may write there: fine for a demo VM only. Stay in your home directory: later mounts use the current folder.
Now the app's key, gcp service dot json, written with echo; ours holds just the placeholder. Paste in the gcp service key from your laptop's secrets folder; part 2 shows how to make one. Never show or commit it.
Last, create the Docker network, cheese app network: a private network where our containers find each other by name. Pause and run these three steps.

## 06:32 — The vector DB and its loader
Stage 3: the containers. Pull the Chroma image, then stop and remove any old vector database. The error, no such container, is harmless here: or true makes the step safe to run again.
Then run it detached on cheese app network, publishing port 8000, restarting always, with a data folder mounted. Its name goes into the phone book.
An extra check: the port is published, the heartbeat answers, Chroma version one at the time of recording.
Now the loader, run vector db cli. It finds the database by name, cheese app vector db, not by address. The project is the README's default; change it to yours.
It downloads, creates the collection, and loads eleven files: 14,356 chunks in all. The embeddings come precomputed, so our placeholder key never mattered.
The loader ran with the remove flag, so it exits and is gone. Pause and run both containers now.
A question. The loader is gone. Are the 14,356 chunks gone too?
No. The loader only sent them; they sit in the vector database container, which keeps running. Remove it, and the loader must fill a new one.
But where inside that container? A small slip: Chroma saves to slash data, so the folder the README mounts stays empty. To keep the data on the VM disk, mount slash data instead, rerun the stop, remove and run lines, then the loader.

## 08:16 — The API and the frontend
Next, run api service. The image is not on the VM yet, so docker run pulls it first.
Two mounts, persistent folder and secrets; port 9000; the key path; and the database by name. The project is the README's default, and the bucket name is passed but never used.
The logs show loading CNN model, then uvicorn running on port 9000. The model comes from a GitHub release, not a bucket, so our picture grays out the slide's bucket.
And the image is big, about five gigabytes on disk, with TensorFlow inside.
Three extra curl checks: the root says welcome to AC215, and slash docs shows the docs page. Slash status says 404: the public image is older than your clone.
The README then offers an interactive variant. Run as written, it fails: the name api service is in use, because the detached container still runs.
Remove the running one with docker rm dash f, and the variant opens a shell. It is optional: we exit and start the detached one again.
Then the frontend, on port 3000. The extra check shows the title, Formaggio, and the base API URL, slash api service, which the page calls on its own address. Pause and start both.

## 09:44 — nginx: one public door
Stage 4: a web server in front. A reverse proxy gives the browser one address: nginx listens on port 80 and forwards each request inside the VM.
In the repository's nginx dot conf, the location block on line 35 catches paths that start with slash api service. It passes them to api service on port 9000.
Look at the end of that address: one slash. With it, nginx swaps the matched prefix for that slash, so slash api service slash status reaches the API as just slash status.
Everything else goes to the next block, the frontend on 3000. Both targets are container names on cheese app network.
The README writes this file with one long echo in single quotes. But the file holds single quotes too, so the shell eats the log format and leaves a dash and two brackets.
Routing still works, but the access logs are useless. Write it with a quoted heredoc instead: cat, the same text, then E O F.
If you used the echo, rewrite the file this way first. Then run nginx with that file mounted, publishing port 80. The container list shows four: ports 80, 3000, 9000 and 8000.
Open the external IP of your VM, from the VM instances list, in a browser, and the home page appears. On the VM, curl agrees: 200 OK, served by nginx, title Formaggio.
Slash api service says welcome to AC215: the prefix was cut on the way. Pause and open your site.
A question. Port 9000 is published on the VM. Does it answer from your laptop?
No. The two ticks opened only 80 and 443; no rule opens 9000. Port 9000 is open on the VM but shut at the network edge: one public door.
Now the puzzle. The web server looks up frontend and api service once, at start. With the frontend stopped, the restart fails that lookup and exits, taking the API route with it.
Start the frontend, then nginx, and the site answers 200 again. Start order matters, and so does a restart policy, which only the vector database command has.

## 12:19 — Twenty-one commands: repeat, review, undo?
Let's count what we typed. Twenty-one commands on the VM, plus console clicks, plus three Docker Hub scripts on the laptop. Each one added a block to the VM.
Now three questions. Repeat: can you build the same thing for a staging copy tomorrow? Review: what exactly is on that VM? Undo: how do you delete every piece?
The lecture answers with one idea: too many steps to keep track of, so let a tool do them.
That is infrastructure as code. You describe the servers, the networks and the software in a real programming language, Python here, and keep it in Git to share. No YAML file, no special language.
An earlier version of the course did these same stages as Ansible playbooks, written in YAML. This version does them with Pulumi, one to one.
One more thing the README never says: delete this VM now, before part 2. In the console, open VM instances, select it, and delete it with its boot disk. Pause and delete yours; the list should be empty.
Part 2 builds it all again, as code, and lets a tool remember every piece.

## 13:30 — Pulumi: desired state, not steps
Part 2. Each Pulumi program says what should exist, not what to do. One firewall rule from this repository: a constructor, compute Firewall; a logical name, allow http; and arguments: port 80, from anywhere, for VMs tagged http server.
The lecture's bucket example has the same shape. Running this line creates nothing: the constructor only registers the resource.
This is the lecture's picture of Pulumi: the command line tool runs your program, which produces the desired state, a tree of resources.
Pulumi also loads its state, what it created last time, from your bucket. The refresh flag first checks that state against what really exists.
Then it compares desired with current, and each difference becomes a plan line: plus to create, tilde to update, minus to delete, plus minus to replace.
Finally it calls the providers, plugins for Google Cloud, Docker and more, which make the API calls. The banner on the slide: Pulumi manages infrastructure through cloud APIs.
The lecture lists seven commands. The tutorial uses five: stack, config, preview, up and destroy, with refresh only as a flag. The command new stays gray, because both projects already exist.
Now the README's command: pulumi up, stack dev, refresh, dash y. Up previews, asks, then applies. Stack dev picks the environment. Refresh syncs the state with reality first.
Dash y answers yes to the question, do you want to perform this update, and skips your chance to check the plan. Step 3 shows when that matters. Preview stops before anything changes.
A question. You run pulumi up again and changed nothing. What should the plan show?
Nothing to do. Desired equals state equals reality, so there is no difference, and nothing is created, changed or deleted. Hold that thought: one stack in this repository breaks the rule.

## 15:46 — Setup: four APIs, two keys
The lecture splits the automated deployment into six steps: setup, images, VM, provisioning, containers and web server. Each maps to a file; we start with step 1.
First, enable four APIs: Compute Engine, Service Usage, Cloud Resource Manager and Artifact Registry. The app's chat also needs Vertex AI, from earlier lectures.
Then create two service accounts. Deployment gets six roles, among them Compute Admin, Compute OS Login, Artifact Registry Administrator and Storage Admin. Create a JSON key, and rename it deployment dot json.
The second, gcp service, gets three roles: Storage Object Viewer, Vertex AI Administrator and Artifact Registry Reader. Its key becomes gcp service dot json.
Why two? Deployment builds things. It needs admin rights on your group's project, not the README's default, to create the VM and log in. The narrow account only runs things: it reads images and stored files and uses Vertex AI.
Both keys go into a secrets folder next to your clone, not inside it. The deployment script of the next step looks three folders up from src deployment to find it. Pause and place your keys.
One step is missing from the README: nothing creates the Artifact Registry repository. We create it with one extra gcloud line in the next step, once the deployment container runs; skip it, and the push fails.

## 17:24 — The deployment toolbox, fixed twice
Rather than each of you installing different tools, the README packs them into one container, the deployment toolbox. Lines 9 to 17 of docker-shell.sh set its environment.
Lines 34 to 43 wire it to your laptop. They mount the Docker socket, so it builds on your Docker, then deployment as slash app, the secrets, a Docker config and the three service folders.
Change into src deployment. In docker-shell.sh, set GCP project to your project ID; ours is a placeholder.
Now run docker-shell.sh, as committed. Downloads answer 404 not found, the build stops, and the script runs the container anyway: pull access denied.
The cause is line 4: the base image is Debian 11, bullseye, whose security updates moved to an archive. Fix 1: change bullseye to bookworm, Debian 12.
Run it again. Now it stops at line 29: google cloud SDK has no installation candidate. Google renamed it, and apt even names the replacement, google cloud CLI.
Fix 2: rename both packages. Here is the real diff of the two fixes, one line each. Pause and make both edits.
The third run builds in about 92 seconds, and the entrypoint starts. First error: invalid grant, account not found. Our key belongs to no account; yours activates the deployment account.
The project and registry helper pass. Then the state bucket: ours could not be created, and Pulumi could not log in. Yours creates the bucket the first time, logs in, and leaves you here.
Check the tools: gcloud, Pulumi and kubectl. One surprise: kubectl is newer than the Dockerfile pins, because Google's apt repository has its own kubectl package with a higher version, and apt picks it.
Last check: gcloud auth list. Ours says no credentialed accounts. Yours lists the deployment account as active; if not, check the file name in secrets. Then create the registry repository with the extra line from earlier. Pause and run both.

## 19:44 — SSH keys and OS Login
This is the one setup the slides skip. Pulumi will log in to the VM over SSH to run scripts and drive Docker. Who logs in? The deployment service account, through OS Login: the VM accepts a key registered to that account's login profile, under a Linux username Google derives from it.
First, turn OS Login on for the project. Typed as printed, the template fails with no such file. It is the angle bracket lesson again: replace the whole placeholder.
The README example uses its own project, which you change to yours. Ours says no active account; yours prints updated.
Next, the key: in slash secrets, run ssh keygen with the name ssh key deployment, press Enter twice, and go back to slash app. No passphrase: Pulumi cannot type one.
The two files now sit in the secrets folder on your laptop: the private key, readable only by you, and the public half.
Then upload the public half to the OS Login profile. Ours stops at the same error; the README shows yours, ending in a username that starts with S A. Copy it: the VM stack's config needs it.
A small slip: the next heading asks you to edit inventory dot yml. No such file exists; it belongs to an earlier, Ansible version of the course. The Pulumi config replaces it.

## 21:12 — Step 2: images with timestamps
Step 2: build and push the images. Your laptop's arrow lands on the registry; slide 21 still calls it GCR, its retired name: today it is Artifact Registry.
Pulumi keeps environments apart as stacks of one program, dev, staging and production, each with its own state and config. The tutorial has one stack, dev, per project.
Its full name, organization, deploy images, dev, is used by the VM project, so do not rename it. Every stack state sits in your bucket.
Change into deploy images and run pulumi stack init dev. Without a bucket login, Pulumi offers its own cloud and waits for a browser. If yours says the stack already exists, use pulumi stack select dev.
Config set, preview and up all print: Pulumi access token must be set. To show them anyway, we use a local folder, pulumi login local: extra, and not for you.
Stack init answers created stack dev, and config set writes your project into Pulumi dot dev dot yaml.
Now the program. Line 13 makes a timestamp, down to the second, and lines 14 and 15 build the registry address.
Each image is one docker build Image resource: a timestamped tag, push true, retain on delete, and one platform, A M D 64. An Apple silicon Mac emulates that slowly. Lines 34 and 35 export the tag for the other project.
The extra preview, frontend only: five provider plugins, one image to create with its timestamped tag, and a warning: skipping preview build. A preview never builds.
Up does build: the npm install, the Next.js build, then the push, which fails here with 403 forbidden. Yours builds all three images, slowly, and ends with each tag in the outputs. Pause and run it.
Remember the earlier question? This stack breaks the rule: each up rebuilds the images, because the timestamp is new every run. Each run can add image layers to the registry, and storage costs money.

## 23:28 — Steps 3–4: the VM, its fences, provisioning
Step 3: create the VM. The slide draws a network share beside it; in this code that is a second disk, mounted at mnt disk 1.
Change into deploy single VM, then stack init, three config sets, preview and up: without the bucket login, each prints the same error.
On the local backend, the config shows the project, your masked username, and the account the VM runs as: deployment at your own project, not the README's. Pause, set all three, and check them with pulumi config.
The main file makes four calls, in the lecture's order: create the instance, provision it, set up the containers, set up the web server.
Create instance builds the fences first. There is a cloud network, also called cheese app network, and three firewall gates: 80 and 443 for the tagged VMs, 22 for every VM.
Then a 50 gigabyte data disk, and a lookup of the newest Ubuntu image. The VM address is an output, a sealed envelope that opens once the VM exists.
The real preview plans a disk, a network and three firewalls, then stops at line 100, invalid grant: the image lookup is the first call needing Google. Yours goes on to about thirty resources.
Check the plan before dash y: a newer Ubuntu image can turn the next up into a VM replacement. Then pause and run up. From here it costs roughly two dollars a day, plus disks and an address.
Step 4, provisioning, has no slide picture: it happens inside the VM, over SSH. Nine remote commands run in a chain: format and mount the disk, update, install Docker.
Pulumi remembers that a command ran, not what it changed. Look at the first one: block ID checks for a filesystem, and only if there is none, make file system formats the disk.
A question. Why check with block ID first, instead of just formatting the disk?
Because formatting erases. If this step ever ran again, after a new trigger or a replaced resource, plain formatting would wipe the data disk: the chat history and the model. Scripts Pulumi cannot inspect must be safe to run twice.

## 26:02 — Steps 5–6: containers over SSH, then test
Step 5: the containers. The VM program asks the images stack for its tags, through a stack reference to organization, deploy images, dev. So run up in deploy images first.
Then a Docker provider whose host is SSH, with your key, so each container on the VM is a resource Pulumi can compare and replace.
Three containers appear: the frontend, the vector database on 8000, the API on 9000. The slide puts the frontend on 80; the code, on 3000.
Step 6: the web server. The nginx container appears on top, and port 80 moves onto it.
Its config file is uploaded with a checksum as a trigger. Change nginx dot conf, and only these steps run again.
No successful pulumi up was captured. So here is what it builds, drawn from the code. It ends on six outputs, among them the instance IP.
A small slip: the exported SSH command leaves out the key. Add dash i slash secrets slash ssh key deployment.
The lecture marks the job of each key: deployment creates the VM and logs in, the narrow key reads images and models.
A question. The running app needs one key. Which would you hand the VM, and why not the other?
The gcp service key: it reads images and stored objects and uses Vertex AI; it cannot create VMs, disks or buckets. Deployment can, which a compromised VM should never hold.
Two footnotes. This repository pulls the images with your deployment credentials and runs the VM itself as deployment, capped only by scopes, a list of what the VM may call. And the API calls Vertex AI with the narrow key. Try the narrow one as an exercise.
The lecture's last step: test the app. Open your instance IP; the footer shows the API version from slash status.
On the VM, through the console's SSH button or the fixed SSH command, the README checks: list the containers, follow each log, Control C to stop. Our stand-in names the database cheese app vector db.
Exec into api service and into nginx. One note: chat needs a Gemini model Vertex AI still serves; change it in the API's helper files, then run up in both projects.

## 28:54 — Destroy, recap, and what's next
The lecture ends with a slide of its own: don't forget to delete.
In deploy single VM, run pulumi destroy, stack dev, refresh, dash y. Pause and run yours. Ours shows the login error; on the local backend, with nothing to delete, it finishes in a second.
Destroy plays the graph backwards: the containers over SSH, then the VM, the disk, the firewalls and the network.
Run it in deploy single VM; in deploy images it only forgets the images, which stay in the registry, retained on delete.
Your teardown checklist. One: destroy the VM stack, and check the VM list is empty. Two: delete the registry repository with gcloud. Three: the state bucket, last, once no stack holds anything.
Four: the part 1 VM, if it still runs. Five: your Docker Hub images, free and optional. Six: when the course ends, both service account keys.
The recap is the lecture's six steps, each with its file: docker-shell.sh, deploy images, create instance, provision instance, setup containers and setup webserver.
The lecture also names six principles. Real language, declarative, state with previews: yes. Components and tests: not here. Many providers, but one cloud.
One VM is a single point of failure. Lecture 21 automates builds and tests, lecture 22 moves to Kubernetes with this toolbox, and lecture 23 runs pulumi up from GitHub Actions.
Test yourself. Trace your instance IP slash api service slash status: which gate, which container, which location block, and which character makes the API see slash status?
What three things does pulumi up compare, what does refresh change, and what does dash y skip? Name the two service accounts, where each key sits, and what each may do.
Which of the six steps can Pulumi inspect afterwards, and which does it only remember? What survives destroy? Answers are in the exercises and the study guide.
