# L11 lecture slides — Data Labeling, Versioning and Monitoring

**Provenance.** One deck, `L11_data_management_and_versioning_Final_2_`, 41 slides. Its title
slide reads "Lecture 11: Data Labeling, Versioning and Monitoring" (AC215/E115, Pavlos
Protopapas, SEAS/Harvard). The file name says "data management and versioning", but the title
slide gives the lecture's name. These are the instructor's lecture slides (PDF), provided by the
student for study; the PDFs are not in this repository; slide numbers are PDF page numbers. I
wrote this digest from the deck's extracted text and from all five contact sheets. I also
enlarged slides 5, 6, 8, 9, 13, 14, 15, 18, 21, 24, 34, 35 and 41 to read their diagrams,
screenshots, arrows and highlights. Everything below is in my own words. Only short titles,
terms, paths and single command lines are quoted. The tutorial side of the lecture is in
[`digest.md`](digest.md). Below, "README" means the `dlops-io/data-labeling` and
`dlops-io/data-versioning` READMEs as recorded there.

Notes for anyone citing the deck:

- **Printed footers match the PDF pages** wherever they appear. Slides 1, 25 and 28–33 have no
  footer, and on slides 5 and 14 the QR code covers it.
- **Many slides are builds** (the same slide with one more element revealed). These are slides
  8–12 (the recap questions, then their answers one at a time), 15–18 (the same SuperAnnotate
  bullet; 16–18 then draw a curation diagram piece by piece), 29–32 (the gcsfuse flow, one box per
  slide, after slide 28's introduction) and the repeated agenda slides 2/3/19/37. Cite the last
  slide of a build for the complete picture.
- **How the deck maps onto this episode.** Slides 5–14 are the `data-labeling` tutorial, and
  slides 26–34 are the `data-versioning` tutorial. Slide 26 links the same Colab notebook that
  `digest.md` downloaded (id `1RRQ1SlHq5lKK76R8LoQdi5LjCnND3jTq`). The surrounding slides (4,
  15–25, 35–36) give the theory and tool landscape, which no README covers.
- **What the slides leave to the tutorial.** The slides never show CORS, signed URLs, Label
  Studio's source/target storage, any `dvc` or `git tag` command, md5 manifests, `dvc_store`, or
  the container's privileged flags. Those come only from the READMEs (`digest.md` §3–§5).
- **Monitoring has slides but no tutorial.** Slides 38–40 are conceptual only. This answers the
  open question in `digest.md` §10: the deck's monitoring section covers why to monitor, three
  approaches and three tools, with no code or demo.

## Outline

The agenda slide, "Outline", lists three numbered sections: Data Labeling, Data Versioning, Data
Monitoring. It appears plain on slide 2, and then on slides 3, 19 and 37 with the current section
in bold.

- **Slide 1 · title.**
- **Slides 2–3 · agenda** (slide 3 marks "Data Labeling" as current).
- **Slides 4–18 · 1. Data Labeling.**
  - 4: why label data (five reasons).
  - 5: the tutorial's goal, the cheese dataset (Brie, Gruyère, Gouda, Parmigiano) and Label
    Studio. It has the repo link and a QR code, beside a cartoon of a mouse with cheese.
  - 6: "Cheese App Data Pipeline", the four-step diagram under the red question "How do we do
    this?".
  - 7: why Label Studio (manual labeling is slow and inconsistent; easy interface; run locally in
    Docker for privacy).
  - 8–12: "Recap Concepts Before Labeling". This is a quiz build:
    - 8 asks whether you remember three earlier concepts (Docker Network, Cloud Storage and
      Credentials, Docker Compose);
    - 9 bolds the first one;
    - 10, 11 and 12 reveal one definition each.
  - 13: "Tutorial: Data Labeling: Label Studio + CLI", the two-container architecture diagram
    with four numbered callouts (1, 2, 3 and 5).
  - 14: the tutorial's steps (create a bucket, run the labeling container, follow the repo). It
    has the link and QR code, beside a cartoon character hauling huge wedges of cheese.
  - 15–18: "Data Labeling (Continued)", other labeling tools:
    - 15: SuperAnnotate for multimodal labeling, with a screenshot of its home page;
    - 16–18: a build of a data-curation flow from a raw-ingest bucket through a "Curation
      Engine" into train, validation and discard folders.
- **Slide 19 · agenda** ("Data Versioning" in bold).
- **Slides 20–36 · 2. Data Versioning.**
  - 20: why version data (five reasons).
  - 21: "From Object Storage to a Data Lake", the bucket-versus-data-lake card diagram.
  - 22: "Data Versioning: Concepts and Technologies", three concepts (data lake, table format,
    time travel) next to the tools that implement them.
  - 23: four approaches to versioning, ending in a teaser ("wait for it").
  - 24: the punchline. A terminal listing twelve renamed copies of one paper (such as
    `…final-final-v3-final.tex`), and an illustration captioned "Friends don't let friends do
    this".
  - 25: "Choosing a Data Versioning Approach", a three-row table (DVC, lakeFS, Delta
    Lake/Iceberg).
  - 26–34: the versioning tutorial:
    - 26: steps (run the versioning container, test versions from Colab), with links to the repo
      and the Colab notebook and a QR code;
    - 27: the one new concept it needs, "Mounting disks from GCS to a container";
    - 28: what `gcsfuse` is;
    - 29–32: "How the gcsfuse mounting works?", a four-box build: Authenticate → Bucket Mounting
      → Connecting the Application → Using the Data;
    - 33: why mount at all;
    - 34: the `gcsfuse` command, taken apart token by token.
  - 35: "Takeaway": no one versioning tool is the industry standard. Below it is a meme
    captioned "You're not that guy, pal, trust me".
  - 36: "DVC vs lakeFS vs Delta Lake/Iceberg", the comparison table again with an "Example"
    question per tool.
- **Slide 37 · agenda** ("Data Monitoring" in bold).
- **Slides 38–40 · 3. Data Monitoring.**
  - 38: why monitor data (five reasons).
  - 39: three approaches (rules-based, anomaly detection, lineage and metadata).
  - 40: three tools (Monte Carlo, Datadog, Soda).
- **Slide 41 · "THANK YOU"**, with an anime character striking a pose.

## Key ideas

1. **Labels are the ground truth a supervised model learns from and is graded against.**
   Accurate, consistent labels make a better model. A wrong label teaches a wrong pattern. Human
   annotators add context that automation misses. Labeling the model's own mistakes and the hard
   edge cases is how the next, better dataset version is made. (Slide 4)
2. **The tutorial's job is to turn unlabeled cheese photos into labeled ones.** The class set has
   four cheeses: Brie, Gruyère, Gouda and Parmigiano. The photos start as unlabeled web images
   and are annotated with Label Studio. (Slide 5)
3. **The data pipeline routes everything through one bucket.**
   - The goal (top of slide 6) is to go from unlabeled to labeled to training in Colab.
   - The "how" runs along the bottom:
     - (1) put the unlabeled photos into the GCS bucket `cheese-app-data-demo`, under
       `cheeses_unlabeled`;
     - (2) a data-labeling container reads from and writes to that bucket;
     - (3) it serves Label Studio to a team of annotators;
     - (4) Colab reads the labeled side (`cheeses_labeled`) to train.

   (Slide 6)
4. **Use a labeling tool, and run it yourself.** Labeling by hand at scale is slow and
   inconsistent. Label Studio gives annotators a simple interface. Running it locally in a Docker
   container keeps the data out of third-party services. (Slide 7)
5. **The labeling setup reuses three things you already know.**
   - A Docker network lets containers talk to each other.
   - Cloud storage plus credentials stores data online and controls who can access it.
   - Docker Compose defines and runs several related containers together.

   The slides pose these as a recall quiz before revealing each answer. (Slides 8–12)
6. **The labeling station is two containers sharing one key.**
   - The Label Studio container exposes port 8080 to the browser and keeps its state in a mounted
     local volume.
   - The CLI container has the source code mounted, and you shell into it to run `cli.py`.
   - Both get the secrets folder mounted and the `GOOGLE_APPLICATION_CREDENTIALS` environment
     variable set, so both can reach the bucket that holds the images and labels.

   (Slides 13–14)
7. **At scale, labeling becomes a platform and a curation step.**
   - Widely used platforms such as SuperAnnotate handle multimodal labeling: image, video and
     audio, and also the data for LLM post-training (RLHF, SFT).
   - A curation engine sorts a raw-ingest area of the data lake into a training set, a
     validation set and a discard pile for low-quality items.

   (Slides 15–18)
8. **Data needs versioning for five reasons.**
   - Keep track of changes.
   - Protection: back up and roll back.
   - Compliance: auditable change history.
   - Collaboration between several users.
   - Efficiency: avoid duplicate copies through snapshots or content-based storage.

   (Slide 20)
9. **A data lake is a bucket plus tools, not a different place.** A bucket only stores named
   objects with metadata. A data lake keeps the data in the bucket and adds tools around it for
   five jobs:
   - ingesting new data;
   - finding data;
   - controlling who may use it;
   - preparing it for analysis or training;
   - returning to earlier versions.

   (Slide 21)
10. **Three concepts, each with its tools.**
    - The *data lake* is the overall architecture.
    - A *table format* is a set of rules that organizes data files and metadata into tables, with
      schemas and versions. Delta Lake and Apache Iceberg are two alternative open table formats.
    - *Time travel* means querying an earlier table version. It only works while that version's
      metadata and files are still kept.
    - The *data version-control tools* are DVC, which versions dataset files and models
      alongside a Git project, and lakeFS, which gives Git-like branches and commits for
      collections of objects in cloud storage.

    (Slide 22)
11. **There are four ways to version data, and one way not to.**
    - *File-based*: hashes plus metadata, with Git holding the history (DVC).
    - *Object-store*: the store's own branches, commits and rollbacks, with no Git needed
      (lakeFS).
    - *Table-based*: transaction logs, metadata and snapshots for structured tables (Delta Lake,
      Iceberg).
    - *Full snapshots*: a complete copy of the dataset at chosen points, used when appropriate.

    The anti-pattern is copying files and encoding the version in the file name ("final-final-v3"),
    which the deck mocks. (Slides 23–24)
12. **Pick the tool by the job.**
    - DVC keeps the data used by each model experiment. It fingerprints each file, and Git
      records which fingerprints make up each version. Example question: which images trained
      this model?
    - lakeFS shares datasets in cloud storage, keeping its own history without Git. Example
      question: can I test new images before everyone uses them?
    - Delta Lake and Iceberg are for tabular data. They record table changes so you can read an
      earlier version. Example question: what did this table contain before the change?

    (Slides 25, 36)
13. **There is no single industry standard.** No one versioning tool wins everywhere; pick by what
    kind of data you have, how much of it, and which platform you are on. (Slide 35)
14. **The versioning tutorial has two halves.** You run a data-versioning container, then test the
    stored versions from a Colab notebook. (Slide 26)
15. **`gcsfuse` makes a GCS bucket look like a local folder inside a container.** Mounting
    happens in four stages:
    - *Authenticate*: the service-account credentials let gcsfuse access GCS.
    - *Bucket Mounting*: the bucket's files appear as the folder `/mnt/gcs_data`.
    - *Connecting the Application*: a bind mount makes `/mnt/gcs_data/images` also appear at
      `/app/cheese_dataset`.
    - *Using the Data*: the app and DVC treat `/app/cheese_dataset` as a local folder, while reads
      and writes actually go to the bucket.

    (Slides 27–32)
16. **Why mount instead of download.** The dataset stays in cloud storage, and nobody keeps a
    separate local copy. Programs read and write it as if it were local files. Everyone works on
    the same central dataset. (Slide 33)
17. **The mount command has four parts.** In order: the tool (`gcsfuse`); the key file that
    authenticates you; the bucket name, which is unique across GCP; and the mount point inside the
    container. (Slide 34)
18. **Data needs monitoring for five reasons.**
    - Quality: missing values, wrong formats, columns that change unexpectedly.
    - Freshness: does new data arrive on time?
    - Anomalies and drift: for example, suddenly far more images of one cheese.
    - Cost: what storing and processing the data costs.
    - Finding problems: which pipeline step failed between the source and the model.

    (Slide 38)
19. **Three monitoring approaches.**
    - Rules-based: when the schema and pipeline expectations are set in advance, test those
      specific constraints.
    - Anomaly detection: ML models keep watching baseline metrics and raise a flag on unusual
      shifts or drops.
    - For all other cases: follow the data's lineage and metadata end to end, which makes it
      quick to find the root cause in a complex pipeline.

    (Slide 39)
20. **Three data-observability tools.**
    - Monte Carlo: ML-driven end-to-end observability, watching freshness, volume and schema
      drift across warehouses.
    - Datadog: application tracing combined with automated data profiling, next to the
      infrastructure monitoring.
    - Soda: SQL-based data tests that engineering teams write and run as code.

    (Slide 40)

## Diagrams

- **Slide 6 · Cheese App Data Pipeline.** Two layers: the goal along the top and the mechanism
  below, with numbered pink circles 1–4.
  - *Top row (the goal):*
    - a dotted box "Unlabeled" holding six mixed cheese thumbnails;
    - a long pale-green arrow to the right, under a large red "How do we do this?";
    - a dotted box "Labeled" with four rows, `brie`, `gouda`, `parmigiano` and `gruyere`, each
      with its thumbnails;
    - a short green arrow to a yellow box "Colab {training}" with a notebook icon (circle 4);
    - a double-headed arrow from Colab to an orange group-of-people icon.
  - *Bottom (the how):*
    - Circle 1: a blue arrow down from the Unlabeled box into a pink dotted band. The band is
      labelled "GCS Bucket: `cheese-app-data-demo`". It holds a cloud icon and two folder chips,
      `cheeses_unlabeled` (red text) and `cheeses_labeled` (green text).
    - Circle 2: a vertical double-headed arrow between the bucket and a purple box "Data
      Labeling", which has an inner beige "Container" label.
    - Circle 3: a curved pink arrow from the container to a small "Label Studio" window with
      cheese thumbnails. A dark-red group of people sits below the container, with double arrows
      to both the container and the Label Studio window (the annotators).
    - An elbow-shaped blue connector, double-headed, runs from the bucket up to the Colab box.
  - *Purpose:* frame labeling as the missing middle step between raw photos and training. All
    traffic goes through the one bucket.
  - *For a re-draw:* draw the top row first with a big "?" on the long arrow. Then reveal the
    bucket, container, Label Studio and annotators underneath as the answer. Light 1 → 2 → 3 → 4
    in turn.
  - *Compared with the tutorial:* "Labeled" is drawn as photos sorted by cheese. In the tutorial,
    Label Studio writes one JSON object per submitted annotation into `cheeses_labeled/` and does not
    sort the photos (`digest.md` §3.1). The slide shows only the labeling half. Unlike the repo's
    unreferenced `pipeline-flow.png` (`digest.md` §10, item 14), it has no versioning container
    and no `dvc_store`.
- **Slide 13 · Label Studio + CLI architecture.**
  - *Layout:* two green boxes sit side by side in the middle, "Label Studio Container" on the
    left and "CLI Container" on the right. Above them, at the top centre, a grey cloud box
    "GCS Bucket" is labelled "Images + Labels". A T-shaped connector joins both containers to the
    bucket, with arrowheads into the bucket and into each container.
  - *Callouts (red, numbered):*
    - **1 · Mount external folders.** This sits under a central "Secrets" box at the bottom,
      which is connected to both containers. Two more mounts, each with an up-arrow labelled
      "Mount": a folder `docker-volume/label-studio` into the Label Studio container, and a
      "Source Code" box (with a `</>` icon) into the CLI container.
    - **2 · Set Environment Variable to access GCS Bucket.** A dashed band runs across the lower
      part of both containers, reading `ENV: GOOGLE_APPLICATION_CREDENTIALS`.
    - **3 · Expose port 8080.** A line marked "HTTP 8080" runs from the Label Studio container up
      to a browser thumbnail of the Label Studio UI, captioned "Browser - http://localhost:8080".
    - **5 · Shell into container.** An arrow runs from the CLI container up to a terminal prompt
      icon captioned "Terminal - cli.py".
    - The numbering skips 4.
  - *Purpose:* the whole Part A setup in one picture. It shows what is mounted, which variable
    carries the key, which port is published, and where you type.
  - *What it leaves out:* no direct container-to-container link is drawn; the containers meet
    only through the shared connector up to the bucket, the shared "Secrets" box and the ENV
    band. In the tutorial, the CLI reaches Label Studio's API over the Docker network at
    `http://data-label-studio:8080` (`digest.md` §3.4), the kind of link slide 10's "Docker
    Network" recap describes.
- **Slides 16–18 · the curation flow (a build).**
  - Slide 16 shows only a pink dotted bucket band with a cloud icon, labelled "GCS Bucket" and
    holding the path `gcs://production-ml-data-lake/raw_unstructured_ingest/` in red.
  - Slide 17 adds a hollow arrow to a green inverted trapezoid (a funnel) labelled "Curation
    Engine".
  - Slide 18 adds three hollow arrows fanning out of the funnel to three coloured path chips:
    `/curated_train/` (orange), `/curated_val/` (purple) and `/discard_low_quality/` (dark
    red).
  - *Purpose:* in an industrial setting, raw data is filtered and split before or alongside
    labeling, and low-quality items are thrown out. The diagram sits under the SuperAnnotate
    bullet.
  - *For a re-draw:* draw a funnel that sorts a stream of mixed items into train, validation and
    reject bins.
- **Slide 21 · From Object Storage to a Data Lake.** Two rounded cards joined by a small
  connector.
  - *Left card:* a purple tag "BASE STORAGE", an archive-box icon and the title "Bucket". Its one
    line says it stores objects identified by names, with object metadata.
  - *Middle:* a small pale-blue box "Add tools to manage & use data" with a right arrow.
  - *Right card*, outlined in blue: a tag "ARCHITECTURE", a hub-and-spoke icon and the title
    "Data Lake". A bold line says the data stays in the bucket and tools around it help. Below it
    are five green check marks: add new data, find data, decide who may use it, prepare it for
    analysis or training, and return to earlier versions with versioning tools.
  - *Purpose:* a data lake is the same storage plus a tool layer, and versioning is one of those
    tools.
  - *For a re-draw:* draw a plain bucket, then grow a ring of five tool icons around it, without
    moving the data.
- **Slide 24 · the anti-pattern.**
  - *Top:* a dark terminal screenshot of `ls` in a folder named for a paper project. It lists
    twelve `.tex` files whose names carry the version history: `-v1`, `-PP-v1.1-IB-PO-v2`,
    `-final`, `-final-v2`, `-final-final-v3-final`, and so on.
  - *Bottom:* an illustration of four people at a table in front of a wall-sized code screen,
    captioned "Friends don't let friends do this".
  - *Purpose:* the "wait for it" fifth approach promised on slide 23, which is versioning by
    copying and renaming. It shows why a real tool is needed.
  - *For a re-draw:* a folder that fills up with ever-longer "final" file names until it
    overflows.
- **Slides 28–32 · How the gcsfuse mounting works (a build).**
  - *Layout:* boxes are added left to right, joined by plain lines. Each box is a darker shade of
    green than the one before:
    - "Authenticate" (slide 29);
    - "Bucket Mounting" (30);
    - "Connecting the Application" (31);
    - "Using the Data" (32, darkest, white text).
  - *Captions:* an outline down-arrow under the newest box points to its caption. Only the newest
    caption is shown on each slide:
    - 29: the service-account key is what lets gcsfuse into GCS;
    - 30: gcsfuse makes the bucket's files appear as a regular folder `/mnt/gcs_data`;
    - 31: a bind mount makes `/mnt/gcs_data/images` also appear at `/app/cheese_dataset`;
    - 32: the app and DVC treat `/app/cheese_dataset` as an ordinary folder, but every read and
      write actually lands in the bucket.
  - Slide 28 introduces `gcsfuse` (highlighted in magenta), and the paths are highlighted in
    green.
  - *Purpose:* the chain of three hops: key → bucket mounted as a folder → that folder re-exposed
    where the app expects it.
  - *For a re-draw:* draw a cloud bucket, a pipe labelled `gcsfuse` into `/mnt/gcs_data`, and a
    second short pipe (bind mount) from its `images` subfolder to `/app/cheese_dataset`. DVC sits
    on the last folder. This matches `docker-entrypoint.sh` (`digest.md` §3.7).
- **Slide 34 · anatomy of the mount command.**
  - *Top:* the full command in grey monospace on two lines.
  - *Below:* a single colour-coded version, with each token on its own background: `gcsfuse`
    (magenta), the `key-file=$GOOGLE_APP_CREDS` flag (blue), `$GCS_BUCKET_NAME` (pink) and
    `/mnt/gcs_data` (green).
  - *Captions:* curved arrows drop from each token to a caption:
    - the command that mounts;
    - points to the credentials file that authenticates us;
    - the bucket to mount, whose name is unique across GCP;
    - the path inside the container where the data appears.
  - *For a re-draw:* type the command, then split it into four coloured chips, each with a
    caption.
- **Tables (layout, not mechanisms).** These are useful as the content of comparison scenes.
  - **Slide 22:** two purple-headed columns, "Concepts" and "Tools and technologies". The
    entries sit side by side without pairing up: data lake is beside table formats (Delta Lake,
    Apache Iceberg), table format beside the data version-control tools (DVC), and time travel
    beside lakeFS.
  - **Slide 25:** three columns: Tool, Useful for, How it keeps versions.
  - **Slide 36:** tools as columns (DVC, lakeFS, Delta Lake / Iceberg) and three rows: Useful
    when, Example, Version history.

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial (READMEs and scripts) |
|---|---|---|
| "Data Labeling", "annotate" | 4–5 | The README has the same idea in its "Annotate Data" step. |
| "Ground Truth", "Model Quality", "Real-World Context", "Continuous Improvement" | 4 | Not in the README. |
| "Label Studio" | 5, 7, 13 | Same tool. The README names the image `heartexlabs/label-studio:latest`, and `docker-shell.sh` runs it as container `data-label-studio`. |
| "Cheese App Data Pipeline"; "Unlabeled" / "Labeled" | 6 | The README uses the same bucket and folder names (`cheese-app-data-demo`, `cheeses_unlabeled`, `cheeses_labeled`). In Label Studio's UI the two folders are "Source storage" and "Target storage", terms the slides never use. "Labeled" holds JSON annotations, not sorted photos. |
| "Data Labeling Container" | 6, 14 | No single container has this name. The README starts `data-label-studio` (`docker-shell.sh`) and `data-label-cli` (`docker-shell-CLI.sh`). |
| "Colab {training}" | 6 | L11's tutorials do no training. Their Colab notebook only reads dataset versions with `dvc get`. Training is a later lecture. |
| "Docker Network", "Cloud Storage and Credentials", "Docker Compose" | 8–12 | In the tutorial these are the network `data-labeling-network` (created by `docker-shell.sh`), the key `../secrets/data-service-account.json`, and the README's "Extra" `docker-shell-compose.sh`. |
| "Label Studio Container", "CLI Container" | 13 | The scripts name the containers `data-label-studio` and `data-label-cli`. |
| "Expose port 8080", "HTTP 8080" | 13 | `docker-shell.sh` publishes the port with `-p 8080:8080`. In earlier lectures this is called "publishing" a port. |
| "Mount external folders"; `docker-volume/label-studio`; "Secrets"; "Source Code" | 13 | The scripts' folder is `docker-volumes/label-studio` (plural), mounted at `/label-studio/data`. The secrets go to `/secrets`, and the source code to `/app`. |
| "Shell into container", "Terminal - cli.py" | 13 | In the README you run `docker-shell-CLI.sh`, then `python cli.py` with `-c`/`-m`/`-p`/`-t`. |
| "Data Pipeline" | 14, 26 | The README has the same idea. |
| "multimodal labeling", "RLHF", "SFT" | 15 | Not in the README. |
| "Curation Engine", `raw_unstructured_ingest`, `curated_train`/`curated_val`/`discard_low_quality` | 16–18 | Not in the README. The path is written `gcs://…`. Real GCS URIs use `gs://`. |
| "Bucket" ("BASE STORAGE") vs "Data Lake" ("ARCHITECTURE") | 21–22 | Not in the README. |
| "Table format", "open table formats", "Time travel" | 22 | Not in the README. |
| "Data version-control tools" | 22 | The starter branch's README (`data-versioning-ac215`, line 69) spells DVC out as Data Version Control; the `main` README never expands the name. |
| "File-based", "Object-store", "Table-based versioning", "Full snapshots" | 23 | The tutorial teaches only file-based versioning (DVC). |
| "fingerprint" | 25 | `digest.md` and DVC say "md5 hash". The README's pointer file is `cheese_dataset.dvc`, which holds the md5 of a `.dir` manifest. |
| "Data Versioning Container" | 26 | The README calls it "the DVC container" (section "Start the DVC container"). The container is named `data-version-cli`. |
| "Test Data Version Notebook" | 26 | The notebook's own title is "Tutorial - Data Pipelines, Labeling, Versioning, Cloud Storage" (`digest.md`, header). |
| "Mounting disks from GCS to a container"; `gcsfuse` | 27–34 | The README covers this in "About docker-entrypoint.sh". The disks are really a bucket, not disks. |
| "Authenticate", "Bucket Mounting", "Connecting the Application", "Using the Data" | 29–32 | Not named in the README. The first three match `docker-entrypoint.sh`: the key file (gcsfuse's own `--key-file`; the separate `gcloud auth activate-service-account` line serves `gcloud`), then `gcsfuse`, then `mount --bind`. "Using the Data" is the `dvc` work that follows. |
| "service-account credentials" | 29 | The README's key is `data-service-account.json`. |
| "bind mount" | 31 | Here this means the Linux `mount --bind` run *inside* the container. The README's Docker `-v` folder mounts are also bind mounts, at the host-to-container layer. Same word, two layers. |
| `$GOOGLE_APP_CREDS` | 34 | A shortened label in the colour-coded line. The real variable, which the slide's own top line uses, is `GOOGLE_APPLICATION_CREDENTIALS`. |
| "Data Quality", "Data Freshness", "Anomalies and Drift", "Cost Control", "Finding Problems" | 38 | No tutorial. |
| "Rules-Based", "Anomaly Detection", "lineage", "root-cause analysis" | 39 | No tutorial. |
| "data observability", "data profiling", "schema drift" | 40 | No tutorial. |

## Commands and code on the slides

The deck has very little code. There are no `dvc`, `git`, `docker` or `cli.py` command lines.

- Slide 34, the mount command (shown on two lines):
  - `gcsfuse --key-file=$GOOGLE_APPLICATION_CREDENTIALS $GCS_BUCKET_NAME /mnt/gcs_data`
- Slide 34, the colour-coded version. On the slide itself the flag starts with a single long
  dash (an em dash), not two hyphens (Conflict 10).
  - `gcsfuse —key-file=$GOOGLE_APP_CREDS $GCS_BUCKET_NAME /mnt/gcs_data`
- Slide 24, the terminal screenshot: `ls`, listing files such as
  `ICML-subm-final-final-v3-final.tex`.
- Paths and names shown in diagrams:
  - slide 6: `cheese-app-data-demo`, `cheeses_unlabeled`, `cheeses_labeled`;
  - slide 13: `http://localhost:8080`, `ENV: GOOGLE_APPLICATION_CREDENTIALS`,
    `docker-volume/label-studio`, `cli.py`;
  - slides 16–18: `gcs://production-ml-data-lake/raw_unstructured_ingest/`, `/curated_train/`,
    `/curated_val/`, `/discard_low_quality/`;
  - slides 30–32: `/mnt/gcs_data`, `/mnt/gcs_data/images`, `/app/cheese_dataset`.

## What the lecture stresses

- **Label quality is model quality.**
  - Wrong labels teach wrong patterns.
  - Labels must be consistent as well as accurate.
  - Labeling the model's errors and hard edge cases is how the next dataset version gets better.

  (Slide 4)
- **Manual labeling at scale is slow and inconsistent**, so use a tool. Run that tool locally in
  Docker so the data is not uploaded to an outside service. (Slide 7)
  - Nuance for the video: in the tutorial the images and labels still live in *your own* GCS
    bucket. The browser fetches images from GCS directly through signed URLs (`digest.md` §3.2).
    "Private" here means no third-party labeling service sees the data.
- **Check your prerequisites first.** Before you label, make sure you can explain Docker
  networks, cloud credentials and Compose. The deck tests this as a quiz. (Slides 8–12)
- **Curate before you train.** Split the data into train and validation sets, and throw out
  low-quality data on purpose. (Slides 16–18)
- **Never version by renaming files.** "Friends don't let friends do this" is the deck's one
  outright prohibition. (Slides 23–24)
- **Time travel has a condition:** an old version can be read only while its metadata and files
  are still kept. (Slide 22)
- **Full snapshots are taken only at selected points**, "when appropriate" (slide 23). Slide 20
  lists snapshots, next to content-based storage, among the ways to avoid needless duplication.
  (Slides 20, 23)
- **Git or no Git is the dividing line.**
  - DVC needs Git.
  - lakeFS and the table formats keep their own history.

  The deck repeats this in both comparison tables. (Slides 23, 25, 36)
- **No single standard.** The choice depends on data type, scale and platform. The deck
  highlights "no single" in yellow, and a meme warns the viewer against thinking they are the
  exception. (Slide 35)
- **Mount, don't copy.** Mounting keeps one central dataset in the cloud, so nobody needs a
  separate local copy. (Slide 33)
- **Bucket names are unique across GCP**, so every student needs their own name. (Slide 34)
- **Monitoring includes finding the broken step.** Next to quality, freshness, drift and cost,
  slide 38 lists locating the step that failed between source and model, and slide 39 uses
  lineage and metadata for root causes in complex pipelines. (Slides 38–39)
- **Three monitoring approaches.** Rules when the expectations are predefined, ML anomaly
  detection on baseline metrics, and lineage plus metadata for all other cases. (Slide 39)

## Pointers

- **Tutorial repo `data-labeling`:** https://github.com/dlops-io/data-labeling. Linked with a QR
  code on slide 5, and again as "Data Labeling" with a QR code on slide 14.
- **Tutorial repo `data-versioning`:** https://github.com/dlops-io/data-versioning (slide 26, with
  a QR code).
- **"Test Data Version Notebook"** (Colab), slide 26: the URL ends in
  `1RRQ1SlHq5lKK76R8LoQdi5LjCnND3jTq?authuser=1`. It is the same notebook as
  `colab/L11_data_versioning_view.ipynb` in `digest.md`.
- **Earlier lectures recalled:**
  - slides 8–12 recall Docker networks (L04, `port_toy`), Docker Compose (L03/L04), and cloud
    storage and credentials (L10);
  - the "Expose port" idea on slide 13 also comes from L04 and L10.
- **Tools named without links:**
  - SuperAnnotate (slide 15, home-page screenshot);
  - Delta Lake, Apache Iceberg, DVC and lakeFS (slides 22–23, 25, 36);
  - `gcsfuse`, described as an open-source tool by Google (slide 28);
  - Monte Carlo, Datadog and Soda (slide 40).
- **No homework, milestone or reading is mentioned** anywhere in the deck. The monitoring section
  has no tutorial or demo.

## This video and the slides

**Basis.** The video is not scripted yet. This folder has no `BRIEF.md`, `script.md`, `ASSETS.md` or `assets/terminal/`. The map below therefore uses the ten planned sections in [`digest.md`](digest.md) §8, the study guide (`MLOps_Learning/guides/L11-data-labeling-versioning.md`) and every slide: the extracted text, all five contact sheets, and larger renders of slides 6, 13, 21 and 34. With no captures yet, "what the tutorial does today" means the two repos at the commits recorded in `digest.md` (`data-labeling` @ `03c3e27`; `data-versioning` README @ `b240b1a`, starter code @ `23762e4`). The lines that the conflicts below depend on were re-read in those clones on 2026-10-16: `data-labeling/docker-shell.sh:15-16`, `data-labeling/docker-shell-CLI.sh:24`, the README's pre-signed-URL and CORS steps (`data-labeling/README.md:131`, `:149-159`), and both copies of `docker-entrypoint.sh` (gcsfuse at line 11 on `main`, line 10 on the starter). When `assets/terminal/` and `ASSETS.md` exist, re-check Conflicts 4, 9 and 10 against them; if they disagree, the captures win.

**One README image is a lecture diagram.** `data-labeling/data-labeling-flow.png`, the figure at the top of the README (`data-labeling/README.md:5`), is the same drawing as slide 6. The repo's unreferenced `pipeline-flow.png`, which plan §1 wants to re-draw, is that drawing extended to the whole pipeline. It adds a Data Versioning container, a `dvc_store` folder in the same bucket, a GitHub box holding both repos, and version tags "v1.0, v2.0" on the labeled set. Its corner carries the page number 16, so it looks like a slide from an earlier version of the deck. This deck does not contain it: here the pipeline picture stops at labeling (slide 6), and versioning is explained with the gcsfuse flow (slides 29–32) instead.

### 1. Map: planned sections ↔ slides

| # | Planned section (`digest.md` §8) | Slides on the same ground | Relation |
|---|---|---|---|
| 1 | The map (2 min) | 4, 6, 36 (the DVC example question) | Same concept for the labeling half: slide 6 is the README's flow figure. The versioning half of the plan's picture (from `pipeline-flow.png`) is not in this deck, and the code contradicts slide 6's ending, labeled photos flowing into Colab training (Conflict 1). |
| 2 | Label Studio in a box (3.5 min) | 5, 7, 8–12, 13, 14 | The tutorial applies it. `docker-shell.sh` is the left half of slide 13: mounted data folder, secrets, the key variable and port 8080. Slides 8–12's three recap concepts are the background for §2–§4. |
| 3 | Who touches the bytes (3.5 min) | 6 (the two bucket folders), 7, 11 | Mostly tutorial-only. Source and target storage, signed URLs and the direct browser download never appear on the slides; they refine slide 7's privacy claim (Conflict 3). |
| 4 | CORS, the browser's bouncer (3 min) | 10, 13 (the CLI container, "Shell into container") | CORS is tutorial-only. The two-address aside is slide 10's Docker network, and the CLI container is slide 13's right half. Slide 13 draws no direct line between the containers (Conflict 4). |
| 5 | Annotations are data (3 min) | 4, 6 (the "Labeled" box), 13 ("Images + Labels", "Terminal - cli.py"), 15–18 | Same concept (labels as ground truth). The JSON form is tutorial-only and differs from slide 6's sorted photos (Conflict 2). Platforms and curation (15–18) are lecture-only. |
| 6 | A bucket that looks like a folder (3.5 min) | 21, 26–34 | Same concept, closely. The tutorial applies slides 29–32 and 34: the slide's command is `docker-entrypoint.sh:11` to the character. Slide 33's "why" and slide 21's bucket-vs-lake card are not in the plan (gaps 5–6). |
| 7 | Fingerprints (4 min) | 20 (Efficiency), 23, 25 | Same concept at slide level ("hashes", "fingerprint", content-based storage). The md5 values, the cache layout and the `.dir` manifest are tutorial-only. |
| 8 | Pointers and names (3.5 min) | 22–23, 25, 35–36 | Same concept: DVC is file-based versioning with Git keeping the history. Annotated tags, `git push --atomic` and `dvc push` are tutorial-only. The comparison with lakeFS and the table formats is lecture-only (gap 2). |
| 9 | Time travel from anywhere (3 min) | 22 (time travel), 26 (the Colab notebook), 36 | The tutorial applies it: slide 26 links the same notebook. The lecture defines time travel for tables, with a condition that holds for DVC tags too (In common 11). |
| 10 | Recap and clean-up (1.5 min) | 35, 38–40 | Clean-up is tutorial-only. Slide 35's takeaway and the monitoring section (38–40, no tutorial) are lecture-only (gaps 2, 8). |
| — | not in the plan | 1–3, 19, 37, 41; 15–18; 21–22; 24; 38–40 | Lecture-only: title, agenda slides and the closing picture; labeling platforms and the curation flow; bucket vs data lake and the concept table; the "final-final-v3" anti-pattern; data monitoring. |

### 2. Already in common

| # | Concept | Section ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | The dataset: four cheeses from unlabeled web images, annotated with Label Studio | §2, §5 ↔ 5 | Yes. The labels are `brie`, `gouda`, `gruyere`, `parmigiano` in both. |
| 2 | One bucket with `cheeses_unlabeled` and `cheeses_labeled` as the hub; a labeling container serving Label Studio to annotators | §1, §3, §5 ↔ 6 | Yes on the hub, the folder names and the numbered steps 1–3. They differ on what "labeled" looks like and where it goes next (Conflicts 1–2). |
| 3 | Run the labeling tool yourself, in Docker | §2 ↔ 7 | Yes. The plan's §3 makes "private" precise: no outside labeling service, but the photos live in your own bucket and the browser fetches them directly (Conflict 3). |
| 4 | The labeling station's setup: two containers; a mounted data folder, the secrets and the source code; the key in `GOOGLE_APPLICATION_CREDENTIALS`; port 8080; a shell into the CLI container to run `cli.py` | §2, §4 ↔ 13–14 | Yes. The plan's peel-off of `docker-shell.sh` matches callouts 1–3 on the Label Studio side, flag for flag; `docker-shell-CLI.sh` is callout 5, plus the CLI's source-code mount from callout 1. The plan also shows the traffic between the parts, which slide 13 leaves out (Conflict 4), and the names differ (Conflict 5). |
| 5 | A Docker network lets containers talk to each other | §4 ↔ 10 | Yes. The plan is more concrete: the same server is `localhost:8080` for the browser and `data-label-studio:8080` for the CLI. |
| 6 | Credentials control access to cloud storage | §2, §3 ↔ 11, 13 | Yes. The plan adds what the slides leave out: the browser never holds the key, and Label Studio hands it a signed URL instead. |
| 7 | Versioning saves space by storing content once | §7, §8 ↔ 20 ("content-based storage") | Yes. The plan's third pause and ponder (one new photo, so `dvc push` uploads two objects) and the "2 objects pushed, not 6" counter of digest §3.5 are the lecture's Efficiency bullet with numbers. |
| 8 | File-based versioning: fingerprint the files, let Git keep the history (DVC) | §7, §8 ↔ 23, 25, 36 | Yes. The plan goes one level deeper than slide 25: Git keeps the fingerprint of a list of fingerprints (Conflict 7). |
| 9 | The question DVC answers: which data went into this model? | §1 (hook) ↔ 25, 36 | Yes, the plan's hook is slide 36's DVC example question. In L11 no model is trained, so the video can only ask it of a tag (Conflict 1). |
| 10 | The versioning tutorial: a versioning container, then a check of the versions from Colab | §6–§9 ↔ 26 | Yes. Slide 26 links the same notebook the digest downloaded. |
| 11 | An old version can be read only while its files are kept | §9, §10 ↔ 22 ("time travel") | Yes. The lecture says it about tables; the digest's coat-check ticket (§3.6) and the plan's "what never to delete (dvc_store)" panel say it about DVC tags. |
| 12 | gcsfuse mounts the bucket at `/mnt/gcs_data`, and a bind mount re-exposes `images/` at `/app/cheese_dataset`, where DVC works | §6 ↔ 27–32 | Yes, closely. Same paths and the same two hops. The lecture adds an explicit Authenticate stage; the plan adds the host's empty folder. |
| 13 | The mount command and its four parts | §6 ↔ 34 | Yes. The slide's first line is the entrypoint's gcsfuse line exactly; only the colour-coded copy below it differs (Conflict 10). |
| 14 | Bucket names are unique across GCP, so rename them | §1, §2, §6 ↔ 34 | Yes. The digest's diagrams mark both buckets "rename". |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **Why version data at all, and why not by renaming files (slides 20, 23–24).** The plan's hook gives one reason (reproduce last week's model). The lecture gives five: track changes, back up and roll back, pass audits, work together, and save space. Its one outright prohibition, the folder of `…final-final-v3-final` copies under "Friends don't let friends do this", is the do-it-yourself versioning habit every student already has. It makes the case for Part B in ten seconds, before any hash appears. **Carry it in** §7, as the opening picture and a pause and ponder ("Which of these files is the real final? What changed between v2 and v3?"), with the five reasons as a quick card that lights "Efficiency" for the hash machine.
2. **Where DVC sits among the tools, and how to choose (slides 22–23, 25, 35–36).** The lecture names four approaches: file-based (DVC), object-store (lakeFS), table-based (Delta Lake, Iceberg) and full snapshots. It draws the dividing line at "Git or no Git" and concludes that there is no single standard; the choice depends on data type, scale and platform. This explains the design the student is building (a bucket *and* a GitHub repo) and directly serves Milestone 2, due 2026-10-20, which asks for basic data or version tracking and accepts snapshot IDs or a light tool such as DVC (`digest.md` §7). **Carry it in** §8, as a closing three-column card with slide 36's example question under each tool, and in §10 as one line of advice for the project.
3. **Labels are ground truth, and errors feed the next version (slide 4).** Accurate, consistent labels make a better model, and wrong labels teach wrong patterns. Labeling the model's own mistakes and hard edge cases is how the next, better dataset version is made. This loop is what makes labeling and versioning one lecture, while the code keeps the two halves apart. It also gives the student a reason to label carefully in A11. **Carry it in** §1 (one line under the two jobs, "attach meaning, freeze history") and §5 (before the JSON envelope).
4. **The recap quiz: network, credentials, Compose (slides 8–12).** The deck asks students to recall three concepts before labeling and reveals one answer per slide. That is a ready-made pause and ponder, and each answer has a place in the tutorial: the network in §4's two addresses, the credentials in §2's `-v ../secrets` plus the key variable, and Compose in the A14 "Extra", which the plan never shows. **Carry it in** §2, as its opening beat.
5. **Why mount instead of download (slide 33).** The dataset stays in the cloud, nobody needs a separate local copy, programs use ordinary file paths, and everyone works on one central dataset. The plan shows how the mount works but never says why the course chose it. **Carry it in** §6, right after the two pipes, together with the correction in Conflict 9 (DVC still keeps a cache on your disk).
6. **A bucket stores named objects; a data lake is the bucket plus tools (slide 21).** A bucket keeps objects identified by name, with metadata, and nothing else. A data lake leaves the data where it is and adds tools to ingest, find, control access to, prepare and version it; DVC is one of those tools. The first half also explains the tutorial's worst trap: folders in a bucket are only name prefixes, so gcsfuse started without `--implicit-dirs` may not show a folder that has no placeholder object (`digest.md` §6 item 2, with the open question on gcsfuse 3.x defaults in §10; the link to slide 21 is ours, not the slide's). **Carry it in** §6, as a two-card beat before gcsfuse.
7. **Why Label Studio, and why run it locally (slide 7).** Manual labeling at scale is slow and inconsistent; a tool gives annotators one simple interface; running it in your own container keeps outside services out. **Carry it in** §2, as the one-sentence "why" before `sh docker-shell.sh`.
8. **Data monitoring (slides 38–40; no tutorial).** The lecture title includes monitoring, and this section answers the open question in `digest.md` §10: monitoring checks quality, freshness, drift (its example: suddenly many more images of one cheese), cost, and which step failed. It names three approaches: rules when expectations are predefined, ML anomaly detection on baseline metrics, and lineage and metadata for all other cases. Slide 38's drift example fits the plan's hook (a 91% model that drops to 84% with no code change). **Carry it in** §10, as a 20-second beat: versioning tells you *what* changed, monitoring tells you *that* something changed. Say plainly that the course has no monitoring tutorial here.
9. **Labeling platforms and data curation (slides 15–18).** At industrial scale, platforms such as SuperAnnotate label images, video, audio and LLM training data (RLHF, SFT), and a curation step sorts raw ingested data into training, validation and discard piles. This matters least for doing the tutorial. **Carry it in** §5, as one sentence, tied to A3's warning not to upload the 21 `__MACOSX` files (the same habit at small scale: throw out junk before it becomes a task).

### 4. Conflicts

No captures exist yet, so "today" is the repos at the digest's commits; the captures will decide once they are made.

| # | Slides say | Tutorial today | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **Where the labels go** (slide 6, which is the README's `data-labeling-flow.png`; slide 36's DVC example). The labeled set flows from the bucket `cheese-app-data-demo` to "Colab {training}", and DVC answers "which images did I use to train this model?". | L11 trains nothing. The Colab notebook installs DVC, runs `dvc list` and `dvc get --rev <tag>`, and counts the files (cells 7–20). Part B versions the `images/` folder of a different bucket (`cheese-app-data-versioning` in the README), which you fill by hand with unlabeled photos; the annotations in `cheeses_labeled/` are never versioned. L13 trains on `cheese_4_labels.zip` from a GitHub release, not on `cheeses_labeled/` or a DVC tag (`digest.md` §7, §10 item 14). | The repos | "Slide 6 shows where this is heading. In this lecture you build two stations, one for labeling and one for versioning, and the code does not connect them yet: Exercise E7 sketches how. Training comes in Lecture 13, from a prepared zip." Draw the Colab box as "view versions" and grey a "training (L13)" box beyond it. |
| 2 | **What "labeled" looks like** (slide 6). The Labeled box shows the photos sorted into rows under `brie`, `gouda`, `parmigiano` and `gruyere`. | Label Studio writes one JSON annotation per submitted label into `cheeses_labeled/`; each record points at the photo's `gs://…/cheeses_unlabeled/…` URI, and the photos never move. No code in either repo produces class folders (`digest.md` §3.1, A12). | The repo | "The slide draws what the labels mean. On disk, a label is a small JSON record that points at the photo, so the photos stay where they are." Morph the sorted rows into a stack of envelopes with arrows back to the unlabeled folder. |
| 3 | **Privacy** (slide 7): run Label Studio locally in Docker, and nothing gets uploaded externally. | You upload the 21 photos to your own GCS bucket (A5). Label Studio's server lists and signs them with the service-account key, and your browser downloads each one straight from `storage.googleapis.com` with a pre-signed URL (`data-labeling/README.md:131`), which is why the bucket needs a CORS rule. | Both, in different senses | "Local here means no outside labeling company sees your data. The photos still live in your own cloud bucket, and your browser fetches them from Google with a short-lived signed link." This is the hinge into §3. |
| 4 | **The arrows on slide 13.** The browser connects only to the Label Studio container (port 8080), apart from their mounts both containers connect only to the bucket, and no line joins the two containers directly. | Two more paths carry traffic. The browser loads every image directly from GCS through its signed URL (the reason for CORS). `cli.py -p` and `-t` call Label Studio's API at `http://data-label-studio:8080` (`data-labeling/docker-shell-CLI.sh:24`) over the network `data-labeling-network`, which is slide 10's recap concept. | The code | "Slide 13 shows how the station is assembled. Once it runs, two more lines carry traffic." Re-draw slide 13, then add the browser-to-bucket line in §3 and the CLI-to-Label-Studio line in §4. |
| 5 | **Names** (slides 6, 13, 14, 26). A single "Data Labeling Container"; the folder `docker-volume/label-studio`; "Expose port 8080"; a "Data Versioning Container". | Two containers, `data-label-studio` and `data-label-cli`. The folder is `./docker-volumes/label-studio` (plural), mounted at `/label-studio/data` (`data-labeling/docker-shell.sh:16`). The port is *published* with `-p 8080:8080` (`:15`), the word the L04 slides use. The versioning container is `data-version-cli`, which the README calls "the DVC container". | The repo | Put the repo's names on screen and give the lecture's name once as a caption ("the lecture's Data Labeling Container is these two"). Say "publish the port", as in L04. |
| 6 | **The bucket URI** (slides 16–18): `gcs://production-ml-data-lake/raw_unstructured_ingest/`. | GCS URIs start with `gs://`, as in `dvc remote add -d cheese_dataset gs://YOUR_BUCKET_NAME/dvc_store` (`data-versioning/README.md:279`). | `gs://` | If the curation path appears, write it with `gs://`, and add once: "when you type a bucket address, it starts with gs://". |
| 7 | **What Git records** (slide 25): DVC gives each file a fingerprint, and Git records which fingerprints belong to each version. | Git holds the six-line pointer `cheese_dataset.dvc`, whose one `md5` is the fingerprint of a `.dir` manifest. The manifest, which lists every file's md5, lives in `.dvc/cache` and `dvc_store/`, not in Git (`digest.md` §3.5–3.6). | Both, at different zoom levels | "One more level: Git keeps the fingerprint of the *list* of fingerprints." This is the plan's §8 rope (tag → commit → pointer → manifest → blobs). |
| 8 | **"Mounting disks from GCS to a container"** (slides 27–28, 34). | What is mounted is a bucket (object storage) through FUSE. On GCP, "disks" are a different product (Persistent Disk) that this tutorial never touches. | The code | Say "mount a bucket" throughout and add once: "the lecture says disks; it means the bucket, made to look like a folder". |
| 9 | **No local copy; reads and writes go to the bucket** (slides 32–33). The app and DVC treat `/app/cheese_dataset` as an ordinary folder whose reads and writes really hit GCS, so no one has to download the dataset. | Reading works that way: `dvc add` reads each image through the mount. But it then copies every image into `.dvc/cache/files/md5/…` on your laptop's disk, through the `/app` bind mount, and `dvc push` uploads those cache objects to `dvc_store/` through the Storage API (gcsfs), not through the mount. The host's `cheese_dataset/` stays empty (`digest.md` B9–B10, §3.7, E6). New uploads can take about a minute to appear in the mounted folder (`digest.md` §6 item 18). | The code | "Mounting spares you a download of the working folder. DVC still keeps its own cache on your disk: that is where the fingerprints are made, and what `dvc push` uploads." Show the three homes of the bytes (`images/`, `.dvc/cache`, `dvc_store/`), which is the plan's recap question 3. |
| 10 | **The colour-coded command** (slide 34): `gcsfuse —key-file=$GOOGLE_APP_CREDS $GCS_BUCKET_NAME /mnt/gcs_data`, with an em dash in front of `key-file` and a shortened variable name; the first token is captioned "Command to mount containers". | `gcsfuse --key-file=$GOOGLE_APPLICATION_CREDENTIALS $GCS_BUCKET_NAME /mnt/gcs_data` (`data-versioning/docker-entrypoint.sh:11`; line 10 on the starter), which is also the slide's own first line. Typed with an em dash, the flag is not recognised. The command mounts a bucket into the container. | The slide's first line, as in the entrypoint | Split the entrypoint's real line into four chips, using the slide's captions with "mounts the bucket" for the first one. Keep two hyphens and the full variable name. |

Not counted as conflicts:
- Slide 13's callouts are numbered 1, 2, 3 and 5 (no 4), and slide 22's two columns are not row-aligned (time travel sits beside lakeFS). Both are layout only.
- Slide 5 spells "Gruyère"; the tutorial's label is `gruyere`.
- Slides 14 and 26 leave out the service account, CORS, the starter branch and the `google-cloud-sdk` → `google-cloud-cli` fix. Those are omissions the READMEs fill (and the broken starter is a README-vs-apt problem, `digest.md` §6 item 1), not contradictions.
- Slide 34 does not pass `--implicit-dirs`, and neither does the entrypoint. The resulting empty-folder trap is a tutorial gotcha, not a slide conflict (proposal for §6 below).
- The deck says Lecture 11, as `tutorials_demo.md` does, while the course site's week page says 10 (`digest.md` §10 item 15). The series follows the deck.

### 5. Proposals for the BRIEF and script authors

**General**
- Tag every section that stands on lecture ground with one grey `lecture_ref(11, "a–b")`, using the ranges below. Re-draw the lecture's diagrams in the series style (laptop GREY, cloud BLUE, containers TEAL) rather than showing slide images or the README PNGs. Re-drawn, they can show today's facts: the two buckets, the JSON envelopes, the missing traffic lines and the local cache.
- **No slide pictures.** Slides 5, 14, 24, 35 and 41 carry cartoons, an illustration, a meme or a screenshot of the instructor's terminal, and slide 15 a screenshot of SuperAnnotate's home page. For slide 24, type a fresh `ls` of invented names in the same spirit (`report-final.tex`, `report-final-v2.tex`, `report-final-final-v3.tex`) instead of the screenshot, which shows the instructor's machine prompt and paper files.
- **Pause and ponder.** The plan has three pauses in about 30 minutes, and the content gate asks for roughly one per two minutes. The lecture supplies five ready-made ones: slide 8's recall quiz (§2), "what's wrong with this folder?" from slide 24 (§7), slide 33's shared central dataset (§6: "a teammate uploads to `images/` while you run `dvc add`; what gets versioned?"), slide 36's example questions as "which tool answers this?" (§8), and slide 38's drift example as the answer to the hook (§10).
- **Length.** The plan is about 30.5 minutes. Keep each lecture beat to 10–25 seconds and the total addition under about 2.5 minutes. If time is short, shorten §9's failure gallery to one card and let the study guide (§6, item 13) carry the rest.
- **Two buckets, said once and drawn always.** Slide 6, the README figure and `pipeline-flow.png` all imply one bucket and one flow. Every re-draw should keep `cheese-app-data-demo` and the versioning bucket as two BLUE shapes, so that Conflict 1 never has to be explained twice.

**Per section**
- **§1 · Lecture 11 · slides 4–6, 36.** After the plan's hook, put slide 36's DVC question on screen in the lecture's words: "Which images did I use to train this model?". Then re-draw slide 6 (the README figure), with the red "How do we do this?" arrow as the question the hour answers, and light steps 1–3. Extend it to the right with the versioning station from `pipeline-flow.png`, but drawn as the code is: a second bucket, Colab as "view versions", and training greyed as "L13" (Conflict 1). One line from slide 4 joins the halves: labels are the ground truth, and the model's mistakes, labeled, become the next version.
- **§2 · Lecture 11 · slides 7–14.** Open with slide 8's quiz as a pause: "Docker network, cloud credentials, Docker Compose: what does each one do?" Answer with slides 10–12's one-liners and point each to where it appears today (§4, the `-v ../secrets` mount plus the key variable, the A14 Extra). Give slide 7's why in one sentence. Then make slide 13 the target picture of the plan's flag peel-off: callout 1 is the `-v` pipes, 2 the `-e` note, 3 the `-p` door, and 5 the second script. Use the repo's names and the word "publish" (Conflict 5).
- **§3 · Lecture 11 · slides 6–7, 13.** The mechanism is tutorial-only. Anchor it on the re-drawn slide 13: "the slide connects the browser only to Label Studio, yet the photos never pass through it". Draw the new browser-to-bucket line, then the ticket-office animation. Close with slide 7's "private" made precise (Conflict 3).
- **§4 · Lecture 11 · slides 10, 13.** Say that CORS is not in the lecture and comes from the README. For the two-address aside, call back to slide 10 ("containers talk over a Docker network") and add the CLI-to-Label-Studio line to the slide 13 re-draw (Conflict 4).
- **§5 · Lecture 11 · slides 4, 6, 15–18.** Start from slide 4: labels are ground truth, and they must be consistent as well as accurate. Then the JSON envelope, and morph slide 6's sorted rows into envelopes that point back at the photos (Conflict 2). One sentence on platforms and curation (slides 15–18), tied to not uploading the `__MACOSX` files.
- **§6 · Lecture 11 · slides 21, 27–34.** Open with slide 21's two cards: a bucket is named objects; a data lake is the same bucket plus tools, and versioning is one of them. "Folders are only name prefixes" then sets up the empty-folder trap. Use slides 29–32's four named stages as the four beats of the two-pipe animation: Authenticate (the key file), Bucket Mounting (gcsfuse → `/mnt/gcs_data`), Connecting the Application (`mount --bind` → `/app/cheese_dataset`), Using the Data (DVC). Then slide 34's chips over the entrypoint's real line (Conflict 10), with a dashed fifth chip, `--implicit-dirs`, marked "not passed here: why `images/` should be created as a folder in the console". Give slide 33's reasons for mounting (gap 5) and immediately qualify them: the cache on your disk (Conflict 9). Say "bucket", not "disk" (Conflict 8). Keep the plan's pause about the host's empty folder, and add the shared-dataset pause.
- **§7 · Lecture 11 · slides 20, 23–25.** Open on the slide-24-style folder of "final" copies as a pause, then slide 20's five reasons as a card with "Efficiency" lit. Put slide 23's definition, "file-based versioning: hashes and metadata, with Git keeping the history", as the headline over the hash machine. Say "fingerprint" (the lecture's word) once, then "md5".
- **§8 · Lecture 11 · slides 22–23, 25, 35–36.** Re-draw slide 25's DVC row, then zoom in to show the extra level (Conflict 7): Git → pointer → manifest → blobs. Close on the three-column card (DVC, lakeFS, Delta Lake / Iceberg) with "uses Git", "own history", "table versions" and slide 36's example question under each, as a pause ("which tool answers each question?"). End with slide 35's takeaway, "no single standard", and one line for the project: Milestone 2 accepts a light tool like this one.
- **§9 · Lecture 11 · slides 22, 26.** Name the move with slide 22's term, "time travel", and its condition: an old version can be read only while its files are kept. On the plan's rope animation, that condition is the `dvc_store` box. Note once that slide 26's notebook link opens the same notebook, whose defaults point at the class repo.
- **§10 · Lecture 11 · slides 35, 38–39.** For the content recap, light the §1 map station by station, with each station's lecture term under it. Then a 20-second monitoring beat (gap 8): slide 38's five reasons, with "many more images of one cheese" circled as one possible answer to the hook. Slide 39's three approaches go in one line, with a plain note that this course has no monitoring tutorial. Keep the plan's clean-up panel.
- **Recap questions.** Keep the plan's six. Add "Why does DVC need Git and lakeFS not?" (slides 23, 25, 36); "Name three reasons to version data besides rollback" (slide 20); "What goes wrong when you version by renaming files?" (slide 24); and "Mounting means no local copy of the dataset, so where does DVC still keep one, and why?" (slides 32–33, Conflict 9).

**Terms**
- Use the lecture's words: *data labeling*, *annotate*, *ground truth*, *Label Studio*, *Cheese App data pipeline*, *Docker network*, *cloud storage and credentials*, *Docker Compose*, *Label Studio container*, *CLI container*, *mount external folders*, *shell into container*, *data versioning*, *bucket* and *data lake*, *file-based versioning*, *object-store versioning*, *table-based versioning*, *full snapshots*, *fingerprint*, *time travel*, *gcsfuse*, the four stages *Authenticate*, *Bucket Mounting*, *Connecting the Application* and *Using the Data*, *bind mount*, *data monitoring*, *drift*.
- Add the repo's words where the lecture stops: *source storage* and *target storage*, *pre-signed URL*, *CORS*, *annotation* (one JSON record), *task*, *md5*, *`.dir` manifest*, *cache*, *remote* (`dvc_store`), *pointer file* (`cheese_dataset.dvc`), *annotated tag*, `dvc get --rev`, *FUSE*, `--privileged`, *mount namespace*.
- Qualify, don't repeat:
  - "nothing gets uploaded externally": no outside labeling service; the photos are in your own bucket.
  - "Data Labeling Container": two containers. "Data Versioning Container": `data-version-cli`.
  - "expose port 8080": publish it with `-p 8080:8080`.
  - "mounting disks": mounting a bucket.
  - "Git records the fingerprints": Git records the fingerprint of the manifest.
  - "time travel": the lecture's term for tables; for DVC, `dvc get --rev <tag>` for as long as `dvc_store/` keeps the files.
  - "bind mount": two layers in this tutorial, Docker's `-v` from laptop to container and Linux `mount --bind` inside the container (slide 31 means the second).
  - "gcs://": write `gs://`.
