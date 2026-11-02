# AC215 · Lecture 15 — ML Workflows with Vertex AI (exam edition)

## 00:00 — The 2 a.m. race
Three nightly jobs on a clock. Prepare the data at 1 in the morning. Train at 2. Deploy at 3. For months, it works.
Then one night, preparation takes 75 minutes. At 2, training starts anyway, on a file that is only half written. At 3, deployment ships whatever training produced.
Every job exits with status zero. Nothing failed. And the endpoint now serves a model trained on half the data. Nothing was right either.
The lecture opens on the same problem: four steps of the cheese app, each run by a person at a terminal. How do we execute these steps? Can we automate this flow?
To automate it, you need a different instruction. Not: train at 2. Instead: train when preparation has finished. That is what a pipeline is for.
Here is the plan: graphs, wires, overlap, order, deployment, and the cheese app.
The gray tag, top right, names the slides behind each idea. Nothing here is a live run.
If an option schedules steps at fixed times, think race: a clock knows nothing about data.

## 01:13 — A pipeline is a graph
Workflow management, in the lecture's words, knows which step needs which. The structure that records this is a directed acyclic graph, or DAG.
Directed, because data flows one way, from producer to consumer. Acyclic, because no step ever waits on itself. Tasks are the nodes; data dependencies are the edges.
Vertex AI Pipelines runs these graphs for you. You describe the graph with Kubeflow Pipelines, the K F P library, and there is no Kubernetes to manage. Today's console calls it Agent Platform.
Here is the toy pipeline from the slides and the demo repo. Three Python functions marked d s l dot component: square, add and square root. A fourth, marked d s l dot pipeline, wires them together.
When the pipeline function runs, the component calls compute nothing. Calling square on a, the pipeline's input, which defaults to 3, creates a task: a node in the graph, with an empty output socket. No number yet.
Line by line, four calls drop four nodes. Square is called twice, so one component gives two tasks; the second is named square 2. The function ran once, and produced only a graph.
The compiler presses that graph into a YAML file. The Vertex AI SDK, the lecture's remote control, submits it as a pipeline job. Your laptop compiles and submits. Vertex executes.
Only now, on Google's machines, does each task get a container, and do numbers appear.
If an option says calling train in the pipeline function trains the model, think again: it only creates a task. Nothing runs until the compiled job runs.

## 03:03 — task.output: the wire that makes an edge
Look at the add call. For x, it passes the first square task, dot output. For y, the second task, dot output. So what is being passed?
Not a number. Dot output is a placeholder for a value that exists only after the upstream task succeeds. Plugging it in draws a wire.
The compiled YAML writes down each wire twice: add's dependent tasks list square and square 2, and each input names its producer task.
At run time, square turns green, and only then does 9 ride the wire into add. One argument gave add both its data and its dependency.
With several outputs, you name the one you want: dot outputs, with the output's name in brackets.
Now the contrast. Often the output is itself a path: the file this run wrote. With the wire, train gets that exact path, after prep succeeds. Hard-code a path instead, and there is no wire: train starts right away, alongside prep.
The file there is last week's, and the step succeeds on stale data. A guessed path looks like a dependency to you, not to the pipeline.
For order without data, dot after adds a dashed edge: the task waits for the other one to succeed, but nothing travels down it.
Try one. Pause here if you want.
B. Naming the output hands over this run's file, and creates the wait. A hard-codes a path: no edge, so train may start at once and read last run's file.
C waits, but it reads a path you assumed, not the one split reported. D fails before anything runs: with two outputs, K F P refuses plain dot output.
If the question says dot output, think: waits for success, and gets this run's value. A hard-coded or guessed path: no edge, maybe stale. Dot after: order, but no data.

## 05:07 — Maximum safe overlap
Back to the toy graph. No path of wires connects the two square tasks, so Vertex is free to run them at the same time.
Add is a join. Its YAML lists both squares as dependent tasks, so it starts only when the second one finishes.
The same shape, one size up: one preprocessing task, two trainings that read its output, and a comparison that reads both models.
A task lights up when every incoming wire carries a token. Both trainings start together, and the comparison starts exactly when the slower one ends.
Add an edge the data does not need: same answer, longer run.
Replace those wires with guessed paths, and the comparison starts at time zero and reads half-finished results. That is a race.
Maximum safe overlap means exactly the edges the data needs, no more and no fewer. The run then lasts its longest path. If an upstream task fails, the join never runs.
Your turn to compute one. Pause here if you want.
B, 16 minutes. The longest path is ingest, clean, the big training, and compare. 2, plus 3, plus 10, plus 1. The small training and the report overlap with the big one.
A adds every task in sequence. D runs the two trainings one after the other. C ignores the edges: training needs clean data, and compare waits for both models.
If there is no path of wires between two steps, think parallel. If a step consumes several outputs, it waits for all of them.

## 06:50 — Enforcing order: edges, not clocks
Now the sequence: preprocess, train, deploy. Here are four ways to make each step wait, on one clock.
Lane one, cron offsets. Lane two, background ampersands. Lane three, an event starts training when preprocessing writes its output, and deploy takes the best model in the tracker. Lane four, pipeline edges.
Roll the length of preprocessing. 40 minutes. Then 75. Then 55.
The clock lane is fine at 40, and broken at 75: training reads a half-written file. The background lane is broken on every roll, because nothing waits.
The tracker lane fails twice. The event can fire on the first file, before preprocessing is done. And the tracker's best model is the best of all runs, not this run's. Only the edge lane is right on every roll. It just stretches.
The cheese app pipeline does exactly this: processing after collection, training after processing, deployment after training, each with dot after.
In the compiled YAML they become dependent tasks. And the README says it plainly: each step starts only after the previous one succeeds.
One more, a subtle one. Some steps only launch work on another machine. Remember exactly what an edge waits for. Pause here if you want.
B. An edge waits for the task, and this task succeeded after 5 seconds. The pipeline never sees the job it launched, so A is wrong, and deploy may ship the previous model.
C: dot after needs no data. D: dot after is enforced, written into the YAML as a dependent task.
The repo's training step is such a launcher. With sync set to true, it waits for its job, and fails if the job fails, so deploy never runs on a failed training. A recent commit made that wait explicit.
If an option uses cron offsets, background commands, or the best model from the tracker, think race or wrong model. Edges from preprocess to train to deploy are correct by construction.

## 09:09 — Registry, endpoint, deploy, predict
The lecture draws deployment in five steps: get the saved model, update its signature, upload it to a bucket, register it, and deploy it to an endpoint.
The signature step moves preprocessing into the model: decode the JPEG, convert to floats, resize to 224 by 224, then call the model. The slides save it one way, the repo with the Keras export archive.
Registering creates a catalog card. It records where the files are, and which container serves them. Nothing is running, and it costs nothing. Can you call it? Not yet.
Next, the endpoint: an address. The repo reuses cheese app endpoint if it exists, or creates it.
Deploy slides a machine under that address and sends it all the traffic. From now on, you pay for that machine while it is deployed, even when nobody calls it.
To predict, the client wraps each JPEG in base 64, under the key bytes inputs. The signature unfolds it, the model returns four scores, and the largest names the cheese.
Cleanup undeploys the model, so the machine stops, then deletes the endpoint. The registry card and the bucket files stay.
The pipeline's deploy step makes the same two calls. And by the slides' rule of thumb, Cloud Run fits when the model is one part of a bigger app.
If the question says registered, think: not callable until it is deployed to an endpoint. If it says deployed, think: a machine is billing until you undeploy it. Then delete the endpoint too.

## 10:48 — The Cheese App pipeline, and the same DAG on AWS
Now the whole cheese app pipeline: collector, processor, training, deploy. Each gets a green check as it succeeds.
Two kinds of steps. The collector and processor are container components that pull published images from a registry, Docker Hub in this repo, the Artifact Registry on the slides, because Google's machines cannot see your laptop. Training and deploy are Python components that call the Vertex AI SDK.
So why dot after, and not dot output? The steps never call each other. Each reads from the bucket and writes back: raw zip, clean zip, then the model folder. The pipeline only decides when each step starts.
So deploy finds the model by name, in the model folder, and the edges make that name safe. Delete one, and deploy may grab last run's model: the stale read from earlier.
One difference from the slides: on the main branch today, training downloads its own dataset, so these edges carry order, not data.
On AWS, SageMaker Pipelines runs the same idea. The training step's input points at the processing step's output property, and that reference is the edge.
Shuffle the pipeline's list of steps, and the graph does not move: order comes from the references.
If the question says SageMaker Pipelines, think: the same DAG. Referencing a step's properties makes the edge.

## 12:16 — Seven rules for the quiz
Seven rules. One: pipelines are DAGs. Calling a component creates a task, a node. Nothing runs until the compiled job runs.
Two: dot output, or a named output, makes the edge and passes this run's value. Three: a guessed path makes no edge, and may be stale.
Four: dot after orders without data. Five: no path between tasks means parallel, a join waits for all its inputs, and the run lasts its longest path.
Six: order comes from edges, not clocks, and a step that launches work must wait for it.
Seven: upload to the Model Registry, create an endpoint, deploy, then predict. Billing starts at deploy. SageMaker builds the same DAG from step properties.
And the lecture's chain: a recipe in the D S L, printed as YAML, submitted by the SDK, run on the Kubeflow engine, and managed by Vertex AI Pipelines, with no Kubernetes to set up.
When you are done, undeploy and delete the endpoint. Good luck on the quiz.
