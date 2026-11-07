# AC215 · Lecture 21 — CI/CD with GitHub Actions II: one push, six fresh machines (follow-along: cheese-app-ci-cd)

## 00:00 — Red run, green summary
You push the course's own code, untouched, to a repository of your own. Soon after, one log says: unit tests, success. Integration tests, success. System tests, success. All tests passed.
And the same file, run end to end, ends like this: job Lint and Format Check failed. Five machines green, one red, and the whole run red. The pipeline says every test passed, and the pipeline failed. Both are true.
So which machine said no, and why didn't the summary hear it? By the end of part 1 you will see this on your own push. In part 2 we open every log.
In lecture 9 these checks ran on your laptop, before a commit. Today they move to GitHub, and they run on every push to main, on fresh machines that nobody owns.
Lecture 21 has four sections: remote Git hooks, GitHub webhooks, continuous integration, and continuous deployment. We follow it slide by slide, and the README Part 5 step by step.
To follow along, you need a fresh clone of the course's repository, Docker running, a GitHub account, and a repository of your own. No cloud and no keys, and on a public repository, no bill.
The tracker names the README step, code panels name their file and lines, and a yellow tag, your turn, means pause and run it. The runs you will see ran right here on fresh machines; the GitHub pages are drawings, and they say so.

## 01:33 — Hooks stay on your laptop
The lecture opens with a recap: local Git hooks. A pre-commit hook runs on your laptop, before the commit even exists. A pre-push hook runs before your commits leave. In lecture 9 you installed this repo's set.
Here is that chain, with this repo's boxes: seven hygiene checks, then Black, then Flake8, both at 120 columns, and only on files under src. The lecture's chain ends with tests. This repo's hooks run none: it leaves the tests to CI.
The lecture's catch: hooks run only on a machine where someone ran pre-commit install. A teammate's laptop without them sends its commit through unchecked. So the checks depend on the laptop.
That's where remote hooks come in: they run on the server that receives the push. A pre-receive hook runs before the push is accepted, so it can refuse it. The update hook does the same, one branch at a time.
A post-receive hook runs after the code is in, for integration tests, notifications and clean-up. It can report, but it can no longer say no.
One honest note: GitHub dot com doesn't run your own pre-receive scripts. It gives you two pieces instead: Actions, which runs after the push, and branch protection, which can say no.
And hooks act only inside Git. To tell a chat what happened, the lecture reaches for webhooks.
Now the lecture's motivation, in three slides. On your laptop, the checks fire on every commit. Then you push, and on the shared repository, nothing runs them at all.
So the checks move to the server: build a container, check the code, summarize the tests. Same idea, new home, for every push to main from every laptop. That move is continuous integration.

## 03:24 — The CI loop and the workflow file
The lecture defines continuous integration as a series of scripts that run automatically whenever the code changes. They integrate changes continuously, test automatically, enforce coding standards, and run static analysis.
In ordinary software, that buys faster releases, better code, and easier teamwork. Machine learning adds a twist; we come back to it at the end.
Slide 21 draws it as a loop. Developers commit to the codebase; the codebase is built, then tested; and notifications flow back to the developers. For now, the way back is a question mark.
The course's pipeline has five stages. A commit triggers it, the container is built, Black and Flake8 check the code, the tests run, and a summary reports pass or fail.
Now the README, Part 5: GitHub Actions, remote CI. It says all CI tests run inside Docker containers using Python 3.11, the same as production. This repo has no production yet: take it as the same image you would deploy.
This one isn't in the README, it's extra: list the workflows folder. One file, C I dot yaml, in dot github, workflows, at the root of the repository. GitHub looks only there; a workflow in a subfolder never runs.
Open it. The file gives the workflow a name, CI Pipeline. The key named on lists the events that start it. Under jobs, each job gets its own machine: runs on, ubuntu latest.
Inside a job, steps run in order. A step is either a shell script, under run, or a reusable action, under uses, like actions checkout, which copies your repository onto the machine. Event, workflow, jobs, steps: that is the whole grammar.

## 05:17 — When does the pipeline wake up?
When does the pipeline wake up? The slide says on every push or pull request. The file is more precise: pushes to main or develop, and pull requests into main or develop.
Push to main, and a runner wakes up. Push to develop, the same. Push to a feature branch, and nothing happens: on any other branch, the pipeline waits for your pull request. A small note: the comment at the top of the file says main only; the triggers say main and develop.
Quick test. You push three commits to feature login. How many runs start? Then you open a pull request into main. How many now?
None for the three pushes: the branch filter. One when the pull request opens, and one more for every later push while it stays open.
And it doesn't test your branch tip. GitHub makes a temporary merge of your branch into main, and the commit ID the jobs see names that merge. What will land is what gets tested: each merge is tested, as the lecture says.
The lecture warns that integrating often costs compute. This file answers with a branch filter, one build shared by every job, and an image kept one day. On private repositories every run counts against your plan; public ones run free.
And timing matters: the run starts after GitHub has accepted your push. It's the bell, not the gate: a red run doesn't undo the push.

## 06:53 — Six jobs, one graph
Next, the README: 6 jobs that run in parallel, except for dependencies. Each has an ID and a name: Build Docker Image, Lint and Format Check, Unit Tests, Integration Tests, System Tests, and Test Summary.
Remember the names: GitHub shows them, not the IDs, and we'll need them to protect main.
Start from the lecture's row of five. Commit drops out first: it's the event, not a job. Build Container stays on the left: it's the build job.
Now each needs line draws one arrow. Lint and format needs build. Unit tests, integration tests and system tests each need build too. So after the build, four jobs run side by side, each on its own machine.
Test summary needs the three test jobs. Look closely: the lint job isn't on that list. The lecture lists the stages in order; on GitHub, four of them run side by side, and the summary listens only to the tests. Keep that gap in mind.
An extra check, not in the README: a tool called act, which you don't need, takes the same file and lists the jobs in stages. Stage 0, build. Stage 1, the four checks. Stage 2, the summary.
Then the key concepts. Artifact sharing and unique image tags come with the build job; parallel execution, you just saw; conditional execution and network modes come with the system tests.
The README's screenshot gives the times: about 2 minutes on the clock, with four jobs side by side. On a private repository, each job is billed and rounded up separately: about 6 billed minutes.

## 08:36 — Push to a repo of your own
Time to push. Start from a fresh clone, not your lecture 9 folder: that one has the Black fix committed, and your first run would come out green. Clone, change into the folder, and git status says the tree is clean.
Your prompt shows your own user. Two extra checks first: the pinned commit is still the head of main on the course's repository, and the last two commits are both called demo class 1. The second undid a bug planted in class; we'll run it later.
Now the README block, Push to GitHub. Git add dot: no output. Then git commit, dash m, Add CI pipeline. And Git answers: nothing to commit, working tree clean.
A small slip, and a harmless one: in a clone or a fork, the pipeline is already committed, so there is nothing to add.
Before the README's git push, an extra check: git remote, dash v. Origin is still the course's repository, and you can't write to it. GitHub would refuse a push from here: permission denied.
So point origin at a repository you own. Either fork the course's repository and enable workflows on its Actions tab, or create a new empty repository. Either way, run git remote set-url origin, with your own address. Pause and set yours up.
This recording machine can't push to GitHub, so an empty repository on the same machine stands in for yours. From now on we just say your repository.
Now the README's git push. New branch, main to main. This push is the event, and run 1 starts now. Pause and push yours.
On a fork, that commit is already on GitHub, so git push says everything up to date and starts nothing. Your first run then comes with the fix in part 2.

## 10:28 — Watch the run: six colours
Watch GitHub Actions: go to your repository, and click the Actions tab. Your run is listed under the commit message, with a yellow dot: in progress. A green checkmark means success; a red X means failure. Pause and open yours.
Click it, and GitHub draws the run as the graph you just built: build first, four jobs side by side, the summary last.
A word on how we show it. We ran every job of this file right here, each on a brand-new machine with an empty Docker, as GitHub does. And a tool called act ran the whole file a second way, with the same verdict.
So the GitHub pages you see are drawings built from the workflow file, marked illustration. Every log line in them is real.
A question, before the colors come in. You already know this run turns red. Is your push on main in your repository now, or did the red run refuse it?
Yes, it's on main: the push landed before any job started, and a red run can't undo it. Build: green. Lint and Format Check: red. The three tests and Test Summary: green. The run: red.
Those checks and crosses next to your commit are the lecture's notifications. And act, the second witness, agrees: five jobs succeeded, one failed.
A kind note: the README's screenshot is all green. It shows an earlier version of the code. Your first run is red, and in part 2 you turn it green.
And here is the hook, on your own push: two of these six machines disagree. In part 2 we open every log, one job at a time.

## 12:17 — Build once; every job starts empty
Part 2, job by job. First, build container: the lecture builds it first, so every check runs in the same environment, and build problems show up early.
The lecture speaks of one remote CI server. GitHub gives you a new one for every job: runs on, ubuntu latest, six times in this file. Each job starts on an empty machine.
The README's build job builds the image once, tagged with the commit ID. It saves it as a tar file and uploads it as an artifact, so every other job gets the exact same image.
On GitHub, click a job, then a step, to open its log. Docker builds the image from the Dockerfile and names it cheese app API, colon, the commit ID. That tag means this commit's image, nothing else.
A small slip: the README promises Buildx caching, but the build runs on the default builder, and nothing saves a cache, so every fresh machine rebuilds from scratch. The exercises show how.
Docker save folds the image into one file, about 176 megabytes. The upload step carries it to the artifact store, kept for one day. Then the build machine is thrown away.
Now step into a fresh check job. An extra command, docker images, shows just the header. No image at all.
So every check job downloads the artifact and runs docker load, dash i, on the tar: the same tag, unpacked from the suitcase. That's artifact sharing. And the artifact expires after a day, so re-running a failed job tomorrow fails at the download.
Your turn to predict. Delete the load docker image step from the unit tests job. Which step fails, and with what error?
The run unit tests step. Docker looks for the image on the machine and finds nothing, then asks Docker Hub, where no such image exists: pull access denied. Exit code 125: the step fails, so the job fails.

## 14:31 — Gates speak in exit codes
Next, lint and format. The lecture's coding standards are Black here, and its static code analysis is Flake8. Remember lecture 9: a formatter rewrites your code; a linter only reports.
Both run inside the image, on the api folder, at 120 columns. The Black step says continue on error, false: it blocks. The Flake8 step says true: it's advisory, a warning that never fails the job.
How does a step fail? Every command ends with an exit code. Zero opens the gate. Anything else shuts it, and the red climbs from the step to the job to the whole run.
Run 1, the Black step: would reformat utils dot py. One file would be reformatted. Exit code 1, so the gate shuts.
The step list shows what happened next. Black, failure. Flake8, skipped. The steps below a failed step don't run, unless they ask to run always.
The cause is the mess you met in lecture 9, still in the repository on purpose: no space after the comma, and three blank lines where two belong.
What would the skipped Flake8 have said? An extra run shows two warnings on those same lines. But even then it's advisory: only Black decides the job.
So that's the whole rule: a step fails when its command exits with anything but zero. It's the only thing CI listens to.

## 15:58 — Three test jobs, three altitudes
Now the tests. The lecture's one test box is three jobs here, side by side, each at a different altitude.
Unit tests check one function at a time, with no outside dependencies. The log collects 11 tests, and 11 pass.
Then the coverage step runs them again, and all 11 pass again. But pytest hits an internal error: permission denied, writing into the coverage folder. Exit code 3.
Yet the job is green. The step says continue on error, so the failure is shunted aside. Then the upload, marked if always, finds no files; on GitHub, a yellow warning says so.
The README has a small gap: it promises terminal, XML and HTML reports. Docker creates the missing coverage folder as root, and the container's user, app, can't write into it. Create the folder writable first; the exercises have the fix.
Integration tests use the FastAPI test client: the app is called inside the same Python process. No server, no port. 10 passed.
System tests need the real thing. One container starts the server in the background and publishes port 9000 on the runner. An extra command, docker ps, shows it running, with 9000 mapped.
Then the job waits 10 seconds, and curl, dash f, knocks on localhost 9000. Only when the welcome message comes back does the next gate open.
A second container runs the tests with network host: it shares the runner's network, so localhost 9000 reaches the server. 5 passed.
Two steps marked if always come last, even after a failure: show the server log, where every test request arrives, then stop and remove the container. That's the README's conditional execution.
In lecture 9, a missing server made these tests skip quietly. Here the curl gate makes it fail loudly instead.

## 18:02 — The summary listens only to tests
Last job: the summary, which the lecture says collects the results and reports pass or fail. Its needs line names the three test jobs. And if always lets it run even when one of them failed: it runs, which isn't the same as passing.
Its script prints each job's result, writes a status to GitHub output for later steps, and exits with 1 if any result isn't success.
In run 1, three success tokens arrive: unit, integration, system. All tests passed.
And here is the hook, answered. Lint isn't in needs, so its failure never reaches the summary. The run is still red, because any failed job turns the whole run red.
The README says the summary checks the results of all test jobs, and that's literally true: lint isn't a test job. Add lint and format to needs and to the check if you want it counted.
Now the bug from class. In the demo commit, the distance function takes the square root of 2 times z, instead of z.
Predict before the run. Which jobs turn red now, and what does Test Summary say?
Integration: red, 1 failed and 9 passed. The distance for 3 and 4 came back as about 7, not 5.
System: red, 2 failed and 3 passed: 3 and 4 again, and the default point, 1 and 2, which came back too large as well. Unit: green, because only the power function has unit tests. Lint: red anyway, for utils dot py.
And the summary now says some tests failed, and exits with 1. This time the summary heard it.

## 19:48 — Fix, push, green: one turn of the loop
Back to run 1 and the lecture's loop. The notification came back red, so now the developer fixes the code and commits again, and the loop goes around once more.
The fix is the tool from lecture 9, Part 4 of the same README, so these steps are extras here. Pip install pre-commit, then pre-commit install, which puts the hook into dot git, hooks.
Then pre-commit run, all files. The hygiene checks pass; Black fails, because it modified a file: reformatted utils dot py. Flake8 then passes. Pause and run it.
Git diff shows exactly what Black changed: a space after the comma, and one blank line gone.
Run it again, and every hook passes. Nothing is left to fix.
Now git add dot, and git commit with a message: Format utils dot py with Black. The message is ours; the README has none. The hooks run on the commit and pass. Then git push. Pause and push yours.
Run 2: all six green. In the lint job, Black is happy, and this time Flake8 runs too, and passes. On a fork, this is your first run, and it's green.
Now your run matches the README's screenshot. One turn of the loop: a red notification, a fix, a commit, and a green run.

## 21:08 — The local conundrum: --no-verify
The lecture calls this one the local conundrum. If the hooks already ran on your laptop, why run the same checks again on a server?
These steps are extras, and you can just watch. A quick edit squeezes the spaces out of one line in service dot py, and git diff shows it.
Git add dot, then git commit, dash m, quick fix. The Black hook fails and reformats the file, so the hook stopped the commit.
Git status, short, shows M twice. Black fixed your working copy, but the staged copy is still the messy one.
Now the lecture's command: git commit, no verify, dash m, quick fix. No hook ran, and the commit exists: no verify skips every pre-commit check.
Push it. Run 3: lint and format, red, on service dot py. The tests and the summary all pass.
The skipped Flake8 would have flagged that line three times. CI caught what no verify let through: slide 31, at your terminal.
Clean up the experiment: git restore puts the file back. If you pushed it too, your main is now red: run pre-commit run, all files, then add, commit and push, before part 6.
But CI repeats only Black and Flake8, and only on the api folder. The seven hygiene hooks never run in CI: trailing whitespace, end of file, YAML, large files, JSON, merge markers, and private keys.
One more gap: the hooks pin an older Black than the image installs. At the time of recording they agreed, but they can drift apart.
A teammate commits a private key file with no verify and pushes to main. Which job of this pipeline catches it?
None. Detect private key is a local hook only. The fix is one CI step, pre-commit run, all files: the very step that fails on the lecture's imagined Slack message. And rotate that key; it's already on GitHub.

## 23:17 — Webhooks, secrets and the Slack bell
That imagined message brings us back to the lecture's webhooks. A webhook is GitHub calling an outside address when something happens: to start an outside CI system such as Jenkins, to deploy, or to post to a chat.
This part is optional: it needs your own Slack workspace. And this webhook works the other way round. Slack gives you an incoming webhook, an address, and the last steps of the test summary job call it. GitHub doesn't ring this bell; your workflow does.
The lecture imagines a Slack channel told about every push, failures included, with the failed step, counts and duration. This workflow sends less: passed or failed, the repository, branch, commit and author, one mark per test job, and two links.
The webhook address is a secret. Add it under Settings, Secrets and variables, Actions, as a new repository secret named Slack webhook URL, not under Webhooks. It never goes in the repository, logs show it as three stars, and pull requests from forks don't get it.
The check step tests whether the secret is set, and writes enabled, true or false. Why not test the secret right in the if line? GitHub doesn't allow secrets there; the repository's own history tried it, and replaced it with this shell check.
In run 1 there's no secret, so enabled is false, and the Slack step is skipped, as it should be.
Now the demo run. Check test results fails. The check step has no if always, so it's skipped too, enabled stays empty, and the Slack step's condition is false.
As written, the bell only rings for good news. The fix is one line: if always, on the check step. The exercises have a hardened version.

## 25:07 — Branch protection: from report to gate
Part 6 of the README is optional, and it's the lecture's gate. A push-triggered run is the post-receive bell. On GitHub dot com, the gate that refuses is branch protection, with required status checks.
Go to Settings, Branches, and add a rule for main. Tick the boxes Require a pull request before merging, and Require status checks to pass. Today's page may call it a classic rule, or offer rulesets instead.
Then pick the checks. A small slip: the picker lists jobs by their names, like Lint and Format Check and Unit Tests, not the README's IDs. They appear only after a recent run. On a private repository this needs a paid plan.
Then test it: git checkout, dash b, feature, test protection. Pushing that branch starts nothing, as you saw with the triggers; the run starts when you open the pull request.
The README breaks the tests by appending def broken, assert False. An extra run in the image still says 11 passed, because pytest only collects functions whose names start with test.
So name it test broken instead, an extra fix. Now 1 failed and 11 passed. That's the one that turns the pull request red, and with protection on, the merge button stays locked.
Then git add dot, git commit, dash m, Intentionally break tests, and git push origin feature, test protection. Open the pull request on GitHub: the merge stays locked until the tests pass. Pause and try it on yours. Here, git checkout puts the test file back.

## 26:44 — Non-determinism, CD next, and recap
The twist the lecture promised: non-determinism enters every stage when the code trains a model. Its answers: version everything; automate retraining and testing, which Milestone 5 asks for; monitor; and roll out with care.
Continuous deployment, the lecture's last section, automates the release: that's lecture 23.
Clean up: switch to main, and delete the test protection branch here and on GitHub; that closes its pull request. Remove the branch rule, and the Slack secret and webhook, if you made them. Disable the workflow on a private repository, and run the Docker cleanup from lecture 9.
Once more, the loop. Your push is the event. Each job gets a fresh machine, so the image travels as an artifact. Every step is a gate that reads an exit code, and the summary hears only the jobs it needs.
Test yourself, pausing on each. One: name two ways code reaches the shared repository without passing your local hooks. Which checks does this pipeline repeat?
Two: which unit gets a fresh machine, a job or a step? And why does that force a docker load in every check job?
Three: your run is red, but the summary says all tests passed. Why, and what is the one-line fix?
Four: why can Flake8 fail without failing its job, and why don't you see its output when Black fails?
Five: is a push-triggered run a pre-receive or a post-receive check, and what makes it a gate? Answers are in the exercises and the study guide.
