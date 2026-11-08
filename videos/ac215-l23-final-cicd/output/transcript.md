# AC215 · Lecture 23 — Final deployment and review: Ansible on one EC2 server, then a commit that redeploys (follow-along: cheese-app-aws)

## 00:00 — Thirty-three commits, one backslash
This repository has 39 commits, and 33 of them carry the same message: slash run deploy app. That sentence is a button. Pushed to main, it rebuilds the app and redeploys a server.
And once, the slash leans the other way. To the workflow, that is a different sentence, and nothing runs at all. One character.
How does a sentence deploy a server, and why did one character stop it? By the end of part 2, you'll push that sentence yourself.
This is the course's last lecture: final deployment and review, in three parts. Its motivation is a playful prediction web page; our reading of it: even a toy prediction app is only useful when it runs somewhere, and stays current.
This recording machine has no AWS account. Everything on the laptop ran for real. Every command that talks to AWS ran exactly as the README writes it, up to its real first error. The consoles, the server and GitHub are drawings, marked illustration.
You need Docker, your own AWS account with billing, and for part 2, a GitHub repository. This lecture runs a server until you delete it. The tracker names the README step, and your turn means pause and run it.

## 01:19 — The final map, in AWS words
Here is the lecture's map. The dev team commits to GitHub, GitHub Actions builds and deploys to the cloud, and users reach the app there.
Above it, the app as one chain, from data to frontend.
The slides speak Google Cloud; we follow the AWS repository, as in lecture 15. Now the same map in AWS words. The Kubernetes cluster becomes one E C 2 server running Docker containers. The image registry becomes E C R, with three repositories. Pulumi becomes Ansible playbooks.
The service account key becomes two secrets: an IAM access key and an E C 2 key pair. The keyword becomes slash run deploy app, and the ingress becomes one nginx container at the front door.
There's no Kubernetes and no Pulumi here: one server, set up by Ansible, and no machine learning lane.
The lecture lists five things to automate. For this repo: pipeline jobs and model training, no, those were lecture 15. Frontend and backend deployment, yes, always together. Building and pushing containers, yes: three app images.
The lecture's plan: we already have a deployment container, so let GitHub Actions run it. Here it's called cheese app deployment.
The slides say: invoke the command line in that container. Here, that means ansible playbook commands. In part 1 you type them; in part 2, they arrive as one long command.

## 02:51 — A policy, a user and two keys
These first commands are extra; the README has no clone step. One branch, unchanged since we pinned it, and inside src, the deployment folder.
The list of APIs to enable sits inside a comment; on AWS there's nothing to switch on. One check: the API calls Bedrock models in U S East 1, chosen in 2024, so check your account can still use them.
Step 2, in the IAM console: create a policy from this JSON. It allows one identity check and nine E C R actions, to log in, push and pull, on any resource.
Name it cheese app E C R policy, and pause to create it; an extra check shows the JSON parses. It can't create a repository, so you'll make three by hand later.
Step 3: create a user, deployment AC215 user. It gets three policies AWS manages: full access to S3, E C 2 and Bedrock. And your own E C R policy.
Step 4: create an access key for a third party service, and download the C S V file. Save it in a secrets folder beside your clone, not inside it, so it can never be committed.
Step 5: create an E C 2 key pair, and save its pem file there too. The badge talks to the AWS API; the key opens the S S H door of your server.
An extra check shows a small gap. The README names the key pair cheese app AC215 key pair. The code expects AC215 underscore 2024, in three files. Easiest fix: use that name, so the file is AC215 underscore 2024 dot pem.
Extra: change mode 400 on the pem file. S S H refuses a private key that others can open.

## 04:48 — Ansible in one picture
Step 6, deployment setup, brings a new tool: Ansible. Pulumi, in lecture 20, described the infrastructure you want. Ansible runs an ordered list of tasks against the machines in an inventory. Many of its modules describe a state; this repo also runs plenty of shell commands.
A playbook is a list of plays. Each play names its hosts and holds tasks, and each task calls one module. The hosts line decides where tasks run: localhost means inside your toolbox; appserver means on the server, over S S H.
Here is that inventory, as one file. Ansible logs in as the user ubuntu. Line 4 points at the key for GitHub Actions; line 7, commented out, at the key on your laptop. Lines 9 to 11 take your keys from the environment: nothing to type.
Then the machine: the region, U S East 1, and a T 2 large instance. The key pair name, marked change this. An Ubuntu machine image for that region, and the disk names and sizes.
The README's four bullets point at exactly these lines. Change two now: the key pair name, unless yours already matches, and line 24, the Next auth secret, to a random value of your own. The host on line 30 comes later.
Every run ends with a recap; success means failed and unreachable stay at zero. A declarative task run twice reports ok the second time.

## 06:25 — Starting the toolbox: three surprises
Step 1: go to the deployment folder. Here are the playbooks, the inventory and docker shell dot S H.
Open the script. It splits the second line of your C S V into two variables. Line 17 hard codes the account ID of the author, a placeholder here.
Run it as cloned, and it stops: credentials file not found. Four dot dots from the deployment folder end at slash home, one level too far.
Step 2 is that fix: three levels up, with sed or your editor. Now the file is found.
Step 3: S H, docker shell dot S H, exactly as written. Surprise 1, on this Ubuntu laptop: a syntax error on line 13, redirection unexpected.
Extra: on Ubuntu, S H is dash, which has no here string. And typing S H skips the first line, which asks for bash. On a Mac the README line works; on Linux, use bash instead.
Surprise 2, at the time of recording, on our machine: the build stops at step 9 of 15. Curl can't verify the Helm download site, so no signing key arrives.
And the script doesn't stop: set dash e is commented out, so it runs an image that was never built. Check the build output, not just the last line.
Our machine didn't trust that certificate's root. Your laptop may. No playbook uses Helm, so delete these two lines and the word helm, and the toolbox builds.
Surprise 3: inside the toolbox, slash secrets is empty. Line 26 has the same four dot dots, so Docker mounted an empty folder. The prompt ID changes on every start.
So fix line 26 like line 10, and put your own account ID on line 17. AWS S T S get caller identity shows it, once your keys work.
Run bash docker shell dot S H again: both files are there, yours named AC215 underscore 2024 dot pem, and four AWS variables are set. Pause, and get to this prompt yourself.

## 08:44 — Inside the toolbox: whose Docker?
How was the toolbox started? Line 36 mounts the Docker socket. Then the deployment folder at slash app, your secrets, and the three app folders. Lines 43 to 46 hand in your keys as environment variables.
A question. Inside the toolbox, Ansible runs docker build for the frontend. Whose disk does the image land on: the toolbox's, or your laptop's?
Your laptop's. No Docker engine runs inside the toolbox; the Docker module of Ansible talks through the socket to your laptop's Docker. So the image lands beside the toolbox, not inside it. That's also why a prune, run from inside, would sweep your laptop.
Extra checks: the AWS command line, Docker, kubectl and Ansible are there, but not the Ansible the Dockerfile asked for.
Without quotes, the greater than sign in that pip install is a shell redirect. So the root folder holds a file whose name starts with an equals sign: pip wrote its log there, and installed Ansible 6, on an old Python. Quoting fixes it, but leave it for now: the provision playbook relies on this old Ansible.
That explains the warnings: the old Python, a collection that doesn't support this Ansible, and an old module name. We hide them from now on.
AWS S T S get caller identity: the security token is invalid. Ours is a placeholder. With your key, this prints your account ID and your user.
The inventory graph shows all, then appserver, then one host. And all five playbooks pass a syntax check. The toolbox is ready.

## 10:38 — Three images, one timestamp
Step 4: in E C R, in U S East 1, create three empty private repositories: the vector D B tool, the API service and the frontend. Your policy can push to them, but not create them.
The first playbook runs on localhost, inside the toolbox. Task 1 logs Docker in to E C R. Task 2 stamps a tag from the date, down to the second, and registers it, so later tasks can use it.
Then it builds the frontend from slash frontend react, the folder the script mounted, names the image with that tag, and pushes it. The API and the vector D B tool follow. Last, it saves the tag in a file: dot docker tag.
Step 5: ansible playbook, deploy docker images, dash i, inventory dot yaml. Pause and run it.
Our first real error: at the E C R login, the security token is invalid. The second line follows from the first: docker login received an empty password. The recap says failed, 1.
Extra: no image was built. The laptop still holds only the toolbox and its base.
With your keys, all 11 tasks run: three images built on your laptop and pushed, and your tag written to dot docker tag. Look for failed, zero, in the recap.
The last task is docker system prune, dash a. Without dash f, it asks, gets no answer, and removes nothing. Every push stores three more images in E C R, and nothing deletes old tags.

## 12:13 — Create a server, then provision it
Step 6 creates the server from localhost, through the AWS API. First, a security group with ports 22, 80 and 443 open to anyone, and a 50 gigabyte disk. Then a T 2 large instance with your key pair and two 100 gigabyte disks of its own. Last, it tries to attach the 50 gigabyte disk.
From here, the meter runs: the instance by the hour until you terminate it, its disks, and its public I P address.
Pause and run step 6. Gathering facts works, then it fails: AWS was not able to validate the provided access credentials. With real keys, watch the untested attach task. If it fails, the server still works; delete that spare disk when you clean up.
A kind note: the heading says G C P; it came over from the Google Cloud README.
Step 7: copy the public I P address of your instance from the E C 2 console into the inventory, under appserver hosts. Ours is a placeholder name.
A small slip: the key switch of step 9 is needed now. Pause, comment out line 4 and turn on line 7. It reads slash secrets, AC215 underscore 2024 dot pem: that exact name. The key on line 4 isn't in your toolbox.
Step 8: pause and run ansible playbook, deploy provision instance. Unreachable: could not resolve hostname external I P, our placeholder. On yours, Ansible logs in as ubuntu, with your key. Host key checking is off, so a new server is trusted blindly: a trade-off.
On a real server, 38 tasks install Docker, then format the second disk and mount it at slash M N T slash disk 1. They install the AWS command line and run AWS configure with your keys: your badge now has a copy on the server.

## 14:15 — Five containers on one network
Step 9: the key switch, done before step 8.
Two extras before you run step 10. The playbook starts Chroma at the tag latest: at the time of recording, version 1, which answers the old API with status 410, gone.
The clients and the repo's compose file pin an older version, which answers 200. So change line 151 to that version first.
Second, the loader uses docker run, dash I T, which Docker refuses without a terminal. We couldn't test whether Ansible provides one; if that task fails, drop dash I T.
Step 10: ansible playbook, deploy setup containers. Pause and run it. Ours is unreachable, for the same reason; here is what it does on a real server.
It writes your keys to a file only root can open, a second copy on the server, and hands them to the API container as environment variables. It creates a Docker network, appnetwork, and two folders on the data disk, and logs in to E C R.
Then it picks the tag: a docker tag variable in the toolbox's environment wins; otherwise, the dot docker tag file. From your laptop, it's the file.
It pulls the three images and starts the frontend on port 3000 and Chroma on 8000. A throwaway container fills the vector database, then the API starts on 9000. The security group keeps those ports shut.
Step 11: look around on the server. Where the README says G C P console, use S S H as ubuntu with your key, or E C 2 Instance Connect. Then list containers, follow logs, or open a shell.
Here they are on our laptop, as a stand-in. The image column carries the tag: check it there. The nginx lines work only after the next step.

## 16:13 — One front door: nginx
The lecture's routing: one address, slash to the frontend, slash API slash to the API. Here the same shape sits on one machine, and the ingress becomes an nginx container.
Step 12 says create nginx dot conf; it's already in the repo. It listens on port 80. Paths that start with slash API slash go to the API service on 9000; everything else goes to the frontend on 3000.
Predict: the browser asks nginx for slash API slash newsletters. Which path does the API service receive? Look at the very end of line 37.
Slash newsletters. The trailing slash after port 9000 replaces the matched prefix. Our stand-ins on the laptop confirm it, and slash API without its last slash gets a redirect.
The frontend calls slash API on the same host, and the API mounts its routes without the prefix: they fit.
Step 13: pause and run ansible playbook, deploy setup webserver. Unreachable again. On a real server, it copies the config, starts nginx on ports 80 and 443, and restarts it.
Step 14: open your server's address in a browser. Only port 80 does the work. Port 443 is open and forwarded to nginx, but nginx serves nothing there: no HTTPS yet.
That's part 1: about a dozen commands and five playbooks, by hand. Next, a commit message does the redeploy.

## 17:59 — CI, CD, and who presses release
Part 2 starts with the lecture's loop. Developers commit to the codebase. It is built and tested: that's the C I half. Then it is deployed and monitored: the C D half. Every stage sends notifications back.
The version in the review adds one box between test and deploy: release, the moment a tested version is handed over for deployment.
Continuous integration runs scripts on every push. Many developers share one repository, and every change passes automated tests, coding standards, and static analysis, which finds defects without running code. You built this in lectures 9 and 21.
Then delivery and deployment. Continuous delivery keeps every change ready to release, but a person presses the button. Continuous deployment ships every passing change by itself.
For machine learning, C I also checks data quality and model performance, which makes it expensive. And C D releases a model only when its metrics are within a tolerance, and must cope with data drift. This repo deploys an app, not a model; lecture 15 was the model.
Now this repo on the loop. Build, release and deploy light up; release is when the tagged images land in E C R. Test stays dashed: the workflow is named continuous integration and continuous deployment, but runs no test. It's the C D half. And monitor is the color of the run, plus your own check of the site.
The lecture names several C I C D services; the course uses GitHub Actions, to build the deployment container and run it, on every commit that asks. The workflow file stays thin; the deploy logic is the playbooks you just ran.

## 19:50 — Two sieves on one commit message
The workflow file, C I C D AWS dot yaml, isn't in the README, so every step on this tracker is extra. It starts on every push to main, but the job runs only if the commit message contains slash run dash.
And the last step, run deployment container, has its own condition on the same message: it must contain slash run deploy app.
Two sieves, one sentence. The message update readme has no slash run dash, so the job is skipped and nothing runs.
Your turn. You push fix typo, slash run tests, to main. Nothing, build and push only, or a full deploy?
Build and push only. It passes the first sieve, so the runner builds three new images and pushes them to E C R, where they cost storage. It stops at the second sieve, so the server keeps the old tag.
Slash run deploy app passes both sieves: new images, and the containers on the server are recreated.
And the commit from the opening? Its slash is a backslash. The text slash run dash isn't in it, so it bounces off the first sieve. That's the one character.
The tutorial slide says the same: a workflow file in dot github, workflows, and a keyword in the commit message. Its keyword, slash deploy app, belongs to the Google Cloud repo. Here it's slash run deploy app.
Head commit means the last commit of a push, so three commits are judged by the last message only. And the match ignores case.

## 21:35 — Secrets and the runner
Part 2 needs your own GitHub repository. Pause, create an empty private one, point origin at it, and push main. Its last message has no slash run dash, so nothing runs yet.
First, give GitHub your secrets: in your repository, settings, secrets and variables, actions. Add four: the access key ID, the secret key, your account ID, and AWS S S H key, the whole pem file. The names come from the workflow.
Your badge has a third copy now, in a vault on GitHub, and your key a second. Every copy is one more place to protect.
The runner is a fresh Ubuntu machine. An action from AWS sets up its credentials from two secrets. Then it checks who it is, lists S3, and logs Docker in to your E C R registry.
Then it builds the same toolbox, from the committed Dockerfile. So the Helm fix from part 1 belongs in your commit. We didn't test whether runners hit the same certificate error.
Next, a fresh tag from the date, written to dot docker tag and to a file GitHub keeps between steps. Run by hand, it gives a timestamp.
Then plain docker build, docker tag and docker push for the frontend, and the same for the other two images. In C I, the runner builds the app images, not the playbook.
So the toolbox only deploys. Compared with your laptop: same toolbox, same socket. But the deployment folder sits at slash deployment, the keys at slash root slash dot S S H, and no app folders.
Last, the S S H key. The step writes an S S H config, and your key as AC215 underscore 2024 dot pem, with mode 600. It copies both into the deployment folder, on the runner only, never committed.

## 23:35 — Follow one tag to the server
The deploy step runs the toolbox on the runner, with the socket, two folders, and five environment variables, docker tag among them.
Inside, one long command: fix permissions, log in to E C R, run deploy setup containers with the new tag, then deploy setup webserver. Each link runs only if the one before succeeded.
Run by hand, as an extra, it prints the tag and lists the key, then stops at the E C R login with our placeholder key. Neither playbook runs.
Follow one tag. The date stamps it on the runner. It reaches Ansible as an extra variable, which beats anything the playbook sets, so the server pulls the three images at that tag.
Then each container is recreated: the old one stops, the new one starts, with a short gap between.
The slides deploy to a Kubernetes cluster, where, as in lecture 22, a rolling update starts new pods before the old ones go. One machine can only swap; it doesn't roll.
Commit four things. Your server address on line 30: C I deploys whatever is committed. Step 9 undone: line 4 on, line 7 off. The Helm fix. The Chroma pin. Git add dot also commits your account ID and Next auth secret, so keep the repository private.
Then the slide's three commands, with this repo's keyword: git add dot, git commit with slash run deploy app in the message, and git push. Pause, and push.
A green run means every step that ran exited with zero, not that the app works. Reload your site, and find the new tag in the server's image column.
In the lecture's words: is typing slash run deploy app continuous delivery, or continuous deployment? What would make it the other?
Delivery. A person decides each release by typing the keyword, and nothing is tested first. Deploy every merge to main, behind the tests from lecture 21, and it becomes continuous deployment. That is Milestone 5.

## 26:01 — The delete that deletes nothing
Back to the README, for its last step: delete. It runs the same playbook with cluster state equals absent. Look at the when lines. Which of these three tasks run?
Run it exactly as written. Security group, skipping. E B S volume, skipping. Then the instance task has no when line, and fails: no attribute group ID. That is before any AWS call.
The skipped task never set the security group, so the instance task trips over it. Even past that, the removal needs a volume ID that only a create run registers, and no task terminates the instance. So clean up by hand.
In the E C 2 console, terminate the instance, then delete the 50 gigabyte volume, which outlives it, the security group and your key pair. Cost is one of the lecture's challenges for C D, and this server bills until you do this.
In E C R, delete the three repositories. In IAM, deactivate and delete the access key, and the user and the policy if you made them only for this. On GitHub, delete the four secrets.
On your laptop, remove the toolbox image, two and a half gigabytes, and keep or restore your edited files.

## 27:32 — The course on one server, and recap
The lecture ends with a review of the course, on the server you deployed.
Virtual machines and containers, lectures 1 and 2. A shared bucket, lecture 3. And the images the senior developer pushed by hand: the runner pushes them now.
The solution architecture: frontend and API execute; E C R and the disk hold state. Retrieval, lecture 5, is the loader and Chroma; agents, lectures 6 and 7. Labeling and fine tuning aren't here: the API calls ready-made models through Bedrock, plus the cheese classifier trained earlier, as a file.
Training and pipelines, lectures 13 and 15, sit beside this server. The API and frontend containers, lecture 18. The C I loop, lectures 9 and 21. Routing, lectures 20 and 22: today's nginx.
Where next? Put the tests from lecture 21 in front, and deploy every merge to main. Replace the copied keys: a role for the server, and O I D C for GitHub. And add HTTPS.
Once more, the path. Two secrets on your laptop. A toolbox using your laptop's Docker. Plays on localhost, or on the server over S S H. One tag, from the date command to a recreated container. One sentence that presses release. And clean up by hand.
Test yourself. One: name the two secrets, what each opens, and three places the access key ends up. What would a role and O I D C remove?
Two: why does S H, docker shell dot S H, fail on Ubuntu but work on a Mac? And what did that unquoted pip install actually do?
Three: where do the tasks of a localhost play run, and of an appserver play? And why can the toolbox fill the disk of your laptop?
Four: follow one timestamp from the date command to a running container. How does the server choose between the variable and the file?
Five: which of these deploy? Update readme, fix typo slash run tests, slash run deploy app in capitals, and backslash run deploy app. And is this pipeline delivery or deployment? Answers are in the exercises.
