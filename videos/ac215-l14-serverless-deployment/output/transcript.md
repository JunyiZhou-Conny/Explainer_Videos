# AC215 · Lecture 14 — Serverless deployment: a function, a service and a job on Cloud Run (follow-along: serverless-deployment)

## 00:00 — It works on localhost
Here is a translation page running on your laptop. Type good afternoon everyone, choose French, press Translate, and it answers: Bonjour à tous.
Now send the address to a classmate. On their laptop, localhost 8086 finds nothing, because localhost always means this machine, and nothing runs on theirs.
Lecture 1 gave one fix: rent a virtual machine. The page gets a public address, but the machine is billed all night, while nobody translates anything.
So here is today's question. Can this page have a public URL, and cost nothing while nobody is using it?
That is the promise of serverless. A copy of your app appears when a request arrives and disappears when the traffic stops. By the end, the same image also runs as a job. It takes a passage from a private bucket, speaks it in French, saves its files and exits.
To follow along, have your clone, Docker, the gcloud tool and your own project with billing ready.
A tracker in the corner names the README step, and a yellow tag, your turn, means pause and run it. Follow the console steps first; the gcloud boxes are alternatives, not extra steps.

## 01:17 — One app, four ways to deploy it
First, where this lecture sits: inside the prototype phase of the course project, where deployment begins.
Of the Cheese App's four parts, three are done. Model deploy is left, and milestone 3 asks you to deploy your model or API with Cloud Functions or Cloud Run.
The lecture's serverless: code runs only when needed, no servers to set up, and costly hardware only for the step that needs it.
Last week's Vertex AI training job was one case; today, functions and Cloud Run; next week, endpoints and pipelines.
Its map is one app, four ways to deploy it. Across, what you hand over, a code file or a container; down, where it runs, a rented machine or serverless. Lectures 1 and 2 filled the top row; today fills the bottom.
The README's four parts sit in that bottom row. Part 1 hands over a file. Parts 2 to 4 hand over one image, first as a web service, then as a job.
And notice what we deploy. Not the translation model, which an outside service runs, but the application code around it. Your Cheese App backend will play that role.
Two small notes. The course page links to sections the rewritten README no longer has, so start at the top. And we follow the README the course link serves now, not the older commit in the course map.

## 02:42 — Before you begin: project, region, clone
Before you begin. Select your course project and check its project ID, not just its display name; the command boxes need the ID. Confirm billing is on and that you may create these resources; if not, ask course staff first.
Choose a region: the README uses Toronto. The speech model later uses us-central1, a separate setting for part 3.
The worksheet names what you will create: the function, the web service, the job, two runtime accounts, and two buckets you name in part 4.
Step 4: clone the repository. The README says clone or download, so our git clone is extra, and so is the git log showing the commit we follow. Pause and clone it.
An extra listing shows older files at the root, including main.py and a Dockerfile, which the README never uses; don't build them. Today's work sits under tutorial: function for part 1, app for the image.
Then the terminal setup, starting with gcloud auth login, a browser sign-in; an extra auth list shows no accounts yet. It logs in the gcloud tool, not the app; the app's identity comes in part 3.
Seven exports follow: project, region, image, two names and two account emails built from your project ID. Pause and run them with your real ID.
About this recording: this machine has no Google account and no project. So every gcloud box runs until its first honest error, the console is drawn, and cloud results come from the README's own recording.

## 04:21 — Part 1: write a function
Part 1: a function. The lecture calls it lightweight code that an event starts, like a file upload, a database change, or today, an HTTP request. It is billed while it runs and scales by itself.
Its four steps: open the console, enable the APIs, write a Python file, deploy. One name has changed: Cloud Functions are now Cloud Run functions, so the README starts at Cloud Run, Services, Write a function.
That opens Create service. Enable the APIs if it asks. Name the service translate-function and choose your region.
For the runtime, pick Python 3.12; the older README said 3.10. Choose Allow public access, so anyone with the URL may call it, then Create.
Open the Source editor; pause and create yours. A gold tag: the function bills as a Cloud Run service, and every deploy runs a build.
Replace main.py with the tutorial's handler. The decorator marks an HTTP function called hello underscore HTTP. It takes text, source and destination from the request, each with a default.
Beside it, the lecture's sketch passes source second, by position. In this library the second slot is the destination, so source and destination would swap; the handler passes them by name.
Replace the requirements file with two exact pins. The newer googletrans is asynchronous and would break this simple handler.
Set the Function entry point to hello underscore HTTP. In the README's words, it is the Python function the framework should call, not the file name or service name. Select Save and redeploy and wait for the revision. Pause and do it.
So the slide's step, create a Python file, is the short version. The console wants the file, its dependencies and the name of the function to call.

## 06:21 — What runs your function?
What runs your function? The lecture says you manage no servers or containers, and that is true: you don't manage them. But Google builds a container anyway.
Save sends your three inputs to Cloud Build. It installs the requirements once, at build time, configures the Functions Framework, and publishes an image to Artifact Registry. Cloud Run starts a revision from that image.
In each instance, the Functions Framework runs a small Flask app under gunicorn, on every interface, at the port Cloud Run provides. On each request, it looks up your function by the entry point name and calls it.
So the lecture's file cell has a container inside. That is why there is an image to clean up at the end.
This layer also runs on your laptop, as an extra local stand-in. The same two pins install the Functions Framework, Flask, gunicorn and googletrans, as the build does.
Start it with target hello underscore HTTP, and it prints nothing while it serves. That silence is normal: the framework logs only errors.
You paste main.py but type translate as the entry point. Does the build fail? If not, what fails, and where would you see it?
Installing the requirements works; they are fine. But the deployment fails. When the new revision starts, the framework looks for the name: main.py should contain a function named translate, but it found hello underscore HTTP.
On Cloud Run, you find this in the logs, not in your code. That is the first of three places to look.

## 08:08 — Call it with a query string
Step 1: in service details, copy the URL near the top; the build page is not your app's address.
Step 2: open it with no arguments; the README's recording shows the default in Spanish: Bienvenido a AC215. Our local stand-in, the same handler under the same framework, agrees.
Step 3: append the query string. The question mark begins it, ampersands split the pairs, and percent 20 is an encoded space. Each pair fills one line of the handler, and its default steps aside.
The recording shows Bonjour à tous, and so does the stand-in. Step 4: try Greek, Hindi, or Z H dash C N for simplified Chinese. Pause and try a few.
The checkpoint: one endpoint, different inputs, no redeploy; and source and destination are languages, not regions.
Step 5: open Observability, Logs. The recording found its French request with status 200.
While we recorded, the provider timed out once: the client got status 500, and the server log showed the timeout, raised from line 12 of main.py. A retry soon after worked.
The README warns: the googletrans library wraps an unofficial outside service, so check the logs, not a finished build.
Now the gcloud alternative. In a new project it may first ask to enable APIs or create a repository; answer yes. With the placeholder, the deploy stops at the project ID check; with a real-format ID, it asks you to sign in first.
The next line stores the URL; the curl lines ran unchanged against the stand-in and answered Bonjour à tous.
From the README's More detail box: a cold start starts an instance of your app, not necessarily a new machine. No fixed idle time predicts it.

## 10:08 — Part 2: the prebuilt app on your laptop
Part 2. Now imagine a containerized web app already working on your laptop. Sharing localhost shares nothing, so we deploy that same image.
Step 1, with Docker running: docker run, remove when done, publish port 8086 to 8080, and the tutorial's public image. Pause and run it.
The digest equals the README's: same bytes, same digest. The image is built for A M D 64, which Cloud Run needs; on Apple Silicon it runs under emulation.
Then gunicorn listens on 0.0.0.0, port 8080: every network interface, so connections from outside the container reach it.
How did Python turn into gunicorn? First, the image has two start-up slots: an empty entrypoint, and a command, translation demo serve. Docker runs the entrypoint, then the command, and arguments you pass replace the command; part 4 depends on this.
That command takes its port from the PORT variable and replaces itself with gunicorn: 1 worker, 4 threads.
Extra checks agree. Docker top shows only gunicorn, a master and a worker; no Python is left. Docker ps shows the door, 8086 outside and 8080 inside, so 8080 on the laptop is refused.
Step 2: open localhost 8086. An extra curl shows status 200 from gunicorn, the title, and the disabled Play audio button.
Step 3: translate. The button sends JSON in a post request and gets back Bonjour à tous, once the browser decodes that escape. Pause and try it.
The query string from part 1 gets 405 here, method not allowed: this app wants JSON posts. A made-up language gets 400.
Step 4: Play audio is disabled, and its request gets 503: speech is disabled. Stop with Control C; gunicorn is the main process, so it shuts down cleanly.
One extra experiment: set PORT to 9090 but keep the pipe at 8080, and the connection resets; the log shows gunicorn on 9090.
Pipe to 9090 instead, and it answers. The right-hand number must be where the app listens.

## 12:39 — Deploy the same image
The lecture's Cloud Run runs a whole container, as a service or a job. Its steps: open Cloud Run, enable the APIs, deploy an image.
Open Cloud Run, Services, Deploy container, and choose Deploy one revision from an existing container image. Paste the same image, name it translation-demo, and choose your region.
Select Allow public access and Request-based billing. Under scaling, minimum 0 instances and maximum 2.
In the container settings: port 8080, 512 mebibytes, 1 CPU, and the command left alone; Cloud Run sets PORT and knocks on it. Then a 120 second timeout and 4 concurrent requests per instance.
Why 4? Each instance runs gunicorn with 4 threads, so it never gets more than it can serve.
With request-based billing and a minimum of 0, the meter moves only while requests are served. That is the lecture's promise: pay only when your code runs. A minimum of 1, or instance-based billing, bills idle time too.
Concurrency 4, maximum 2 instances. Ten people press Translate at once. How many instances start, and what happens to the last two?
Two instances, the ceiling, with 8 slots. The other two wait for a free slot and can be refused. Raise the maximum, or raise concurrency together with the threads; a higher minimum doesn't help.
Select Create; the recording shows the public page answering Bonjour à tous, speech still disabled. Then check Revision History and Logs. A revision is a deployed version of the image and its settings. Pause and deploy yours.
Nothing was built this time.
The console took a tag, a movable label; the revision keeps the digest, a fixed fingerprint. To reproduce a deployment later, deploy by digest.
The gcloud alternative sets the same values in one command.
First half done: your laptop's page at a public URL. But Play audio still waits: to speak, the app must call an API that asks who is calling. Who is it?

## 15:06 — Who may call it, and who it runs as
Part 3. The README separates two questions: who may call our public app, and what the running app may access.
The first door, who may call it, is Allow public access; gcloud spells it no invoker IAM check. If an organization policy forbids it, the URL answers 403.
So, a quick test. The service allows public access. Does that let it call Agent Platform?
No. That door only admits callers. Calling out goes through the other door, as whatever identity the service runs as; until you attach one, that is normally the project's default compute account.
Step 1: in the API Library, enable the Agent Platform API, the console's current name for what earlier lectures called Vertex AI.
Steps 2 and 3: create a service account named Translation demo runtime, with the ID translation-demo-runtime.
Step 4: two roles. Agent Platform User lets it call the model. Service Usage Consumer lets it charge calls to a quota project: the project whose quota and bill they count against. The app names your project there. Leave both principal fields empty and select Done.
Step 5: note the account's email. No key to create or download: in lecture 3 a JSON key sat in a secrets folder; here none exists. The recording shows the account enabled, with no keys; pause and create yours.
The gcloud alternative enables the API, creates the account, and adds the two roles; both bindings are on the whole project.

## 16:56 — Attach the identity, turn on speech
Attaching the account takes a permission of yours: Service Account User on that account. That is your deployment right, separate from the account's own roles.
Step 1: open translation-demo. Step 2: on the Security tab, choose your runtime account, and check its email.
A small gap: the README promises this access in section 3.3, but that section grants Token Creator instead. Project owners already have it; in a restricted project, ask course staff.
Step 3: three environment variables. ENABLE SPEECH, true; GOOGLE CLOUD PROJECT, your project ID; and GOOGLE CLOUD LOCATION, us-central1. The service runs in Toronto, the model in us-central1: two different settings.
Step 4: View diff and redeploy, keep Serve this revision immediately on, then Deploy changes. That makes a new revision; the old instance is replaced, not edited. Step 5: wait for the rollout.
Here is the speech path. The app checks the flag, the size and the language, then asks Google's auth library for a token; on Cloud Run, the badge supplies it. That lookup is Application Default Credentials. Gemini speech in us-central1 sends audio straight back; no bucket.
Step 6: reload the page, because it checks the flag when it loads. Then Translate and Play audio; the recording shows French audio playing. A gold tag: each Play audio is a paid model call.
Step 7: if it fails, check the message and the logs before changing permissions. Without the flag, you get our captured 503: speech is disabled. A missing identity or a denied call each has its own message.
That is limited control and debugging, made workable. The gcloud alternative makes the same change in one command.

## 18:54 — Develop locally with ADC
Section 3.3 is optional, and needs uv: how would you develop locally, without publishing an image for every edit? Application Default Credentials lets the same code find a token on Cloud Run and a file on your laptop.
To test the runtime account's real permissions, your laptop impersonates it. You sign in as yourself and receive short-lived tokens as that account; no private key is ever downloaded.
Step 1: on the runtime account, grant your own user Service Account Token Creator. Replace any preselected role, and don't leave Service Account Admin. Enable the IAM Service Account Credentials API too.
Step 2 begins with three commands that repeat step 1 from the terminal; if you used the console, skip them.
Then two new ones: an application default login, impersonating the runtime account, and its quota project. It is separate from gcloud auth login, and its file stays on your machine, never in Git or the image. Pause and sign in; a restricted project may also need Service Usage Consumer for you.
Step 3: change into the tutorial app folder, and run uv sync with frozen. It installs 41 packages exactly as the lock file says. An extra uv tree shows the six direct dependencies.
Step 4: in the terminal with your exports, start the app with the three variables and PORT set to 8086; this time you set the port. Pause, run it, then translate and Play audio at localhost 8086; with your sign-in, it speaks.
Extra checks: the button now says Play audio, and translation works. Speech answers 503: Google credentials are unavailable. That is the missing sign-in, what you see if you skip step 2.
Step 5: go back up two levels to the repository root.

## 20:55 — Finite work: a job and two buckets
Part 4. A web request has a person waiting, but a translated audio edition should take its input, translate it, speak it, save the files and exit. That is a job.
The lecture says a container runs as a service or as a job. Same image, two programs: serve keeps listening, with no end; batch walks four steps and exits.
You have seen this shape before: last week's Vertex AI training job was finite work too: start, train, save, exit.
A job has no URL, and its disk vanishes when it exits. So input comes from Storage and results go back there; a remote container cannot see a file on your laptop.
Step 1: Cloud Storage, Buckets, Create. Step 2: a globally unique name, such as your project ID plus translation input. Step 3: region Toronto, class Standard, public access prevention, uniform access, default soft delete, then Create and Confirm. Pause and create it.
Step 4: repeat for a separate output bucket. A gold tag: storage bills while files exist, and soft delete keeps deleted ones for a while.
Step 5: create a folder named run zero zero one in the input bucket and upload the sample passage, four short lines. Step 6: copy its Storage URI. Pause, upload and copy the URI.
That run zero zero one is a prefix you chose, not a real directory. The gcloud alternative makes both buckets and uploads the passage in one block.

## 22:39 — Command, arguments and the job's badge
Section 4.2: the job gets its own identity. Create translation-audio-job, give it the same two project roles, and note its email.
Then, per bucket: Storage Object Viewer on the input, and Storage Object Creator on the output, which adds files but cannot list or overwrite them. The web account needs neither.
Your own identity needs separate rights to upload, execute and see results. Pause and create the account and both grants.
The gcloud alternative creates the account and adds all four grants.
Section 4.3: attaching this account again takes your Service Account User on it. In Cloud Run, Jobs, Deploy container opens Create job. The same image, the name translation-audio, 1 task.
Container command: python, then Enter to make a chip. It fills the entrypoint slot, which this image left empty.
Container arguments: eleven values, each its own chip, and together they take the command slot's place. Dash m, translation demo, batch, input URI and your passage, source en, destination fr, output URI and your prefix. Each chip is one item of the argument list.
Then the same three variables, a task timeout of 5 minutes, and 0 retries, because a retry repeats paid work. On Security, choose the job's account by its email. Leave Execute job immediately unchecked, then select Create; pause and build it.
Paste all eleven into one chip, and Python looks for a module with that whole sentence as its name. The name is cut at the first dot.
Now the other mistake. You fill all eleven argument chips but leave Container command empty. What does the container try to run?
The arguments replace the default command, and with no entrypoint, dash m becomes the program. Docker's version fails: executable not found.
With nothing changed, the job starts the web server and waits until the timeout fails it after 5 minutes.
The gcloud alternative passes the same eleven values, comma separated, with command python.

## 25:09 — Execute it and collect the files
Section 4.4: open the job and select Execute. The recording shows it succeeding, with a green check in History.
What would a red mark mean? Our extra laptop run without the speech flag exits with status 1, an honest failure, so History tells the truth.
Step 2: open the execution, then Tasks, View logs. The job exits; it has no web URL. Its last output is a JSON summary with the output and manifest locations, status complete, and the files.
Step 3: open your output bucket, then run zero zero one. Inside is a folder with a random name. Step 4: three files: translated dot txt, speech dot wav, and manifest dot json.
The order matters. Each upload is create-only, and the manifest, saying complete, is written last. It is the receipt.
So, the third place to look. A green check says the process exited with 0; the manifest says the work is complete. Files without a manifest prove nothing.
Execute the same job again, with the same arguments. Is the first result overwritten?
No. A new attempt folder lands beside the first, and create-only uploads cannot overwrite. But it is not exactly once: a retry repeats paid work, which is why retries are 0.
Step 5: download the text and the audio with the icons. Pause and run your job. A gold tag: each execution bills its running time plus one speech call.
The gcloud alternative executes with wait, makes a results folder, and copies the output down. The wait flag does not stream your app's logs.
The README's checkpoint: the task finished, the process stopped, and its files remain in Storage.

## 27:09 — From the terminal, then the helper
Section 4.5: new work from the terminal. First, a permission of yours: running a job with overrides needs its own right, separate from the job account's roles.
Console only so far? Run the terminal setup first. Save a short passage, under 5,000 characters, as passage dot txt in the repository root, or copy the sample. Export both bucket names and upload it under run zero zero two; it stops at the placeholder again.
Step 3: execute the existing job with overrides. They replace the whole argument list for this execution only: a new path and Spanish. The saved job still says French, and a flag you leave out is not taken from it.
Step 4: after it succeeds, make the results folder and copy run zero zero two down. The README's recording shows a successful Spanish execution.
Section 4.6: the helper combines all three. An extra dry run shows its plan. It uploads to a fresh run folder named by the time and a random part, executes with the eleven arguments, and downloads.
Run for real, it prints each gcloud command before running it and stops at the first failure. Pause and run it with your names.
Step 2: open the result folder and play speech dot wav. The helper prints downloaded results only after it finds a complete manifest: the receipt again.

## 28:42 — Clean up, and what serverless costs
Clean up. Step 1: download what you want to keep. Step 2: delete translate-function and translation-demo, then the job.
Step 3: delete your buckets and the two runtime accounts once nothing uses them. Step 4: the function's image in Artifact Registry, still there after the service is gone. Pause and delete them all now.
Three additions. Soft-deleted files stay billable for a while; the build also leaves source archives and logs. And keep the shared public image; others use it.
Stuck on a step? The README ends with a troubleshooting table of symptoms and checks.
Here is the whole map. Part 1 handed over a file, and Cloud Build made the image. Parts 2 to 4 handed over one image: a service that scales to zero, and a job that exits with a receipt.
Now the lecture's three downsides, and our answers. Cold starts: a minimum of 1 keeps an instance warm, for money.
Limited control and debugging: three places to look, the build logs, the service logs, and the job's logs and manifest.
Vendor lock-in: the image and the Functions Framework ran on your laptop; only the console, the permissions and the build are Google's.
Next lecture: a Vertex AI endpoint for a trained model, then pipelines.
Test yourself, pausing on each. One: place parts 1 and 2 on the lecture's map. What do you hand over, and who builds the image?
Two: which two settings make the meter run while nobody uses the app, and what does a minimum instance buy?
Three: who may call it, and who it runs as. Which setting answers each, and why is no key file needed?
Four: why does the job set a command and eleven separate arguments, and what happens with neither?
Five: name the lecture's three downsides of serverless, and what this tutorial gives you for each.
