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

- **Printed footers match the PDF pages** wherever they appear. Slides 1, 25 and 28–33 print no
  footer.
- **Many slides are builds** (the same slide with one more element revealed). These are slides
  8–12 (the recap questions, then their answers one at a time), 15–18 (a curation diagram drawn
  piece by piece), 28–32 (the gcsfuse flow, one box per slide) and the agenda slides 2/3/19/37.
  Cite the last slide of a build for the complete picture.
- **How the deck maps onto this episode.** Slides 5–14 are the `data-labeling` tutorial, and
  slides 26–34 are the `data-versioning` tutorial. Slide 26 links the same Colab notebook that
  `digest.md` downloaded (id `1RRQ1SlHq5lKK76R8LoQdi5LjCnND3jTq`). The surrounding slides (4,
  15–25, 35–36) give the theory and tool landscape, which no README covers.
- **What the slides leave to the tutorial.** The slides never show CORS, signed URLs, Label
  Studio's source/target storage, any `dvc` or `git tag` command, md5 manifests, `dvc_store`, or
  the container's privileged flags. Those come only from the READMEs (`digest.md` §3–§5).
- **Monitoring has slides but no tutorial.** Slides 38–40 are conceptual only. This answers the
  open question in `digest.md` §10: the deck's monitoring section covers why to monitor, three
  approaches and three commercial tools, with no code or demo.

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
    with five numbered callouts.
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
  - 24: the punchline. A terminal full of `…final-final-v3-final.tex` files, and an illustration
    captioned "Friends don't let friends do this".
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
  - 35: "Takeaway". There is no single industry standard for data versioning tools. It sits
    beside a meme captioned "You're not that guy, pal, trust me".
  - 36: "DVC vs lakeFS vs Delta Lake/Iceberg", the comparison table again with an "Example"
    question per tool.
- **Slide 37 · agenda** ("Data Monitoring" in bold).
- **Slides 38–40 · 3. Data Monitoring.**
  - 38: why monitor data (five reasons).
  - 39: three approaches (rules-based, anomaly detection, lineage and metadata).
  - 40: three tools (Monte Carlo, Datadog, Soda).
- **Slide 41 · "THANK YOU"**, with an anime character striking a pose.

## Key ideas

1. **Labels are the ground truth a supervised model learns from and is graded against.** Their
   accuracy and consistency limit the model. A wrong label teaches a wrong pattern. Human
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
   - Commercial platforms such as SuperAnnotate handle multimodal labeling: image, video and
     audio, and also the data for LLM post-training (RLHF, SFT).
   - Before labeling, a curation engine filters a raw-ingest area of the data lake into a
     training set, a validation set and a discard pile for low-quality items.

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
      schemas and versions. Delta Lake and Apache Iceberg are two competing open table formats.
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
13. **There is no single industry standard.** The right versioning tool depends on the data type,
    the scale and the platform. (Slide 35)
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
19. **Choose a monitoring approach by how much you know in advance.**
    - If the schema and pipeline expectations are fixed, use rules and test specific
      constraints.
    - Otherwise, ML models track baseline metrics and flag unusual shifts or drops (anomaly
      detection).
    - In every other case, trace end-to-end lineage and metadata, so you can find root causes
      quickly across complex pipelines.

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
    - a short green arrow to a yellow box "Colab (training)" with a notebook icon (circle 4);
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
    Label Studio writes one JSON annotation per labeled image into `cheeses_labeled/` and does not
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
  - *What it leaves out:* no direct container-to-container link is drawn; the only line between
    them is the shared connector up to the bucket. In the tutorial, the CLI
    reaches Label Studio's API over the Docker network at `http://data-label-studio:8080`
    (`digest.md` §3.4), which is the point of the "Docker Network" recap on slide 10.
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
    - 29: service-account credentials give gcsfuse permission to access GCS;
    - 30: gcsfuse makes the bucket's files appear as a regular folder `/mnt/gcs_data`;
    - 31: a bind mount makes `/mnt/gcs_data/images` also appear at `/app/cheese_dataset`;
    - 32: the app and DVC use `/app/cheese_dataset` like a local folder, while reads and writes
      go to the bucket.
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
  - **Slide 22:** two purple-headed columns, "Concepts" and "Tools and technologies". Their rows
    line up: data lake ↔ table formats (Delta Lake, Apache Iceberg); table format ↔ data
    version-control tools (DVC); time travel ↔ lakeFS.
  - **Slide 25:** three columns: Tool, Useful for, How it keeps versions.
  - **Slide 36:** tools as columns (DVC, lakeFS, Delta Lake / Iceberg) and three rows: Useful
    when, Example, Version history.

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README |
|---|---|---|
| "Data Labeling", "annotate" | 4–5 | The README has the same idea in its "Annotate Data" step. |
| "Ground Truth", "Model Quality", "Real-World Context", "Continuous Improvement" | 4 | Not in the README. |
| "Label Studio" | 5, 7, 13 | Same tool. The README runs the image `heartexlabs/label-studio:latest` as container `data-label-studio`. |
| "Cheese App Data Pipeline"; "Unlabeled" / "Labeled" | 6 | The README uses the same bucket and folder names (`cheese-app-data-demo`, `cheeses_unlabeled`, `cheeses_labeled`). In Label Studio's UI the two folders are "Source storage" and "Target storage", terms the slides never use. "Labeled" holds JSON annotations, not sorted photos. |
| "Data Labeling Container" | 6, 14 | No single container has this name. The README starts `data-label-studio` (`docker-shell.sh`) and `data-label-cli` (`docker-shell-CLI.sh`). |
| "Colab (training)" | 6 | L11's tutorials do no training. Their Colab notebook only reads dataset versions with `dvc get`. Training is a later lecture. |
| "Docker Network", "Cloud Storage and Credentials", "Docker Compose" | 8–12 | In the README these are the network `data-labeling-network`, the key `../secrets/data-service-account.json`, and the "Extra" `docker-shell-compose.sh`. |
| "Label Studio Container", "CLI Container" | 13 | The README's container names are `data-label-studio` and `data-label-cli`. |
| "Expose port 8080", "HTTP 8080" | 13 | The README publishes the port with `-p 8080:8080`. In earlier lectures this is called "publishing" a port. |
| "Mount external folders"; `docker-volume/label-studio`; "Secrets"; "Source Code" | 13 | The README's folder is `docker-volumes/label-studio` (plural), mounted at `/label-studio/data`. The secrets go to `/secrets`, and the source code to `/app`. |
| "Shell into container", "Terminal - cli.py" | 13 | In the README you run `docker-shell-CLI.sh`, then `python cli.py` with `-c`/`-m`/`-p`/`-t`. |
| "Data Pipeline" | 14, 26 | The README has the same idea. |
| "multimodal labeling", "RLHF", "SFT" | 15 | Not in the README. |
| "Curation Engine", `raw_unstructured_ingest`, `curated_train`/`curated_val`/`discard_low_quality` | 16–18 | Not in the README. The path is written `gcs://…`. Real GCS URIs use `gs://`. |
| "Bucket" ("BASE STORAGE") vs "Data Lake" ("ARCHITECTURE") | 21–22 | Not in the README. |
| "Table format", "open table formats", "Time travel" | 22 | Not in the README. |
| "Data version-control tools" | 22 | The README spells DVC out as Data Version Control. |
| "File-based", "Object-store", "Table-based versioning", "Full snapshots" | 23 | The tutorial teaches only file-based versioning (DVC). |
| "fingerprint" | 25 | `digest.md` and DVC say "md5 hash". The README's pointer file is `cheese_dataset.dvc`, which holds the md5 of a `.dir` manifest. |
| "Data Versioning Container" | 26 | The README calls it "the DVC container" (section "Start the DVC container"). The container is named `data-version-cli`. |
| "Test Data Version Notebook" | 26 | The notebook's own title is "Tutorial - Data Pipelines, Labeling, Versioning, Cloud Storage" (`digest.md`, header). |
| "Mounting disks from GCS to a container"; `gcsfuse` | 27–34 | The README covers this in "About docker-entrypoint.sh". The disks are really a bucket, not disks. |
| "Authenticate", "Bucket Mounting", "Connecting the Application", "Using the Data" | 29–32 | Not named in the README. They match `docker-entrypoint.sh`: `gcloud auth activate-service-account`, then `gcsfuse`, then `mount --bind`. |
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
- Slide 34, the colour-coded version. The extracted text renders the flag's double dash as a
  long dash.
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
  - Consistency matters as much as accuracy.
  - Model errors and edge cases are where new labels pay off most.

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
- **Full snapshots are a fallback**, used only "when appropriate", because each one is a whole
  copy. Efficiency means avoiding duplication. (Slides 20, 23)
- **Git or no Git is the dividing line.**
  - DVC needs Git.
  - lakeFS and the table formats keep their own history.

  The deck repeats this in both comparison tables. (Slides 23, 25, 36)
- **No single standard.** The choice depends on data type, scale and platform. The deck
  highlights "no single" in yellow, and a meme warns the viewer against thinking they are the
  exception. (Slide 35)
- **Mount, don't copy.** Mounting keeps one central dataset in the cloud and avoids stale local
  copies. (Slide 33)
- **Bucket names are unique across GCP**, so every student needs their own name. (Slide 34)
- **Monitoring is about finding the broken step**, not only about raising alerts. Freshness and
  drift are examples. Use lineage and metadata for root causes in complex pipelines. (Slides
  38–39)
- **Pick the monitoring approach by what you know in advance.** Use rules when the expectations
  are fixed, learned baselines when they are not, and lineage for everything else. (Slide 39)

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
  - Delta Lake, Apache Iceberg, DVC and lakeFS (slides 22–25, 36);
  - `gcsfuse`, described as an open-source tool by Google (slide 28);
  - Monte Carlo, Datadog and Soda (slide 40).
- **No homework, milestone or reading is mentioned** anywhere in the deck. The monitoring section
  has no tutorial or demo.
