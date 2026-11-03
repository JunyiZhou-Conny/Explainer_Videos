# AC215 · Lecture 11 — Data labeling and versioning: a label is a record, a version is a fingerprint (follow-along: data-labeling + data-versioning)

## 00:00 — Same names, different data?
Two folders, both called cheese dataset, with the same file names and the same count. On Monday you trained a model on one of them. On Friday the model got worse, and nobody touched the code. So which photos, with which labels, did that model see? And can you get exactly those back?
Most of us answer with file names: final, final version 2, final final version 3, until nobody knows which one is final.
Here is a better answer: one short line. In part 2 you will compute this exact string on your own laptop from 4 cheese photos. It will match the instructor's tag in the class repo, character for character. How can one line pin down about 600 kilobytes of photos?
And before that, when someone clicks gouda, where does that word actually go?
To follow along you need Docker Desktop, a Google Cloud project with billing and your own bucket, and a GitHub account. This lecture stores a few megabytes in the cloud, and gold tags mark where. The tracker in the top left follows both READMEs. A yellow your-turn tag means pause and run it; a gray extra tag marks a check that is not in the README. Every command is in the study guide.

## 01:15 — Two stations, two buckets
First, the map. The lecture draws unlabeled cheese photos, then labeled ones, then training, and the arrow in between asks how. Labels are the ground truth a model learns from and is graded against. The model's mistakes, once labeled, go into the next dataset version.
Underneath, the two stations this lecture builds. Part 1 is the labeling station: Label Studio and a small command line container, with one bucket for photos and labels. Part 2 is the versioning station: one DVC container, a bucket with two folders, your own GitHub repo, and Colab to view versions. The code does not connect the halves yet; exercise E7 does.
Now, the lecture's recall quiz. Docker network, cloud credentials, Docker Compose: where will each one show up today?
The network lets the command line container call Label Studio by name. The credentials are one key file, mounted into every container. And Compose is the README's extra section, which starts both containers together.
Clone the data-labeling repo and move into it; pause and run it. Give Docker more than 4 gigabytes of memory, as the README asks; the setting is now under Settings, Resources.
An extra git log shows this video's commit, from October 2025; an extra listing shows the scripts, cli.py and three pictures.
Next, the secrets folder, beside the repo and never inside it; it serves both repos today. Pause and make it; an extra tree view matches the README.

## 03:14 — A key, 21 photos and a bucket
Now the key. In the console, create a service account named data-service-account, with the Storage Admin role. Then create one JSON key, saved in your secrets folder as data-service-account dot json. This role is broader than needed: it covers every bucket in the project. Pause and create yours.
An extra listing shows the key in place: a stand-in, explained in scene 5.
Download the unlabeled photos from the README link; we use curl, and a browser works too. Then extract the zip. Pause and do both. Notice that every image comes with a twin in a hidden Mac folder.
A quick prediction: the zip held 42 files. How many tasks should Label Studio make?
21. An extra count shows 21 images, one of them a PNG, plus 21 Mac metadata files. Upload only the images, or you get 21 broken tasks. The lecture calls this curation, dropping junk before it becomes a task.
One more extra, for part 2: each photo's fingerprint, computed from its bytes alone. Same bytes, same string; change one byte, and it changes completely. Remember the first one.
Then create your bucket with a name of your own, since names are global, and keep the defaults. Add two folders, cheeses unlabeled and cheeses labeled, and upload the 21 images into the first. Pause and set it up. A gold tag: storage starts here, a fraction of a cent a month.

## 04:54 — A whole web app in one docker run
The README runs Label Studio from a ready-made image, in your own container, so no outside labeling service sees your photos. Its script creates the network only if it is missing, and removes any old container with that name.
Then one docker run, flag by flag. The flag dash d runs it in the background, and the network flag puts it on a private street. Then dash p, 8080 colon 8080, publishes the port: a door in your laptop wall. Two dash v flags mount a database folder and your secrets; the dash e lines set the login and key path.
Pause and run sh docker-shell.sh; it pulls the image. Then the README's check, docker container ls: up, port 8080 published.
But look again 25 seconds later, with an extra dash a: exited. Something to ponder: where do you look first?
The logs. Label Studio explains itself: its data folder is not writable. It runs as user 1001, but Docker created the missing folder as root.
The fix is an extra, for Linux; Docker Desktop for Mac normally avoids this. Give the folder to user 1001 with sudo chown, run the script again, and now it stays up. On Linux, pause and do the same.
Extra checks: the logs show a box offering version 1.23.2, newer than this image, which ran 1.23.0 at the time of recording. The tag is latest, so yours may differ.
Open localhost 8080 and log in with the username and password from lines 19 and 20 of your script. Create a project with the image classification template, with the choices brie, gouda, gruyere and parmigiano. Pause and do it. Underneath, our stand-in calls replay the page's requests: we are logged in, and project 1 holds the four cheeses.

## 07:13 — Who touches the bytes?
Back in the project, open settings, then cloud storage, and add source storage, where the photos come from. Use the README's values: Google Cloud Storage, your bucket, the prefix cheeses unlabeled, and pre-signed URLs on. If a checkbox is missing, carry on. Leave the credentials empty: that means the key the container already has.
Then click Check Connection. Here it fails: file not found. An extra listing shows why: slash secrets inside Label Studio is empty. The target storage, where labels go, with the prefix cheeses labeled, fails too, with a vaguer message.
One honest note about this recording. This machine has no Google account, no bucket, no browser, and no SSH route to GitHub. The key in the folder listings is an obviously invalid stand-in, moved out before every cloud step. So each cloud step here fails exactly the way a misplaced key fails. That is the most common mistake in this lecture. Every success you should expect is tagged recorded, with its source, and clicks and uploads are replayed locally, tagged stand-in.
With a real key, add both storages and click sync: one task per photo, 21 for you. Our stand-in imports 3 tasks with the same kind of addresses. Pause, add both, and sync.
So who touches the photos? Label Studio holds the key and lists the bucket; your browser asks for task 1. Something to ponder: your browser never sees the key, so how can it show a private photo?
With a signed ticket. Label Studio does not relay the photos; it signs a web address with the key: permission for one photo, for a short time. Your browser carries that ticket straight to Google, and the key stays in the container. Then the thumbnails break, and the README warns you: it is CORS.

## 09:20 — CORS: the bouncer, configured on the bucket
The page comes from localhost 8080, the photo from Google's storage address: a different origin. When the page's own code fetches the photo, as Label Studio does, your browser hands the answer over only if it carries a header that allows this origin. Google adds that header only if the bucket has its own CORS rule.
A small slip: the README blames a reverse DNS lookup, but the cause is that same-origin rule.
The README sets the rule from a second container. Put your bucket name on line 23 of docker-shell-CLI.sh, then run it with sh. The ID in the prompt changes every run, and Apple Silicon says aarch64 where this machine says x86. Pause and do both.
This container joins the same street and calls Label Studio by name, not localhost. It mounts the repo by its folder name, so keep that name.
Inside, run python cli.py dash c, then dash m; pause and run them. Here both stop at the storage client: file not found, because ADC looks for the key. The code builds one rule, any origin, GET only, max age one hour, and patches the bucket.
With a real key, dash c prints the rule, and dash m prints the bucket settings. Now the header arrives and the thumbnails load. The max age only caches preflight checks, which a plain image request never makes.
Something to ponder. You ran dash c and refreshed, and the thumbnails are still broken. Name two suspects.
One: the rule missed your bucket. Dash c failed, or line 23 names another bucket of yours; dash m shows which bucket got it. Two: your browser reused cached answers; hard refresh. And curl never met a bouncer: CORS is a browser rule, not access control.

## 11:27 — A label is a record; read it back by name
Back in Label Studio, click a task, pick a cheese, and submit; repeat for a few. Pause and label some. Here is what one click becomes, as a stand-in call: a small JSON document whose result says choices, gouda.
Label Studio saves it in its database, and the target storage writes a copy to cheeses labeled, pointing back at the photo, which never moved. The slide sorts photos into rows, but on disk a label is a small JSON note, and a labeled dataset is photos plus notes. In the console, that folder shows one JSON file per annotation. Open one to see the note.
The command line container calls Label Studio by name. Something to ponder: what if its address were localhost 8080?
It cannot connect: inside a container, localhost is that container, and nothing listens there. The name works, because the Docker network keeps a phone book of container names.
To list labels from code, copy your access token from Account and Settings, then run the README command: python cli.py dash p, dash k, and your token. Pause and try it. On Label Studio 1.23.0 it fails with a 401; ours says legacy token authentication has been disabled for this organization.
An extra check shows why: this version has two kinds of token. The page shows a newer personal token by default, the legacy kind is switched off, and cli.py speaks only legacy.
The fix: in organization, API token settings, enable legacy tokens. Then copy the legacy token, not the personal one. Pause and do both.
Run dash p again, and it lists project 1, cheese labels. Then dash t with your token: 3 tasks in our stand-in, 21 for you; ours has one labeled, as gouda. Pause and run both. The README's sample says amanita; the format is the same.

## 13:50 — Both containers in one file, and a clean exit
The README's extra section runs both containers from one compose file. Leave the command line container with exit, stop Label Studio, and check with docker ps; pause and do it. Then run sh docker-shell-compose.sh. Here it stops on a name conflict: docker stop leaves the container behind, still holding its name.
An extra docker rm frees the name; pause, remove it, and run the compose script again. This time Compose creates Label Studio plus a one-off command line container.
An extra echo prints the README's bucket name: compose keeps its own copy, on line 17 of docker-compose.yml, so edit it too.
And the first call is refused: the depends on setting starts Label Studio first, but does not wait until it listens. After an extra wait loop, project 1 is back, because the same folder is mounted.
Label Studio keeps running after you exit the command line container. Then the README's cleanup: list, stop, prune, and list the images; pause and run them. The prune also removed the network, so next time run docker-shell.sh first.
Something to ponder: after docker system prune, is your labeled project gone?
No. The database file is still in the mounted folder, and prune never touches folders you mount. But the photos they point at can change under them: same name, new picture. So how do you freeze exactly which photos a model saw? That is part 2.

## 15:41 — A repo of your own, from the starter
Part 2: freezing which photos a model saw. Git alone would copy every photo version into every clone. Of the lecture's four approaches, we build the file-based one: git versions a small file of fingerprints, and a bucket holds the photos. The tool is DVC.
First, move up one folder, so the new clone sits beside data-labeling and secrets. The data-versioning README starts with the same three cleanup commands. Pause and run them.
Then clone the starter branch the README names. Its SSH command needs your key on GitHub, and this machine has no SSH route. So the same branch comes over HTTPS, which the README allows. Pause, clone it, and move in.
One note: on the day of the lecture the README changed, and it now says to clone main. That branch brings the instructor's finished DVC files along, as an extra second clone shows. This video follows the course's pinned README: the starter branch, plus one fix.
Remove the old git history, so the code is no longer tied to the class repo, and start fresh with git init. Pause and run both. Git's hint mentions master, which is why the branch gets renamed next.
On GitHub, create an empty private repo called data-versioning, with no README, license or git ignore file. Then the five commands: rename the branch, add your repo as origin, add, commit, and push. Pause and run them. Your repo now shows the 7 files on main.

## 17:30 — A bucket that looks like a folder
A bucket stores named objects, nothing else. Add tools, like versioning, and the lecture calls it a data lake. Its folders are only shared name prefixes, which sets a trap.
The secrets folder from part 1 already sits beside this repo, as an extra tree view shows. The README wants the same service account and key, so reuse both.
In your bucket, create two folders in the console: DVC store and images. A small gap: the course's README never says to put the first photos into the images folder, yet later it says to add more. So upload Image 1 through Image 4 from the zip. Pause and do it.
In docker-shell.sh, replace the bucket, project and zone with yours. Only the bucket name is ever used. Pause and edit it.
The entrypoint runs the four stages the lecture draws. Authenticate with the key. Mount the whole bucket as a folder, with gcsfuse. Bind its images folder to the path the app expects, cheese dataset. Then use the data: DVC works on that folder as if it were local, while each file is fetched from the bucket.
The lecture takes the mount line apart: tool, key file, bucket, mount point. One flag is not passed, implicit dirs, so gcsfuse only shows folders the console made, which leave a marker object. That was the trap.
Note the two bind mounts: dash v joins your laptop's repo to the container, and the inner one joins the bucket's images folder.
Mounting needs the fuse device and mount rights, hence the privileged flag and the extra capability. The script also mounts your repo, secrets and git config. Set up git before the first run, or Docker creates a folder in its place.

## 19:29 — The starter that no longer builds
You are already in the data-versioning folder, so run sh docker-shell.sh. Pause and run it. On the starter branch, the build dies: package google-cloud-sdk has no installation candidate. The message even names the replacement, google-cloud-cli.
A small slip, and not your fault: Google renamed the package, the main branch fixed line 36, and the starter never got the fix. Make the same one-word change, as an extra. Pause and edit it.
Pause and run it again. The first build is slow. Then the entrypoint runs, and every stage fails the way a missing key fails. The gcloud tool cannot find the key file, and neither can gcsfuse, so the bucket never mounts. Yet the next line says bucket mounted, because the script prints it no matter what. Then the bind mount fails: special device does not exist.
And still you get a root prompt, because the entrypoint does not stop at errors. Extra checks: the cheese dataset folder is empty, and DVC 3.63.0 is installed, pinned by the lock file. So the rule for today: list the folder before you add it.
With a real key, the folder inside lists your four photos. Something to ponder: on your laptop, the same folder is empty. Is the mount broken?
No. Both mounts exist only inside the container. Your laptop sees the empty folder the entrypoint made through the repo mount; an extra listing shows it, owned by root.

## 21:19 — Files named by their fingerprint
Inside the container, run dvc init. On Linux it may stop: the repository path is not owned by the current user. You are root inside, the repo is yours on disk, so git refuses, leaving a half-made folder.
The fix is an extra, for Linux: on your laptop, remove the half-made files. Then mark slash app as a safe directory in your git config. Start the container again, and dvc init works. Pause and run it.
If you cloned main, it stops here: DVC is already set up, the remote is refused, and the config points at the class bucket. Start from the starter.
Then point DVC at the DVC store folder in your bucket, as its default remote. Pause and add it.
Here is what dvc add will do with photos. It fingerprints each photo with MD5. It files a copy in its cache under that fingerprint, on a shelf named by the first 2 characters. Then it fingerprints a manifest, the list of fingerprints and names, and writes that fingerprint into the pointer file, which stands in for the folder in git.
A second trap: the mount failed, so the folder is empty, and dvc add happily makes a version with zero files.
With no bucket mounted, our stand-in copies four photos into the laptop folder, which the container sees through the repo mount, and we add again. Now the pointer file says 4 files and one fingerprint for the folder. Pause and add yours.
The cache shows those shelves, plus the empty version from before.
So one line pins 600 kilobytes: it fingerprints the list of fingerprints. And the instructor's tag in the class repo holds the same fingerprint, character for character.
Something to ponder. You give Image 2 the new name brie 2, and add again. Which changes: the photo fingerprint, the manifest fingerprint, the size, or the file count?
Only the manifest fingerprint, because one name in the list changed. The opening's two folders were the reverse: same names, new bytes. And DVC stores whole files, not differences; one changed pixel means a new fingerprint and a new copy.

## 24:01 — A pointer in git, the bytes in a bucket
Next, dvc push. Pause and run it. Here it fails without credentials. To show what a push uploads, an extra push goes to a local stand-in remote: 5 files pushed, the four photos and the manifest.
In your bucket, the DVC store now mirrors the cache. A gold tag: a second copy of the photos, still a fraction of a cent a month. So the bytes now sit in three places: the images folder you upload to, and the cache on your disk, filled by dvc add. The third is the DVC store, where every file is named by its fingerprint. The images folder can change; the DVC store never overwrites, because new bytes get a new name.
Now git, outside the container. Here, git status shows the DVC files that dvc init already staged, the new pointer file, and your two edits. Add and commit: 6 small text files and no photos, because the git ignore file excludes the dataset folder.
Tag the commit as dataset v20, a permanent name, and push the branch and the tag together; atomic means both arrive, or neither. Pause and run them. An extra log shows the tag, which pins these six lines.
An extra diff against the instructor's tag: identical, same bytes, same fingerprint, on any machine. That is the whole trick: git keeps the fingerprint of a list of fingerprints. A rope leads from the tag to the bytes in your bucket.
The README warns that this tag may be taken; that applies only to a fork, and your fresh repo has no tags. Its table sums it up: git holds code and small DVC files, DVC tracks the dataset, the bucket stores the versions.

## 25:54 — One more photo: what moves?
Now a second version. Upload a few more photos to the images folder; our stand-in copies in one, Image 5. With a real bucket, the mount can take a little while to notice, so list before you add. Pause and upload one or two.
Something to ponder. Four photos are already in the DVC store, and you add one. How many objects will dvc push upload?
Two: the new photo and a new manifest. Start the container again, list the folder, and add it; pause and run them. It gives 5 files and a new manifest fingerprint. The class version 21 has a different one, because its fifth photo was another image.
Then dvc push; pause and run it. Here the local stand-in shows 2 files pushed, because the four old photos are already on the shelf. That is the saved space the lecture promised.
Back on your laptop, the five git commands again: status shows only the pointer file changed; then add, commit, tag dataset v21, and push. Pause and run them. An extra diff shows the whole change in three lines.
The starter branch keeps an older README that adds the remote again at this point. That fails: remote origin already exists. The pinned README says not to.
One extra experiment, on our stand-in folder: check out the old pointer file with git, run dvc checkout, and the folder holds four photos again. Back to main, and five, from the cache on disk. With a real mount, this folder is your bucket's images folder, so checkout deletes and rewrites photos there.

## 27:59 — Time travel from anywhere
Now, time travel from anywhere: the lecture's phrase for reaching an earlier version, which works only while its files are kept. The command dvc get, with a tag, walks the rope. It clones the repo at that tag, reads that commit's config to find the bucket, then fetches the manifest, then the photos.
Open the notebook from the README and save a copy. Install DVC, load the libraries, and sign in with your Google account. Then list a repo, fetch a version, and count the files.
Our stand-in is not signed in, and pip gives it a newer DVC, 3.67.1, at the time of recording. Listing the class repo fails with a 401, and look where: at the manifest, because DVC fetches the list first, in the rope's order.
The instructor's signed-in run lists five files on the class repo, the same set as its version 21, and counts 5. Your account probably cannot access the class bucket, so use your repo: replace the address and the tag; your version 20 gives 4. Your repo is private, so put an access token in the address, or make it public. Pause and work through it.
Something to ponder. Cell 19 asks quietly for dataset v25, and prints nothing. Did it work?
No. The next cell fails: no such folder. Without the quiet flag, the error appears: unknown Git revision. The class repo only has tags v20, v21 and v30. The stored count of 3 is left over from an older run; the quiet flag hides errors too.

## 29:53 — Monitoring, teardown and recap
A quick prediction: three questions, three tools. Match Delta Lake or Iceberg, DVC, and lakeFS.
DVC, lakeFS, then the table formats. There is no single standard; your project milestone accepts a light tool like this.
The lecture ends with monitoring: watch quality, freshness, drift, cost and broken steps. Versioning tells you what changed; monitoring tells you that something changed.
On one map: Label Studio runs in a container and signs tickets for the photos. A rule on the bucket satisfies the browser's bouncer. Labels are small notes; a mounted bucket feeds DVC. Photos are filed by fingerprint; a tag pins the list. So Monday's photos come back with one dvc get; their labels join in exercise E7.
5 questions to test yourself. One: who fetches the photos, and why does the bucket need its CORS rule? Two: why can't the command line container and your browser swap addresses? Three: what is in the pointer file, and what changes on a rename? Four: where do the bytes sit after a push? Five: without the DVC store, what does dvc get do?
Cleanup is the README's three commands; pause and run them. If you keep the labeling bucket, remove its CORS rule with dash r. Buckets cost money until you delete them, but never delete the DVC store while any tag should still work; a tag is only a pointer. Delete the key and its JSON file when the course is done.
Answers are in the exercises. Lecture 13 trains from a prepared zip; a tagged version would make that run reproducible.
