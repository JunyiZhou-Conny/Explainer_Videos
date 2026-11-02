# AC215 · Lecture 16 — System Tradeoffs: networking, runtime config and capacity (with L10) (exam edition)

## 00:00 — Launch day: three alarms
Launch day for the Cheese App. Last week it ran on a laptop. This morning it runs in the cloud, inside a private network. Within an hour, three alarms go off.
First alarm. Chat answers that call an outside language model time out. Yet the saved chat history, read from the database, loads fine.
Second alarm. The page loads for every visitor, but the Predict button fails. On the developer's laptop, the same button worked.
Third alarm. At 9 in the morning traffic doubles, and the autoscaler adds replicas. The newest ones fail with too many connections, while their processors sit idle.
And one problem nobody has noticed yet. The production key is sitting inside the container image.
Each alarm is one mechanism from Lectures 10 and 16. We go from addresses, to routes and NAT, to the browser, to configuration, to capacity, and finally to the database.
The gray tag, top right, names the slides behind each idea. Nothing here is a live run.

## 01:08 — From localhost to a front door
Start on the laptop. In the course app, uvicorn starts FastAPI inside a container, on host 0.0.0.0, port 9000. That host means listen on every interface. Bound to 127.0.0.1 instead, it would answer only from inside the container.
The container is sealed off until you publish a port. Dash p, 9000 to 9000, is the tunnel from the laptop's door into the container's.
So the README says the app is served at localhost 3200, and it calls the API at localhost 9000. Localhost always means this machine: the one the code runs on.
An IP address picks the machine, and a port picks the service on it. Addresses that start with 10, with 192.168, or with 172.16 through 172.31 are private. The internet does not route them.
Move the same container into the cloud. Inside the private network it gets the address 10.0.2.5. A packet from the internet cannot reach it: nobody out there has a route to a private address.
Lecture 10 sums it up. On the laptop, your router keeps the world out. In the cloud, the public finds you by a DNS name, a firewall starts closed, and a load balancer lets traffic in.
The browser asks a resolver for api dot example dot com, the resolver asks the authoritative DNS, and the load balancer's public address comes back. Then the browser connects to the load balancer on port 443.
The load balancer ends the HTTPS connection and sends its own request to the task's port 8000. There, a security group allows only the load balancer, on port 8000. A stranger's packet bounces, and the reply goes back out, because the firewall remembers the connection.
SSH reaches the machine, while clients reach the service. The lecture draws Amazon names. On Google Cloud the neighbors are Compute Engine, Cloud Load Balancing and Cloud NAT.
If the question says localhost, think: the machine the code runs on. A 10 dot address: private, unreachable from the internet. Public clients: a DNS name, the load balancer on 443, then the private target on 8000.

## 03:45 — Private subnets, route tables and NAT
Now the first alarm: the language model times out, but the database answers. A VPC is one block of addresses, here 10.0.0.0 slash 16. The slash counts the fixed bits out of 32. Slash 16 leaves 16 bits to vary: 65,536 addresses. Slash 24 leaves 8: 256.
The lecture cuts it into three subnets. A public one for the load balancer. A private app subnet for the FastAPI tasks. A private data subnet for the database.
Every subnet has a route table. Both send the VPC's own block to the local route. The only difference is the default row, 0.0.0.0 slash 0. A public subnet sends it to the Internet Gateway, a private subnet to the NAT Gateway.
A route alone is not enough, slide 13 adds: the machine also needs a public address and an open firewall.
A packet for the database at 10.0.3.7 matches both rows, and the most specific match wins: slash 16 beats slash 0. The packet stays inside, on the local route.
A packet for the language model API matches only the default row, so it goes to the NAT Gateway. NAT rewrites the private source to its own public address, writes the mapping in its notebook, and sends it out.
The reply comes back, NAT finds the line, and hands it to the task. A packet nobody asked for has no line, so it is dropped. NAT only carries connections that start inside. Nothing uninvited gets in, which keeps the private subnet private.
Now NAT fails. Every call to the internet stalls at the dead hop. But the database packet still matches the local route, and the load balancer still reaches the tasks. That is the first alarm.
First question. A worker in a private subnet downloads model weights from a public website at startup, and nobody on the internet may open a connection to it. Where should its default route point? Pause here if you want.
C. NAT carries the worker's request out, maps the reply back, and refuses uninvited connections. A, the Internet Gateway, would download too, but it makes the subnet public, a direct path in, guarded only by firewall rules.
B fails: the local route covers only the VPC's own block, and the website is outside it. D fails: a load balancer brings requests in to its targets. It is not a way out.
If the question says private subnet, think: the default route goes to NAT. NAT only carries connections that start inside. And if NAT is down, internet calls fail, while traffic inside the VPC, like the database, still works.

## 06:56 — The browser lives outside the VPC
Now the second alarm, the failing button. Loading a page is two trips. First the browser downloads HTML, CSS and JavaScript from a static host. Then that JavaScript runs on the visitor's own machine, and calls the API.
So the browser lives outside the VPC. Static files never enter it, and every API request must come in through the front door, the load balancer.
Now the course app. In development, the frontend takes its API address from next public base API URL, and that variable says localhost 9000. On the developer's laptop, that was exactly where the API ran.
Ship that to a visitor, and localhost means the visitor's laptop. Nothing listens there, so the request fails. That is the second alarm.
Swap in the private address, 10.0.2.5, and the request never reaches the VPC: that address means something only inside the visitor's own network. The public HTTPS name works: DNS, the load balancer, then a task.
The production file says just slash api. A relative path goes back to the host that served the page. That works when one public front door serves both the page and the API, the lecture's layout B, and routes slash api to FastAPI.
Slide 24 writes that rule twice, as an Nginx proxy pass or a load balancer path rule. With a separate static host, the code must name the public API address instead.
Notice where the private address lives: in the proxy's config, inside the VPC. Never in browser code.
Two more facts. Next public variables are compiled into the JavaScript at build time, so every visitor downloads them: public by design, never a secret. And NAT does not help here: it only carries traffic that starts inside the VPC.
If the question says code that runs in the browser, think: it is outside the VPC. Call the public HTTPS endpoint, never localhost or a 10 dot address. NAT does not help inbound.

## 09:15 — Build once, configure at startup
Now the quiet problem, the key inside the image. First, how a release should work. Build the image once, push it with a version tag, and every deployment pulls that exact version. No rebuild.
The image is immutable. It moves from development to staging to production, and its digest never changes. What differs is the runtime values plugged in when the container starts: log level debug in development, info in production.
Secrets follow the same rule. A secret manager delivers the key at startup, only to the workload that is authorized for it. Never place secrets in source code, in container images, or in Git.
The course already does the laptop version. The run script mounts the secrets folder at slash secrets, and points Google Application Credentials at the key's path inside the container.
The project and the ChromaDB host arrive as environment variables too. The app reads them with os dot environ when it starts.
The README says why: we do not want any secure information in Git. The key lives next to the repository, never inside it.
Now the wrong way. Bake the key into the image, and anyone who can pull the image can read it. Rotating it means a rebuild, and per environment images mean what you tested is not what you ship.
Second question. A teammate bakes an API key into the Dockerfile and pushes the image to the team's private registry. Which statement is true? Pause here if you want.
D. The image's settings and layers are readable by anyone who pulls it, and changing the key means a rebuild. A, the private registry, is still a long list of people and machines, and the image is copied to every host.
B fails: the key is written in the Dockerfile, which is in Git, and in the image. Ignoring a different file changes nothing. C fails too: development images leak, and separate images break build once.
If a question asks how to move an image to production, think: the same image, promoted unchanged. Environment values and authorized secrets are injected at startup. Never rebuild per environment, and never bake a secret.

## 11:48 — Autoscaling meets the connection budget
Now the third alarm. An autoscaler measures a signal, like processor use, applies a policy with a target, a minimum and a maximum, and asks for that many replicas. But downstream limits still bound the result.
The database accepts a fixed number of connections, here 100. Other clients already hold some: an admin console, a batch job.
Each replica opens its own connections. In the course app, every API process creates its own database client at import. That client is ChromaDB, standing in here for a connection pool.
The autoscaler adds replicas, each plugging its pool into free slots, until the slots run out. The next replica cannot connect, though its processor is idle.
So read the rule off the picture. 100 slots, minus 10 for the other clients, leaves 90. Divide by 20 per replica: 4.5. A replica cannot open half a pool, so round down to 4, and set 4 as the autoscaler's maximum.
To go higher, add a connection pooler or shrink each pool, or buy a bigger database tier. Raising the maximum alone does not help.
Third question. Each replica opens 15 connections, other clients hold 30, and at peak you need 10 replicas. Which is the smallest database tier that works? Pause here if you want.
B, 200. Ten pools of 15 make 150, plus 30 others: 180. That fits under 200.
A, 150, holds the pools but forgets the other clients. C, 250, works, but costs more than it needs to. D: a higher maximum adds no connections, so the extra replicas fail.
If the question gives a database connection limit, think: the limit minus other clients, divided by connections per replica, rounded down. And set it as the maximum, because the autoscaler does not know the database limit.

## 14:05 — Relational plus vectors: one database
The last mechanism is where the data lives. Classify it first. Users and orders, linked by foreign keys, saved in transactions that are all or nothing: that is relational. Find the five most similar cheeses: that is vector search.
Today the course runs ChromaDB as its own container. It is a vector store with metadata, and the team operates it: patches, backups and recovery are yours.
The lecture compares three homes: ChromaDB on a virtual machine, a PostgreSQL service with pgvector, and a vector search service. Vector chips land everywhere. Foreign keys and transactions bounce off the two vector-only homes.
You could run two databases. But then they must stay in sync, and one day an order exists in one while its embedding is missing from the other.
Only PostgreSQL with pgvector takes every chip. The vector column sits beside the relational columns in the same table, and one query filters with SQL and orders by similarity.
Managed means the provider runs the hosts and the patching. Your team still owns the schema, queries, pooling and restore tests. On Google Cloud: Cloud SQL for PostgreSQL, or AlloyDB.
If the question says relational and vector needs in one managed database, think: PostgreSQL plus pgvector. Foreign keys, transactions and similarity search, in one place.

## 15:39 — Seven rules for the quiz
Seven rules for the quiz. One: localhost is the machine the code runs on, and 10 dot addresses are private. The public reaches a DNS name and a load balancer.
Two: a VPC is an address block cut into subnets, and the most specific route wins. Three: NAT only carries connections that start inside. If it fails, internet calls fail, and the database still answers.
Four: the browser is outside the VPC, so it calls the public HTTPS endpoint. Five: build one image, and inject settings and secrets when it starts.
Six: maximum replicas is the connection limit minus other clients, divided by each pool, rounded down. Seven: relational plus vectors in one managed database means PostgreSQL with pgvector.
Here is the whole picture, every alarm fixed. Static files from the edge, requests through the load balancer, tasks in the private app subnet, PostgreSQL in the data subnet, and NAT for calls out.
When a question looks hard, do what the lecture does last. Trace the request first. Good luck on the quiz.
