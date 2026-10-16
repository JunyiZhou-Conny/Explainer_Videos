# L08 lecture slides — LLM Finetuning

Source: one deck by Pavlos Protopapas (AC215, SEAS/Harvard), `L08_FineTuning_v2` (73 slides),
titled "Lecture 8: LLM Finetuning". These are the instructor's lecture slides (PDF), provided by
the student for study; the PDFs are not in this repository; slide numbers are PDF page numbers.
I wrote this digest from the deck's extracted text and from all nine contact sheets. I also
enlarged slides 7, 14, 16, 19, 28, 29, 38, 40, 44, 53, 54, 65, 67 and 72 to read their diagrams and
small print. Everything below is in my own words. Only short titles, terms, formulas and single
lines are quoted. The tutorial side of the lecture is in [`digest.md`](digest.md).

Read this first:

- **The printed footer numbers are not the slide numbers.** The deck was cut from a longer one.
  Slides 1–3 have no footer. After that the footers run 5–17 (slides 4–16), none (17), 19–21
  (18–20), none (21), 25–30 (22–27), 32–43 (28–39), none (40), 46 (41), none (42), 48–57 (43–52)
  and 59–78 (53–72). Slide 73 has none. Always cite the PDF page numbers used here.
- **The text extraction loses some maths.** Superscripts and subscripts come out as stray digits
  and symbols (for example `X 2345` for X^FP32 and `X 6(78` for X^Int8). Slide 62 reads
  "every 𝑛 layer" in the text, but the slide itself says **every √n layer**. The formulas below
  were read from the slide images.
- **Lecture numbering.** The title slide says "Lecture 8". The course site's weekly schedule
  lists "LLM - Finetuning" on Oct 1 but calls it "Lecture 7" (digest, header). The slides
  support the series' L08 label.
- **How the deck maps onto the tutorial.** The deck is all theory. It gives the ideas behind
  **Track B**, the Colab notebook "Tutorial - Finetuning with QLoRA": 4-bit NF4 loading, LoRA
  adapters with `r` and `lora_alpha`, a paged AdamW optimizer, gradient checkpointing, and
  merging the adapter at the end. The memory story on slides 13–16, 37–39 and 71–72 explains why
  the notebook can fine-tune on one Colab GPU. **Track A** (the repo: a synthetic cheese Q&A set
  made with Gemini, then a managed Gemini tuning job on Vertex AI / Agent Platform) is not on the
  slides. The one shared idea is the instruction dataset (slides 4–5), which is what
  `dataset-creator` builds. The deck never mentions Gemini, Vertex AI, Docker, Hugging Face, Qwen,
  TRL, bitsandbytes, Colab or any command.
- **Where the slides and the tutorial disagree** (details under Terms and Diagrams):
  1. **Compute and adapter precision.** The slides run QLoRA in BF16, with BF16 adapters (66–72).
     The notebook computes in `float16` (`bnb_4bit_compute_dtype="float16"`, `fp16=True`) so that
     T4 GPUs work. It also casts the adapters back to fp32 after TRL had cast them to bf16
     (digest §3.7).
  2. **Double quantization.** The slides skip it on purpose (sticky note on 53). The notebook
     turns it on (`bnb_4bit_use_double_quant=True`).
  3. **How A is initialized.** The slides say A is drawn from a normal distribution and B is zero
     (27–28). That follows the LoRA paper. PEFT 0.20.0's default (`init_lora_weights=True`), which
     the notebook uses, sets B to zero but draws A from a **Kaiming-uniform** distribution. I read
     this in `peft/tuners/lora/layer.py:331-339` of the 0.20.0 wheel. `"gaussian"` is an opt-in
     setting.
  4. **Where adapters go.** The slides say LoRA adds update matrices "to each layer" (22, 41). In
     the notebook PEFT's default for Qwen3 adapts only `q_proj` and `v_proj` in each of the 28
     layers (digest §3.6).
  5. **The quantization constant.** The worked example (45–51) uses one absmax constant for the
     whole array and Int8 with `round`. bitsandbytes NF4 keeps one absmax constant per small block
     of weights and maps each weight to one of 16 NF4 levels (digest §3.5). Double quantization
     then compresses those per-block constants.
  6. **Backward pass wording.** Slides 29 and 70 say the pretrained weights are not used in the
     backward pass. More precisely, W₀ gets no gradient and no update. The gradient for earlier
     layers still passes *through* W₀ (in QLoRA, through its dequantized copy). The digest says it
     that way (§3.7).
  7. **Merging.** Slide 30 says you can merge the update into the weights at inference. The
     notebook does that with `merge_and_unload()`, but into a freshly loaded **FP16** base, not the
     4-bit one (digest Step 26).

## Outline

The deck has three sections (outline on slide 2), with QLoRA added as a fourth part on 42. The
outline slide repeats with the current part in bold (3, 17, 21, 42).

- Slide 1 · title "Lecture 8: LLM Finetuning", AC215, Pavlos Protopapas, SEAS/Harvard
- Slide 2 · outline: Instruction-tuning (Full Parameter; Parameter-Efficient Fine-Tuning (PEFT)),
  LoRA, QLoRA
- Slides 3–16 · **Instruction-tuning (Full Parameter)**
  - 3 · outline, "Instruction-tuning" and "Full Parameter" in bold
  - 4 · fine-tuning usually means instruction fine-tuning; what an instruction dataset holds
  - 5 · an example instruction dataset (Instruction / Context / Output), from Alpaca-GPT4
  - 6 · task-specific fine-tuning on a smaller dataset ("Summarize this, translate that")
  - 7 · a ChatGPT 4o screenshot: the reply starts "Sure, here's a haiku…", boxed in red
  - 8 · the same, contrasted with plain next-word prediction
  - 9 · catastrophic forgetting
  - 10 · multi-task fine-tuning as the remedy, which needs much data and compute (meme: a man
    standing in a heap of shredded paper labelled "Data")
  - 11 · full fine-tuning updates every weight, which needs a lot of GPU memory; "Fun Fact" about
    the cost of training GPT-4
  - 12 · the same fact restyled as "Not so fun Fact", with a penguin GIF
  - 13 · set-up: fine-tune a 10-billion-parameter model in FP16 (2 bytes per parameter)
  - 14 · memory stack: parameters 20GB, gradients 20GB, Adam optimizer states 80GB
  - 15 · the same stack needs at least five 24-GB RTX 4090 GPUs
  - 16 · full fine-tuning is out of reach for "normal folks like us" (Winnie-the-Pooh meme)
- Slides 17–20 · **Instruction-tuning (PEFT)**
  - 17 · outline, "Instruction-tuning" and "Parameter-Efficient Fine-Tuning (PEFT)" in bold
  - 18 · PEFT keeps most original weights; three families: Additive, Selective,
    Reparameterization
  - 19 · Venn diagram of PEFT methods (source: paper "Scaling Down to Scale Up")
  - 20 · the same diagram with LoRA circled: "We're interested in LoRA"
- Slides 21–41 · **LoRA**
  - 21 · outline, "LoRA" in bold
  - 22 · "LoRA - Introduction": what LoRA is and does
  - 23–25 · "LoRA - Intuition": a 5×5 matrix as B × A at rank 1 (25 vs 10 elements), then rank 2
    (20 elements)
  - 26–30 · "LoRA - Working": the update equation with its parts labelled (26), the initialization
    (27, with an "I'm lost" dog meme), the block diagram (28), its backward pass (29) and merging
    at inference (30)
  - 31–35 · "LoRA - Intuition": a table of trainable-parameter counts by rank and model size,
    built row by row, with a caveat on 35
  - 36 · "LoRA - Advantages"
  - 37–40 · "LoRA – Isn't it enough?": memory of full fine-tuning vs LoRA for a 10B model
    (37–39), then LoRA's quality vs full fine-tuning (40, a results table)
  - 41 · "LoRA - Summary"
- Slides 42–72 · **QLoRA**
  - 42 · outline variant: "Training Cycle – LLM", Instruction-tuning (Full Parameter, PEFT),
    LoRA, **QLoRA** in bold. "Training Cycle – LLM" is not in this deck.
  - 43 · QLoRA extends LoRA by quantizing the base weights; quantization as "splitting range into
    buckets"
  - 44 · three number lines: a continuous range, whole-number buckets and buckets of ten
  - 45–51 · worked example: FP32 → Int8 with absmax (45–50), then dequantization and its error (51)
  - 52 · "QLoRA – The Pizza": QLoRA as a pizza, with a cartoon mouse
  - 53 · "The Ingredients": 4-Bit NormalFloat (dough) and Paged Optimizer (cheese); sticky note
    on double quantization
  - 54–55 · "Ingredient 1: 4-Bit NormalFloat": 16 buckets; equally spaced vs equally sized
    buckets over a bell curve
  - 56 · the ingredients again (back to the pizza)
  - 57–64 · "Ingredient 2": the out-of-memory problem and gradient checkpointing on a four-layer
    network
  - 65 · "Ingredient 2 : Paged Optimizer": paging between GPU and CPU
  - 66–67 · "QLoRA – Last Details": BF16 in QLoRA vs FP16 in LoRA; bit layouts of FP16,
    bfloat16 and TF32
  - 68–72 · "QLoRA – Putting it all together": W stored in NF4 (68), forward pass (69), backward
    pass (70), the memory comparison repeated (71) and QLoRA's memory (72, 10B ⇒ ~12GB)
- Slide 73 · "After completing Finetuning:" a cat-and-mouse cartoon meme ("Students",
  "Prof. Pavlos", "Wisdom"), "Thank you!"

## Key ideas

1. **Fine-tuning usually means instruction fine-tuning.** You train on an instruction dataset:
   pairs of an instruction and its answer, sometimes with extra context. (4–5)
2. **Task-specific fine-tuning teaches a narrow job.** A smaller dataset for one task (summarize,
   translate) teaches the model that task's nuances and specialised vocabulary. (6)
3. **Instruction tuning changes how the model behaves.** A chat model answers "write a haiku" by
   starting "Sure, here's a haiku…". A plain next-word predictor would just continue the text,
   so it would produce the haiku with no preamble. The preamble is a learned habit. (7–8)
4. **Catastrophic forgetting.** Fine-tuning on a new task can overwrite what the model learned
   before, so earlier tasks get worse. Training on many tasks at once (multi-task fine-tuning)
   helps, but it needs a lot of data and compute. (9–10)
5. **Full-parameter fine-tuning updates every weight**: 7 billion for a 7B model, 13 billion for a
   13B model. Storing and updating them takes a lot of GPU memory. (11)
6. **The memory bill for a 10B model is 120 GB.** In FP16 the parameters take 20 GB and the
   gradients another 20 GB. Adam keeps two FP32 states per weight (momentum and variance), which
   adds 80 GB. That needs at least five 24-GB RTX 4090s, which is out of reach for most people.
   (13–16)
7. **PEFT trains a small part and keeps the rest.** Parameter-efficient fine-tuning leaves most
   original weights untouched. Its methods fall into three overlapping families: *additive*
   (add new trainable layers or parameters), *selective* (fine-tune a subset of existing
   parameters) and *reparameterization-based* (use low-rank representations). LoRA is
   reparameterization-based and among the most popular. (18–20)
8. **LoRA trains pairs of small update matrices.** It adds a pair of rank-decomposition matrices
   (the "update matrices") to each layer and trains only those. They have far fewer parameters
   than the original weights. (22, 41)
9. **A big matrix can be written as a tall thin matrix times a short wide one.** A 5×5 matrix
   (25 numbers) as 5×1 times 1×5 needs 10 numbers at rank 1. At rank 2 (5×2 times 2×5) it needs
   20. A higher rank is more expressive. (23–25)
10. **LoRA factorizes the update, not the weights.** The fine-tuned weight is
    `W₀ + ΔW = W₀ + (α/r)·B·A`. Here W₀ is the initial LLM weights, α a scaling parameter and r
    the rank of BA. The slide stresses that ΔW is decomposed and W₀ is left alone. (26)
11. **B starts at zero, so the update starts at zero.** B is initialized to zero and A from a
    normal distribution. BA is therefore zero at step 0, and the model starts out exactly as the
    pretrained one. (27–28)
12. **The adapter runs beside the frozen layer.** The input x goes through W₀ and, in parallel,
    through A then B. The two outputs are added to give h. In the backward pass only the adapters
    are trained. At inference you can fold BA into W₀, so the adapter costs nothing extra. (28–30)
13. **The savings are enormous.** Treat a 7B model as one big layer: rank 1 trains 167K
    numbers, rank 8 about 1M, rank 8192 about 1.4B, against 7B for full fine-tuning. The slide
    warns that this pretends the LLM has one layer. (31–35)
14. **LoRA's advantages** over full fine-tuning: it is much faster, needs less GPU memory, costs
    less and forgets less, because the original weights stay the same. (36)
15. **LoRA alone still needs ~40 GB for a 10B model.** The optimizer state and the trainable
    weights shrink to just A and B. But the frozen FP16 base model (20 GB) must still sit in GPU
    memory for the forward pass. This is the motivation for QLoRA. (37–39, 71)
16. **LoRA matches full fine-tuning.** In the results table LoRA equals or beats full
    fine-tuning while training a tiny fraction of the parameters. (40)
17. **Quantization means sorting numbers into buckets.** Fewer buckets means fewer bits per
    number and less precision. QLoRA is LoRA on top of a base model whose weights are quantized.
    (43–44)
18. **Absmax quantization, worked through.** To map FP32 values to Int8 (−128…127), multiply
    every value by `c = 127 / absmax(X)` and round. The largest magnitude lands exactly on 127.
    Dividing by c gives the values back, but never exactly: there is always some dequantization
    error. (45–51)
19. **QLoRA is a pizza with two ingredients**: 4-bit NormalFloat (the dough) and the paged
    optimizer (the cheese). A third ingredient, double quantization, sits between them but is
    skipped. (52–53, 56)
20. **NF4 puts its 16 buckets where the weights are.** Four bits give 2⁴ = 16 buckets. Pretrained
    weights are roughly normally distributed around 0, so precision near the middle matters most.
    NF4 uses "equally sized" buckets (equal share of the weights, an enhanced quantile
    quantization) instead of equally spaced ones. (54–55)
21. **Gradient checkpointing trades compute for memory.** A forward pass normally stores every
    layer's activations for backpropagation. Instead you keep only some (checkpoints every √n
    layers) and recompute the others from the nearest checkpoint during the backward pass.
    GPUs have plenty of compute; memory is what they lack. Memory spikes remain, especially for
    long sequences in a batch. (57–64)
22. **The paged optimizer spills to the CPU.** When GPU memory runs out, pages of optimizer state
    move to CPU RAM automatically and come back when needed and there is room. This absorbs the
    spikes that gradient checkpointing cannot remove. (65, 72)
23. **BF16 keeps FP32's range with less precision.** It is a 16-bit format: 8 exponent bits like
    FP32 (FP16 has 5) and 7 fraction bits. The slides' QLoRA computes in BF16, where their LoRA
    used FP16. (66–67)
24. **QLoRA puts it all together.** W is stored in NF4. In the forward pass W is dequantized to
    BF16, used together with BF16 A and B, then the BF16 copy is deleted. In the backward pass W
    stays frozen and only the adapters get gradients. Repeat until a minimum is reached. The
    memory for a 10B model falls from 120 GB (full) to ~40 GB (LoRA) to ~12 GB (QLoRA). (68–72)

## Diagrams

Memes and decoration, not mechanisms: 10 (shredded-paper "Data" meme), 12 (penguin GIF), 16
(Winnie-the-Pooh meme: plain Pooh "OPEN AI · Pre-training using thousands of GPUS", tuxedo Pooh
"NORMAL FOLKS · Use Parameter Efficient Finetuning"), 27 ("I'm lost" dog with "What? How? Why?"),
52 (pizza and a cartoon mouse), 53/56 (dough and cheese icons) and 73 (cat-and-mouse meme). The
dough icon sits in the corner of 54–55, the cheese on 57–65 and the pizza on 66–67. Those icons
tell you which "ingredient" a slide belongs to.

- **5 · an instruction dataset as a table.** Three blue-headed columns: **Instruction | Context |
  Output**. Three rows:
  - "Suggest a good restaurant" | "Los Angeles, CA" | a named Italian restaurant in LA;
  - "Rewrite the sentence with more descriptive words" | "The game is fun" | "The game is
    exhilarating and enjoyable";
  - "Calculate the area of the triangle" | "Base: 5cm; Height: 6cm" | "…15 cm²".

  Credited to the Alpaca-GPT4 dataset. Purpose: show what one training example looks like. A
  re-draw can show a three-part card, then the tutorial's two-part version (question, answer).
  That version becomes a Gemini JSONL line with `user` and `model` turns, and in the notebook a
  Qwen chat-template string.
- **7–8 · the "Sure…" fingerprint.** A dark mobile ChatGPT 4o screen. The user bubble asks for a
  haiku about making pizza. The reply's first line, "Sure, here's a haiku about making pizza:",
  has a red box around it on 7, and three short haiku lines follow. Slide 8 removes the box and
  adds the contrast with next-word prediction. Purpose: instruction tuning leaves a visible
  habit. A re-draw can show two answers side by side: a raw model that merely continues the
  prompt, and a tuned one that opens with a preamble. That is the same effect as the tutorial's
  Pavlos openers ("Welcome welcome…", "Yello…").
- **14 · the 120 GB memory stack.** Title "10B parameter model". A vertical stack of blue boxes
  with sizes to their right:
  - "Parameters (FP16)" — 20GB;
  - "Gradient (FP16)" — 20GB;
  - a taller box "Optimizer States (FP32)" containing "Momentum" and "Variance" — 80GB.

  Red speech bubbles point at the optimizer box from both sides. Left: "We use the Adam
  Optimizer." Right: these states generally need more precision. The arithmetic behind it:
  10B × 2 bytes = 20 GB, twice, plus 2 states × 4 bytes × 10B = 80 GB. A re-draw should keep
  the three bars proportional (1 : 1 : 4).
- **15 · how many GPUs.** The same stack at left. At right, five red tiles "4090 GPU", each
  labelled 24GB: four in a row, the fifth under the first. An orange thought cloud says the model
  needs at least five top consumer GPUs to fine-tune. 5 × 24 GB = 120 GB, with no headroom for
  activations. A re-draw can pour the stack into 24-GB buckets.
- **19–20 · the PEFT family map** (from "Scaling Down to Scale Up"). Three overlapping circles:
  - **Additive** (top, blue), callout "Add trainable layers or parameters to model";
  - **Reparametrization-based** (lower left, yellow; spelled "Reparamertization-based" on the
    slide), callout "use low-rank representations to minimize the number of trainable
    parameters";
  - **Selective** (lower right, orange), callout "Subsets the existing parameters to finetune".

  Methods by region:
  - Additive only: Ladder-Side Tuning, AttentionFusion;
  - Additive ∩ Reparametrization: PHM Adapter;
  - Additive ∩ Selective: Sparse Adapter;
  - all three: S4;
  - Reparametrization only: LoRA, KronA;
  - Reparametrization ∩ Selective: Sparse LoRA;
  - Selective only: Fish-Mask, Attention Tuning.

  Slide 20 draws a black ellipse round LoRA. Purpose: place LoRA in the landscape. A re-draw can
  fade everything but the LoRA label.
- **23–25 · low rank with counted cells.**
  - 23: a 5×5 grid "W", then "=", a 5×1 column "B", "×", a 1×5 row "A". A thought cloud says
    "Rank 1". The headline: any m×n matrix W can be written as B (m×r) times A (r×n).
  - 24: the same picture with counts: "25 elements" under W, and one bracket under B and A with
    "10 elements".
  - 25: B is 5×2 and A is 2×5, "20 elements". The caption says a higher rank gives better
    performance.

  Purpose: the parameter saving of a factorization. Note for a re-draw: at 5×5, rank 2 barely
  saves anything (20 vs 25). The saving grows with size: a d×d matrix needs d² numbers, its
  factors 2·r·d. Scaling up to the tutorial's 2048×1024 `q_proj` with r = 8 (2,097,152 vs
  24,576, digest §3.6) makes the point. Also, W = BA holds exactly only when r is at least W's
  rank. For small r it is an approximation, and LoRA's bet is that the *update* ΔW is
  low-rank.
- **26 · the annotated LoRA equation.** `W₀ + ΔW = W₀ + (α/r)·B·A` with five blue callouts:
  "Initial LLM Weights" → W₀; "Update matrix" → ΔW; "Scaling parameter" → α; "Decomposed
  matrices" → BA; "Rank of BA" → r (under the fraction). The caption reminds you that ΔW is
  decomposed, not W₀. A re-draw can light up each symbol as it is named. Then show the
  notebook's `lora_alpha=16` and `r=8` on the same symbols (scale α/r = 2).
- **28–30 · the LoRA block diagram** (the deck's central mechanism):
  - At the bottom, a red bar "X" (the input), with a bracket "d" over its width.
  - Two blue arrows rise from X. The left one enters a large blue square "Pretrained Weights,
    W₀ ∈ ℝ^{d×d}". The right one enters the adapter: a lower orange box "A = N(0, σ²)", a
    bracket labelled "r", and an upper orange box "B = 0". A's box has bevelled upper corners
    and B's bevelled lower corners, so the pair reads as an hourglass that narrows to width r.
  - From W₀ and from B, blue arrows rise to a red bar "h" at the top, with a blue "+" between
    them. In symbols, h = W₀x + BAx.
  - All three slides carry the caption that the reparameterization (LoRA) runs parallel to the
    original model.
  - On 29, W₀ and its arrows turn grey (frozen). A dashed curved arrow labelled "Backward Pass"
    runs from h down to X. A red box says the backward pass skips the pretrained weights and
    gradients flow only through the adapters (see disagreement 6 above for the precise
    version).
  - On 30 the colours return, and a blue cloud says the update matrix can be merged into the
    original weights at inference to make it efficient.

  Purpose: where LoRA sits, what is trained, and why serving costs nothing extra. A re-draw can
  animate the forward pass (both branches light, outputs add), the backward pass (W₀ greys out,
  a gradient pulse runs down the adapter branch) and the merge (BA slides over and fuses into
  W₀).
- **32–35 · the trainable-parameter table**, built one row per slide: rank 1 (32), + rank 2 (33),
  + rank 8 (34), then all rows (35). Columns: Rank | Model 7B | Model 13B | Model 70B |
  Model 180B. Rows 1, 2, 8, 16, 512, 1024, 8192 and Full (values under Commands and code). A
  warning triangle on 35 says this generalizes from a one-layer LLM. **How the numbers were
  made:** each entry equals 2·r·√N for a model of N parameters. The whole model is treated as
  one square d×d matrix with d = √N, and LoRA adds 2·r·d. For example, √7×10⁹ ≈ 83,666, and
  2 × 83,666 = 167K. Every cell checks out to the rounding shown. Purpose: the scale of the
  saving. Real counts depend on the layer shapes and on which matrices get adapters. The
  notebook's r = 8 on `q_proj`/`v_proj` across 28 layers gives 1,146,880 (digest §3.6), a good
  real-world foil.
- **37–39, 71 · memory columns: full fine-tuning vs LoRA.**
  - Left column, "Full Parameter Fine Tuning": a large light-blue box labelled "Optimizer State
    (FP32)" and a short wide box "Base Model (FP16)". Footer "10B → 120GB".
  - 38 fills the boxes with "100GB" and "20GB". It adds a right column "LoRA" with three rows:
    "Optimizer State (FP32)" with two small dark boxes A and B; "LoRA Adapter (FP16)" with two
    smaller A and B; and "Base Model (FP16)", a wide dark box "20GB". Footer "10B → ~40GB".
  - 39 adds a red callout over the LoRA base model: it is frozen, so it is not optimized, but it
    must still be stored in memory for the forward pass.
  - 71 repeats 38 without the GB labels, with "FP16" under each base model and the footers
    "10B => 120GB" and "10B => ~40GB".

  Note for a re-draw: the "100GB" optimizer box folds slide 14's 20 GB of gradients into the
  80 GB of Adam states. The ~40 GB for LoRA is not itemized on the slides; only the 20 GB base is
  explained. Keep slide 14's three-part split and don't invent a breakdown of the remaining
  ~20 GB.
- **40 · LoRA vs full fine-tuning, measured.** A screenshot of a results table whose caption
  reads "Table 3: GPT-2 medium (M) and large (L) with different adaptation methods on the E2E NLG
  Challenge" (the LoRA paper's table; the slide names no source). Columns: # Trainable Parameters,
  BLEU, NIST, MET, ROUGE-L, CIDEr. Rows: FT, two Adapter variants, Adapterᴴ, FT^Top2, PreLayer and
  LoRA for GPT-2 M; FT, two Adapter variants, PreLayer and LoRA for GPT-2 L. The headline: for
  GPT-2 M, FT trains 354.92M and scores BLEU 68.2, while LoRA trains 0.35M and scores 70.4. For
  GPT-2 L, FT trains 774.03M (68.5) and LoRA 0.77M (70.4). LoRA's row is in bold for most
  metrics. A blue callout says these metrics are used for performance evaluation. A re-draw
  needs only two bars per model: trainable parameters on a log scale, and BLEU.
- **44 · quantization as buckets.** Three horizontal number lines, each with a cost label at
  right:
  - "Any number between 0 and 100": a plain line with ticks at 27, 55.3 and 83.78. Cost
    "1 num = infinite bytes" (red).
  - "Quantized by whole numbers": a bar of many narrow blue cells. Arrows drop the three values
    to 27, 55 and 83. Cost "0.875 bytes" (7 bits for 101 values).
  - "Quantized by 10s": a bar of ten wide red cells. Arrows drop the values to 20, 50 and 80.
    Cost "0.5 bytes", with an aside "(3 bits ~ 0.375 bytes)".

  Note: this slide buckets by **flooring** (83.78 → 83 → 80), while the Int8 example rounds.
  0–100 in tens has 10–11 buckets, so 4 bits (0.5 bytes) is the honest figure; 3 bits would give
  only 8. A re-draw can drop the same three dots through ever coarser grids while a bits counter
  falls.
- **45–50 · absmax Int8, worked.**
  - 45: a row of ten blue cells, X^FP32 = 1.5, 2.3, 3.7, 4.1, 5.6, 6.8, 7.9, 8.4, 9.2, 10.2. A
    callout explains that FP32 is a 32-bit float. The question: how do we go to Int8?
  - 46: the formula X^Int8 = round(127/absmax(X^FP32) · X^FP32), with three callouts: "Int8
    values range from -128 to 127" (on the 127), "Array of values" (on X^FP32) and "The absolute
    maximum value in the array" (on absmax).
  - 47–48: an arrow collapses the fraction into a constant, X^Int8 = round(c^FP32 · X^FP32). On 48
    the fraction and c^FP32 are red, to show they are the same thing.
  - 49: c^FP32 = 127/10.2 = 12.4509.
  - 50: round(12.4509 × the array) = 18, 29, 46, 51, 69, 85, 98, 105, 115, 127.

  **Arithmetic slip:** rounding gives **19** for 1.5 (18.68) and **70** for 5.6 (69.73). The
  slide's 18 and 69 are truncations, but the other eight values are rounded. A re-draw should
  use 19, 29, 46, 51, 70, 85, 98, 105, 115, 127. A re-draw can scale the row so 10.2 hits the 127
  wall, then snap each value to the integer grid.
- **51 · dequantization.** X^FP32 = X^Int8 / c^FP32, with a thought cloud saying there will always
  be some dequantization error. Worked with correct values: 70 / 12.4509 = 5.622 instead of 5.6,
  and 19 / 12.4509 = 1.526 instead of 1.5. A re-draw can show the round trip with the small gaps
  highlighted.
- **54–55 · NF4's buckets.** At right, a tall narrow bell curve centred on a dashed line at 0.
  Under it are two bars of 16 cells each:
  - red "Equally spaced buckets": all cells the same width;
  - blue "Equally sized buckets": thin cells crowded around the centre and wide ones in the
    tails.

  A pointer labels the blue bar "an enhanced version of quantile quantization". Slide 54's text
  gives 2⁴ = 16; slide 55's says pretrained weights are normally distributed and precision near
  the mean is valuable. Purpose: NF4 spends its 16 levels where the weights are. A re-draw can
  slide 16 evenly spaced lines into the quantile positions under the bell, with each bucket's
  area shaded equal. Here "equally sized" means equal probability mass, not equal width.
- **58–64 · gradient checkpointing on a chain.** An input X, then four circles h₁, h₂, h₃, ŷ
  joined by arrows and labelled Layer 1–4 underneath:
  - 58: all circles white; a forward pass computes each layer's activation.
  - 59: h₁–h₃ are filled light blue (stored). The text: this takes memory; computers are good at
    parallel processing but short of memory.
  - 60: back to plain circles; keep only what is needed and drop activations once the next one
    has been computed.
  - 61: h₁–h₃ are empty circles with no labels (discarded). The backward pass must recompute
    them, so checkpoints are introduced.
  - 62: all labels are back (recomputed). Checkpoints sit every √n layers, so recomputation does
    not start from the beginning.
  - 63: only h₂ is filled (the checkpoint); h₁ and h₃ are empty. It helps with out-of-memory
    errors but doesn't remove them; long sequences still cause memory spikes.
  - 64: the same, faded, with a banner saying this is where the second ingredient comes in.

  A re-draw can run a forward sweep (fill, then empty all but the checkpoint) and a backward
  sweep that refills h₃ from h₂, with a memory meter beside it.
- **65 · paging between GPU and CPU.** Title "Paged Optimizer - Looping in your CPU". Two
  dashed rounded boxes, "GPU" with six page icons and "CPU" with two. A light-bulb callout
  defines paging: RAM split into fixed-size blocks called pages. The slide is a build: a yellow
  "⚠ GPU Memory is full" note (visible only in the extracted text) is overlaid by a green
  "✅ GPU Memory has space now." Pages have moved to the CPU. A blue callout says that a page is
  moved back to the GPU for computation when it is needed and there is room. Body text: automatic
  page-to-page transfers between CPU and GPU; it avoids the memory spikes that gradient
  checkpointing leaves with long-sequence mini-batches.
- **66–67 · BF16 tags and the float formats.** Slide 28's LoRA diagram again, with "BF16" tags
  beside W₀ and beside B and A. 67 overlays a figure (credited "Image Source") of three bit
  layouts:
  - IEEE half precision, 16 bits: 1 sign, 5 exponent, 10 fraction;
  - bfloat16: 1 sign, 8 exponent, 7 fraction;
  - NVIDIA TensorFloat-32, 19 bits: 1 sign, 8 exponent, 10 fraction.

  A cloud with a Google logo says BF16 keeps FP32-like range with less precision, to speed up
  training. A re-draw can line up FP32, FP16 and BF16 bit strips, with the exponent width
  (range) and fraction width (precision) highlighted.
- **68–70 · QLoRA's block diagram.** Slide 66's diagram plus a dark "NF4" tag beside W₀, under
  its "BF16" tag. A dough icon marks "Ingredient 1: 4-Bit NormalFloat".
  - 68: W is stored as NF4.
  - 69, "Forward Pass": dequantize W from NF4 to BF16, compute with the BF16 W, A and B, then
    delete the BF16 copy of W.
  - 70, "Backward Pass": W₀ greyed with its NF4 tag, the dashed backward arrow from h to X.
    As in LoRA, W stays frozen and gradients go only to the adapters; repeat until a minimum.

  A re-draw can show W₀ as a compact 4-bit block that briefly "inflates" into a BF16 copy for
  the matmul and deflates again.
- **72 · QLoRA's memory column.** Cheese icon, "Ingredient 2: Paged Optimizer", title "QLoRA".
  Three rows:
  - "Optimizer State (FP32)": three blue tiles, each with a page icon;
  - "LoRA Adapter (BF16)": three plain tiles;
  - "Base Model": one small tile, "4bit NormalFloat".

  A dashed "CPU" box at right holds six pages. Curved arrows run from the middle optimizer tile
  out to the CPU and from the CPU back to the right-hand tile. A blue callout says pages go to
  the CPU when the GPU lacks space and come back when needed and there is room. Footer
  "10B => ~12GB". The ~12 GB is not itemized; a 4-bit base for 10B parameters is about 5 GB
  (my arithmetic). A re-draw can put 38's two columns and this one side by side, with
  120 → ~40 → ~12 GB as a shrinking bar.

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / notebook / digest |
|---|---|---|
| "LLM Finetuning", "Finetuning" / "fine-tuning" / "Fine Tuning" (all three spellings) | 1, 4, 18, 37 | README: "Fine-tune Gemini", "Fine-tuning"; notebook title "Tutorial - Finetuning with QLoRA". |
| "instruction fine-tuning", "Instruction-tuning", "instruction dataset" (instructions, answers, context) | 2–16, 4–5 | The tutorial's dataset is question/answer pairs, with no context field (README "Generate Question Answer Dataset"). Its CSV is named `instruct-dataset.csv`, echoing the slides' term. |
| "Instruction", "Context", "Output" (Alpaca columns) | 5 | Tutorial: `question`, `answer`. Gemini JSONL uses roles `user`/`model`; the notebook's chat template uses `user`/`assistant`. |
| "Task-specific fine-tuning" | 6, 9 | The tutorial's cheese persona tuning is a task/style-specific fine-tune. |
| "catastrophic forgetting" | 9–10, 36 | Not in the README. Closest in the notebook: Poll 4 (the model takes on the style but keeps most general knowledge, digest Step 23). |
| "multi-task finetuning" | 10 | Not in the tutorial. |
| "Full Parameter" (fine-tuning) | 2–16, 37–39, 71 | Neither track does it. Track A tunes an adapter (`adapter_size`); Track B uses LoRA. |
| "FP16 (half precision)", "FP32", "Int8", "BF16 (BrainFloat16)" | 13–15, 45–50, 66–67 | Notebook: `bnb_4bit_compute_dtype="float16"`, `fp16=True`; its GPU check reports bf16 support but still trains in float16 for T4s. **The slides' QLoRA uses BF16; the notebook uses FP16** (disagreement 1). |
| "Parameters", "Gradient", "Optimizer States", "Momentum", "Variance", "Adam Optimizer" | 14–15 | Notebook: `optim="paged_adamw_32bit"`, Adam(W) with 32-bit states, as on slide 72. |
| "PEFT" / "Parameter Efficient Finetuning" / "Parameter-Efficient Fine-Tuning (PEFT)" | 2, 17–20 | Also the name of the Hugging Face library the notebook uses (`peft` 0.20.0). The slides never mention the library. |
| "Additive", "Selective", "Reparameterization" (18) / "Reparamertization-based" (19, sic) | 18–20 | Not in the tutorial. |
| "LoRA", "update matrices", "rank decomposition weight matrices", "adapters", "LoRA Adapter" | 22, 29, 38, 41, 70, 72 | Notebook: `LoraConfig`, "adapters", the saved adapter folder (~4.6 MB). Track A's `adapter_size="ADAPTER_SIZE_FOUR"` is, by the digest's reading, the managed analogue of a LoRA rank (§3.4); the README never says "LoRA". |
| "Initial LLM Weights" W₀, "Update matrix" ΔW, "Scaling parameter" α, "Decomposed matrices" BA, "Rank of BA" r | 26–27 | Notebook comments use the same words: `lora_alpha=16` "# The LoRA scaling parameter", `r=8` "# Rank of the LoRA" (digest Excerpt 11). |
| "Pretrained Weights W₀ ∈ ℝ^{d×d}" | 28–30, 66–70 | Square on the slides. Real projections are not square: Qwen3-0.6B's `q_proj` is 2048×1024 (d_out × d_in, digest §3.6). |
| "B = 0", "A = N(0, σ²)" | 27–30, 66–70 | B = 0 matches PEFT. **A differs:** PEFT's default is Kaiming-uniform; `init_lora_weights="gaussian"` is an option (disagreement 3). |
| "reparameterization (LoRA) runs parallel to the original model" | 28–30 | Same structure as PEFT's LoRA layer: base output + scaled adapter output. |
| "merged" (update matrix merged with original weights) | 30 | Notebook: `merge_and_unload()` on an FP16 reload, saved as `…_merged` (~1.2 GB). |
| "Number of trainable parameters" | 32–35 | Notebook: "trainable params: 1146880 \|\| all params: 376995840 \|\| trainable%: 0.30…". |
| "Base Model" | 37–39, 71–72 | Notebook: `base_model`; digest's evaluation table "Base (4-bit)". |
| "quantization", "splitting range into buckets", "buckets" | 43–44, 54–55 | Notebook: 4-bit loading, `Linear4bit` layers, the "Deeper Dive" note on FP4 vs NF4 (digest Step 19). |
| "absmax", "dequantize", "dequantization error" | 46–51 | bitsandbytes uses an absmax constant **per block of weights**, not per array (digest §3.5). The slides never name c; the QLoRA paper calls it the quantization constant. |
| "4-Bit NormalFloat" / "NF4" / "4bit NormalFloat" | 53–55, 68–72 | `bnb_4bit_quant_type="nf4"`; bitsandbytes' default would be `"fp4"`. |
| "quantile quantization", "Equally spaced buckets", "Equally sized buckets" | 54–55 | Not in the tutorial. |
| "Double quantization" | 53 (sticky note) | `bnb_4bit_use_double_quant=True` in the notebook. **Skipped on the slides, used in the notebook** (disagreement 2). |
| "Paged Optimizer", "paging", "pages" | 53, 56, 65, 72 | `optim="paged_adamw_32bit"`. |
| "gradient checkpointing", "checkpoints", "activations", "hidden states", "OOM (Out of memory)", "memory spikes" | 57–65 | The notebook turns gradient checkpointing on through `prepare_model_for_kbit_training` (digest §3.7); `use_cache = False` goes with it (digest Step 21). |
| "Forward Pass", "Backward Pass", "minima" | 29, 69–70 | Notebook: `trainer.train()`, 450 steps; the loss falls from 2.01 to 1.35 (digest Step 23). |
| "Ingredient 1" / "Ingredient 2", "The Pizza" | 52–72 | The lecture's metaphor: dough = NF4, cheese = paged optimizer, pizza = QLoRA. Not in the tutorial. |
| "4090 GPU" (24GB), "A100" | 11, 15 | The notebook's stored run used an A100; Colab offers T4, L4 and A100. |
| "Training Cycle – LLM" | 42 | Outline item with no slides in this deck. |

Slips on the slides, so a scene does not copy them:
- Slide 50 gives 18 and 69 where rounding gives 19 and 70.
- Slide 44 floors where the Int8 example rounds, and its "3 bits" aside cannot hold eleven
  tens-buckets.
- Slide 23 says *any* matrix factors as BA; that is exact only when r is at least W's rank.
- Slide 25 says a higher rank gives better performance; it gives more capacity, at more cost
  (digest Poll 3).
- Slides 29 and 70 say the backward pass doesn't use the pretrained weights. W₀ gets no update,
  but gradients still pass through it.
- Slide 66 says "FP16 in LoRA" as if it were part of LoRA; it is only the deck's LoRA set-up.
- Slides 38 and 71 call 100 GB "Optimizer State" though it includes the 20 GB of gradients.
- Slide 11's GPT-4 figures are uncited estimates, not official numbers.
- Typos: "relavant" (6), "update matix" (26), "Reparamertization" (19–20), "a minima" (70).

## Commands and code on the slides

There are no shell commands, Python, Docker or configuration on the slides. The only literal
formulas and numbers are:

- 14–15 · `10B parameter model`: `Parameters (FP16) 20GB`, `Gradient (FP16) 20GB`,
  `Optimizer States (FP32) 80GB` (Momentum, Variance); `4090 GPU 24GB` × 5.
- 11 · ~25,000 A100 GPUs, ~90–100 days, nearly $100 million (GPT-4, "Fun Fact").
- 23 · `W ∈ ℝ^{m×n}`, `W = BA`, `B ∈ ℝ^{m×r}`, `A ∈ ℝ^{r×n}`.
- 24–25 · `25 elements` vs `10 elements` (rank 1) and `20 elements` (rank 2).
- 26–27 · `W₀ + ΔW = W₀ + (α/r)·BA`.
- 28–30 · `W₀ ∈ ℝ^{d×d}`, `B = 0`, `A = N(0, σ²)`, widths `d` and `r`.
- 32–35 · trainable parameters by rank (columns Model 7B / 13B / 70B / 180B):

  | Rank | 7B | 13B | 70B | 180B |
  |---|---|---|---|---|
  | 1 | 167K | 228K | 529K | 849K |
  | 2 | 334K | 456K | 1M | 2M |
  | 8 | 1M | 2M | 4M | 7M |
  | 16 | 3M | 4M | 8M | 14M |
  | 512 | 86M | 117M | 270M | 434M |
  | 1024 | 171M | 233M | 542M | 869M |
  | 8192 | 1.4B | 1.8B | 4.3B | 7B |
  | Full | 7B | 13B | 70B | 180B |

  (Slide 32 writes "334k" in lower case.)
- 37–39, 71–72 · `10B → 120GB` (full), `10B → ~40GB` (LoRA), `10B => ~12GB` (QLoRA);
  `Optimizer State (FP32) 100GB`, `Base Model (FP16) 20GB`.
- 40 · GPT-2 M: FT 354.92M params, BLEU 68.2; LoRA 0.35M, BLEU 70.4. GPT-2 L: FT 774.03M, 68.5;
  LoRA 0.77M, 70.4.
- 44 · `27`, `55.3`, `83.78` → `27`, `55`, `83` → `20`, `50`, `80`; `1 num = infinite bytes`,
  `0.875 bytes`, `0.5 bytes (3 bits ~ 0.375 bytes)`.
- 45 · `X^FP32 = [1.5, 2.3, 3.7, 4.1, 5.6, 6.8, 7.9, 8.4, 9.2, 10.2]`.
- 46–48 · `X^Int8 = round( 127 / absmax(X^FP32) · X^FP32 )`, `X^Int8 = round(c^FP32 X^FP32)`;
  Int8 range `-128` to `127`.
- 49 · `c^FP32 = 127 / absmax(X^FP32) = 127 / 10.2 = 12.4509`.
- 50 · `X^Int8 = [18, 29, 46, 51, 69, 85, 98, 105, 115, 127]` (see the slip above).
- 51 · `X^FP32 = X^Int8 / c^FP32`.
- 54 · `2^4 = 16` possible buckets.
- 62 · checkpoints every `√n` layers for an n-layer network.
- 67 · bit layouts: FP16 1/5/10, bfloat16 1/8/7, TF32 1/8/10 (sign/exponent/fraction).

## What the lecture stresses

- **Instruction tuning teaches behaviour.** The "Sure…" opener is the visible result; a raw
  next-word model would not answer that way. (7–8)
- **Be careful with task-specific fine-tuning**: catastrophic forgetting can erase earlier
  abilities. The fix (multi-task fine-tuning) is expensive in data and compute. (9–10)
- **Full-parameter fine-tuning is a memory problem, not just a compute problem.** The optimizer
  states, kept in FP32 because they need precision, are the biggest item. (11, 14)
- **It is inaccessible to "normal folks like us".** "So, what can we do?" sets up PEFT. (16)
- **Decompose the update, not the weights.** It is stated as a "Remember" on 26.
- **Initialize B to zero** and A randomly. (27)
- **LoRA runs in parallel to the original model.** The caption is repeated on 28–30.
- **Merge at inference** so serving costs nothing extra. (30)
- **The parameter table is a one-layer simplification.** It carries a warning sign. (35)
- **LoRA forgets less**, because the original weights are kept. (36)
- **LoRA is not enough on its own**: the frozen base still has to fit in memory for the forward
  pass. "Isn't it enough?" (37–39)
- **LoRA is as good as full fine-tuning**, and sometimes better. (40)
- **Quantization always loses something**: there is always some dequantization error. (51)
- **Precision near the mean is what matters** for normally distributed weights, hence NF4. (55)
- **Out of memory is the problem everyone has hit** training a network. GPUs have compute to
  spare; memory is the bottleneck. (57, 59)
- **Gradient checkpointing helps but doesn't fix OOM**: memory spikes remain with long
  sequences. (63–64)
- **QLoRA's recipe**: store in NF4, compute in BF16, delete the temporary BF16 copy, train only
  the adapters, and page the optimizer state to the CPU when the GPU is full. (68–72)
- **The headline numbers to remember**: 120 GB → ~40 GB → ~12 GB for a 10B model. (37–39, 71–72)

## Pointers

- **Alpaca-GPT4 dataset.** Slide 5 links it as the source of the example table. The URL is not
  in the extracted text.
- **"Scaling Down to Scale Up" (arxiv.org).** Slides 19–20 credit the PEFT Venn diagram to this
  paper, the PEFT survey by Lialin, Deshpande and Rumshisky (2023). The slide gives only the
  title and "arxiv.org".
- **LoRA results table.** Slide 40 shows a table captioned "Table 3: … E2E NLG Challenge" with
  no source on the slide. It is from the LoRA paper (Hu et al., 2021). The deck does not name
  the LoRA or QLoRA papers anywhere.
- **Float-format figure.** Slide 67 has an "Image Source" link. The URL is not in the extracted
  text.
- **ChatGPT 4o screenshot.** Slides 7–8.
- **Skipped material.** Double quantization is "skipped here" (53). The outline on 42 lists
  "Training Cycle – LLM", which this deck does not contain.
- **No tutorial pointer.** The deck links neither the `llm-finetuning` repo, the Colab
  notebook, the Ed lesson, the README's hosted "Pavlos Cheese Model" demo, nor any homework or
  milestone. The pairing of these slides with the tutorial comes from the course site (see
  `digest.md`). For a scene, the closest tutorial anchors are:
  - slides 4–5 → `dataset-creator --generate/--prepare` (the instruction dataset);
  - 22–30 → the notebook's `LoraConfig` and `SFTTrainer`;
  - 43–55 → `BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", …)`;
  - 57–65 → `prepare_model_for_kbit_training` and `paged_adamw_32bit`;
  - 30 → `merge_and_unload()`.
