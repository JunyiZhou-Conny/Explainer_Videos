# AC215 · Lecture 14 — Serverless Deployment (exam edition)

## 00:00 — A job that never finishes
Here is a Cloud Run job called translation audio. It uses the same image as a translation web app that works perfectly. We press Execute, and the job starts.
Minutes pass. Nothing lands in the output bucket, and the job never says it is done. It runs straight into the task timeout we gave it. 5 minutes, and the platform stops it.
The clue is the last line of the Dockerfile: its default command starts the web server. The README's troubleshooting table even lists the symptom: a job that starts a server instead of finishing.
Same image, same code. So why does the web app work, while the job never ends? Hold that question.
For the quiz, this lecture comes down to five ideas. Service or job. Who pays for idle time. What you hand over to deploy. Who may call your code, and who it runs as. And the model endpoint: where preprocessing lives, and which function it calls.
The gray tag, top right, names the lecture slide behind each idea.

## 01:10 — Service or job: read the lifecycle
The lecture says Cloud Run runs a container as a service or a job. The demo app shows both: one image, two startup commands, serve or batch.
Serve starts gunicorn, a web server, on the port Cloud Run gives it, 8080 by default. Then it waits, and answers each request that arrives.
That shape is a service. It has a URL, adds instances when traffic rises, and can scale to zero when it stops. It never finishes on purpose: listening is its job.
Batch has a different shape. It reads the passage, translates it, generates speech, saves the files, and exits. If a step fails, it exits with status 1, so the execution shows failed, not a false success.
The README calls this a job: no URL, nothing waiting for requests. Something starts it, and it runs to completion.
Now the hook. The job inherited the image's default command, serve, so it started a web server and waited for requests that never come. The fix: the command python, with the batch arguments. Same image, and now the strip ends.
Who presses start? In the README, you click Execute. For a nightly run, the usual trigger is Cloud Scheduler, which this README does not use.
Try one. A container indexes new documents and exits, once an hour. Read the lifecycle, not the product names.
B, a job on a Cloud Scheduler timetable: it runs to completion and costs nothing between runs. A pays for an instance all hour, and an idle service's CPU is throttled, so the loop stalls. C breaks the service contract: an instance that exits has crashed. D works, but the VM is paid for all hour while it idles. Why that matters is next.
So the rule: if the question says it runs, writes its output and exits, or that it runs every night, pick a job. If it says it answers requests, has a URL, or listens on a port, pick a service.

## 03:32 — Who pays for the idle hours?
The lecture promises you pay only while your code runs. Let's make that exact: two meters, one day. The yellow ticks are requests.
The top row is a virtual machine. Its meter runs from boot to shutdown, requests or not. The gold shading is idle time, and you pay for all of it.
The bottom row is a function, or a Cloud Run service with request-based billing and minimum instances 0, as in the README. Its meter moves only with invocations and how long each one runs.
Now stretch the quiet gaps between requests. The VM meter grows, because idle hours are still provisioned hours. The function meter does not move at all: no requests, no charge.
Zero idle cost has a price, and slide 16 names it: the cold start. After a quiet stretch, the first request waits while an instance starts. The README's remedy is minimum instances. Set it to 1, and a warm instance stays on for the first request, with its own meter running.
That always-on instance now sits in the VM row. So does next lecture's Vertex AI endpoint: its deploy call asks for a minimum replica count of 1, which the README calls the part that costs money.
Test it on a new case. Twice as many requests, each just as long, in the same days. Which bill changes?
B, only the function's. Watch: every request splits in two, and the function meter climbs, since every invocation and its running time are billed. The VM meter does not move, because it bills provisioned hours: A is backwards, and C is wrong. D confuses no minimum charge with free work.
So the rule is not, serverless is cheap. The rule is: is anything always on? Idle time moves only the bills of always-on things. Request count and duration move only the pay-per-use bill.

## 05:45 — Function or container: what you hand over
Next, what you hand over. The lecture deploys one translate app four ways: virtual machine or serverless, code file or container. Earlier lectures filled the VM row. Today fills the serverless row.
For a function you hand over a source file, its requirements file, and one name. The file is main.py: an HTTP handler called hello underscore HTTP, which reads the text and two language codes from the request.
That name is the entry point: the Python function the framework should call. Not the file name, and not the service name.
Then Google builds. Cloud Build installs the requirements, configures the Functions Framework, and publishes an image to Artifact Registry. This happens once, at build time, not on every request.
The framework finds your function by that name. Type main as the entry point, and there is nothing called main to find. The function build fails, and its build logs tell you why.
Slide 11 says a function runs without managing containers. You do not manage one, but Google still builds one. And the slides' Cloud Functions are now Cloud Run functions.
For a Cloud Run service, you hand over a finished image by its URL. Deploying it builds nothing: the image was built beforehand. Its Dockerfile picks the base Python, the default port, 8080, and the startup command. You control all three.
Both are called through an HTTPS URL. The function takes new inputs through its query string, with no redeploy.
Both end as the same thing: a container instance on Cloud Run. A function is a container you did not write. On the quiz, source plus an entry point means a function. Your own image, or your own startup command, means a service.

## 07:46 — Who may call it, who it runs as, where to look
Every deployed service faces two permission questions, and the README keeps them separate. Who may call our public app? And what may the running app access?
The left door is the caller. With public access allowed, any browser's request gets in. Without it, a caller with no permission is turned away with a 403, before your code even runs.
The right door is who your code is when it calls out. The web app wears a service account badge, translation demo runtime, with two roles: Agent Platform User and Service Usage Consumer. You do not create or download a key.
The code just asks for default credentials, and on Cloud Run the platform hands it a token for the attached account. No key file anywhere.
One more arrow, from you. To attach that badge to a service, your own identity needs Service Account User on it. That is a deployment permission, separate from what the badge itself may do.
The job gets its own badge. It has the same two Agent Platform roles, plus Storage Object Viewer on the input bucket and Storage Object Creator on the output bucket. The web app's account needs no bucket roles, because its audio goes straight to the browser. One badge per workload.
Slide 16 warns that serverless is harder to debug. The README says where to look: build logs when a function build fails, service logs when a request fails, and the job's execution logs. A finished build is not proof that it works.
The rule: public access answers who may call, and a refused caller is stopped before your code runs. The service account answers what your code may touch. When your own code is denied, fix the badge's roles, not the caller.

## 09:38 — Where preprocessing lives
To serve a trained model, the next lecture uses a Vertex AI endpoint, and the quiz asks where its preprocessing should live. Picture two clients: a phone app, and a web page.
Each client carries the same gear: decode the JPEG, scale the pixels to between 0 and 1, and resize to 224 by 224. Only then does it send numbers to the model. That is two copies of one recipe, in two code bases.
The lecture calls this client-side brittleness. Every client preprocesses slightly differently, and a model trained on one recipe quietly receives another.
Now move the gear into the endpoint. Clients send raw JPEG bytes, wrapped as base64, because JSON cannot carry raw bytes. The preprocessing travels with the model, so every client gets exactly the preprocessing used in training.
Look at the repo's own client. It reads the image files, base64 encodes them, and calls predict. No resizing, no normalizing. That is a thin client.
Now ship a bad resize in version 2. Both clients break at once. Roll back to version 1, and both are healthy at the same instant. One deployment fixed everyone, with no client release.
Now put the gears back on the clients. What does the same rollback cost?
Two releases: a phone update waiting in app store review, and a web deploy. They land at different times, and in between, the clients disagree.
The rule: when the question says several clients, one place to update or roll back, and no client release, put preprocessing at the endpoint. Preprocessing on the clients means every client is re-released in lockstep.

## 11:37 — Register serve: preprocess, then model
Preprocessing at the endpoint works only if the endpoint calls the right function. Here is the chain: JPEG bytes, decode, convert to floats, resize, the model, and four probabilities, one per cheese.
In the repo, preprocess image does the first three steps, for one image. It returns an image, not an answer.
The serving function takes a batch of strings, maps preprocess image over each one, then calls the model. Preprocessing and inference, in one function. Its argument, bytes inputs, is the key clients use. Exam questions may call this function serve: not the web app's serve command, but the function that preprocesses, then predicts.
The export registers it under the name serving default, and the model server calls whatever sits behind that name. The slide saves it with a different call; the idea is the same.
Before we try plugs, one last check. A phone app sends float arrays, a new web client sends JPEG bytes, and the team wants one place to fix preprocessing. What should they register?
Try B first: register preprocess image alone. A request comes back as a 224 by 224 image. Nothing was classified.
A and D keep the raw model. It demands float tensors, so JPEG bytes no longer fit. The server only turns base64 back into bytes. The gears jump back onto every client: two copies to keep in sync.
C, the serving function: bytes go in, probabilities come out. The phone app switches to sending bytes once; after that, one exported version holds the recipe, and every fix or rollback is one deployment. The repo's test step loads serving default and feeds it bytes inputs, as the server will.
This echoes the function's entry point: the platform calls exactly the name you registered, and nothing downstream can fix a wrong one.
The rule: register the function that does preprocessing and inference. Preprocessing alone returns images, and the raw model makes every client preprocess.

## 14:05 — Seven rules for Tuesday
Seven rules for Tuesday. One: read the lifecycle. If it listens, it is a service; if it runs and exits, it is a job, started on demand or by Cloud Scheduler. Two: idle time costs only what is always on. Three: pay-per-use bills invocations and execution time, and zero idle cost buys you cold starts.
Four: a function is source, requirements and an entry point, and Google builds the image; a service is your own image. Five: who may call it is not who it runs as, and the runtime service account needs no key.
Six: preprocess at the endpoint, so one deployment updates or rolls back every client. Seven: register the serving function that preprocesses and then calls the model, because the platform calls exactly the name you register.
Which one to use? The next lecture's rule of thumb: Vertex AI to serve a trained model in production, Cloud Run when the model is part of a broader app. And remember the costs on slide 16: vendor lock-in, cold starts, harder debugging.
That's the lecture in seven rules. Good luck on Tuesday.
