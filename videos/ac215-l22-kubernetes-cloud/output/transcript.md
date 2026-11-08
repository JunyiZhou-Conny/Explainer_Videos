# AC215 · Lecture 22 — Scaling: Kubernetes in the cloud (follow-along: cheese-app-v3)

## 00:00 — Who restarts it at 2 a.m.?
Here is a small app on one virtual machine: a web server in front, a frontend and two APIs behind it. If one of them crashes in the night, who restarts it?
At two in the morning, one API container crashes. The app owner finds out when users complain, and the operator logs in over SSH and restarts it by hand.
In lecture 20, Docker could restart a crashed container, but only on that one machine: if the machine itself failed, the whole site waited for you.
So the app owner asks for several servers. The operator answers with three machines, and a backup copy beside each API.
Each backup sits on the same machine as its original. Name one failure that still takes that API down, and say who switches to the backup.
The machine itself: one failed disk or network takes both copies at once. And even when a backup survives, a person still has to switch over by hand.
The lecture wants three jobs done with nobody awake. Failover: a working copy takes over. Load balancing: requests spread across copies. Scaling: more copies when traffic grows.
This card stays in the corner, and we tick each item once we see what does the job. The tool for all three is Kubernetes.

## 01:28 — From one box to a fleet
Kubernetes is an orchestrator: it runs containers across a cluster of machines and keeps them the way you declared. The name is Greek for helmsman, and Helm, a tool in part 2, borrows it.
On the left, one machine runs every container on one Docker engine. On the right, many machines, called nodes, share the containers, and one control plane coordinates them.
A word of warning: here, deployment means a way of deploying, not the Deployment object we meet later.
In lecture 20 the cheese app ran on one machine. Now the same app goes to a cluster, and the tools gain kubectl. Our toolbox already has it, plus Helm and the GKE auth plugin, which the slides do not list.
To follow along: cheese app version 3 with your secrets folder beside it, Docker, and a Google Cloud project with billing. A cluster costs money by the hour, so each part ends by deleting it.
The tracker names the README step, code panels name their file and lines, and your turn means pause and run it. A grey tag in the corner names the lecture slides.
One honest note: our recording machine has no Google account. What runs on a machine you own is real; every Google step stops at its first honest error, and we say what yours prints.
We follow main, the branch the course site links, at this November 2025 commit. Git log tells you which one you have.
Part 1 does the lecture's warm-up by hand. Part 2 deploys the cheese app as code.

## 03:04 — Inside a cluster: brain and workers
Let's open the cluster. The lecture draws it in three steps. First: one control plane, with arrows to several worker nodes, each an ordinary virtual machine.
Second, the two planes get names. The control plane is the brain. On GKE, Google runs it, and you never see its machines. The workers carry your containers: for the cheese app, a pool of one or two nodes.
Third, the parts. The API server is the single entry point; every other part talks only to it. Etcd is the memory of the cluster: its state and configuration.
The scheduler picks a node for each new Pod. The controllers keep watching and fix any difference between what you asked for and what runs; some of them ask the cloud for nodes and addresses.
On every worker, the kubelet is the hands of the API server: it starts and stops the containers. Kube proxy routes traffic for Services, and a container runtime runs the containers, grouped in Pods.
A small note: the slide names Docker as the runtime. On GKE it is containerd, line 52 of create cluster dot py. You still build images with Docker, and they run unchanged.
Now follow the arrows. Every kubectl command goes to one place, the API server, which stores your wish in etcd. The scheduler and the kubelets pick up their work from it.
The lecture gives kubectl one grammar: a command, a type, an optional name, and flags. Get nodes. Get pods. Get pods, with a flag for every namespace.
When something is stuck, ask which of these parts is waiting. Four lamps on this picture will light up later, each with a symptom you will meet.

## 04:53 — The toolbox, still fixed twice
The README keeps this warm-up after the cheese app's deployment. The lecture does it first, and so do we: it is the gentlest first contact with kubectl.
First, enable five APIs in the console. A small slip: Google Container Registry has been shut down. Enable Artifact Registry instead.
Then start the toolbox: from the S R C folder, change into deployment and run docker-shell.sh. As committed, it fails: 404 Not Found from Debian, then pull access denied.
If you did lecture 20, you have seen this: the base image is Debian bullseye, whose security packages are gone. On Windows there is no docker-shell.bat. Use WSL.
The fix is the same two one-line edits, an extra here. Bullseye becomes bookworm, and google cloud SDK becomes google cloud CLI, with its GKE auth plugin. Every kubectl call to GKE goes through that plugin.
As in lecture 20, also put your project on line 13 of docker-shell.sh.
Run it again: it builds in about 92 seconds and starts. The login then fails, because our key belongs to no account; with yours, these lines say activated and logged in.
Pause here and start your toolbox; the rest of this part runs at its prompt.
Next, check the tools. The gcloud tool and its auth plugin are there. Plain kubectl version prints the client, then connection refused: there is no cluster yet, so the server half has nobody to ask.
A small surprise: the Dockerfile pins one kubectl version, but Google's own package wins: a dispatcher that matches each cluster.
Last, check that you are authenticated: gcloud auth list. Ours says no credentialed accounts; yours lists the deployment service account as active.

## 06:52 — A test cluster and a first look
Now Create Cluster: gcloud container clusters create test cluster, two nodes, zone us east 1 c. Ours stops at once: no active account. Pause and run yours; it costs money every hour it exists.
Yours takes a short wait, prints a table, and adds an entry to your kubeconfig so kubectl knows where to go. The slide makes one node; the README two, so two copies can land on different machines.
To keep going, we start a small real cluster on the laptop with a tool called kind: one control plane, two workers. Same API server, same kubectl, same YAML, but no Google. It is not in the README; don't run it.
Here even the control plane is a container we can see; on GKE, Google hides it.
Next, look around the console: Kubernetes Engine, your cluster, its nodes, and the Pods on each node. In Compute Engine, your nodes are ordinary virtual machines.
Then try some kubectl commands. First an extra, kubectl version: the dispatcher picked a client that matches the server's version.
The first README command, get all, shows only a service named kubernetes, the door to the API server itself. We are looking in the namespace called default; more on that later.
With all namespaces, kube system appears, and here you can spot the control plane by name: etcd, the API server, the controller manager, the scheduler. On GKE those stay hidden.
Component statuses prints a deprecation warning, which is expected, then three healthy lines. Get nodes is the better check: three nodes ready here; yours shows two workers and no control plane. Pause and try all five.

## 08:45 — Two objects: a Deployment and a Service
The warm-up deploys a small game, tic-tac-toe, from one file with two objects. The Deployment says what runs in a Pod, how many copies, and to keep them running. The Service says how traffic reaches them, and lets Pods die.
The slide trims the lines that glue them together. The template gives every Pod a label, run web, and both objects find their Pods by that label, not by name.
Each Pod runs the image dlops tic-tac-toe, listening on port 8080. The Service listens on port 80 and forwards to 8080.
Deploy the app: kubectl apply, dash f, and the file. Apply only hands a wish to the API server; the scheduler picks two nodes, and their kubelets start the containers.
An extra check, rollout status, watches it happen: zero, then one of two available, then rolled out, on two different workers.
Next, kubectl get services. The web Service is a load balancer: port 80, mapped to 31366 on every node, and on to 8080 in the Pod. Its external IP says pending.
43 seconds later it still says pending. Which part of the cluster picture is waiting, and on what?
The controllers, waiting on the cloud provider. On GKE they ask Google for a load balancer and an address, which arrives after a short wait. The kind cluster has no cloud to ask.
Pause: on GKE, wait for the external IP, copy it into your browser, and the game appears.
On the stand-in, an extra: port forward to the Service, then curl: 200 OK. The lecture suggests it for your browser, but from the toolbox the port opens inside the container: test it there.

## 10:47 — Desired state: Pods that come back
Back to the night-time problem: who restarts the container? In Kubernetes, a controller does. Let's watch one work.
An extra listing shows the chain. The Deployment named web owns a ReplicaSet, whose name adds a hash of the Pod template. The ReplicaSet owns two Pods, each with that hash and a short random suffix.
The labels confirm it: every Pod carries the template hash and the run web label.
The ReplicaSet controller runs a loop: observe the Pods, compare with the number you declared, act on the difference. You set the number; the controller keeps it true, like a thermostat.
First, one more extra: kubectl scale, replicas 4. Two more Pods appear, spread over both workers, and the Service already lists them. Scale back to 2, and remember this command: your project's Milestone 5 asks for it.
Now delete one of the two web Pods. A second later, how many web Pods are there, and which part of the new name stays the same?
Two. The delete returns, and a new Pod is already being created. Its name keeps the ReplicaSet hash, with a new suffix.
15 seconds later, both run. Nobody logged in: the loop noticed, and acted.
That ticks failover, with an honest footnote: it is a restart, not a hot standby. With one replica there is a short gap, which is why the game's file asks for two replicas.
In lecture 20, Docker restarted a container on the same machine. A ReplicaSet places a new Pod wherever there is room. Declare the result, don't script the steps.

## 12:37 — Labels, Services, namespaces, then delete
Pods are mortal: the new Pod got a new address. So how does traffic find it? The Service keeps a list of every Pod wearing its label, and that list follows the Pods.
An extra from a throwaway Pod: the name web dot default dot svc dot cluster dot local points to the Service, and fetching just web returns the game page. The name stays while the Pods change.
This is how the cheese app's API will find its database: by the Service name, vector db.
Another extra: kubectl exec into the web Deployment. Hostname prints the name of one Pod, and the game's files are inside. The README shells into the API the same way.
Why did get all look empty? Namespaces: folders for objects. Without a flag, kubectl looks only in default; this extra lists them, then creates and deletes the cheese app namespace.
So in part 2, every command about the app gets dash n, cheese app namespace, in the flags slot.
Before deleting the cluster, an extra tip: kubectl delete with the same file. On GKE, this releases the load balancer while the cluster still exists.
Then delete the cluster: gcloud container clusters delete test cluster, zone us east 1 c. Yours asks whether to continue; answer yes.
We delete the stand-in too.
The lecture's last word fits here: don't forget to delete. Pause, check that your test cluster is gone, and part 1 is done.

## 14:16 — The cheese app's cluster, as code
Part 2: the cheese app on GKE, as Pulumi code. The course link lands on Deployment with Scaling using Kubernetes; the cluster steps continue under the next heading, Create and Deploy Cluster.
Here is the plan, piece by piece from lecture 20. Each long-running container becomes a Deployment. The one-shot loader becomes a Job: it retries a failed run a few times, and once it succeeds, it stays done.
Container names on a Docker network become Services with DNS names. The folders on the VM disk become two persistent volume claims, each backed by a cloud disk.
The nginx container becomes an Ingress controller with an Ingress rule. The JSON key becomes Workload Identity, with no key file at all. One machine becomes a pool of one or two nodes.
Around it, a private network. The nodes get no public addresses; a Cloud NAT gateway lets them reach out, for example to pull Chroma from Docker Hub. The app sits in one namespace, behind one load balancer.
The program in deploy k8s says the same in four calls, one per file: the network, the cluster, the containers, the load balancer. Line 17 keeps the HTTPS variant switched off.
While it is up, it costs money: the fee of a regional cluster, one or two nodes, a load balancer, one NAT gateway and two disks. By our estimate, roughly five to eight dollars a day: check the pricing calculator, and destroy it the same day.

## 15:55 — Setup and the images stack
This section enables the five APIs again; turn on the Vertex AI API too, which the API Pods call.
You also need the two service accounts from lecture 20. The deployment account does what the toolbox does, and here it is also the nodes' identity. The gcp service account is for the API Pods, with no key file.
Two one-time steps the README leaves out. The deployment account very likely needs Service Account Admin on gcp service; we could not test this. And create the registry repository, cheese app repository, which no code creates.
The deployment key goes in the secrets folder, beside the repository, as in lecture 20.
Then the toolbox steps from part 1, the same commands; if the toolbox is still running, the script simply attaches to it.
Next, the images stack, only if you have not built it before: change into deploy images, pulumi stack init dev, and set G C P project to yours. Ours says Pulumi access token must be set: our bucket login failed, so Pulumi falls back to its cloud service.
To show the rest, we point Pulumi at a local folder, a recording workaround: don't run it. Now the stack is created, as yours is.
Then pulumi preview, stack dev: three image builds, skipped in a preview, and three tags stamped with the time. Plus 4 to create: three images and the stack itself.
Those tag outputs matter: deploy k8s looks them up through a stack reference, to know which images to run.
Last, pulumi up, stack dev, dash y: it builds and pushes three images. Skip it if you did it in lecture 20, with one condition we meet next; otherwise, pause and run it.

## 17:50 — deploy_k8s: config and a 23-resource plan
Now Create and Deploy Cluster. From the deployment folder, change into deploy k8s and run pulumi stack init dev: the same token error, and on the local backend, created stack dev.
Then three config keys: your project, and two service account emails, deployment and gcp service. Replace ac215 project with yours in all three.
Line 9 takes the deployment email: the nodes run as that account. Line 10 takes the gcp service email, which the API Pods will act as.
An extra, pulumi config, lists your three keys and two leftovers from the committed file, setup SSL and an SSH user, which the program never uses. A typo in a key name fails quietly later, so check this list.
Then Preview: pulumi preview, stack dev, refresh. On the local backend, a Python error at line 70 of setup containers: none type is not subscriptable. The program asked the images stack for its tags, and got nothing.
You see this if the images stack never finished pulumi up in this same state bucket. Skipping it is safe only when it already ran there.
So we gave the program a stand-in images stack with placeholder tags; nothing is built. Now the real plan appears: the network, the cluster, the node pool, the Kubernetes objects, and plus 23 to create.
Two more lines are lookups, not counted in the 23: the stack reference and the nginx Service. In the outputs, only the cluster name is known; the address and the URL wait until the cluster exists.
Pause and run your preview: you should see the same 23, with real image tags.

## 19:40 — pulumi up: what builds, in what order
Then the big one: pulumi up, stack dev, refresh, dash y. On the local backend the update starts, and the very first resource, the network, fails: invalid grant, account not found.
The network is the first thing that needs Google, so from here on this is a picture. Pause and start yours; from now on, the meter runs.
Pulumi follows the dependencies. First the network and its subnet. Then, side by side, the router with its NAT gateway, and the cluster, the long wait: a quarter of an hour or more, by our estimate.
Then the node pool. A Kubernetes provider, built from the cluster outputs, waits for that pool, so no Pod is created before there are nodes.
Through it come the namespace, the service account of the API and its binding, the two disk claims, the frontend and the vector database.
Next, the loader Job fills the vector database. Pulumi creates the API only after the Job completes: lines 319 to 321 set that dependency.
In parallel, Helm installs the nginx Ingress controller. Its Service asks for a load balancer, so the controllers ask the cloud for an address: the part 1 lamp, green this time. That address becomes a host name, and the Ingress comes last.
Identity, in two parts. Pulumi and kubectl reach the API server through the GKE auth plugin, fix two from the toolbox, so there is no cluster password.
And the API Pod wears its Kubernetes service account, which Workload Identity swaps for gcp service at the door to Vertex AI. No JSON key sits in the cluster.
Keep in mind: Pulumi connects kubectl once, inside this toolbox, which is removed when you exit. The next session starts unconnected.

## 21:46 — The journey of one click
Lecture 20 put one nginx container in front. The game opened its own load balancer, one door per app. The cheese app opens one door, with a receptionist behind it.
The README draws the path: browser, load balancer, the nginx Ingress controller, then the frontend on 3000 or the API on 9000, and the vector database on 8000.
A small slip: the README draws the dotted arrow from the vector database to the loader. The data flows the other way, from the Job into the database.
Follow one click. Your IP dot sslip dot io points back to that same IP, with no setup at all. The packet passes the cloud load balancer and lands on the nginx controller.
The Ingress rule starts with the host name: for that host, slash api service goes to the API on 9000, every other path to the frontend on 3000. The controller follows that rule, like the nginx dot conf of lecture 20, now generated.
This time the prefix is kept: nothing strips it. The API mounts itself under its root path, slash api service, so slash api service slash status answers version three point zero.
The page comes from the frontend; then your browser calls the API directly, at slash api service.
Inside the cluster, the API reaches Chroma by its Service name, vector db, on port 8000.
Now open the bare IP: the same load balancer, without sslip dot io. What answers?
The nginx controller answers 404 Not Found. The rule matches only that host name, so the same door with the wrong name finds no route. Use the app URL from the outputs.
That ticks load balancing: the cloud load balancer at the door, nginx behind it, and each Service spreading requests across its Pods.

## 24:02 — kubectl on the app, and the outputs
Next, try some kubectl commands. With no cluster here, all five say connection refused. You will see exactly this in any new toolbox session: the kubeconfig Pulumi wrote went away with the old container.
The fix is the command Pulumi ran, an extra here: gcloud container clusters get credentials, cheese app cluster. The code passes the region to the zone flag; write region, which says what it means.
Once connected, get all still shows only the kubernetes Service, because the app sits in its own namespace. With dash n, cheese app namespace, yours lists the frontend, database, API and nginx controller Pods, and a loader Pod marked completed. Get nodes shows one node, or two.
The next README step shells into a Pod. The Pod name in the README is the author's own; use the name your first command prints.
Inside, you get a shell in the API container, just as we did in the game. Print its environment and look for ROOT PATH. Pause and try it.
To view the app, the README shows an outputs block a little older than the code. Today the address is called ip address, not nginx ingress ip, and the Ingress is called cheese app ingress.
Pause and open your app URL. A footer that says API version three point zero proves the whole path works: it asks slash api service slash status. Then pick the RAG model in the chat; a reply proves Vertex AI and Chroma too.
Right after deploying you may see 502 or 503: the API is still loading TensorFlow. Wait, and try again.

## 25:49 — Logs, then scaling at two levels
The README's debugging block has 14 kubectl commands. As typed, they all fail; most say the namespace, cheese app cluster namespace, is not found.
Lines with pod name in angle brackets are shell redirections: replace the whole placeholder, brackets included.
Two fixes: the namespace is cheese app namespace, and the Job has one container, so drop the wait for chromadb flag. Pause and try them.
On a Job that exists, an extra on the stand-in, the same commands work: done, one succeeded. Nothing replaces a finished Job's Pod.
A small note: after a database restart, run the loader again; the chip shows why.
Now scaling. The lecture promises scaling on CPU, memory or custom metrics, but the code sets no replicas and no Pod autoscaler. It switches on the node layer: one to two nodes.
The scheduler packs Pods onto nodes by their requests. The frontend asks for a quarter CPU and 2 gigabytes. Chroma and nginx ask for little, and the API for nothing, so nobody can plan for it.
Scale the frontend to 3; Milestone 5 asks you to show scaling. A copy that does not fit waits, pending, until the autoscaler adds a second node. Ask for many more, and some stay pending: the pool stops at two.
The API's disk attaches to one node at a time. Suppose you scaled the API to 3, and some copies landed on the second node. What happens to them, and can the autoscaler fix it?
They stay stuck creating, with a multi attach error: the disk already sits on node 1. More nodes do not help; the limit is the disk.
That ticks scaling, in two levels: nodes automatically, Pods in your hands; a Pod autoscaler on CPU needs requests, and the API has none. Scale back to 1 when you are done.

## 28:03 — Destroy, audit, recap
Last, delete the cluster: pulumi destroy, stack dev, refresh, dash y. Ours has nothing real to delete; yours deletes what this stack created, in reverse order, from the Ingress down to the network.
Then check what may survive, our suggestion: list clusters, forwarding rules, disks and firewall rules. Those are deleted in the background and can be left behind; look for disks named pvc.
Registry images stay on purpose: delete them in the console. Delete the lecture 20 machine too, if it still runs. Pause and check.
Back to the three asks. Failover: the ReplicaSet brings Pods back, and node auto repair replaces broken machines. Load balancing: the cloud load balancer, nginx and the Services. Scaling: the node autoscaler, and kubectl scale in your hands.
The lecture lists five payoffs. Self-service: one pulumi up. Lower cost: Pods packed by their requests. Automatic adjustment: the node autoscaler. Smooth running: self-healing. Simpler development: the same images as lecture 20.
Test yourself. Which control plane part decides where a new Pod runs, and which one notices that a Pod died? Why does get all show only the kubernetes Service, and what flag fixes it?
How does the web Service know its Pods, and why does the API reach Chroma at vector db? Trace one click from sslip dot io to the API Pod; why does the bare IP answer 404?
Why can the frontend scale to 3 but the API cannot, and what does the autoscaler add? Answers are in the exercises and the study guide.
Next, in lecture 23, the two Pulumi programs, in version 4 of the app, run from GitHub Actions on every merge.
