# L11 · Data Labeling, Versioning and Monitoring — tutorial digest

- **Ed lesson:** https://edstem.org/us/courses/97373/lessons/166036/
- **Course map:** `tutorials_demo.md:148-158` lists two GCP tutorials for this lecture: "Label Studio" (`dlops-io/data-labeling`) and "Data Versioning" (`dlops-io/data-versioning`). It also links an AWS variant (`dlops-io/data-labeling-aws`), which this digest does not cover.
- **Repos and exact versions used:**

  | Repo | Branch | Commit (full hash) | Commit date | Role |
  |---|---|---|---|---|
  | `dlops-io/data-labeling` | `main` (default) | `03c3e277abeee2cdaf4c1a8149c11c9fd259577d` | 2025-10-20 07:04:39 -0400 ("removed pipfile") | Part A, run as is |
  | `dlops-io/data-versioning` | `main` (default) | `b240b1a03e0abd1964b689ea68e35f0990a33ebc` | 2026-09-19 13:18:57 -0400 ("Removing redundant bits from the repo") | Part B **instructions** (README rewritten 2026-09-18/19) and an instructor's **finished state** (`.dvc/`, `cheese_dataset.dvc`; these DVC files were last changed in `8a1d9b0`, 2024-09-18, and are identical to tag `dataset_v30`) |
  | `dlops-io/data-versioning` | `data-versioning-ac215` | `23762e49ae890af40757c93356fae6cf2e526db2` | 2025-10-20 07:23:09 -0400 ("Merge pull request #3 from dlops-io/main") | Part B **starter code** that the main README tells you to clone |

  Not used: the `pipenv` branches of both repos (`data-labeling` `origin/pipenv` = `17e75a0`, `data-versioning` `origin/pipenv` = `6f8b73e`), which are the older Pipenv versions. `data-versioning` also has three annotated tags: `dataset_v20` → commit `299bcab` (`cheese_dataset.dvc` with `nfiles: 4`), `dataset_v21` → `6de43d1` (`nfiles: 5`), `dataset_v30` → `8a1d9b0` (`nfiles: 5`, same manifest as v21). `data-labeling` also carries two stray annotated tags, `dataset_final` and `dataset_final2` (both on `f69a53a`, 2024-09-17, a commit with no DVC files); ignore them.
- **Which data-versioning branch the lecture uses:** read the README on **`main`**, and clone the code from **`data-versioning-ac215`**. The main README says so itself (`data-versioning/README.md:78-81`). The ac215 branch is a clean starter. It has no `.dvc/` folder and no `cheese_dataset.dvc`, so `dvc init` and `dvc add` work from scratch. `main` already contains the instructor's DVC metadata, so `dvc init` would refuse to run there (§6). One catch: the ac215 branch still installs the retired apt package `google-cloud-sdk` (`data-versioning@data-versioning-ac215/Dockerfile:36`). `main` fixed this to `google-cloud-cli` (`data-versioning/Dockerfile:36`). In October 2026 the starter's Docker build fails unless you apply that one-line fix (§6, item 1). Line references of the form `data-versioning/<file>:N` are to `main`. The only other code difference you will meet is in `docker-entrypoint.sh`: `main` has an extra `echo $GCS_BUCKET_NAME` at line 7, so in the ac215 copy every later line is one lower (gcloud at 8, gcsfuse at 10, `mount --bind` at 13).
- **README sections covered:**
  - `data-labeling/README.md`: `#prerequisites`, `#ensure-docker-memory`, `#cheese-app-data-labeling`, `#setup-gcp-credentials`, `#create-a-local-secrets-folder`, `#setup-gcp-service-account`, `#attaching-gcp-credentials-to-the-container` (informational: the scripts already set `GOOGLE_APPLICATION_CREDENTIALS`), `#prepare-dataset`, `#download-data`, `#create-gcs-bucket`, `#upload-data-to-bucket`, `#run-label-studio-container`, `#run-docker-shellsh`, `#setup-label-studio`, `#create-annotation-project`, `#configure-cloud-storage`, `#enable-cross-origin-resource-sharing-cors`, `#annotate-data`, `#view-annotations-in-gcs-bucket`, `#view-annotations-using-cli`, `#extra-using-docker-compose-to-run-both-containers`, `#docker-cleanup`.
  - `data-versioning/README.md` (main): the four walkthroughs linked from its Contents (`data-versioning/README.md:41-44`): `#-prepare-docker-and-create-your-repository`, `#-set-up-gcp-storage-and-credentials`, `#-start-the-dvc-container`, `#-create-and-view-dataset-versions`. Also `#-about-docker-entrypointsh` (inside step 3), `#-create-an-updated-dataset-version-dataset_v21`, `#-what-you-learned` and `#-docker-cleanup`. The README is accidentally duplicated: the whole text appears twice, and the second copy starts at `data-versioning/README.md:425`. Use the first copy (lines 1-425). §10 has details.
- **Colab notebook:** "Tutorial - Data Pipelines, Labeling, Versioning, Cloud Storage", https://colab.research.google.com/drive/1RRQ1SlHq5lKK76R8LoQdi5LjCnND3jTq (linked at `data-versioning/README.md:326` and `:383`). I downloaded a copy to `colab/L11_data_versioning_view.ipynb` (22 cells; cell numbers in this digest are 0-based). It installs `dvc dvc-gs` and runs `dvc list` and `dvc get --rev <tag>` against a GitHub repo. Its stored outputs come from two different runs: cells 7-19 were run by Pavlos Protopapas on 2025-10-28/29 (cell 7 started one minute after the `dataset_v21` tag was created), while cell 20's output (`Number of items: 3`) is left over from a 2024-10-04 run by another user and has no execution count.
- **"Monitoring":** no tutorial covers the monitoring part of the lecture title (§10).

> Framing note: the two repos teach two halves of one data pipeline. The `data-labeling` repo even contains a diagram of it, `pipeline-flow.png`, which no README references. In the code the halves never meet. Label Studio writes to `cheese-app-data-demo/cheeses_labeled/`, while DVC versions a different bucket's `images/` folder. The video should present them as two tools. Exercise 7 asks how you would connect them.

---

## 1. What you build

**Part A (data-labeling).** You run a *labeling station* on your laptop. Label Studio, a Django web app from the prebuilt image `heartexlabs/label-studio:latest`, runs in a container on port 8080. It reads 21 unlabeled cheese photos from a GCS bucket folder (`cheeses_unlabeled/`) and creates one labeling task per photo. When you click a label (`brie`, `gouda`, `gruyere`, `parmigiano`), it writes one JSON annotation object back to the same bucket under `cheeses_labeled/`. Your browser loads the photos *directly from Google Cloud Storage* through short-lived signed URLs. That is why you must give the bucket a CORS policy. A second container, built from the repo's `Dockerfile` (Python 3.12 + uv), runs `cli.py`. This tool sets that CORS policy and reads projects and annotations through the Label Studio REST API.

**Part B (data-versioning).** You run a *versioning station*. A privileged container (Python 3.11 + uv + DVC + `gcsfuse` + `gcloud`) mounts your bucket as a folder and bind-mounts the bucket's `images/` folder at `/app/cheese_dataset`. `dvc add` fingerprints every image (md5) and copies it into a local cache. `dvc push` uploads the fingerprinted copies to `gs://<bucket>/dvc_store/`. Back on the host, git commits the six-line pointer file `cheese_dataset.dvc` and tags the commit `dataset_v20`. You add images, then repeat to get `dataset_v21`. Finally, a Colab notebook runs `dvc get <repo> cheese_dataset --rev <tag>` to rebuild any tagged version from GitHub and GCS.

```text
PART A — data-labeling  (everything runs on your laptop except the bucket)

 YOUR LAPTOP ─────────────────────────────────────────────────────────────────────────────┐
 │                                                                                        │
 │  Browser  ── http://localhost:8080 ──┐   published port  -p 8080:8080                  │
 │    │                                  ▼                                                │
 │    │       ┌──────────────────────────────────────────────────────────┐                │
 │    │       │ container  data-label-studio                             │                │
 │    │       │ image      heartexlabs/label-studio:latest (amd64+arm64) │                │
 │    │       │ Django app + SQLite                                      │                │
 │    │       │ -v ./docker-volumes/label-studio:/label-studio/data      │                │
 │    │       │ -v ../secrets:/secrets                                   │                │
 │    │       │ GOOGLE_APPLICATION_CREDENTIALS=                          │                │
 │    │       │       /secrets/data-service-account.json                 │                │
 │    │       └───────────▲─────────────────────────────┬────────────────┘                │
 │    │                   │ http://data-label-studio:8080 (Docker DNS)                    │
 │    │      docker network "data-labeling-network"     │                                 │
 │    │       ┌───────────┴─────────────────┐           │                                 │
 │    │       │ container  data-label-cli   │           │                                 │
 │    │       │ image built from Dockerfile │           │                                 │
 │    │       │ /app ◄── ../data-labeling   │           │                                 │
 │    │       │ python cli.py -c|-m|-p|-t   │           │                                 │
 │    │       └───────────┬─────────────────┘           │                                 │
 └────┼───────────────────┼─────────────────────────────┼──────────────────────────────────┘
      │ (3) GET image via │ (4) bucket.patch(): set     │ (1) list objects, sign URLs
      │  signed URL; needs│     CORS policy (cli.py -c) │ (2) write 1 JSON per annotation
      │  CORS headers     ▼                             ▼
      └────────►  GCS bucket  cheese-app-data-demo   (rename: bucket names are global)
                    cheeses_unlabeled/Image_1.jpg … Image_53.jpg   ← "Source storage"
                    cheeses_labeled/<annotation-id>                ← "Target storage"


PART B — data-versioning

 YOUR LAPTOP ───────────────────────────────────────────────────────────────────────────
 │  data-versioning/              (your own private GitHub repo; git runs HERE, on host)
 │   ├─ .git/                     tags: dataset_v20, dataset_v21
 │   ├─ .dvc/config               remote "cheese_dataset" = gs://BUCKET/dvc_store
 │   ├─ .dvc/cache/files/md5/…    local copies of every image (git-ignored)
 │   ├─ cheese_dataset.dvc        pointer: md5 of the version's ".dir" manifest
 │   └─ cheese_dataset/           EMPTY when viewed from the host
 │          │  -v "$BASE_DIR":/app
 │  ┌───────▼───────────────────────────────────────────────────────────┐
 │  │ container data-version-cli  (--privileged --cap-add SYS_ADMIN     │
 │  │                              --device /dev/fuse, runs as root)    │
 │  │  /mnt/gcs_data          ══ gcsfuse ══►  gs://BUCKET (whole bucket)│
 │  │  /app/cheese_dataset    ══ mount --bind ══► /mnt/gcs_data/images  │
 │  │  dvc init │ dvc remote add │ dvc add │ dvc push                   │
 │  └───────┬──────────────────────────────────────┬────────────────────┘
 └──────────┼──────────────────────────────────────┼────────────────────────────────────
            │ reads image bytes (FUSE)             │ uploads blobs (gcsfs, ADC)
            ▼                                      ▼
   GCS bucket  cheese-app-data-versioning  (rename)
     images/Image_1.jpg …                      mutable "workspace" you upload to
     dvc_store/files/md5/5b/53853e667c…        immutable, named by content md5
     dvc_store/files/md5/89/db50de27ac….dir    manifest = one dataset version

   host:  git add . && git commit && git tag -a dataset_v20 && git push --atomic …  ─► GitHub
   Colab: dvc get https://github.com/<you>/data-versioning cheese_dataset --rev dataset_v20
          (reads cheese_dataset.dvc from GitHub at that tag, then fetches blobs from dvc_store)
```

---

## 2. Prerequisites and costs

**Accounts**
- A GCP project with billing enabled, and permission to create service accounts and keys. Some organization-managed projects (for example university ones) block key creation by policy (§6).
- A GitHub account, ideally with an SSH key. The data-versioning README uses `git@github.com:` URLs (`data-versioning/README.md:81`, `:115`, `:122`) and asks for SSH access "if you use the SSH commands below" (`:31`); it also says HTTPS cloning works (`:84`).
- A Google account for Colab that can read your bucket. If you own the project, it can.

**Local installs**
- Docker Desktop. Give it more than 4 GB of memory (`data-labeling/README.md:18` says "> 4GB"; the menu is now *Settings → Resources*).
- git and a browser. You do not need Python on the host, because every Python and DVC command runs inside a container.

**GCP APIs.** Only Cloud Storage, which is on by default in new projects. The console enables IAM as needed when you create the service account. No Vertex AI or Compute is used.

**Service account and key: where the code expects it**

| What | Value | Evidence |
|---|---|---|
| SA name | `data-service-account`, role *Cloud Storage → Storage Admin* | `data-labeling/README.md:45-46`, `data-versioning/README.md:150-160` |
| Key file on host | `../secrets/data-service-account.json`, i.e. a `secrets/` folder **next to** each repo folder | `data-labeling/docker-shell.sh:17`, `data-labeling/docker-shell-CLI.sh:18`, `data-versioning/docker-shell.sh:6` |
| Path inside containers | `/secrets/data-service-account.json` via env var `GOOGLE_APPLICATION_CREDENTIALS` | `data-labeling/docker-shell.sh:21`, `data-labeling/docker-shell-CLI.sh:20`, `data-versioning/docker-shell.sh:10` |
| Bucket name (Part A, CLI) | `GCS_BUCKET_NAME="cheese-app-data-demo"`: **edit it** | `data-labeling/docker-shell-CLI.sh:23` and, for the compose path, `data-labeling/docker-compose.yml:17` |
| Bucket name (Part B) | `export GCS_BUCKET_NAME="cheese-app-data-versioning"`: **edit it** | `data-versioning/docker-shell.sh:7` |
| Label Studio login | `pavlos@seas.harvard.edu` / `awesome` (env vars) | `data-labeling/docker-shell.sh:19-20`, `data-labeling/docker-compose.yml:31-32` |
| Label Studio API token | passed on the command line as `-k <TOKEN>` | `data-labeling/cli.py:161` |

Both repos use the **same key file name**. If you clone both into one parent folder, one `secrets/` folder serves both:

```text
~/Desktop/AC215/
├── secrets/data-service-account.json     ← never inside a git repo
├── data-labeling/                        ← git clone https://github.com/dlops-io/data-labeling
└── data-versioning/                      ← your own repo, started from the ac215 branch
```

If `AC215/` itself is a git repository (for example the planned `MLOps_Learning` repo), add `secrets/` to *that* repo's `.gitignore` before your first commit.

`GCP_PROJECT` and `GCP_ZONE` are set in every script (`data-labeling/docker-shell.sh:22-23`, `data-versioning/docker-shell.sh:8-9`), but no code reads them. `cli.py` reads only `GCS_BUCKET_NAME` and `LABEL_STUDIO_URL` (`data-labeling/cli.py:12-13`). The Google client libraries take the project from the key file. Editing them does no harm, but it does not matter either.

**Billable resources and shutdown**
- **GCS storage:** about 3.8 MB for the 21 images (3,767,117 bytes uncompressed; `cheeses_unlabeled.zip` is 3,720,496 bytes) in the Part A bucket. Part B stores the handful of images in `images/` (about 0.6-0.8 MB for 4-5 photos) plus a second copy in `dvc_store/`. That is a fraction of a cent per month. Operation counts (list/get/put from Label Studio, gcsfuse and DVC) and browser egress are also tiny.
- **Label Studio, DVC, the containers:** run locally, free.
- **Shutdown:**
  - Stop the containers: `docker stop data-label-studio` then `docker rm data-label-studio`. The other containers use `--rm`. If you used compose, run `docker-compose down` or stop `data-label-studio` the same way.
  - Remove the network: `docker network rm data-labeling-network`.
  - Optionally remove CORS: `python cli.py -r` (`data-labeling/cli.py:143-148`).
  - Delete the service-account key when the course no longer needs it (*IAM → Service accounts → Keys*).
  - **Only delete the buckets if you no longer need the dataset versions.** Deleting `dvc_store/` turns every `dataset_v*` tag in GitHub into a pointer to nothing (§3.6).

---

## 3. Concepts this tutorial teaches

★ = deserves an animated explanation (five concepts are marked).

### 3.1 A labeling tool is a database of *tasks* and *annotations*

- **Explanation:** a Label Studio *project* has a *labeling config*, an XML template. The "Computer Vision → Image Classification" template you pick (`data-labeling/README.md:113`) shows one image and a set of choices. Each image in the bucket becomes a *task*. Each click-and-submit creates an *annotation*: a JSON record whose `result` holds the chosen label, who chose it, when, and how long it took (`lead_time`). The sample output at `data-labeling/README.md:204` shows the shape: `'from_name': 'choice', 'to_name': 'image'`, `'value': {'choices': [...]}`.
- **Mental model:** images stay where they are. The labels are a *separate table* keyed by task, and a labeled dataset is the *join* of images and annotations.
- **Analogy:** a stack of exam papers (tasks), a rubric (labeling config), and a gradebook (annotations). The grader never rewrites the exam papers.
- **Misconception:** "after labeling, my images are sorted into `brie/`, `gouda/` … folders." They are not. Label Studio writes JSON objects into `cheeses_labeled/`, one per annotation. Getting class folders, or `cheese_4_labels.zip` as used in L13, takes an extra export step that no tutorial code here performs.

### 3.2 ★ Source storage, target storage and signed URLs: who touches the bytes

- **Explanation:** *Source storage* (`cheeses_unlabeled` prefix) tells Label Studio where tasks come from. *Sync Storage* lists the bucket and creates one task per object. *Target storage* (`cheeses_labeled` prefix) tells it where to write annotations. Label Studio's server has the service-account key (`GOOGLE_APPLICATION_CREDENTIALS`), but your browser does not. With **"Use pre-signed URLs"** enabled (`data-labeling/README.md:131`), the server signs a URL for each image with the key. Anyone holding that URL can GET that one object until it expires. The browser then downloads the image **directly from `storage.googleapis.com`**, not through Label Studio.
- **Mental model:** Label Studio is a ticket office. It never carries the cheese photos. It hands your browser a dated, signed ticket, and the browser takes the ticket to Google's door.
- **Analogy:** a museum gives you a timed-entry ticket. The guard at the door checks the stamp, not your identity.
- **Misconception:** "Label Studio uploads or copies my images." It only lists them, signs URLs and writes annotation JSON. The service account needs read access for source storage and write access for target storage. Storage Admin covers both, and more.
- **Animation:** three actors (Browser, Label Studio box, GCS vault). (1) Label Studio draws a line to the vault and lists 21 object names, which turn into 21 task cards. (2) The browser asks for card 1. Label Studio stamps a URL with a wax seal (the signature) and an hourglass (the expiry) and slides it to the browser. (3) The browser walks to the vault with the sealed URL. The vault checks the seal and returns the image. (4) When you click "gouda", a JSON envelope flies from Label Studio into the vault's `cheeses_labeled/` drawer.

### 3.3 ★ CORS: the browser's bouncer, configured on the bucket

- **Explanation:** the Label Studio page is served from the origin `http://localhost:8080`, and the image lives on a different origin, `https://storage.googleapis.com`. When page JavaScript fetches a cross-origin resource in CORS mode, the **browser** only hands the response to the page if it carries `Access-Control-Allow-Origin` matching the page's origin. GCS adds that header only if the bucket has a matching CORS rule. `python cli.py -c` installs one rule: any origin `*`, method `GET`, max age 3600 s (`data-labeling/cli.py:26-34`).
- **Mental model:** CORS is a *browser-side* filter keyed on *which website is asking*. It is not authentication. The signed URL already proved the request is allowed. CORS decides whether the page is allowed to *read* the answer.
- **Analogy:** a bouncer at your door (the browser) only lets in packages carrying a note from the sender saying "I agree to be delivered to localhost:8080".
- **Misconceptions:**
  - "CORS makes my bucket public." It does not. Without a signed URL or credentials, GCS still returns 401/403.
  - The README's explanation (`data-labeling/README.md:153`, "GCP buckets restrict access from domains that can't be resolved via reverse DNS lookup") is not how CORS works. The restriction is the browser's same-origin policy, and the fix is a response header.
  - "curl works, so CORS is fine." curl ignores CORS.
  - "`maxAgeSeconds` is how long the browser caches the image permission." It becomes `Access-Control-Max-Age`, which only controls how long a browser caches a *preflight* (`OPTIONS`) answer. A plain `GET` with no custom headers is a "simple" request and needs no preflight. If thumbnails stay broken right after `cli.py -c`, the usual cause is the browser's cache of earlier responses that lacked the header, so do a hard refresh.
  - The README says it "must be done programmatically" (`:157`). The *console* has no CORS editor, but `gcloud storage buckets update gs://BUCKET --cors-file=cors.json` also works.
- **Animation:** two origin "islands", `localhost:8080` and `storage.googleapis.com`. A response package travels from the GCS island to the browser. The bouncer inspects it for a label and rejects it (red X, console error), and the image tile in Label Studio stays broken. Then `cli.py -c` sticks a rule card onto the bucket, the next package carries the `Access-Control-Allow-Origin: *` label, the bouncer waves it through, and the tile fills with a cheese photo.
- This repeats L10's lesson (the browser calls the API across origins), now with a bucket as the server.

### 3.4 One server, two addresses (Docker networking recap)

- **Explanation:** the browser reaches Label Studio at `http://localhost:8080` through the published port (`data-labeling/docker-shell.sh:15`). The CLI container reaches it at `http://data-label-studio:8080` (`data-labeling/docker-shell-CLI.sh:24`). That address works because both containers are on the user-defined network `data-labeling-network` (`data-labeling/docker-shell.sh:6,14`; `data-labeling/docker-shell-CLI.sh:17`), whose built-in DNS resolves container names.
- **Mental model:** `localhost` means "this machine". Inside a container, "this machine" is the container itself.
- **Misconception:** setting `LABEL_STUDIO_URL=http://localhost:8080` inside the CLI container. That points at the CLI container itself, where nothing listens on 8080, so you get "connection refused".

### 3.5 ★ Content addressing: files named by their fingerprint

- **Explanation:** `dvc add cheese_dataset` computes the md5 of every file's bytes. It stores each file in the cache under a path built from that md5: `.dvc/cache/files/md5/<first 2 hex>/<remaining 30 hex>` (DVC 3 layout; `CacheManager.FILES_DIR = "files"` in DVC 3.63). It then writes a *manifest*, a sorted JSON list of `{"md5": …, "relpath": …}`, and hashes the manifest too. The manifest is stored with a `.dir` suffix, and *its* md5 is the identity of the whole folder version. `dvc push` copies the same layout to `gs://BUCKET/dvc_store/files/md5/…`, skipping objects already there.
- **Real numbers (reproduced while preparing this digest):** the upstream tag `dataset_v20` has `md5: 89db50de27acfd6822faabc3da39b0a8.dir`, `size: 611101`, `nfiles: 4` (`git show dataset_v20:cheese_dataset.dvc`). Hashing `Image_1.jpg`…`Image_4.jpg` from `cheeses_unlabeled.zip` with DVC's manifest rule gives exactly `89db50de27acfd6822faabc3da39b0a8.dir`, 611,101 bytes, 4 files. So the instructor's v20 dataset is those four photos. `Image_1.jpg` has md5 `5b53853e667c8a76121fdc475996c895` and is stored at `dvc_store/files/md5/5b/53853e667c8a76121fdc475996c895`. The v21 manifest `3280f8f9629451704dca3f792534e1f5.dir` (785,481 bytes, 5 files) adds one 174,380-byte image that is not in the zip. The notebook's stored `dvc list -R` output (Colab cell 13) names it: `cheese_dataset/csm_Gruyere_Website_Header_Desktop_1920x1080px_Homepage_Curling_cdd2c6527c.jpg.webp`. Cell 15's progress bar shows a 170k file, and 174,380 B ≈ 170.3 KiB.
- **Mental model:** a library where every book is shelved by a fingerprint of its text, plus a catalog card listing the fingerprints of one collection. A *version* is a catalog card.
- **Analogy:** a recipe card that says "the four photos whose fingerprints are 5b53…, ba04…, 91f4…, 5b85…" instead of carrying the photos.
- **Misconceptions:**
  - "DVC stores diffs." It stores whole files and deduplicates per file. Change one pixel and the whole image is stored again under a new md5.
  - "Renaming a file creates a new blob." It does not. The blob is unchanged, and only the manifest (relpath) changes.
- **Animation:** four photos drop into a "hash machine". Each comes out as a 32-character label and slides onto a shelf whose aisle is the first two characters (`5b/`, `ba/`, `91/`, `5b/`). A manifest card gathers the four labels, is itself hashed into `89db50…`, and shrinks into the six-line `cheese_dataset.dvc`. For v21, a fifth photo is hashed. The old four labels light up as "already on the shelf", and only the new photo and a new manifest card fly to the cloud shelf. The counter shows "2 objects pushed, not 6".

### 3.6 ★ Pointer in git, bytes in the remote, names in tags

- **Explanation:** git tracks the small text files (`.dvc/config`, `.dvcignore`, `cheese_dataset.dvc`). The dataset folder itself is git-ignored (`data-versioning@data-versioning-ac215/.gitignore:3`). A git **annotated tag** (`git tag -a dataset_v20 -m …`) gives a commit a human name, and `git push --atomic origin main dataset_v20` pushes the branch and the tag together, or neither. To rebuild a version, follow the chain **tag → commit → `cheese_dataset.dvc` → `.dir` manifest → blobs**. `dvc get <repo-url> cheese_dataset --rev <tag>` (Colab cell 15) walks exactly this chain. It clones the git repo at the tag, reads the remote URL from `.dvc/config` at that commit, and downloads the listed blobs.
- **Mental model:** git is the *table of contents*, the bucket is the *warehouse*, and a tag is a *bookmark* in the table of contents.
- **Analogy:** a coat-check ticket. The ticket (`.dvc` file in git) is small and portable, but useless if the coat room (`dvc_store`) burns down or you never handed in the coat (forgot `dvc push`).
- **Misconceptions:**
  - "The tag versions the data." A tag only names a commit, and the data must exist in the remote.
  - "Tags record when the data was made." The upstream `dataset_v21` tag was created 2025-10-28 (tagger timestamp 1761701089) on commit `6de43d1`, which is dated 2025-10-20. You can tag any commit later.
  - "GCS Object Versioning does the same thing." Bucket versioning keeps old generations of *individual objects*. It does not give you a named, consistent snapshot of *a set* of files tied to a code commit.
- **Animation:** a horizontal git timeline with commits as beads. A flag labelled `dataset_v20` plants on one bead. Zoom into the bead: a `.dvc` card with `89db50….dir`. A dotted rope runs from the card down into the cloud warehouse to the manifest box, which fans out to four photo blobs. Then a second flag `dataset_v21` plants on a later bead with its own rope. Its manifest fans out to *five* blobs, four of them the same as v20's. Finally, `dvc get --rev dataset_v20` pulls the first rope and four photos materialize in Colab.

### 3.7 ★ A bucket that looks like a folder (gcsfuse + bind mount)

- **Explanation:** at container start, `docker-entrypoint.sh` runs `gcsfuse … $GCS_BUCKET_NAME /mnt/gcs_data` (`data-versioning/docker-entrypoint.sh:11`). FUSE turns file-system calls (`ls`, `open`, `read`) into GCS API calls. It then runs `mount --bind /mnt/gcs_data/images /app/cheese_dataset` (`:14`) so the bucket's `images/` folder appears at the path DVC tracks. FUSE needs the `/dev/fuse` device and mount privileges, hence `--privileged --cap-add SYS_ADMIN --device /dev/fuse` (`data-versioning/docker-shell.sh:18-20`) and running as root (`data-versioning/Dockerfile:52`).
- **Mental model:** two views of one folder. Inside the container, `/app/cheese_dataset` shows the bucket's images. On the host, `data-versioning/cheese_dataset/` is an **empty directory**. The FUSE and bind mounts exist only in the container's mount namespace. `mkdir -p /app/cheese_dataset` (`:13`) created the empty host folder through the `/app` bind mount.
- **Analogy:** a TV in the container showing a live feed of the bucket. The host sees the TV switched off.
- **Misconceptions:**
  - "The images are on my laptop now." gcsfuse streams them on demand. The only local copies appear in `.dvc/cache/` after `dvc add`, which reads every file through FUSE and copies it into the cache on your disk.
  - "Object storage folders are real folders." GCS is flat. The console's "Create folder" writes a placeholder object `images/`, and gcsfuse without `--implicit-dirs` only shows folders that have such placeholders (§6, item 2).
- **Animation:** a cloud bucket on the right and the container box on the left. A pipe labelled `gcsfuse` connects them to `/mnt/gcs_data`, and a second short pipe labelled `mount --bind` connects `/mnt/gcs_data/images` to `/app/cheese_dataset`. Camera pulls back to show the host laptop around the container. The `/app` folder is shared through a window (bind mount), but the `cheese_dataset` sub-folder seen from the host side is dark and empty.

### 3.8 One key, many consumers (ADC)

- **Explanation:** the same JSON key file is read by five different programs:
  - `google-cloud-storage` in `cli.py`, through `storage.Client()` and Application Default Credentials (`data-labeling/cli.py:23`).
  - Label Studio's GCS storage, when the credentials field is left blank (`data-labeling/README.md:132`).
  - `gcloud`, through `activate-service-account` (`data-versioning/docker-entrypoint.sh:9`).
  - `gcsfuse`, through `--key-file` (`:11`).
  - DVC's `dvc-gs` → `gcsfs`, through ADC, because `credentialpath` is unset.
  - Colab is the exception: it uses *your user identity* via `auth.authenticate_user()` (cell 11).
- **Misconception:** "`GCP_PROJECT` tells the libraries which project to use." No code reads it (§2).

---

## 4. Step-by-step walkthrough

Commands in `bash` blocks are copied exactly from the READMEs or scripts. The only exception is `<YOUR_TOKEN>` in A13, a placeholder I added where the README says "followed by your Access Token". Commands in `text` blocks are copied exactly from the Colab notebook cells. Run every step from the folder named in the step.

### Part A — Label Studio (`data-labeling`, branch `main`)

**A1. Lay out folders and give Docker memory**
- Action: clone `https://github.com/dlops-io/data-labeling` next to a `secrets/` folder (`data-labeling/README.md:33-40`). Set Docker memory to more than 4 GB (`:18`).
- Under the hood: every script mounts `$(pwd)/../secrets` (`data-labeling/docker-shell.sh:17`), and the CLI script also mounts `$(pwd)/../data-labeling` as `/app` (`data-labeling/docker-shell-CLI.sh:19`). So the folder must literally be named `data-labeling` (§6, item 9).
- Checkpoint: `ls ..` from inside the repo prints `data-labeling  secrets`.

**A2. Create the service account and key**
- Action: create `data-service-account` with *Storage Admin*, add a JSON key, and save it as `secrets/data-service-account.json` (`data-labeling/README.md:44-50`).
- Under the hood: this key becomes the identity of Label Studio (bucket listing, URL signing, annotation writes) and of `cli.py` (CORS patch).
- Checkpoint: `ls ../secrets` shows `data-service-account.json`. The file contains `"type": "service_account"` and a `"private_key"`.
- If it fails: if the console says key creation is disabled by an organization policy, see §6, item 20.

**A3. Download and extract the unlabeled images**
- Action: download `https://github.com/dlops-io/datasets/releases/download/v4.0/cheeses_unlabeled.zip` and extract it (`data-labeling/README.md:64-65`).
- Checkpoint: `cheeses_unlabeled/` holds **21** images (`Image_1.jpg` … `Image_10.jpg`, `Image_19.jpg` … `Image_23.jpg`, `Image_49.jpg` … `Image_53.jpg`, plus `Image_3.png`). The zip also holds 21 macOS resource-fork files under `__MACOSX/cheeses_unlabeled/` (20 `._Image_*.jpg` plus `._Image_3.png`, 194 bytes each). Do not upload those.

**A4. Create the bucket and two folders**
- Action: create a bucket (your own globally unique name; the README's example is `cheese-app-data-demo`) with folders `cheeses_unlabeled` and `cheeses_labeled` (`data-labeling/README.md:69-72`).
- Checkpoint: both folders appear in the bucket browser.

**A5. Upload the images**
- Action: upload the 21 image files into `cheeses_unlabeled/` (`data-labeling/README.md:76`).
- Checkpoint: the bucket browser lists 21 objects under `cheeses_unlabeled/`.

**A6. Start Label Studio**
```bash
sh docker-shell.sh
```
- Under the hood (`data-labeling/docker-shell.sh:6-24`):
  1. Creates the network `data-labeling-network` if missing.
  2. Force-removes any old `data-label-studio` container.
  3. Runs `heartexlabs/label-studio:latest` **detached** (`-d`) with port 8080, persistent data at `./docker-volumes/label-studio` (git-ignored, `data-labeling/.gitignore:3`), the secrets mount, and env vars that pre-create the admin user and disable open sign-up.
- Checkpoint: `docker container ls` shows a line like `heartexlabs/label-studio:latest … 0.0.0.0:8080->8080/tcp … data-label-studio` (`data-labeling/README.md:93-97`). First start runs database migrations. Watch with `docker logs -f data-label-studio` until it reports it is serving on port 8080.
- If it fails:
  - "port is already allocated": another app or course container already uses 8080 (§6, item 5).
  - On a Linux host, permission errors on `/label-studio/data`: §6, item 12.

**A7. Log in and create the project**
- Action: open `http://localhost:8080/` and log in with `pavlos@seas.harvard.edu` / `awesome` (`data-labeling/README.md:108-109`).
  1. *Create Project* and give it a name.
  2. Skip *Data Import*.
  3. In *Labeling Setup*, choose *Computer Vision → Image Classification*.
  4. Replace the choices with `brie`, `gouda`, `gruyere`, `parmigiano`.
  5. Save (`:110-115`).
- Checkpoint: an empty project page saying there are no tasks yet.

**A8. Add Source Storage (read images)**
- Action: *Settings → Cloud Storage → Add Source Storage*, then fill in (`data-labeling/README.md:121-136`):
  - Storage Type: `Google Cloud Storage`
  - Storage Title: `Cheese Images`
  - Bucket Name: your bucket
  - Bucket Prefix: `cheeses_unlabeled`
  - Import Method: `Files - Automatically creates a task for each storage object (e.g. JPG, MP3, TXT)`
  - Enable "Treat every bucket object as a source file" (this option may no longer appear next to the newer Import Method field; see §10, open questions)
  - Enable "Use pre-signed URLs"
  - Leave the credentials and project ID fields empty

  Then *Check Connection*, *Add Storage*, *Sync Storage*.
- Under the hood: the Label Studio server uses the key from `GOOGLE_APPLICATION_CREDENTIALS` to list objects under the prefix and creates one task per object.
- Checkpoint: the project shows **21 tasks**.
- If it fails:
  - "Check Connection" fails: wrong bucket name, a missing key file, or IAM. Run `docker exec data-label-studio ls /secrets` to confirm the key is visible.
  - A field from the README is missing in your UI: `heartexlabs/label-studio:latest` is a moving tag (last pushed 2026-09-29), and the README was last updated for the Oct 2025 UI (§10).

**A9. Add Target Storage (write annotations)**
- Action: *Add Target Storage* with Storage Type `Google Cloud Storage`, Storage Title `Cheese Images`, your bucket name, bucket prefix `cheeses_labeled`, and the credentials and project ID fields empty. *Check Connection*, then *Add Target Storage* (`data-labeling/README.md:138-147`).
- Checkpoint: the target storage card appears under Cloud Storage.

**A10. Fix CORS from the CLI container**

Edit the bucket name first, at `data-labeling/docker-shell-CLI.sh:23` (`-e GCS_BUCKET_NAME="cheese-app-data-demo" \`). Then, from the `data-labeling` folder:
```bash
sh docker-shell-CLI.sh
```
The README says "Run `docker-shell-CLI.sh`" (`data-labeling/README.md:165`); `sh docker-shell-CLI.sh` is the same thing. Inside the container:
```bash
python cli.py -c
python cli.py -m
```
- Under the hood:
  1. `data-labeling/docker-shell-CLI.sh:7` builds image `data-label-cli`: Python 3.12 slim, `uv sync --frozen` into `/.venv` (`data-labeling/Dockerfile:2,18,45`), non-root user `app`.
  2. `:15-25` runs it interactively on the same network, with the repo mounted at `/app`.
  3. The entrypoint activates `/.venv` and opens bash (`data-labeling/docker-entrypoint.sh:12,15`).
  4. `cli.py -c` calls `bucket.patch()` with the CORS rule (`data-labeling/cli.py:22-34`).
  5. `-m` prints bucket metadata, including the `Cors:` line (`:44-72`).
- Checkpoint: `-c` prints `set_cors_configuration()` and then `Set CORS policies for bucket <your-bucket> is [...]` with `'origin': ['*']`, `'method': ['GET']` and `'maxAgeSeconds': 3600` (format from `data-labeling/cli.py:40`). `-m` prints `Cors: [...]` with the same rule. Back in Label Studio, refresh: the task thumbnails now show cheese photos.
- If it fails:
  - `docker: Error response from daemon: network data-labeling-network not found`: you skipped A6 or pruned the network (§6, item 7).
  - `403 … does not have storage.buckets.update`: the role is narrower than Storage Admin.
  - `KeyError: 'GCS_BUCKET_NAME'`: you ran `cli.py` on the host instead of in the container.

**A11. Annotate**
- Action: click tasks, pick a label, *Submit* (`data-labeling/README.md:174-177`).
- Checkpoint: the task grid shows them as completed.

**A12. See annotations in the bucket**
- Action: open `cheeses_labeled/` in the bucket browser (`data-labeling/README.md:184-187`).
- Under the hood: on submit, Label Studio writes one object per annotation to the target prefix.
- Checkpoint: one object per submitted annotation. Its JSON includes the task's `image` (a `gs://…/cheeses_unlabeled/Image_…` URI) and the `result` with your choice.
- If it fails: annotations made before you added the target storage are not written retroactively. Click *Sync* on the target storage card.

**A13. Read annotations through the API**
- Action: copy your access token from *User Profile → Account & Settings* (`data-labeling/README.md:193-196`). In the CLI container, run the two commands below with your token as the `-k` value (`:198-199`):
  ```bash
  python cli.py -p -k <YOUR_TOKEN>
  python cli.py -t -k <YOUR_TOKEN>
  ```
- Under the hood: the legacy SDK `Client` (`from label_studio_sdk import Client`, `data-labeling/cli.py:9`) already calls `GET /api/version` in its constructor (`label_studio_sdk/_legacy/client.py:111,122`), then `/health` (`check_connection()`), `/api/projects` and the tasks API. `-t` takes `projects[0]` and filters tasks whose `completed_at` is not empty (`get_labeled_tasks`, `data-labeling/cli.py:94-108`).
- Checkpoint:
  - `-p` prints `get_projects`, the project list, then for each project its id, title and description followed by the project object (`data-labeling/cli.py:82-88`).
  - `-t` prints `Number of tasks: 21`, `Number of labeled tasks: N` and one `Annotations: [...]` line per labeled task (the shape of `data-labeling/README.md:204`).
- If it fails:
  - `401 Client Error: Unauthorized`: you probably copied a JWT *Personal Access Token*. The legacy `Client` always sends `Authorization: Token <key>` (verified in `label_studio_sdk/_legacy/client.py:104`, SDK 2.0.12 as locked in `data-labeling/uv.lock:466-467`). See §6, item 11.
  - `-k argument i required…`: you forgot `-k` (`data-labeling/cli.py:122-123`).

**A14 (Extra). Run both containers with compose**
- Action: stop the containers, then run `docker-shell-compose.sh` (`data-labeling/README.md:218`):
  ```bash
  sh docker-shell-compose.sh
  ```
- Under the hood (`data-labeling/docker-shell-compose.sh:6-12`):
  1. Ensures the network exists.
  2. Builds `data-label-cli`.
  3. Runs `docker-compose run --rm --service-ports data-label-cli`. Because of `depends_on` (`data-labeling/docker-compose.yml:19-20`), compose first starts `data-label-studio`, then gives you a shell in a one-off CLI container. That container is named `data-labeling-data-label-cli-run-…`, which explains the stray line at `data-labeling/README.md:95`.
- Checkpoint: the same Label Studio at `localhost:8080`, with your old projects, because the same `./docker-volumes/label-studio` folder is mounted (`data-labeling/docker-compose.yml:27`).
- If it fails:
  - "container name "/data-label-studio" is already in use": `docker stop` alone leaves the container behind, so also `docker rm data-label-studio` (§6, item 6).
  - `docker-compose: command not found`: use `docker compose run --rm --service-ports data-label-cli` (§6, item 8).

**A15. Clean up**
- `docker container ls`, stop running containers, `docker system prune`, `docker image ls` (`data-labeling/README.md:243-246`).
- Note: `prune` deletes the stopped `data-label-studio` container but **not** `./docker-volumes/`, so your projects survive.

### Part B — DVC (`data-versioning`: README on `main`, code from `data-versioning-ac215`)

**B1. Clean Docker** (`data-versioning/README.md:57-71`)
```bash
docker container ls
docker system prune
docker image ls
```
- Checkpoint: no running containers. Note that `prune` also removes unused networks, such as `data-labeling-network` if Label Studio is stopped.

**B2. Clone the starter and detach it from the class repo** (`data-versioning/README.md:81-101`)
```bash
git clone -b data-versioning-ac215 git@github.com:dlops-io/data-versioning.git
cd data-versioning
rm -rf .git
git init
```
- Under the hood: you keep the files and throw away the history, *including the class tags*. A GitHub *fork* (or a clone that keeps `.git`) can carry the tags `dataset_v20`/`v21`/`v30`, which is the only situation where the README's "this tag is taken" disclaimer (`:321`) applies.
- **Patch before building (my recommendation, not in the README):** change `google-cloud-sdk` to `google-cloud-cli` in `Dockerfile` line 36. Compare `data-versioning@data-versioning-ac215/Dockerfile:36` with `data-versioning/Dockerfile:36`. Reason in §6, item 1.
- Checkpoint: `ls -A` shows `.git .gitignore Dockerfile README.md docker-entrypoint.sh docker-shell.sh pyproject.toml uv.lock`. There is **no `.dvc/` folder**.

**B3. Create your private repo and push** (`data-versioning/README.md:108-126`)
- Action: on GitHub, create a new **private**, **empty** repository named `data-versioning`. Do not add a README, license or `.gitignore`, because these files already exist locally (`:108-110`). Then, in the local folder:
```bash
git branch -M main
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/data-versioning.git
git add .
git commit -m "Initial commit"
git push -u origin main
```
- Under the hood: `git branch -M main` renames the default `master` (if your git uses it) to `main`. The older ac215 README omits it (`data-versioning@data-versioning-ac215/README.md:39-43`), and `git push -u origin main` then fails.
- Checkpoint: GitHub shows the 7 files on `main`.

**B4. Secrets and bucket folders** (`data-versioning/README.md:136-187`)
- Reuse `../secrets/data-service-account.json` from Part A. If you do Part B alone, create a `secrets/` folder next to `data-versioning/` (`:136-144`) and make the key as in `:150-170`: service account `data-service-account`, role *Cloud Storage → Storage Admin*, *Continue* → *Done*, then *⋮ → Manage keys → Add Key → Create new key → JSON*, saved as `secrets/data-service-account.json`. That list starts at "3." because step 1-2 (where to find *IAM & Admin → Service Accounts*) was deleted from this copy (§10, item 1).
- In your bucket, create `dvc_store/` and `images/` (`:174-187`). The README never says to create the bucket itself; it assumes "access to a GCS bucket" (`:29`), and its example name is `cheese-app-data-versioning`. A new bucket or the Part A bucket both work.
- **Then put the first dataset into `images/`.** The README never says this; it only says "Upload a few *additional* images" later (`:338`). To reproduce the instructor's v20 exactly, upload `Image_1.jpg`, `Image_2.jpg`, `Image_3.jpg`, `Image_4.jpg` from Part A's zip (§3.5).
- Checkpoint: the bucket browser shows `images/` with 4 objects and an empty `dvc_store/`.

**B5. Point the container at your bucket** (`data-versioning/README.md:197-205`)
```bash
export GCS_BUCKET_NAME="YOUR_BUCKET_NAME"
export GCP_PROJECT="YOUR_GCP_PROJECT_ID"
export GCP_ZONE="YOUR_GCP_ZONE"
```
- Edit these values in `docker-shell.sh` lines 7-9 (`data-versioning/docker-shell.sh:7-9`). Only the bucket name is actually used (§2).

**B6. Build and enter the DVC container** (`data-versioning/README.md:237-243`)
```bash
cd data-versioning
sh docker-shell.sh
```
- Under the hood:
  1. `data-versioning/docker-shell.sh:14` builds `data-version-cli` (Debian bookworm + Python 3.11; apt installs `gcsfuse` from the `gcsfuse-bionic` repo and `google-cloud-cli`; `uv sync --frozen` installs `dvc` 3.63.0, `dvc-gs` 3.0.2, `gcsfs` 2025.9.0 into `/.venv`).
  2. `:17-27` runs it privileged with `/dev/fuse`, mounting the repo at `/app`, `../secrets` at `/secrets` and `~/.gitconfig` at `/etc/gitconfig`.
  3. The entrypoint (`data-versioning/docker-entrypoint.sh:9-21`) activates the service account for `gcloud`, mounts the bucket at `/mnt/gcs_data`, bind-mounts `images/` onto `/app/cheese_dataset`, activates `/.venv`, and `exec`s bash.
- Checkpoint:
  - The output shows `Container is running!!!`, `Architecture: aarch64` (Apple Silicon) or `x86_64`, `Python version: Python 3.11.x`, `UV version: …`, `Activated service account credentials for: [data-service-account@…]`, gcsfuse start-up log lines, `GCS bucket mounted at /mnt/gcs_data` and `Activating virtual environment...`. The bare bucket-name line appears only with `main`'s entrypoint (`data-versioning/docker-entrypoint.sh:7`). The ac215 starter you cloned does not print it.
  - At the root prompt, `ls cheese_dataset` lists your 4 images, and `which dvc` prints `/.venv/bin/dvc`.
- If it fails:
  - The build stops at `google-cloud-sdk`: §6, item 1.
  - `mount: /app/cheese_dataset: special device /mnt/gcs_data/images does not exist`: §6, item 2.
  - `Unable to read file [/secrets/data-service-account.json]`: §6, item 3.
  - The entrypoint has no `set -e`, so after any of these errors you still get a shell. **Always check `ls cheese_dataset` before `dvc add`.**

**B7. Initialize DVC (inside the container)** (`data-versioning/README.md:269`)
```bash
dvc init
```
- Under the hood: creates `.dvc/config`, `.dvc/.gitignore` (ignores `/config.local`, `/tmp`, `/cache`) and `.dvcignore`, then stages them in git (`dvc/repo/init.py` uses `scm_context(autostage=True)`). It refuses if `/app` is not a git repo, or if `.dvc/` exists.
- Checkpoint: `Initialized DVC repository.` and `You can now commit the changes to git.`, plus a notice that DVC collects anonymous usage analytics (opt out with `dvc config core.analytics false`).
- If it fails:
  - `/app is not tracked by any supported SCM tool (e.g. Git)`: you skipped `git init` in B2.
  - `'.dvc' exists. Use `-f` to force.`: you cloned `main` instead of the ac215 branch.

**B8. Add the GCS remote** (`data-versioning/README.md:279`)
```bash
dvc remote add -d cheese_dataset gs://YOUR_BUCKET_NAME/dvc_store
```
- Under the hood: writes the remote into `.dvc/config` and makes it the default (`-d`). The result looks exactly like `data-versioning/.dvc/config:1-4` with your bucket name.
- Checkpoint: `Setting 'cheese_dataset' as a default remote.`, then `cat .dvc/config` shows `remote = cheese_dataset` and `url = gs://…/dvc_store`.

**B9. Track the dataset** (`data-versioning/README.md:293`)
```bash
dvc add cheese_dataset
```
- Under the hood:
  1. Reads every file through FUSE and md5-hashes it.
  2. Copies each into `.dvc/cache/files/md5/xx/…` on your host disk, through the `/app` bind mount.
  3. Builds and hashes the `.dir` manifest.
  4. Writes `cheese_dataset.dvc`.
  5. Does not touch `.gitignore`, because `/cheese_dataset` is already ignored (`data-versioning@data-versioning-ac215/.gitignore:3`). scmrepo skips paths that are already ignored.
- Checkpoint:
  - `cat cheese_dataset.dvc` shows five fields: `md5: <32 hex>.dir`, `size`, `nfiles`, `hash: md5`, `path: cheese_dataset` (compare `data-versioning/cheese_dataset.dvc:1-6`).
  - With exactly `Image_1.jpg`…`Image_4.jpg`, you should get `md5: 89db50de27acfd6822faabc3da39b0a8.dir`, `size: 611101`, `nfiles: 4`.
  - DVC prints `To track the changes with git, run:` followed by `git add cheese_dataset.dvc`.

**B10. Push the data** (`data-versioning/README.md:303`)
```bash
dvc push
```
- Under the hood: uploads every cache object missing from `gs://BUCKET/dvc_store/files/md5/`, authenticating with ADC from `GOOGLE_APPLICATION_CREDENTIALS` via `gcsfs`.
- Checkpoint: a summary line `N files pushed`. I expect 5 for four images, because the transferred hash list includes the `.dir` manifest (`dvc_data/index/push.py`), but I did not run it. In the bucket browser, `dvc_store/files/md5/` now has two-character sub-folders (`5b/`, `ba/`, `91/`, `89/`, …).
- If it fails: `403 … storage.objects.create`: IAM. `Forbidden` on a bucket you don't own: the remote URL still points at the class bucket, so fix B8.

**B11. Commit and tag on the host (outside the container)** (`data-versioning/README.md:315-319`)
```bash
git status
git add .
git commit -m "Track initial cheese dataset with DVC"
git tag -a dataset_v20 -m "First version of cheese dataset"
git push --atomic origin main dataset_v20
```
- Under the hood: commits `.dvc/config`, `.dvc/.gitignore`, `.dvcignore` and `cheese_dataset.dvc`, but not the images (git-ignored) and not `.dvc/cache` (ignored by `data-versioning/.dvc/.gitignore:3`). It creates an annotated tag object and pushes branch and tag atomically.
- Checkpoint: `git status` before `add` shows `.dvc/.gitignore`, `.dvc/config` and `.dvcignore` under "Changes to be committed", because `dvc init` already staged them (`dvc/repo/init.py:86-91`). It shows `.dvc/config` again under "Changes not staged", because `dvc remote add` edited it after staging. `cheese_dataset.dvc` is untracked. After `git add .` all four are committed. GitHub shows the tag under *Tags*.
- If it fails: `fatal: tag 'dataset_v20' already exists`: you forked, or you re-ran the step. Pick another name (`:321`) or delete it with `git tag -d dataset_v20`.

**B12. View v20 in Colab** (`data-versioning/README.md:326-328`)
- Save a copy of the notebook in Drive (cell 5). Run `!pip install dvc dvc-gs` (cell 7), the imports (cell 9, which includes `from google.colab import auth`; cell 11 fails with `NameError` without it) and `auth.authenticate_user()` (cell 11). Then:
  ```text
  # Replace github url with your url
  !dvc list -R https://github.com/dlops-io/data-versioning.git
  ```
  ```text
  !rm -rf cheese_dataset
  !dvc get https://github.com/dlops-io/data-versioning cheese_dataset --force --rev dataset_v21
  ```
  These are cells 13 and 15, copied exactly. **Replace the URL with your repo and the rev with your tag (`dataset_v20`).** Then run cell 17 (`print("Number of items:",len(os.listdir("cheese_dataset")))`).
- Checkpoint: with your own v20 of four images, cell 17 prints `Number of items: 4`. The notebook's stored outputs are for the class `dataset_v21`: cell 13 lists five files under `cheese_dataset/`, cell 15 downloads 5 files, and cell 17 prints `Number of items: 5`.
- If it fails:
  - Your repo is private (the README asks for private at `:108`), so Colab's anonymous `git clone` fails. Use a token URL or make the repo public (§6, item 13).
  - Against the class repo you will likely get a 403 from GCS, because the class bucket `cheese-app-data-versioning` is not readable anonymously (checked: 401 "Anonymous caller does not have storage.objects.list access").

**B13. Change the data and make v21** (`data-versioning/README.md:338-369`)
- Upload one or more images to `images/` in the bucket. Wait up to about a minute (gcsfuse metadata caching; §6, item 18) until `ls cheese_dataset` inside the container shows them. Then, inside the container:
  ```bash
  dvc add cheese_dataset
  dvc push
  ```
  Then on the host:
  ```bash
  git status
  git add .
  git commit -m "Add images to cheese dataset"
  git tag -a dataset_v21 -m "Updated cheese dataset with additional images"
  git push --atomic origin main dataset_v21
  ```
- Under the hood: only the new image(s) and the new manifest are uploaded. `git status` shows only `cheese_dataset.dvc` modified.
- Checkpoint: `git diff HEAD~1 -- cheese_dataset.dvc` shows a new `md5:`, a larger `size:` and a larger `nfiles:`. `dvc push` reports far fewer files than the folder holds.
- Do **not** run `git remote add origin` again (`:372`). The older ac215 README tells you to (`data-versioning@data-versioning-ac215/README.md:148`), and it fails with `error: remote origin already exists.`

**B14. View v21 in Colab and switch versions**
- Same notebook with `--rev dataset_v21`. Cell 19 switches to another tag, and cell 20 counts the files again:
  ```text
  !rm -rf cheese_dataset
  !dvc get https://github.com/dlops-io/data-versioning cheese_dataset --force --quiet --rev dataset_v25
  ```
  The class repo has no tag `dataset_v25`; its tags are only `dataset_v20`, `dataset_v21` and `dataset_v30` (checked with `git ls-remote --tags`). Use your own tag.
  - Because of `--quiet`, a failing `dvc get` prints nothing: DVC sets its log level to CRITICAL and its errors are logged at ERROR (`dvc/cli/__init__.py:183-184`). The failure then appears in cell 20 as `FileNotFoundError: … 'cheese_dataset'`, because cell 19 already deleted the folder.
  - Cell 20's stored `Number of items: 3` is a leftover from a 2024-10-04 run by another user (no execution count). It is not the result of the stored cell 19 run.
- Checkpoint: `Number of items:` changes between revisions, for example 4 for your v20 and 5 or more for your v21.

**B15. Clean up** (`data-versioning/README.md:403-425`)
- `docker container ls`, `docker system prune`, `docker image ls`.
- The container used `--rm`, and exiting the shell unmounts gcsfuse. `.dvc/cache/` keeps local copies of every version until you delete it, which is safe because `dvc pull` can restore them.

---

## 5. Code tour

```text
data-labeling/                        (branch main, 03c3e27)
├── README.md                         Part A instructions
├── docker-shell.sh                   start Label Studio (prebuilt image) detached on :8080
├── docker-shell-CLI.sh               build + run the Python CLI container on the same network
├── docker-shell-compose.sh           build CLI image, then `docker-compose run` both
├── docker-compose.yml                the two services, external network, volumes, env
├── Dockerfile                        python:3.12-slim-bookworm + uv; user `app`; venv in /.venv
├── docker-entrypoint.sh              activate /.venv, exec bash
├── pyproject.toml / uv.lock          google-cloud-storage 3.4.1, label-studio-sdk 2.0.12, pandas 2.3.3
├── cli.py                            -c/-r set/remove bucket CORS, -m metadata, -p/-t Label Studio API
├── data-labeling-flow.png            figure in README (Part A flow)
├── pipeline-flow.png                 unreferenced figure of the whole labeling+versioning pipeline
└── cheeses-labels.png                example labels figure

data-versioning/                      (README from main b240b1a; code from data-versioning-ac215 23762e4)
├── README.md                         Part B instructions (main copy duplicated after line 425)
├── docker-shell.sh                   build image; run privileged with /dev/fuse; env + mounts
├── docker-entrypoint.sh              gcloud auth, gcsfuse mount, bind images/ → /app/cheese_dataset (ac215: 1 line shorter)
├── Dockerfile                        python:3.11-slim-bookworm + gcsfuse + google-cloud-cli + uv; root (ac215: google-cloud-sdk)
├── pyproject.toml / uv.lock          dvc 3.63.0, dvc-gs 3.0.2, google-cloud-storage, pandas
├── .gitignore                        ignores /cheese_dataset (plus legacy mushroom entries on main)
└── (main only) .dvc/config, .dvc/.gitignore, .dvcignore, cheese_dataset.dvc   ← what B7-B9 produce (instructor run, 2024-09-18)
```

**`data-labeling/docker-shell.sh:12-24`**
```bash
docker run -d \
  --name data-label-studio \
  --network data-labeling-network \
  -p 8080:8080 \
  -v "$(pwd)/docker-volumes/label-studio:/label-studio/data" \
  -v "$(pwd)/../secrets:/secrets" \
  -e LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK="true" \
  -e LABEL_STUDIO_USERNAME="pavlos@seas.harvard.edu" \
  -e LABEL_STUDIO_PASSWORD="awesome" \
  -e GOOGLE_APPLICATION_CREDENTIALS="/secrets/data-service-account.json" \
  -e GCP_PROJECT="ac215-project" \
  -e GCP_ZONE="us-central1-a" \
  heartexlabs/label-studio:latest
```
- `-d`: detached. You get your terminal back, and the logs go to `docker logs data-label-studio`.
- `--network`: joins the user-defined network so the CLI container can reach it by name.
- `-p 8080:8080`: host port to container port, which is what the browser uses.
- First `-v`: Label Studio's SQLite DB and uploads persist in a git-ignored host folder. Delete the folder and you lose projects, users and annotations that were not exported to target storage.
- Second `-v` + `GOOGLE_APPLICATION_CREDENTIALS`: the key Label Studio uses when the credentials field in the UI is blank.
- `LABEL_STUDIO_USERNAME`/`PASSWORD`: create the login used at `data-labeling/README.md:109`. `DISABLE_SIGNUP_WITHOUT_LINK`: nobody else can self-register.
- `:latest`: a moving tag, so the UI may differ from the README.

**`data-labeling/cli.py:22-34`**
```python
    # Initiate Storage client
    storage_client = storage.Client()
    if set:
        bucket = storage_client.get_bucket(bucket_name)
        bucket.cors = [
            {
                "origin": ["*"],
                "method": ["GET"],
                "responseHeader": ["Content-Type", "Access-Control-Allow-Origin"],
                "maxAgeSeconds": 3600,
            }
        ]
        bucket.patch()
```
- `storage.Client()`: no arguments, so credentials come from `GOOGLE_APPLICATION_CREDENTIALS` and the project from the key file.
- `get_bucket`: an API call that fails with 404 if the bucket name is wrong, or 403 without `storage.buckets.get`.
- `"origin": ["*"]`: any website may read responses. Tighter would be `["http://localhost:8080"]`.
- `"method": ["GET"]`: the browser only downloads images.
- `"responseHeader"`: non-simple headers GCS will allow in cross-origin requests and expose in responses (`Access-Control-Allow-Headers` / `Access-Control-Expose-Headers`). Listing `Access-Control-Allow-Origin` here is harmless but has no effect.
- `"maxAgeSeconds": 3600`: sent as `Access-Control-Max-Age`, so browsers may cache *preflight* (`OPTIONS`) answers for an hour. Plain image `GET`s are simple requests with no preflight (§3.3).
- `bucket.patch()`: sends only the changed field. This requires `storage.buckets.update`, which Storage Admin has and *Storage Object Admin* does not.

**`data-labeling/docker-shell-CLI.sh:15-25`**
```bash
docker run --rm -ti \
  --name data-label-cli \
  --network data-labeling-network \
  -v "$(pwd)/../secrets:/secrets" \
  -v "$(pwd)/../data-labeling:/app" \
  -e GOOGLE_APPLICATION_CREDENTIALS="/secrets/data-service-account.json" \
  -e GCP_PROJECT="ac215-project" \
  -e GCP_ZONE="us-central1-a" \
  -e GCS_BUCKET_NAME="cheese-app-data-demo" \
  -e LABEL_STUDIO_URL="http://data-label-studio:8080" \
  data-label-cli
```
- `--rm -ti`: an interactive throwaway container, deleted on exit.
- `--network data-labeling-network`: this script does **not** create the network (compare `data-labeling/docker-shell.sh:6`), so run A6 first.
- `-v "$(pwd)/../data-labeling:/app"`: mounts *the repo itself*, found by its folder name, over the image's `/app`. Live-edits to `cli.py` take effect without rebuilding. If your folder has another name, Docker silently mounts an empty new folder instead (§6, item 9).
- `GCS_BUCKET_NAME`: the line you must edit.
- `LABEL_STUDIO_URL`: the Docker-DNS address of the Label Studio container (§3.4).

**`data-labeling/cli.py:94-108`**
```python
    # Examples using SDK: https://labelstud.io/sdk/project.html#label_studio_sdk.project.Project
    label_studio_client = Client(url=LABEL_STUDIO_URL, api_key=api_key)
    label_studio_client.check_connection()

    projects = label_studio_client.get_projects()
    project_id = projects[0].id
    project = label_studio_client.get_project(project_id)
    print(project)
    # print(project.get_tasks())
    print("Number of tasks:", len(project.tasks))

    labeled_tasks = project.get_labeled_tasks()
    print("Number of labeled tasks:", len(labeled_tasks))
    for labeled_task in labeled_tasks:
        print("Annotations:", labeled_task["annotations"])
```
- `Client(...)`: the **legacy** SDK client. In `label-studio-sdk` 2.0.12 it is still exported (`from ._legacy import Client`) and authenticates with `Authorization: Token <api_key>`.
- `Client(...)` itself already sends the token header once: its constructor calls `GET /api/version` (`label_studio_sdk/_legacy/client.py:111,122`).
- `check_connection()`: `GET /health`, a health check. The first token-checked API call is normally `get_projects()` (`/api/projects`). (I did not check the Label Studio server source to see whether `/api/version` also enforces the token.)
- `projects[0]`: "the first project". With several projects you may be reading the wrong one.
- `project.tasks`: fetches all tasks.
- `get_labeled_tasks()`: server-side filter `filter:tasks:completed_at` not empty (`label_studio_sdk/_legacy/project.py:929-956`).
- `labeled_task["annotations"]`: a list of annotation dicts. The label is in `result[0]["value"]["choices"]`.

**`data-labeling/docker-compose.yml:6-20`**
```yaml
services:
    data-label-cli:
        image: data-label-cli
        container_name: data-label-cli
        volumes:
            - ../secrets:/secrets
            - ../data-labeling:/app
        environment:
            GOOGLE_APPLICATION_CREDENTIALS: /secrets/data-service-account.json
            GCP_PROJECT: "ac215-project"
            GCP_ZONE: "us-central1-a"
            GCS_BUCKET_NAME: "cheese-app-data-demo"
            LABEL_STUDIO_URL: "http://data-label-studio:8080"
        depends_on:
            - data-label-studio
```
- This is the same container as `docker-shell-CLI.sh`, written declaratively. Relative paths are resolved from the compose file's folder.
- `GCS_BUCKET_NAME` is hard-coded a **second** time here (line 17). The README only tells you to edit the shell script.
- `depends_on`: compose starts `data-label-studio` (lines 21-35) first, but does not wait until it is *ready*.
- `docker-compose run` ignores `container_name` and names the one-off container `<project>-data-label-cli-run-<id>`.
- Lines 2-5 (not shown) declare the network as `external: true`, so compose will not create it. That is why `data-labeling/docker-shell-compose.sh:6` creates it first.

**`data-versioning/docker-shell.sh:13-27`**
```bash
echo "Building image"
docker build -t data-version-cli -f Dockerfile .

echo "Running container"
docker run --rm --name data-version-cli -ti \
--privileged \
--cap-add SYS_ADMIN \
--device /dev/fuse \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v ~/.gitconfig:/etc/gitconfig \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCP_ZONE=$GCP_ZONE \
-e GCS_BUCKET_NAME=$GCS_BUCKET_NAME data-version-cli
```
- `--privileged --cap-add SYS_ADMIN --device /dev/fuse`: lets the container create FUSE and bind mounts. `--privileged` alone already implies the other two.
  - Repo history shows `--device /dev/fuse` was removed in `6ed453d` and restored two days later in `da15b45`.
- `-v "$BASE_DIR":/app`: the host repo (`BASE_DIR=$(pwd)`, line 5) is the container's working directory. Everything DVC writes (`.dvc/`, `cheese_dataset.dvc`, the cache) lands on the host, where git sees it.
- `-v ~/.gitconfig:/etc/gitconfig`: your git identity inside the container, in case you commit there. If the file does not exist, Docker creates a *directory* by that name (§6, item 4).
- `GCS_BUCKET_NAME`: read by the entrypoint for the gcsfuse mount.

**`data-versioning/docker-entrypoint.sh:9-21`** (identical to `data-versioning@data-versioning-ac215/docker-entrypoint.sh:8-20`; subtract 1 from the line numbers below for the starter)
```bash
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
mkdir -p /mnt/gcs_bucket
gcsfuse --key-file=$GOOGLE_APPLICATION_CREDENTIALS $GCS_BUCKET_NAME /mnt/gcs_data
echo 'GCS bucket mounted at /mnt/gcs_data'
mkdir -p /app/cheese_dataset
mount --bind /mnt/gcs_data/images /app/cheese_dataset

# Activate virtual environment
echo "Activating virtual environment..."
source /.venv/bin/activate

# Keep a shell open
exec /bin/bash
```
- Line 9: lets you use `gcloud storage ls gs://…` in the container. DVC does not need it.
- Line 10: creates `/mnt/gcs_bucket`, which nothing uses. The mount point `/mnt/gcs_data` was created in `data-versioning/Dockerfile:48`.
- Line 11: mounts the **whole bucket**, so `/mnt/gcs_data/dvc_store` is visible too. gcsfuse daemonizes, so the script continues. Without `--implicit-dirs`, only folders with placeholder objects are visible.
- Line 12 prints success **unconditionally**, even if line 11 failed.
- Line 13: creates the mount target. Through the `/app` bind mount this also creates an empty `cheese_dataset/` on the host.
- Line 14: puts the bucket's `images/` exactly where `dvc add cheese_dataset` looks.
- Lines 18-21: put `/.venv/bin` (dvc) on PATH, then replace the script with an interactive bash that inherits that environment.

**`data-versioning/Dockerfile:30-36`**
```dockerfile
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    echo "deb http://packages.cloud.google.com/apt gcsfuse-bionic main" > /etc/apt/sources.list.d/gcsfuse.list && \ 
    apt-get update && \
    apt-get install -y  gcsfuse && \
    apt-get install -y --no-install-recommends google-cloud-cli && \
```
- Lines 30 and 32: install Google's apt signing key twice, once into the global keyring (used by the gcsfuse repo, which has no `signed-by`) and once into a dedicated keyring (used by the cloud-sdk repo). `apt-key` is deprecated but still present in Debian bookworm, which the base image pins.
- Line 33: the gcsfuse repo for Ubuntu *bionic* is used on Debian *bookworm*. It works because gcsfuse is a static Go binary, and the repo serves amd64 and arm64. On 2026-10-01 it served gcsfuse 3.12.1. The line ends in `\ ` (backslash plus a space). Docker's parser tolerates whitespace after the line-continuation character.
- Line 36: `google-cloud-cli` is the current package name. The ac215 branch still says `google-cloud-sdk` here.
- gcsfuse and gcloud are not version-pinned, so builds on different days can differ.

**`data-versioning/.dvc/config:1-4`**, the instructor's result of B8
```ini
[core]
    remote = cheese_dataset
['remote "cheese_dataset"']
    url = gs://cheese-app-data-versioning/dvc_store
```
- `[core] remote`: the default remote, set by `-d`. `dvc push` and `dvc get` use it.
- `url`: the bucket and prefix. `dvc-gs` maps `gs://` to `gcsfs`.

**`data-versioning/cheese_dataset.dvc:1-6`**, the instructor's result of B9 (5 files, the v21/v30 manifest)
```yaml
outs:
- md5: 3280f8f9629451704dca3f792534e1f5.dir
  size: 785481
  nfiles: 5
  hash: md5
  path: cheese_dataset
```
- `md5: ….dir`: the hash of the sorted JSON manifest. It identifies the exact set of (relpath, file-md5) pairs.
- `size` / `nfiles`: totals, for humans and quick checks.
- `hash: md5`: marks DVC-3 hashing, a plain md5 of the bytes. DVC 2's legacy `md5-dos2unix` normalized line endings in text files.
- `path`: the tracked folder, relative to this file.

**Colab notebook, cells 13, 15 and 19** (`colab/L11_data_versioning_view.ipynb`)
```text
# Replace github url with your url
!dvc list -R https://github.com/dlops-io/data-versioning.git
!rm -rf cheese_dataset
!dvc get https://github.com/dlops-io/data-versioning cheese_dataset --force --rev dataset_v21
!rm -rf cheese_dataset
!dvc get https://github.com/dlops-io/data-versioning cheese_dataset --force --quiet --rev dataset_v25
```
- `dvc list -R <repo>`: lists git-tracked and DVC-tracked files at the default branch. Expanding the DVC directory needs the `.dir` manifest from the remote. The stored output (2025-10-29) lists `.dvcignore`, `.gitignore`, `Dockerfile`, `README.md`, `cheese_dataset.dvc`, five `cheese_dataset/…` entries (`Image_1.jpg`-`Image_4.jpg` and the Gruyère `.webp`), `docker-entrypoint.sh`, `docker-shell.sh`, `pyproject.toml` and `uv.lock`.
- `dvc get <repo> <path> --rev <tag>`: a temporary clone of the repo at that tag, then a download of the blobs into `./cheese_dataset`. No `dvc init` is needed in Colab.
- `--force`: overwrite. `--quiet`: suppresses progress **and error messages**. With `-q`, DVC raises its log level to CRITICAL (`dvc/cli/__init__.py:183-184`), so a failed `dvc get` prints nothing and only returns a non-zero exit code.
- `dataset_v25` does not exist in the class repo.

---

## 6. Gotchas and common errors

1. **The starter branch no longer builds (google-cloud-sdk).**
   - Symptom: during `sh docker-shell.sh` on the ac215 branch, apt stops at `apt-get install -y --no-install-recommends google-cloud-sdk`. Expect apt's message for a name that is only referenced (`Package google-cloud-sdk is not available, but is referred to by another package … However the following packages replace it: google-cloud-cli`). The build exits non-zero, and `set -e` in `data-versioning/docker-shell.sh:3` stops the script.
   - Cause: Google's `cloud-sdk` apt repo (index dated 2026-10-07) contains no `google-cloud-sdk` package for amd64 or arm64, only `google-cloud-cli` (latest 588.0.0-0), which declares `Replaces/Breaks: google-cloud-sdk (<< 467.0.0-0)`.
   - Fix: edit `data-versioning@data-versioning-ac215/Dockerfile:36` to `google-cloud-cli`, exactly as `main` did in commit `ebf09c8` (`data-versioning/Dockerfile:36`).

2. **`cheese_dataset` is empty or the bind mount fails.**
   - Symptom: `mount: /app/cheese_dataset: special device /mnt/gcs_data/images does not exist`, or `ls cheese_dataset` shows nothing.
   - Causes:
     - (a) You never uploaded the initial images. The README only says to create the folder (`data-versioning/README.md:180-187`).
     - (b) The objects were uploaded with a CLI or SDK, so there is no `images/` placeholder object. gcsfuse is started without `--implicit-dirs` (`data-versioning/docker-entrypoint.sh:11`), so it does not see the folder.
     - (c) A gcsfuse auth failure (see item 3).
   - Fix: create the folder in the console and upload images, or add `--implicit-dirs` to the gcsfuse line, then restart the container.
   - Never `dvc add` an empty folder: you would version "nothing" and tag it.

3. **Missing or misplaced key file.**
   - Symptom: `gcloud` says it cannot read `/secrets/data-service-account.json`, gcsfuse fails, and Label Studio's "Check Connection" fails.
   - Cause: `../secrets` did not exist. With `-v`, Docker silently creates an empty host directory and mounts it.
   - Fix: put the key at `<parent>/secrets/data-service-account.json`, next to the repo, and restart the container. The entrypoint has no `set -e`, so you still get a shell, and errors scroll past.

4. **`~/.gitconfig` becomes a directory.**
   - Symptom: after running `docker-shell.sh`, git on the host warns it cannot read `~/.gitconfig`.
   - Cause: `-v ~/.gitconfig:/etc/gitconfig` (`data-versioning/docker-shell.sh:23`). If the source path does not exist, `docker run -v` creates it as a directory.
   - Fix: run `git config --global user.name …` *before* the first container run. If it already happened: `rmdir ~/.gitconfig`, then configure git.

5. **Port 8080 is taken.**
   - Symptom: `Bind for 0.0.0.0:8080 failed: port is already allocated`.
   - Cause: another process or course container uses 8080. The cheese-app `frontend-simple` containers in later lectures also publish `-p 8080:8080` (e.g. `cheese-app-v1/src/frontend-simple/docker-shell.sh:20`).
   - Fix: stop it, or change the host side to `-p 8081:8080` and browse `localhost:8081`. The CLI container still uses `data-label-studio:8080`.

6. **Container name conflict when switching to compose.**
   - Symptom: `Conflict. The container name "/data-label-studio" is already in use`.
   - Cause: `docker-shell.sh` runs Label Studio without `--rm`, so `docker stop` (the README's advice at `data-labeling/README.md:225`) leaves a stopped container that still owns the name.
   - Fix: `docker rm data-label-studio`, or `docker rm -f data-label-studio`.

7. **Network not found.**
   - Symptom: `docker-shell-CLI.sh` fails with `network data-labeling-network not found`.
   - Cause: only `data-labeling/docker-shell.sh:6` and `data-labeling/docker-shell-compose.sh:6` create the network, and `docker system prune` (B1, A15) deletes unused networks.
   - Fix: run `sh docker-shell.sh` first, or `docker network create data-labeling-network`.

8. **`docker-compose` vs `docker compose`.**
   - Symptom: `docker-compose: command not found` (Compose v2-only installs), or a warning that the `version` attribute is obsolete (`data-labeling/docker-compose.yml:1`).
   - Fix: edit `data-labeling/docker-shell-compose.sh:12` to `docker compose run --rm --service-ports data-label-cli`. The warning is harmless.
   - Note: after you exit the CLI shell, `data-label-studio` keeps running. Stop it with `docker compose down` or `docker stop`.

9. **The repo folder must be called `data-labeling`.**
   - Symptom: the CLI container exits at once with `/bin/bash: docker-entrypoint.sh: No such file or directory`, or `cli.py` is missing.
   - Cause: `-v "$(pwd)/../data-labeling:/app"` (`data-labeling/docker-shell-CLI.sh:19`, `data-labeling/docker-compose.yml:12`) hard-codes the folder name. A clone named anything else (e.g. `data-labeling-main` from a ZIP download) makes Docker mount a new empty folder over `/app`. The entrypoint is resolved relative to `/app` (`data-labeling/Dockerfile:51`).
   - Fix: rename the folder, or change the mount to `"$(pwd)":/app`.

10. **Images do not load in Label Studio (CORS).**
    - Symptom: broken thumbnails. The browser console shows `blocked by CORS policy: No 'Access-Control-Allow-Origin' header`.
    - Cause: the bucket has no CORS rule, or the rule went to the wrong bucket because `GCS_BUCKET_NAME` was not edited (`data-labeling/docker-shell-CLI.sh:23`).
    - Fix: edit the bucket name, then run `python cli.py -c` and verify with `python cli.py -m`. Hard-refresh the page (or use a private window), because the browser may reuse cached responses that lacked the header. `maxAgeSeconds` = 3600 s only governs cached *preflight* answers (§3.3).

11. **`401 Unauthorized` from `cli.py -p/-t`.**
    - Cause: the token type. Recent Label Studio versions show JWT *Personal Access Tokens* (long strings starting `eyJ`) in Account & Settings. The legacy `Client` used by `data-labeling/cli.py:95` always sends `Authorization: Token <key>`, which only works with a *legacy* token. The newer `LabelStudio` client detects JWTs and refreshes them into `Bearer` access tokens (`label_studio_sdk/tokens/client_ext.py`, `core/client_wrapper.py`).
    - Fix (either):
      - Use a legacy token. Your Label Studio version may require enabling legacy tokens in the organization's token settings.
      - Replace the client with `from label_studio_sdk import LabelStudio` and `LabelStudio(base_url=LABEL_STUDIO_URL, api_key=api_key)`, then list projects with `.projects.list()`.
    - I could not confirm which token type `label-studio:latest` shows by default.

12. **Label Studio data folder permissions on Linux hosts.**
    - Symptom: Label Studio exits with `PermissionError` under `/label-studio/data`.
    - Cause: Docker creates `./docker-volumes/label-studio` as root, and the image runs as a non-root user.
    - Fix: create the folder yourself and make it writable for the container user (e.g. `sudo chown -R 1001 docker-volumes/label-studio`; the uid is my assumption from Label Studio's image, so check `docker run --rm --entrypoint id heartexlabs/label-studio:latest`).
    - Docker Desktop on macOS normally does not hit this.

13. **Colab cannot fetch your versions.**
    - (a) Private repo: `dvc get https://github.com/<you>/data-versioning …` needs git credentials. Use `https://<user>:<token>@github.com/<you>/data-versioning` with a fine-grained read-only token (not saved in the notebook), or make the repo public.
    - (b) Class repo: the default URL in cells 13/15/19 points at `dlops-io/data-versioning`, whose remote is the class bucket. That bucket rejects anonymous listing (401, checked), and your account is probably not on its IAM policy, so expect a 403.
    - (c) `--rev dataset_v25` does not exist (item 13 of §10). Because cell 19 uses `--quiet`, you see no error there. Cell 20 then fails with `FileNotFoundError`, since cell 19's `rm -rf` already removed `cheese_dataset`. To see the real error, drop `--quiet`.
    - (d) Signed in with a Google account that has no access to *your* bucket: `auth.authenticate_user()` uses the account you pick.

14. **"Tag already exists".**
    - Symptom: `fatal: tag 'dataset_v20' already exists`.
    - Cause: you forked instead of copying (forks carry the class tags `dataset_v20/v21/v30`), or you re-ran the tag command.
    - Fix: choose another number, as the README's disclaimer suggests (`data-versioning/README.md:321`), or `git tag -d` it locally. With a fresh `git init` repo no tag is "taken".

15. **`git push -u origin main` fails on the old instructions.**
    - Symptom: `error: src refspec main does not match any`.
    - Cause: git's default branch is `master`, and the ac215 README omits `git branch -M main` (`data-versioning@data-versioning-ac215/README.md:39-43`).
    - Fix: run `git branch -M main`, as in `data-versioning/README.md:121`.

16. **`dvc init` refuses.**
    - `'.dvc' exists. Use `-f` to force.`: you cloned `main`, which already has `.dvc/`. Use the ac215 branch, or delete `.dvc/`, `.dvcignore` and `cheese_dataset.dvc` first.
    - `/app is not tracked by any supported SCM tool (e.g. Git)`: run `git init` on the host first.

17. **Forgetting `dvc push` (or pushing to the wrong remote).**
    - Symptom: Colab's `dvc get` fails with an error about missing files or cache entries. DVC 3.63's wording for this case is "Some of the cache files do not exist neither locally nor on remote" (`dvc/data_cloud.py`), and the top-level `dvc get` error may be phrased differently.
    - Cause: git has the pointer, but the bucket lacks the blobs.
    - Fix: `dvc push` from the container, then check `dvc_store/files/md5/` in the console.

18. **New images "don't appear".**
    - Symptom: you uploaded to `images/`, but `ls cheese_dataset` and `dvc add` do not see them yet.
    - Cause: gcsfuse caches metadata and directory listings for a while.
    - Fix: wait about a minute, or exit and restart the container. Check with `ls` before `dvc add`.

19. **Where to run git.**
    - The README says to run git on the host (`data-versioning/README.md:312`). The container has git and your `/etc/gitconfig`, but it runs as root. On Linux hosts, files it creates (the `.dvc/` folder, `cheese_dataset.dvc`) are root-owned, and git inside it may complain about "dubious ownership" because `/app` belongs to another uid.
    - On macOS this is usually invisible. The instructor's commit `ebf09c8` ("Track initial cheese dataset with DVC", which in fact changed only `Dockerfile` and `docker-entrypoint.sh`) was made with timezone `+0000`, consistent with committing from inside the container.

20. **Key creation blocked or over-privileged.**
    - Organization policies can forbid service-account keys. Use a personal project, or ask the admin.
    - *Storage Admin* is project-wide: it can delete every bucket in the project. For this tutorial, a bucket-level role would do (object read/write plus `storage.buckets.update` for the CORS patch). Never commit the JSON. Both repos keep it in `../secrets` for that reason.

21. **Apple Silicon.** No emulation is needed.
    - `heartexlabs/label-studio:latest` ships `linux/amd64` and `linux/arm64` (Docker Hub, pushed 2026-09-29).
    - The `python:3.x-slim-bookworm` bases are multi-arch.
    - The gcsfuse and cloud-sdk apt repos serve arm64.
    - `docker-entrypoint.sh` prints `Architecture: aarch64` on M-series Macs.

22. **Uploading macOS metadata files.** If you extract the zip with `unzip` on the command line, you also get `__MACOSX/cheeses_unlabeled/` with 21 `._Image_*` files (20 `.jpg`, 1 `.png`). If they end up under `cheeses_unlabeled/`, Label Studio creates 21 extra broken tasks. Upload only `cheeses_unlabeled/*.jpg|png`.

---

## 7. Where this sits in the course

- **Before (L10, cheese-app-v0, Ed lesson 166035):** service accounts, JSON keys and `GOOGLE_APPLICATION_CREDENTIALS` / ADC; the `../secrets` folder convention; published ports versus container DNS; and CORS, when the browser calls a container API across origins. L11 reuses all four, now pointed at **data**: the same key-file pattern (`/secrets/data-service-account.json`) and the same CORS idea, applied to a bucket. L02-L04 supply the rest: Dockerfiles and containers (`simple-translate`), multi-container pipelines on GCS with docker-compose (`mega-pipeline`), and Docker networks and ports (`port_toy`), per `tutorials_demo.md:31-67`. Together they explain the two-container setup and the compose "Extra".
- **What L11 adds:**
  - (1) Human labeling as a containerized web service backed by cloud storage.
  - (2) Data as a *versioned artifact*: content-addressed blobs in a bucket, pointers and names in git.
  - (3) A FUSE-mounted bucket in a privileged container.
  - It also feeds Milestone 2 (due 2026-10-20, `milestones_dates.yaml:7-9`), which requires "basic data/version tracking (e.g., dataset snapshot IDs, file versions, or a lightweight versioning tool such as DVC …)" (`milestone2.md:49`).
- **After:**
  - L12 (App Design) has no tutorial (`tutorials_demo.md:162-163`).
  - L13 (experiment tracking, Vertex AI training; `tutorials_demo.md:167-177`) trains on the *labeled* cheese data, but downloads it from a GitHub release (`https://github.com/dlops-io/datasets/releases/download/v4.0/cheese_4_labels.zip`, `model-training/package/trainer/task.py:97`, commit `b9aee1c`). It does not use DVC. Swapping that download for `dvc get … --rev dataset_vNN` is the natural way to make L13 runs reproducible.
  - L15 (`ml-workflow`, `tutorials_demo.md:198-208`, with `src/data-collector`, `data-processor`, `model-training`, `workflow`) uses the same release-download pattern (`ml-workflow/src/model-training/package/trainer/task.py:104`).
- **Branch diff (this lecture's repo):** `git diff --stat origin/data-versioning-ac215 origin/main` in `data-versioning`:

  ```text
   .dvc/.gitignore      |   3 +
   .dvc/config          |   4 +
   .dvcignore           |   3 +
   .gitignore           |   3 +
   Dockerfile           |   2 +-
   README.md            | 900 +++++++++++++++++++++++++++++++++++++++++++++------
   cheese_dataset.dvc   |   6 +
   docker-entrypoint.sh |   1 +
   8 files changed, 814 insertions(+), 108 deletions(-)
  ```

  Meaningful changes:
  - The four DVC files are the *output* of B7-B9 from an instructor run. They were last changed in `8a1d9b0` ("new version v30", 2024-09-18), and `cheese_dataset.dvc` equals the `dataset_v21`/`dataset_v30` pointer. The 2026 commit `ebf09c8` did not touch them.
  - `Dockerfile` swaps `google-cloud-sdk` for `google-cloud-cli`.
  - `docker-entrypoint.sh` adds `echo $GCS_BUCKET_NAME`.
  - `.gitignore` adds legacy `/docker-volumes`, `/mushroom_dataset_prep` and `/mushroom_dataset` lines, left over from the course's earlier mushroom app.
  - `README.md` is rewritten into the 4-walkthrough format (and duplicated).
  - `docker-shell.sh`, `pyproject.toml` and `uv.lock` are identical.
- **`data-labeling` vs its `pipenv` branch:** `main` replaced `Pipfile`/`Pipfile.lock` with `pyproject.toml`/`uv.lock` and rewrote the Dockerfile for uv (commits `a537a0b`, `03c3e27`, 2025-10-20). README line 162 still mentions "Pipfiles".
- **Course-site numbering quirk:** the weekly module page lists "Oct 13 · Data Management and Versioning · Lecture 10" and "Oct 15 · App Design · Lecture 11" (`_modules/week-07.md:5-11`). `tutorials_demo.md:148` calls the same content Lecture 11. Going by the module page, the session is on Tue 2026-10-13 (the date of this check).

---

## 8. Video plan (suggestion)

**Hook question:** "Your cheese classifier scored 91% last week and 84% today. Nobody touched the code. Which photos, with which labels, did last week's model see, and can you get exactly those back?"

**Chapters** (≈ 30 min, about 4,600 spoken words at 155 wpm; each chapter ends with the viewer's terminal in a known state)

1. **The map (2 min).**
   - Idea: data work has two jobs. Attach meaning (labels) and freeze history (versions).
   - Visual: a redraw of `pipeline-flow.png`. Unlabeled photos → bucket → labeling container → labeled → versioning container → GitHub + `dvc_store` → Colab. The two halves light up in turn. An honest overlay notes that "in the code these two halves use different buckets."
   - On screen: the folder layout from §2 (`AC215/secrets`, `data-labeling`, `data-versioning`).

2. **Label Studio in a box (3.5 min).**
   - Idea: a prebuilt image plus ports, volumes, env vars gives you a whole web app in one command.
   - Visual: the `docker run` flags from `data-labeling/docker-shell.sh:12-24` peel off one by one and attach to a container drawing. `-p` becomes a door at 8080. `-v` becomes two pipes (SQLite folder, secrets). `-e` becomes sticky notes (login, key path).
   - On screen: `sh docker-shell.sh`, `docker container ls`, browser at `localhost:8080`, login, create the project with the four cheese labels.

3. **Who touches the bytes (3.5 min, ★ §3.2).**
   - Idea: Label Studio lists and signs, and the browser downloads from GCS.
   - Visual: the ticket-office animation (list → 21 task cards → sealed URL → vault).
   - On screen: the Source Storage form fields (`data-labeling/README.md:125-133`), *Sync Storage* → "21 tasks". Then broken thumbnails, a cliff-hanger.
   - **Pause-and-ponder 1:** "Label Studio has the key and your browser doesn't. How can the browser show a private image without ever seeing the key?" (Answer: a signed URL is a capability for one object for a limited time.)

4. **CORS, the browser's bouncer (3 min, ★ §3.3).**
   - Idea: the block is the browser enforcing origins, and the fix is a header the bucket must send.
   - Visual: the two islands and the bouncer. The rule card from `data-labeling/cli.py:26-34` sticks onto the bucket.
   - On screen: edit `data-labeling/docker-shell-CLI.sh:23`; `sh docker-shell-CLI.sh`; `python cli.py -c`; `python cli.py -m`; refresh, and the photos appear.
   - Two-address aside: `data-label-studio:8080` vs `localhost:8080`.

5. **Annotations are data (3 min).**
   - Idea: a label is a JSON record next to, not inside, the image.
   - Visual: clicking "gouda" emits a JSON envelope that drops into `cheeses_labeled/`. Zoom into `result → value → choices`.
   - On screen: annotate 3 images; open one JSON in the console; `python cli.py -t -k <TOKEN>`. Callout: the 401 trap with JWT tokens.

6. **A bucket that looks like a folder (3.5 min, ★ §3.7).**
   - Idea: gcsfuse + bind mount let DVC treat cloud objects as files.
   - Visual: the two-pipe animation, then the camera pulls back to show the host's dark, empty `cheese_dataset/`.
   - On screen: B2 clone + Dockerfile fix (`google-cloud-sdk` → `google-cloud-cli`); upload 4 images to `images/`; `sh docker-shell.sh`; `ls cheese_dataset`.
   - **Pause-and-ponder 2:** "In another terminal on your Mac, `ls data-versioning/cheese_dataset` prints nothing. Is the mount broken?" (Answer: no. The mounts live in the container's mount namespace, and the host sees only the empty directory created at `data-versioning/docker-entrypoint.sh:13`.)

7. **Fingerprints (4 min, ★ §3.5).**
   - Idea: content addressing; a version is the hash of a manifest of hashes.
   - Visual: the hash-machine animation with the real values. `Image_1.jpg` → `5b53853e…` → shelf `5b/`. Manifest → `89db50de….dir`.
   - On screen: `dvc init`; `dvc remote add -d cheese_dataset gs://YOUR_BUCKET_NAME/dvc_store`; `dvc add cheese_dataset`; `cat cheese_dataset.dvc` (show it matches `89db50de…`, 611101, 4 if they used Image_1-4); `ls .dvc/cache/files/md5`.

8. **Pointers and names (3.5 min, ★ §3.6).**
   - Idea: git stores the 6-line pointer and a tag names it; the bucket stores the bytes.
   - Visual: the git timeline with flags and ropes.
   - On screen: `dvc push`; browse `dvc_store/files/md5/`; host `git status` / `add` / `commit` / `tag -a dataset_v20` / `push --atomic`. Then upload a 5th image, `dvc add`, `dvc push`.
   - **Pause-and-ponder 3 (before `dvc push` of v21):** "You added one photo to a four-photo dataset. How many objects will `dvc push` upload?" (Answer: two, the new photo and the new `.dir` manifest. The four old blobs are already there.) Then show `git diff` of `cheese_dataset.dvc` and tag v21.

9. **Time travel from anywhere (3 min).**
   - Idea: `dvc get --rev` walks tag → commit → pointer → manifest → blobs.
   - Visual: pull the v20 rope, and four photos materialize in a Colab box. Pull v21 and five appear.
   - On screen: Colab cells 7, 9, 11, 13, 15, 17 with *your* repo URL and tags. A failure gallery (private repo, class bucket 403, `dataset_v25`).

10. **Recap and clean-up (1.5 min).**
    - Visual: the map from chapter 1 with everything now lit, and a "what to delete / what never to delete (dvc_store)" panel.
    - On screen: `docker container ls`, `docker rm -f data-label-studio`, `docker system prune`.

**Recap questions**
1. Why does the browser, not Label Studio, need the bucket's CORS policy?
2. What exactly is inside `cheese_dataset.dvc`, and which of its fields would change if you renamed one image?
3. Where are the image bytes after `dvc add`, and after `dvc push`? Name three locations.
4. Why must the DVC container run `--privileged` with `/dev/fuse`?
5. What breaks if you delete `gs://<bucket>/dvc_store` but keep the GitHub repo and its tags?
6. Why does `cli.py` reach Label Studio at `data-label-studio:8080` while you use `localhost:8080`?

**Target length:** ~30 minutes (two tutorials; chapters 2-5 for Part A, 6-9 for Part B). It can be split into two ~15-minute videos at the chapter 5/6 boundary.

---

## 9. Exercises

**E1 (hands-on, predict, then run): predict the dataset fingerprint.**
- Put exactly `Image_1.jpg`, `Image_2.jpg`, `Image_3.jpg`, `Image_4.jpg` from `cheeses_unlabeled.zip` into `images/` and run `dvc add cheese_dataset`. Predict `md5`, `size` and `nfiles` *before* you look.
- *Answer:* `md5: 89db50de27acfd6822faabc3da39b0a8.dir`, `size: 611101`, `nfiles: 4`. This is exactly the class repo's `dataset_v20` (`git show dataset_v20:cheese_dataset.dvc`), because DVC hashes the sorted JSON list `[{"md5": "5b53853e…", "relpath": "Image_1.jpg"}, …]`.
- The same bytes give the same hash on any machine. Rename one file and only the manifest hash changes; the four blob md5s stay the same.

**E2 (hands-on): remove CORS and watch the UI.**
- Inside the CLI container run `python cli.py -r`, then `python cli.py -m`. Reload a Label Studio task page with the browser dev-tools console open. Predict what you'll see, then restore with `python cli.py -c`.
- *Answer:*
  - `-r` sets `bucket.cors = []` (`data-labeling/cli.py:35-38`), and `-m` prints `Cors: []`.
  - The page still gets signed URLs, but the image responses lack `Access-Control-Allow-Origin`. The console reports a CORS block and the images break.
  - Because of browser caching of earlier image responses, the effect (and the fix) may need a hard refresh or a private window. The 3600 s `maxAgeSeconds` only affects cached preflight answers, which simple image `GET`s do not use.
  - `curl <signed-url>` still downloads the image, which proves CORS is browser-side, not access control.

**E3 (debugging): `python cli.py -p -k eyJhbGciOi…` prints a traceback ending in `401 Client Error: Unauthorized`.**
- *Answer:*
  - The token starting with `eyJ` is a JWT *Personal Access Token*. `cli.py` uses the legacy `Client` (`data-labeling/cli.py:95`), which sends `Authorization: Token <key>`, a scheme only valid for legacy tokens.
  - The constructor's `GET /api/version` and `check_connection()`'s `GET /health` come first. The 401 normally comes from `/api/projects`, the first token-checked API call. If your server also guards `/api/version`, the traceback ends at the `Client(...)` line instead.
  - Fix: use a legacy token (enable it in the organization's token settings if your version requires it), or switch to `LabelStudio(base_url=…, api_key=…)`, which recognizes JWTs and exchanges them at `/api/token/refresh/` for a `Bearer` access token.

**E4 (debugging): following the README, `sh docker-shell.sh` in the freshly cloned ac215 starter stops during the image build at the line that installs `google-cloud-sdk`. Why, and what is the minimal fix?**
- *Answer:*
  - Google renamed the package to `google-cloud-cli`. In 2026 the apt index has no installable `google-cloud-sdk`, only `google-cloud-cli`, which `Replaces/Breaks google-cloud-sdk (<< 467.0.0-0)`.
  - The RUN step uses `set -ex`, so apt's failure aborts the build, and `docker-shell.sh` has `set -e`.
  - Fix: change `data-versioning@data-versioning-ac215/Dockerfile:36` to `apt-get install -y --no-install-recommends google-cloud-cli && \`, exactly as `main` did.

**E5 (conceptual + hands-on): delete a photo and time-travel.**
- After tagging v21, delete `Image_2.jpg` from `images/` in the bucket. Run `dvc add cheese_dataset`, `dvc push`, then commit and tag `dataset_v22`.
- Questions:
  - (a) Does `dvc push` upload anything?
  - (b) Can Colab still `dvc get … --rev dataset_v20` and get 4 images?
  - (c) What if you then delete `dvc_store/` from the bucket?
- *Answer:*
  - (a) Only the new `.dir` manifest. Every remaining photo blob already exists.
  - (b) Yes. `Image_2.jpg`'s blob (`ba/044df258bd989cbbe84513f14e3616`) is still in `dvc_store`, and DVC never deletes remote objects unless you run `dvc gc --cloud`.
  - (c) Every tag still resolves to a `.dvc` pointer, but `dvc get` fails with missing cache files. The pointers are only as good as the warehouse.

**E6 (hands-on, predict): two views of one folder.**
- With the DVC container running, compare `ls -la cheese_dataset` inside the container with `ls -la cheese_dataset` in a host terminal in the same repo. Then run `ls .dvc/cache/files/md5` on the host after `dvc add`. Predict each output.
- *Answer:*
  - Inside: your images, served through gcsfuse (`data-versioning/docker-entrypoint.sh:11,14`).
  - On the host: an empty directory (created by `mkdir -p /app/cheese_dataset` at `:13` through the `/app` bind mount). The FUSE and bind mounts are private to the container's mount namespace.
  - `.dvc/cache/files/md5` on the host *does* contain two-hex-character folders. `dvc add` copied each image into the cache on your disk through the `/app` bind mount, so the only local copies of the photos live in the cache, not in `cheese_dataset/`.

**E7 (design): connect the two halves.**
- Sketch a small script (new `cli.py` flag) that turns Label Studio annotations into a versioned, labeled dataset.
- *Answer outline:*
  1. Read annotations from `cheeses_labeled/` with `google-cloud-storage`, or use `project.get_labeled_tasks()` (`data-labeling/cli.py:105`).
  2. For each task, take `data.image` (a `gs://…/cheeses_unlabeled/Image_N.jpg`) and the label `annotations[0].result[0].value.choices[0]`.
  3. Copy the image to `gs://<bucket>/images/<label>/Image_N.jpg`, i.e. the folder the DVC container mounts. Because those sub-folders have no placeholder objects, add `--implicit-dirs` to gcsfuse or create the folders in the console.
  4. Run `dvc add cheese_dataset && dvc push`, then commit and tag.
  - The resulting `.dir` manifest now encodes the labels in the relpaths, so a tag pins images *and* labels together, which is what L13's `cheese_4_labels.zip` provides by hand.

**E8 (debugging): Colab cell 19 prints nothing, but cell 20 then crashes with `FileNotFoundError` for `cheese_dataset`. When you point cell 15 at the class repo you get a 403.**
- *Answer:*
  - The class repo has only `dataset_v20`, `dataset_v21` and `dataset_v30` (`git ls-remote --tags`), so `dataset_v25` cannot resolve. `--quiet` hides DVC's error (it raises the log level to CRITICAL), and cell 19's `rm -rf` already removed the folder, so the failure shows up one cell later. Remove `--quiet` to see the real message.
  - The 403 comes from the class bucket `cheese-app-data-versioning`, which is not readable by you (anonymous listing returns 401).
  - Fix: use your own repo URL (with a token if it is private) and your own tags. The `.dvc/config` at those tags points to *your* bucket, which your Colab identity can read.

---

## 10. Errata and open questions

**Errata (with evidence)**
1. **Duplicated README.** `data-versioning/README.md` contains the whole tutorial twice. The duplication was introduced by the rewrite commit `b362f1e` (2026-09-18). The second copy starts on the same line as the closing code fence of the first: line 425 reads `` ```# 🧀 Data Versioning with DVC ``. The later fix commit `b240b1a` edited only the first copy. It deleted service-account steps 1-2 (open the console, find *IAM & Admin → Service Accounts*), so copy 1's list now starts at "3." (`:150`) and no longer says where to go. It also added the "tag is taken" disclaimers (`:321`, `:371`) to copy 1 only. Copy 2 still has the old steps 1-2 and the heading "Create the first dataset version: `dataset_v20`".
2. **README points to a starter that no longer builds.** `data-versioning/README.md:81` says to clone `data-versioning-ac215`, whose `data-versioning@data-versioning-ac215/Dockerfile:36` installs `google-cloud-sdk`. That package is absent from Google's apt repo (index of 2026-10-07; only `google-cloud-cli` 543-588 exist). `main` fixed it in `ebf09c8` but the branch was not updated.
3. **Missing step: initial images.** The main README never says to put the initial dataset into `images/` (`:180-187`), yet it later says "Upload a few *additional* images" (`:338`). The class's own v20 was `Image_1-4.jpg` from `cheeses_unlabeled.zip` (hash reproduced, §3.5).
4. **Misleading tag disclaimer.** "this tag is taken" (`data-versioning/README.md:321`, `:371`) is only true if you forked. After `rm -rf .git` + `git init` (`:95-101`) your repo has no tags.
5. **Old ac215 README bugs** (`data-versioning@data-versioning-ac215/README.md`): no `git branch -M main` before `git push -u origin main` (`:39-43`); `git init` twice (`:30`, `:39`); "Add a remote origin" again in the v21 section (`:148`), which fails.
6. **Wrong CORS explanation.** `data-labeling/README.md:153` attributes the block to "domains that can't be resolved via reverse DNS lookup". CORS is the browser's same-origin policy, satisfied by a response header (§3.3). `:157` ("must be done programmatically"): the console lacks a CORS editor, but `gcloud storage buckets update --cors-file` also works.
7. **Stale file references.** `data-labeling/README.md:162` says "The Dockerfile, Pipfiles and docker-CLI.sh is available". The Pipfiles were removed in `03c3e27`, and the script is `docker-shell-CLI.sh`.
8. **Sample output and listing.** The sample annotation output (`data-labeling/README.md:204-206`) shows `'choices': ['amanita']`, a mushroom from the course's older mushroom app, not a cheese label. The sample `docker container ls` output contains a stray line `data-labeling-data-label-cli-run` (`:95`) from a compose run.
9. **Bucket name lives in two places.** `data-labeling/README.md:164` only says to change the bucket name in `docker-shell-CLI.sh`. `data-labeling/docker-compose.yml:17` hard-codes it too, so the compose "Extra" silently targets `cheese-app-data-demo`.
10. **Unused env vars and dead code.**
    - `GCP_PROJECT` / `GCP_ZONE` are passed everywhere but never read (`grep` over both repos).
    - `data-versioning/docker-entrypoint.sh:10` creates an unused `/mnt/gcs_bucket`.
    - `data-versioning/docker-entrypoint.sh:12` prints "GCS bucket mounted" unconditionally.
11. **Small `cli.py` defects.** Typo "-k argument i required" (`data-labeling/cli.py:123`). The `-m` help text says "View the CORS configuration" (`:153`) but prints all bucket metadata. `parser` is a module global that only exists when `cli.py` runs as `__main__` (`:135`), so importing `main()` elsewhere would fail on `parser.error`.
12. **Inconsistent labels and descriptions.**
    - Tutorial numbering: "Tutorial (T6)" (`data-labeling/README.md:1`) vs the ac215 README "Tutorial (T7)" (`data-versioning@data-versioning-ac215/README.md:1`). Main removed the number in `d646ee3`.
    - Old UI path: "Docker>Preferences>Resources" (`data-labeling/README.md:18`); it is now Settings.
    - The main README says "You will do this in two rounds:" and then lists four steps (`data-versioning/README.md:11-19`).
13. **Colab notebook issues** (cells as extracted from `colab/L11_data_versioning_view.ipynb`):
    - Cell 19 uses `--rev dataset_v25`, which does not exist in the class repo. Its `--quiet` flag hides the resulting error.
    - Stale output: cell 20's stored `Number of items: 3` comes from a 2024-10-04 run by another user (no execution count). Cells 7-19 come from the instructor's 2025-10-28/29 run (cell 17 prints `Number of items: 5`). A viewer could wrongly read "3" as the result of the `dataset_v25` cell.
    - The header says "Fall 2025" and links the 2023 course site.
    - Cell 2 says to complete "Data Labeling & Versioning" but links only to `dlops-io/data-labeling`.
    - `cv2`, `numpy`, `pandas` and `google.cloud.storage` are imported but unused. Cell 9 must still run, because it imports `auth`, which cell 11 uses.
    - The defaults point at the class repo/bucket, which students cannot read.
    - The README's "private repository" (`data-versioning/README.md:108`) conflicts with anonymous `dvc get` from Colab.
14. **Two halves, two buckets.** `pipeline-flow.png` (unreferenced) puts `dvc_store` inside `cheese-app-data-demo` next to `cheeses_labeled`. The code uses a separate bucket `cheese-app-data-versioning` and versions `images/`, not the labeled output.
15. **Course-site numbering.** `_modules/week-07.md:5-11` calls this session "Lecture 10" (Oct 13) and App Design "Lecture 11", while `tutorials_demo.md:148` calls it Lecture 11.

**Open questions (could not determine from the sources)**
- **Monitoring:** the lecture title includes it, but no L11 tutorial or repo covers it. The course map has a later "Lecture 17: Evaluating and Monitoring ML Systems in Production" (`tutorials_demo.md:218`) with no repo listed here. The Ed lesson slides (not accessible here) may cover data monitoring, such as drift checks.
- **AWS variant:** `dlops-io/data-labeling-aws` (linked in `tutorials_demo.md:154`) was not cloned or examined.
- **Label Studio UI drift:** `label-studio:latest` was last pushed 2026-09-29. I could not verify:
  - whether "Treat every bucket object as a source file" (`data-labeling/README.md:130`) still exists next to the newer "Import Method" field (`:129`, added Oct 2025);
  - the exact object key format of target-storage annotations (with or without a `.json` extension);
  - the default pre-signed URL expiry;
  - whether legacy API tokens are enabled by default.
- **gcsfuse 3.x defaults:** the build installs whatever gcsfuse is current (3.12.1 on 2026-10-01). I did not confirm its default `implicit-dirs` behaviour or metadata-cache TTLs, or whether `--key-file` prints a deprecation warning.
- **Linux hosts:** whether `dvc init` / scmrepo inside the root container trips git's "dubious ownership" check on a bind-mounted repo owned by uid 1000 (no owner-validation handling found in scmrepo 3.5.2). macOS Docker Desktop evidently works (the instructor's container commit).
- **Exact outputs:** nothing was executed here (no Docker/GCP in this environment). Printed messages come from the source: the `dvc init` / `remote add` / `push` strings in DVC 3.63.0, and the `print` calls in `cli.py`. The exact `N files pushed` count (I expect images + 1) and gcsfuse's log wording are unverified.
- **Class bucket access:** whether enrolled students are granted read access to `gs://cheese-app-data-versioning` (anonymous access is denied). If so, the notebook's defaults work for them.
- **The 5th image in v21 (resolved):** the class `dataset_v21`/`dataset_v30` manifest (`3280f8f9…`, 5 files, 785,481 bytes) adds the 174,380-byte `csm_Gruyere_Website_Header_Desktop_1920x1080px_Homepage_Curling_cdd2c6527c.jpg.webp`, named in Colab cell 13's stored output. It is not in `cheeses_unlabeled.zip`. It looks like a web-downloaded Gruyère header image; its exact origin is unknown.
- **Did `dataset_v25` ever exist?** It is absent today. The notebook's only evidence for it is cell 20's stale 2024 output (3 items), so the class repo may have had such a tag in 2024 that was later deleted. This cannot be confirmed from the clone.

_Verified against the repos on 2026-10-13 (adversarial check)._
