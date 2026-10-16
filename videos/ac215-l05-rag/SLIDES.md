# L05 lecture slides — Introduction to RAG and Advanced RAG

Source: two decks by Pavlos Protopapas (AC215, SEAS/Harvard).

- **Deck A**, `L05_RAGs_I_fix` (64 slides), titled "Lecture 5: Introduction to RAG".
- **Deck B**, `Lec05b_RAG_II_added_j_suffix_in_RRF` (89 slides), titled "Lecture 5 suppl: Advanced RAG".

These are the instructor's lecture slides (PDF), provided by the student for study; the PDFs are
not in this repository; slide numbers are PDF page numbers. This digest cites them as **A12**
(deck A, page 12) and **B46** (deck B, page 46). I wrote it from both decks' extracted text and
from all eighteen contact sheets. I also enlarged A11, A12, A13, A16, A18, A21, A25, A26, A32, A37,
A53, A58 and B5, B18, B19, B43, B46, B53, B57, B59, B60, B76, B78, B81, B85 and B88 to read their
diagrams. Everything below is in my own words. Only short titles, terms, formulas and single lines
are quoted. The tutorial side of the lecture is in [`digest.md`](digest.md).

Read this first:

- **The printed footer numbers are not the slide numbers.** Both decks were cut from longer ones.
  After the unnumbered title slides, deck A's footers run 8, 10–17, (none), 19–37, 39–45, 47,
  49–57, 59–73, (none), 75. Deck B's run 3–33, 35–41, 43–46, 48–61, 63–73, 75–80, 82–86, 88–92,
  96–98, 100, 113. Always cite the PDF page numbers used here.
- **How the decks map onto the tutorial (`dlops-io/llm-rag`).** Deck A explains, piece by piece,
  the pipeline the tutorial builds: chunk, embed, store in a vector database, query, assemble the
  prompt, generate. Deck B's semantic-chunking walk-through (B19–B34) matches the README's
  "Advanced RAG: Semantic Chunking" step, though the rule differs (see Terms). The rest of deck B
  (query rewriting, hybrid search with BM25 and RRF, re-ranking with cross-encoders, Self-RAG) has
  **no code in the tutorial**. A scene can teach it only as a concept. Neither deck mentions the
  tutorial, ChromaDB, Gemini, Vertex AI, Docker or any command.
- **Lecture numbering.** Both title slides say "Lecture 5". The course site's weekly schedule calls
  the same session "Lecture 4" (digest E17), so the slides support the series' L05 label.
- **Where the slides and the tutorial disagree** (details under Terms):
  1. the semantic-chunking rule (a fixed 0.8 similarity threshold vs the code's 95th percentile of
     distances);
  2. where metadata filtering happens (after ranking on the slides, before ranking in Chroma);
  3. similarity scores (higher is better) vs Chroma's cosine distances (lower is better);
  4. what "Indexing" means;
  5. the system prompt (part of the final prompt on the slides, defined but never sent in the
     tutorial, digest E1).

## Outline

**Deck A — "Lecture 5: Introduction to RAG"** (two sections, listed on A3).

- A1 · title slide
- A2 · "Logistics / Reminders": groups, Milestone 1, office hours, AWS credits, team form (QR code)
- A3 · outline: Introduction - RAG; Naïve RAG
- Slides A4–A14 · **Introduction - RAG**
  - A4 · outline with "Introduction - RAG" in bold
  - A5 · divider, with a Winnie-the-Pooh meme: plain Pooh "Hallucinating LLMs", tuxedo Pooh "LLMs
    with RAG"
  - A6 · "LLMs ISSUES?": four problems
  - A7 · the same, with a banner saying RAG tackles the first two
  - A8 · option 1 for many documents: pass all the text to the LLM → "Garbage"
  - A9 · option 2: fine-tune the LLM → "Takes too long!"
  - A10 · option 3: use RAG, with a meme ("LLMs with all their problems" / "RAGs")
  - A11 · "Retrieval Augmented Generation": a dense landscape map of advanced-RAG techniques, red
    arrows to four questions (What is Vector Database? What is query? What is context? What is
    embedding?), and a confused-face meme
  - A12 · "What is RAG?": definition and a five-box flow
  - A13 · "What is RAG?": a query linked to one paragraph of a cheese-making document
  - A14 · "What is RAG?": query + context into the LLM, an answer out
- Slides A15–A62 · **Naïve RAG**
  - A15 · outline with "Naïve RAG" in bold
  - A16 · the Naïve RAG pipeline diagram (Knowledge Base outlined)
  - A17 · "Naïve RAG – Knowledge Base": websites, PDF files, Word files
  - A18 · pipeline again (Knowledge Base outlined)
  - A19 · pipeline (Chunking outlined)
  - A20–A22 · "Naïve RAG - Chunking": definition (A20), the document cut into three chunks (A21),
    banner "different methods of chunking … discussed later" (A22)
  - A23 · pipeline (Chunking outlined)
  - A24 · pipeline (Embedding Model outlined)
  - A25 · the embedding model turns each chunk into a vector (BERT-like callout)
  - A26 · "Index data": Lexical, Graphical, Semantic
  - A27 · picture slide, "Semantic Embeddings" (three stacked vectors)
  - A28 · "Sentence Embeddings": two sentences as two vectors
  - A29 · pipeline (Embedding Model outlined)
  - A30 · pipeline (Vector Database outlined)
  - A31 · "Naïve RAG – Vector Database": why relational databases are not enough
  - A32 · vector database definition and its four-stage strip (Indexing → Vector Database →
    Querying → Post Processing)
  - A33–A36 · the query compared with millions of vectors one by one ("very slow"), the query
    vector moving down the list
  - A37 · what an index is
  - A38 · three indexing algorithms (LSH, PQ, HNSW), PostgreSQL callout
  - A39 · querying: nearest neighbour; the cheese query becomes a query vector
  - A40–A43 · "Pavlos game #4275": who is most similar to Pavlos? Big Five scores (A41), the
    cosine-similarity formula (A42), the three similarities (A43)
  - A44 · "But, how do we compare?": cosine, Euclidean, dot product
  - A45–A47 · "Similarity Measures" table, built up row by row (cosine; + Euclidean; + dot product)
  - A48–A53 · ranking: similarity scores appear one by one (A48–A52), then the vectors re-sort and
    top-K is introduced (A53)
  - A54 · Post Processing: optional re-ranking and metadata filtering
  - A55 · metadata filtering example (author, publication date, category)
  - A56 · pipeline (Vector Database outlined)
  - A57 · pipeline ("Prompt + query + context" outlined)
  - A58 · "Naïve RAG – Prompt + query + context": the three parts defined
  - A59 · a worked final prompt (system prompt, user query, context)
  - A60 · pipeline ("Prompt + query + context" outlined)
  - A61 · pipeline (LLM outlined)
  - A62 · the LLM step: "Nothing new to be added" (sleeping-Pikachu picture; title still reads
    "Naïve RAG – Vector Database")
- A63 · the landscape map of A11 again, closing the four questions
- A64 · closing "THANK YOU!" picture (Tom the cat bowing)

**Deck B — "Lecture 5 suppl: Advanced RAG"** (five sections, listed on B2; each section opens
with the outline repeated and the current item in bold, then a divider).

- B1 · title slide
- B2 · outline: Naïve RAG - Recap; Pre-Retrieval Optimization; Retriever Optimization;
  Post-Retrieval Optimization; Self-RAG
- Slides B3–B10 · **Naïve RAG - Recap**
  - B3 · outline (Recap bold)
  - B4 · divider, with a handshake meme ("User after getting a response" / "LLM hallucinating and
    making things up")
  - B5 · the deck-A pipeline with numbered steps 1–6 and three dashed phase boxes (Indexing,
    Retrieval, Augmentation & Generation)
  - B6 · "Now, let's look at the big picture": Indexing → Retrieval → Augmentation & Generation
  - B7 · + a Pre-Retrieval band
  - B8 · the same, blurred, with a callout on what Pre-Retrieval deals with
  - B9 · + a Post-Retrieval band
  - B10 · the same, with a callout on what Post-Retrieval does
- Slides B11–B39 · **Pre-Retrieval Optimization**
  - B11 · outline (Pre-Retrieval bold); B12 · divider
  - B13 · two levers: 1. Indexing, 2. Query Manipulation
  - B14–B34 · "Pre-Retrieval Optimization - Indexing"
    - B14–B15 · character splitting a two-sentence text at chunk size 50
    - B16 · a mock research paper split at chunk size 200
    - B17 · meme over B16 ("Do you see the problem here?")
    - B18 · B16 with the bad cut points marked in red
    - B19 · "The optimal way": one chunk per section, "This is called semantic chunking"
    - B20 · meme over B19 ("Huh? What?")
    - B21 · "Semantic Chunking – Steps" (four steps)
    - B22–B33 · worked example over six sentences (anchor, window, groups, similarities, chunk)
    - B34 · B19 again (without the cloud)
  - B35–B39 · "Pre-Retrieval Optimization – Query Manipulation"
    - B35 · divider
    - B36 · two problems: cluttered and ambiguous queries
    - B37 · cluttered query → rewritten query (dolphin picture)
    - B38 · ambiguous query about a Microsoft annual report
    - B39 · the LLM's rewrite of it, flagged as made up
- Slides B40–B48 · **Retrieval Optimization** (named "Retriever Optimization" on B2, B3, B11)
  - B40 · outline (Retrieval bold); B41 · divider, with a SpongeBob meme ("LLM" vs "LLM+RAG")
  - B42 · "Retrieval Optimization – Hybrid Search": keyword matching plus vectors, the Chester
    sentence
  - B43 · BM25 and TF-IDF (two callouts; "To learn more about BM25: Click here")
  - B44 · three candidate paragraphs, annotated
  - B45 · their BM25 and vector-search ranks
  - B46 · the Reciprocal Rank Fusion (RRF) formula
  - B47 · RRF computed for the three paragraphs
  - B48 · the fused ranking 1, 2, 3
- Slides B49–B65 · **Post-Retrieval Optimization**
  - B49 · outline (Post-Retrieval bold); B50 · divider, with a Simpsons crowd meme labelled CNN,
    GPT, LLM, RNN, RAG and "ME"
  - B51–B57 · "Post-Retrieval – Re-ranking": all chunks in the vector database (B51), the query
    arrives (B52), the retriever returns top-K = 25 with the truly relevant records scattered
    (B53), meme "I think I see the problem" (B54), cosine misses key details (B55), meme "What do
    we do now?" (B56), a re-ranker reorders the list (B57)
  - B58–B59 · two questions and their answers; bi-encoder callout (B59)
  - B60 · bi-encoder diagram
  - B61 · why retrieval is fast; its drawback is information loss
  - B62 · B61 dimmed, with a callout defining a cross-encoder
  - B63 · cross-encoder diagram, "Can you guess why reranking is slower…?"
  - B64 · the cross-encoder is better but slow; the two balance each other
  - B65 · that conclusion with an "epic handshake" meme (Retrieving × Reranking, "Strong
    together")
- Slides B66–B88 · **Self-RAG**
  - B66 · outline (Self-RAG bold); B67 · divider (the B50 meme again)
  - B68 · three limitations of advanced RAG
  - B69–B71 · open-book exam intuition: question (B69), answer A highlighted (B70), meme "But
    why?" (B71)
  - B72 · costs of always looking things up; B73 · the same with a "Self-RAG" banner
  - B74 · "Self-RAG - Introduction": reflection tokens, two types
  - B75 · "Self-RAG – Retrieve token": definition
  - B76 · the retrieve-token decision tree
  - B77 · B76 dimmed under "How to check if the extracted context is relevant?"
  - B78 · "Self-RAG – Critique token": IsREL, IsSUP, IsUSE, with "A hallucination check" callout
    on IsSUP
  - B79 · the same, "Let's summarize all the new tokens!" (no summary slide follows)
  - B80 · example where no retrieval is needed (summer-vacation essay)
  - B81–B84 · example "How did US states get their names?": three chunks checked one by one
    (B81 relevant and supported; B82 not relevant; B83 relevant, partially supported; B84 overlay
    "take the best … using the ISUSE token")
  - B85 · ISUSE ratings of the three responses (5, 1, 3)
  - B86 · the best response becomes the new response
  - B87 · B86 dimmed under "The RETRIEVE token is used!" (Continue → retrieve more)
  - B88 · the retrieve/continue loop and the final response
- B89 · closing "And…. we are done! Thank you!" (cartoon, "Students after the session is over")

## Key ideas

1. **LLMs have four weaknesses.** Their training data is updated rarely. They lack knowledge of
   specialised domains. They hallucinate. They do not cite their sources. The lecture presents
   RAG as the fix for the first two. (A6–A7)
2. **Three ways to put many documents in front of an LLM.** Pasting all of the text into the
   prompt overloads the context and the output is garbage. Fine-tuning on the documents takes too
   long (and comes in a later lecture). RAG is the third way. (A8–A10)
3. **RAG fetches the relevant pieces and adds them to the prompt.** The user's question goes to a
   RAG component, which asks a vector database for related text. It combines the question and the
   retrieved texts into a full prompt for the LLM, and the LLM's response goes back to the user.
   It helps most when answers need accurate, detailed information. (A12–A14)
4. **Naïve RAG is two lanes that share one embedding model and one database.** Lane 1: knowledge
   base → chunking → embedding model → document embeddings → vector database. Lane 2: user query →
   the same embedding model → query embedding → vector database. The database's output, a prompt
   with query and context, goes to the LLM, whose response returns to the user. (A16, B5)
5. **A knowledge base is any useful source**: websites, PDF files, Word files. (A17)
6. **Chunking cuts documents into smaller pieces** so the model can focus on the relevant
   information. There are several methods (deck B). (A20–A22)
7. **The embedding model turns text into vectors that capture meaning.** It is applied to
   document chunks and to queries alike. The slides describe it as BERT-like, pooling word
   embeddings into one vector per text. A sentence embedding is not the same as a word embedding.
   Two sentences are similar when their vectors are close. (A25, A27–A28)
8. **Data can be indexed lexically, as a graph, or semantically.** The lecture follows the
   semantic (embedding) route; keyword search returns in deck B as hybrid search. (A26; B42–B43)
9. **Relational databases cannot search by meaning.** They are good at exact matches, ranges and
   structured relations, but cannot tell that "best cheese for melting" and the cheeses Pavlos
   would pick for a midnight snack mean similar things. Vector databases fill that gap. (A31)
10. **A vector database indexes, stores, queries and post-processes vectors**, for fast retrieval
    and similarity search. (A32)
11. **An index avoids comparing the query with every vector.** With millions of vectors a
    sequential scan is too slow. An index maps the vectors into a data structure that lets a query
    jump to a small subset of likely neighbours. The usual families are hashing (LSH), quantization
    (PQ) and graphs (HNSW). Relational databases such as PostgreSQL now offer a vector column type.
    (A33–A38)
12. **Querying means finding the nearest neighbours of the query vector** among the indexed
    vectors. (A39, A44)
13. **Cosine similarity compares directions.** It is the dot product divided by both lengths, the
    cosine of the angle between the vectors. In the "Pavlos game", Big-Five personality scores are
    five-number vectors, and option A comes out most similar to Pavlos (0.986, then 0.976 and
    0.886). (A40–A43)
14. **Pick the similarity measure to fit the data.** Cosine ignores magnitude and suits text
    embeddings. Euclidean distance captures magnitude and suits numeric feature vectors. Dot
    product mixes both and suits cases where a vector's length means importance or confidence.
    (A44–A47)
15. **Scoring every candidate gives a ranking, and RAG keeps the top K**, with K fixed in
    advance. (A48–A53)
16. **Post-processing is optional.** An advanced setup re-ranks the retrieved results with a
    different measure. It can also filter by metadata (data about the data: author, publication
    date, category). (A54–A55)
17. **The final prompt has three parts.** The system prompt tells the model how to behave. The
    query is the user's input. The context is the relevant text retrieved from the database. The
    example casts the model as a cheese expert. (A57–A59)
18. **The LLM itself is unchanged.** RAG reuses the LLM from earlier sessions. (A61–A62)
19. **Advanced RAG adds stages around retrieval.** The big picture is Indexing → Retrieval →
    Augmentation & Generation. Pre-Retrieval improves what goes in: chunking, embedding and
    handling the embeddings, plus the query. Post-Retrieval polishes what the retriever returns.
    (B5–B10)
20. **Pre-retrieval has two levers: better indexing (chunking) and query manipulation.** (B13)
21. **Fixed-size character splitting breaks meaning.** At 50 characters, a word is cut in two
    (`"…artificial intelli"` / `"gence…"`). At 200 characters, a mock paper's chunks end mid-word
    and run one section's heading into another's text. The ideal chunks follow the document's own
    sections (title, abstract, methodology). That is semantic chunking. (B14–B19, B34)
22. **Semantic chunking walks an anchor through the sentences.** Split on sentence punctuation.
    Pick an anchor sentence and a window of neighbours on each side. Compare the group by cosine
    similarity of embeddings. Join sentences whose similarity clears a threshold (0.8 in the
    example), then move the anchor on. (B21–B33)
23. **User queries can be cluttered or ambiguous.** A cluttered query buries the question in
    chatter; an LLM can rewrite it to the point ("Where do dolphins live?"). An ambiguous query
    lacks information ("Was there significant turnover in the executive team?" asked of a
    Microsoft annual report). (B36–B38)
24. **Rewriting can backfire.** Asked to expand the ambiguous query, the LLM invented specifics
    (CEOs, CFOs, the past year, causes) that have nothing to do with the annual report. (B39)
25. **Hybrid search combines a keyword retriever with a vector retriever.** In "Chester went to
    the bank of the river…", the vectors resolve which kind of "bank" is meant, and keyword
    matching finds documents about "Chester". The keyword retriever is usually BM25. (B42–B43)
26. **BM25 builds on TF-IDF.** TF is how often a word appears in a document. IDF is how rare it is
    across the collection. "the" is frequent everywhere and scores low; "GPT-3" is rare and scores
    high. (B43)
27. **Reciprocal Rank Fusion merges rankings by rank, not by score.** Each retriever j adds
    w_j / (k + r_j(d)) for document d. The weights and k are hyper-parameters. With k = 0 and
    weights 0.5, the three paragraphs score 0.75, 0.67 and 0.42. The near-paraphrase wins even
    though BM25 preferred the money-bank paragraph. (B44–B48)
28. **A fast retriever's top-K holds the right chunks in the wrong order.** For "What is cheese?"
    with top-K = 25, the truly relevant records sit scattered through the list. A simple score
    like cosine similarity misses key details, so a re-ranker reorders the short list and moves
    them to the top. (B51–B57)
29. **Bi-encoders are fast but lose information; cross-encoders are accurate but slow.** A
    bi-encoder embeds documents ahead of time and the query once, so retrieval is one cheap
    comparison per document. But the document vectors never saw the query. A cross-encoder (a
    BERT-like model) reads query and document together and outputs one score, which is better but
    costs a model run per pair. So retrieve broadly with the bi-encoder, then re-rank the few
    survivors with the cross-encoder. (B58–B65)
30. **Advanced RAG still has three gaps.** The chunks may not be relevant. The answer may not be
    supported by the chunks (hallucination). And it retrieves even when retrieval is unnecessary.
    (B68)
31. **Look things up only when you need to.** In an open-book exam you answer familiar questions
    directly and consult the book for the rest. Consulting it every time is slower, adds confusion
    and can bring in irrelevant or wrong information. (B69–B73)
32. **Self-RAG steers retrieval with reflection tokens.** A Retrieve token judges whether
    retrieving (or retrieving more) is useful. Critique tokens judge the results. IsREL asks
    whether a document is relevant. IsSUP asks whether the output is supported by it (the
    hallucination check). IsUSE asks whether the output answers the query, on a 1–5 scale.
    (B74–B79, B85)
33. **Self-RAG in action.** An essay prompt needs no retrieval (Retrieve = No). For "How did US
    states get their names?" it retrieves three chunks and drafts an answer from each. It checks
    each draft with IsREL and IsSUP, discards the irrelevant one, rates the rest with IsUSE and
    keeps the best. Then the Retrieve token decides whether to continue and fetch more, and the
    loop repeats until it says No. (B80–B88)

What the slides leave to the tutorial: they never show any code, Docker Compose, the two
containers, ChromaDB, collections, `gemini-embedding-001`, the 256-number vectors, the chunk
sizes 350/20, recursive splitting, chunk overlap, `n_results=10`, the `where_document` text
filter, or the service account. A scene that needs any of these must take them from
`digest.md`.

## Diagrams

**Deck A**

- **A8 · "pass all the text in".** A stack of document pages (a "Cheese Making" sheet) on the
  left, a cartoon machine labelled "LLM" (funnel in, gears and light bulbs, a horn out) in the
  middle, and the word "Garbage" coming out on the right. A warning triangle and a green callout
  say that too big a context makes the LLM give garbage. Purpose: the naive first idea fails.
- **A9 · "fine-tune instead".** The same pages and LLM machine, with a thought cloud ("We will
  talk about fine-tuning in upcoming lectures") and a green warning box "Takes too long!".
  Purpose: the second idea is too slow. A re-draw can show both as two crossed-out roads before
  the RAG road.
- **A11 (repeated as A63) · RAG landscape map.** A crowded hand-drawn chart of advanced RAG,
  with no credit on the slide. It closely resembles LangChain's "RAG from scratch" overview. A
  central row runs Question → two small circles → three stores (Graph DB, Relational DB,
  VectorStore) → Documents → a filter funnel → a brain → Answer. Colour-coded boxes surround it:
  - Query Construction (yellow): Text-to-SQL, Text-to-Cypher, Self-query retriever;
  - Query Translation (pink): Multi-query, RAG-Fusion, Decomposition, Step-back, HyDE;
  - Routing (orange): logical and semantic routing;
  - Retrieval (green): Re-Rank, RankGPT, RAG-Fusion, CRAG, Active Retrieval;
  - Indexing (blue): Semantic Splitter, Parent Document, Dense X, fine-tuned embeddings, ColBERT,
    RAPTOR;
  - Generation (purple): Self-RAG and related.

  Red arrows point from four labels ("What is Vector Database?", "What is query", "What is
  context?", "What is embedding?") into the chart, and a confused-face meme sits in the corner.
  Purpose: "this looks overwhelming; we will answer four questions". Not a mechanism to animate.
  Our version could show a blurred map with four glowing labels that the episode then answers one
  by one.
- **A12 · RAG in five boxes.** Left to right:
  - a "User" figure;
  - an arrow "Question" to a cluster of three gears labelled "RAG";
  - from RAG, an arrow "Question" to a sparkling stack of books labelled "Vector Database", and an
    arrow "Retrieved Texts" back to RAG;
  - from RAG, an elbow arrow "Full Prompt" down into a box "LLM" (with an OpenAI-style logo);
  - from the LLM, an arrow "Response" back to the User.

  A thought cloud says the vector database comes later in the slides. Purpose: the RAG component
  sits between the user and the LLM, and the database talks only to RAG, never to the LLM.
- **A13–A14 · query meets a paragraph.** A13: a one-page document "Cheese Making" with three bold
  sections: "Definition and Scope", "Key Concepts and Techniques", "Challenges and Innovations".
  A rounded box "Query: What are different techniques of cheese making?" sends dashed lines to
  the middle section, which is outlined. A14: that query and that one paragraph (labelled
  "Context") go into the LLM machine, and out comes "The different techniques of cheese making
  are ….". Purpose: retrieval picks the matching passage, and generation answers from it.
- **A16 (also A18, A19, A23, A24, A29, A30, A56, A57, A60, A61) · Naïve RAG pipeline.**
  - Top row: "Knowledge Base" (database icon) → "Chunking" (small box) → arrow labelled
    "Documents" → a tall box "Embedding Model" that spans both rows → arrow "Document Embedding" →
    a large cylinder "Vector Database" that also spans both rows.
  - Bottom row: "User" (person icon) → arrow "User Query" → the same Embedding Model → arrow
    "Embedded Query" → the same cylinder → arrow "Prompt + query + context" → small box "LLM".
  - Return path: a line "LLM Response" runs from the LLM down, left along the bottom and up to
    the User.

  On each repeat one element gets a purple rounded outline, so the deck walks the pipeline:
  Knowledge Base (A16, A18), Chunking (A19, A23), Embedding Model (A24, A29), Vector Database (A30,
  A56), the prompt label (A57, A60), LLM (A61). Note that the diagram draws no separate
  "prompt builder" box: the database's output arrow is the prompt. Purpose: the master map of the
  episode. A re-draw should keep one shared embedding model for both lanes. That is the rule the
  tutorial depends on, with the same model and dimension for chunks and query.
- **B5 · the same pipeline, numbered and grouped.** Blue numbered circles: 1 on Chunking, 2 on
  Document Embedding, 3 on User Query, 4 on Query Embedding, 5 on Prompt + query + context, 6 on
  LLM Response. Three dashed regions:
  - red "Indexing" around the top lane (knowledge base to the top of the cylinder);
  - green "Retrieval" around the query lane (embedding model's lower half, query embedding,
    cylinder);
  - light-blue "Augmentation & Generation" around the LLM.

  Purpose: names the three phases that deck B then optimises.
- **A17 · knowledge base sources.** The Knowledge Base icon beside three icons: "Websites" (www),
  "PDF Files", "Word Files".
- **A20–A21 · chunking.** A20: the "Chunking" box beside the whole one-page cheese document. A21:
  the same document cut into three side-by-side pieces, one per bold section. Purpose: a chunk is
  a self-contained piece. Note that this picture already splits by section, which deck B later
  calls semantic chunking.
- **A25 · embedding.** The tall "Embedding Model" box on the left. The three chunks each send an
  arrow to a six-cell vector bar: blue, red and green. A green cloud says the model is BERT-like
  and pools word embeddings. Purpose: one vector per chunk, one colour per chunk. The deck reuses
  these colours for the stored vectors.
- **A26 · three ways to index.** A folder-with-gear icon labelled "Index Data" and a red database
  icon above three options: "Lexical" (magnifier over a word), "Graphical" (a small tree or graph
  under a magnifier), "Semantic" (three vertical vector columns). A27 enlarges the semantic
  option. Purpose: the lecture picks the semantic option.
- **A28 · sentence embeddings.** Two tall vertical vectors of about ten coloured cells, labelled
  "Pavlos is from Cyprus" and "Harvard is in Massachusetts". The cells are shaded pink, red and
  lavender, and the two columns share a similar pattern. Purpose: a whole sentence becomes one
  vector, and similar sentences get similar vectors.
- **A32 · vector database strip.** A 4 × 3 grid of dots labelled "Vectors", in green, pink and
  orange rows, with a callout "Embeddings". Arrows lead through four blue boxes: "Indexing" →
  cylinder "Vector Database" → "Querying" → "Post Processing". The same strip sits, greyed, at the
  top of A33–A55, and the current stage is lit:
  - Indexing on A33–A38;
  - Querying on A39 and A44–A53;
  - Post Processing on A54–A55.
- **A33–A36 · the slow scan.** A column of stored vectors (blue, red, green, dots, purple) and a
  purple "Query" vector that moves down the column one row per slide (A34 beside red, A35 beside
  green, A36 at the bottom). A36 adds "Comparing them sequentially would be a very slow process."
  Purpose: motivate the index. Animate as a scanning pointer with a ticking counter that reaches
  "millions".
- **A37 · index.** Two columns: "Index" (one small coloured square per vector) and "Embeddings"
  (the full vectors). Text: the index maps vectors into a structure that lets a query zoom into a
  small subset. The slide does not show how. For a mechanism a re-draw has to supply one, such as
  HNSW's layered graph (the index Chroma uses in the tutorial), and label it as our illustration.
- **A39 · query vector.** A box "Query: What are different techniques of cheese making?" with an
  arrow down to a purple query vector, next to the Index and Embeddings columns.
- **A40–A43 · Pavlos game.** A40: Pavlos's cartoon head and three cartoon candidates in coloured
  frames: Option A (woman with glasses), Option B (man with glasses), Option C (woman). A41: "BIG
  5 Personality test RESULTS", one coloured column per person, with five rows (extroversion,
  emotional stability, agreeableness, conscientiousness, imagination):

  | | Pavlos | A | B | C |
  |---|---|---|---|---|
  | Extroversion | 4.8 | 3.3 | 4.8 | 1.0 |
  | Emotional stability | 4.5 | 4.0 | 2.7 | 3.6 |
  | Agreeableness | 4.2 | 4.1 | 4.9 | 3.8 |
  | Conscientiousness | 3.3 | 3.1 | 2.5 | 4.4 |
  | Imagination | 4.1 | 4.6 | 4.2 | 2.2 |

  A42: two arrows A (red) and B (blue) from the origin of an x1–x2 plot with the angle θ between
  them, and the cosine formula. A43: three lines "COSINE SIMILARITY(Pavlos, X) =" 0.986 (A, green
  tick), 0.976 (B), 0.886 (C). I recomputed them from the table: 0.987, 0.976 and 0.886. The
  ranking holds. Not on the slides: by dot product B wins (81.2 vs 80.2), because B's scores are
  larger overall. That makes a good scene for A44's question "How do these measures differ from
  each other?".
- **A45–A47 · similarity-measure table.** Columns: Measure, Formula, What it Measures, Range,
  Strengths, When to Use. Rows:
  - Cosine: x·y / (|x||y|); the angle; [−1, 1]; ignores magnitude; text embeddings, semantic
    search, normalised LLM embeddings.
  - Euclidean: ‖x − y‖₂; straight-line distance; [0, ∞]; captures magnitude; numeric or tabular
    feature vectors.
  - Dot product: x·y; magnitude times cosine; unbounded; combines both; relevance scoring when
    length means importance or confidence.

  A45 shows only the cosine row, A46 adds Euclidean, A47 is complete.
- **A48–A53 · rank and cut.** Stored vectors on the left (blue, red, green, …, purple), the purple
  query vector on the right moving down. Scores appear beside each row: blue 0.57 (A49, arrow
  "Similarity Score"), red 0.77 (A50), green 0.43 (A51), purple 0.93 (A52). On A53 the column
  re-sorts to purple 0.93, red 0.77, blue 0.57, …, green 0.43. A brace says the positions follow
  the similarity ranking, and a note says RAG returns the top-K, with K fixed in advance. Purpose:
  the core retrieval mechanism. Animate the bars sliding into sorted order and a K-line cutting
  the list. If the scene uses Chroma output, convert to distance (1 − similarity) or say why the
  numbers go the other way.
- **A54–A55 · post-processing.** A54 is text only (re-rank, metadata filtering, "optional", and a
  green callout defining metadata). A55 shows a miniature of the cheese document next to the list
  "Author, Publication date, Category".
- **A58–A59 · prompt anatomy.** A58: three headings in three colours: "Prompt" (system prompt =
  instructions), "Query" (the user's input, drawn as the purple query vector), "Context" (the
  retrieved, relevant information, drawn as two stored vectors, blue and red). A59: the worked
  version, with a "System Prompt" quote (a cheese-expert persona), a "User Query" quote (the main
  steps and methods of cheese making) and "Context (Relevant Extracts)", one paragraph in a blue
  box (pasteurisation, rennet, ageing, milk types, herbs). A right-hand brace labelled "Final
  Prompt" groups all three. Purpose: the G step is just prompt assembly. Our scene can stack the
  three blocks into one prompt card. If it shows the tutorial's code, it must say that the
  tutorial's system instruction is never sent (digest E1).

**Deck B**

- **B6–B10 · the advanced-RAG frame.**
  - B6: "Knowledge Base Documents" (page-stack icon) → "Indexing" (small box) → a tall, narrow,
    blue-outlined box "Retrieval". "User Query" enters Retrieval at the bottom. Retrieval →
    "Augmentation & Generation" (small box) → "Response".
  - B7: a peach column "Pre-Retrieval" covers the Indexing box and the incoming User Query arrow,
    just left of Retrieval.
  - B9: a second peach column "Post-Retrieval" between Retrieval and Augmentation & Generation.
  - B8 and B10: callouts saying what each new column handles.

  Purpose: the section map for deck B. It works well as a persistent mini-map in a scene's
  corner, with the active column lit.
- **B14–B15 · fixed-size cut.** A two-sentence paragraph about machine learning, then its five
  50-character pieces (a–e) with a callout "Do you think this is a good chunk?" pointing at piece
  a, which ends in "intelli". The slide's pieces are illustrative: b–d are 48 characters long, and
  a true 50-character split cuts at different places. A scene that animates this should compute
  the real cuts.
- **B16–B19 · paper example.**
  - Left on every slide: a mock one-page paper titled "Advancements in Transfer Learning for NLP"
    with bold Abstract, Methodology and Results sections, captioned "Model research paper".
  - Right on B16 and B18: two 200-character chunks. B18 marks in red the word cut "dom|ain", and
    the place where chunk 2 runs from the abstract's last words straight into "Methodology:".
  - Right on B19 and B34: three chunks, one per section (title, abstract, methodology), and a cloud
    "This is called semantic chunking".

  Note: chunk 1's text begins with a different title ("Recent techniques in transfer learning for
  NLP") from the one on the paper, and the "200-character" chunks are about 220 characters long.
  Purpose: the contrast between a ruler and the document's own structure.
- **B22–B33 · semantic chunking, step by step.** A row of six rounded blue boxes "Sentence 1" …
  "Sentence 6" (inside a "Document" frame on B22), with an up-arrow and a label "Anchor N" under
  the current anchor.
  - B22–B23: Anchor 1 under Sentence 1; window size = 1.
  - B24: Sentences 1–2 turn green with a bracket "Group 1". Anchor 1 is the first sentence, so the
    window only reaches right.
  - B25–B26: a tag "Cosine similarity = 0.89" over the pair; it is high, so they are joined.
  - B27: the pair is framed as "Chunk 1".
  - B28: Chunk 1 turns orange; Anchor 2 moves under Sentence 3.
  - B29–B30: "Group 2" = Sentences 2, 3, 4 (one each side of the anchor).
  - B31: two tags, "Cosine similarity = 0.85" over Sentences 2–3 and "= 0.68" over Sentences 3–4.
  - B32: the threshold is 0.8, so Sentence 3 joins Chunk 1 and Sentence 4 does not.
  - B33: Chunk 1 = Sentences 1–3 (orange); "Anchor 3" sits under Sentence 5, and the process
    continues to the end.

  The slides do not say what happens to Sentence 4. Presumably it opens Chunk 2 inside Anchor 3's
  window (Sentences 4–6). Purpose: the core pre-retrieval mechanism. A re-draw: sentence tiles, a
  sliding window bracket, similarity numbers on the links between tiles, a threshold line, and
  tiles changing colour as they are absorbed. If the scene follows the tutorial's code, swap the
  rule; see Terms.
- **B37–B39 · query rewriting.** Two rows, "❓Original Query" and "🧠Rewritten query".
  - B37: a rambling essay-planning text about penguins and dolphins becomes "Where do dolphins
    live?". A cartoon dolphin is on the right; the callout says the rewrite is concise and to the
    point.
  - B38: the turnover question, with callouts "In what sense? Retirements? Promotions?" and "Too
    broad a term. Directors? Senior Vice Presidents?", and a picture of someone reading a Microsoft
    report.
  - B39: the LLM's long rewrite, with the callout that it is made up and unrelated to the report.

  Purpose: rewriting helps when the query is noisy and can hallucinate when it is vague.
- **B44–B48 · hybrid search and RRF.** Original sentence (top right, in a blue box): "Chester went
  to the bank of the river in the morning". Three candidate paragraphs:
  1. Chester went to the riverbank early in the morning (callout: almost the same as the original);
  2. In the morning, Chester went to the bank by the river to borrow some money (words "bank" and
     "borrow some money" boxed; callout: a completely different bank);
  3. Chester went to the river for swimming and splashing around, then lay on the riverbank (words
     "river" and "riverbank" boxed; callout: related words).

  The tables:

  | Paragraph | BM25 rank | Vector rank (cosine) | RRF (k = 0, w = 0.5) | Final |
  |---|---|---|---|---|
  | 1. riverbank early | 2 | 1 | 0.5·½ + 0.5·1 = 0.75 | 1 |
  | 2. bank, borrow money | 1 | 3 | 0.5·1 + 0.5·⅓ = 0.67 | 2 |
  | 3. swimming, riverbank | 3 | 2 | 0.5·⅓ + 0.5·½ = 0.42 | 3 |

  B45 shows the two rank columns, B47 adds the RRF column with a callout "We take the k to be 0 and
  w_j = 0.5", B48 replaces the sums with the final ranks. Purpose: two retrievers disagree, and
  fusion by reciprocal rank settles it. Animate two ranked lists side by side, each item sending
  1/(k + rank) to a fused bar.
- **B51–B57 · retrieve then re-rank.**
  - B51: a long horizontal strip of about 45 pale-green cells, "All chunks", funnels into a blue
    "Vector database" cylinder.
  - B52: "❓User Query: What is cheese?" on the left.
  - B53: an arrow "top_K = 25" into the database, and a vertical list of 25 rows hanging below it.
    Four or five rows are yellow ("True relevant records", with a bracket): two at the top, the
    rest at positions spread down the list.
  - B55: a red callout: a simple score like cosine similarity can miss key details, so the ranking
    is off.
  - B57: a blue diamond "Re-ranker" takes the list and outputs a second list on the right, whose
    yellow rows are now at the top (four together, then one more).

  Purpose: re-ranking does not find new chunks; it reorders a short list. A re-draw can keep the
  25 rows as cards and let the diamond shuffle the yellow ones to the top.
- **B60 · bi-encoder.** Two columns. Left: "Document 1…N" (blue) → "BERT-like encoder" (pink,
  dashed) → "Vector 1…N". Right: "Query" (green) → "BERT-like encoder" → "Query Vector". A red box
  between them: these are the same encoder, used at different times. Caption: the bi-encoder
  encodes the data at rest and the query. Purpose: document vectors are computed before any query
  exists.
- **B63 · cross-encoder.** "Document" (blue) and "Query" (green) boxes at the top, both feeding
  one "BERT-like model" (pink, dashed), which outputs "Similarity Score". Question: why is this
  slower? Answer, implied by B61–B64: it must run once per query–document pair at query time, with
  nothing precomputed. A scene can put B60 and B63 side by side and count model runs: N + 1 ahead
  of time vs N at query time.
- **B76 · Retrieve-token decision tree.**
  - "Query" splits two ways: "Retrieve = No" → "Answer₁" (green), and "Retrieve = Yes" → "Query +
    Context₁".
  - That node splits again: No → "Answer₂"; Yes → "Query + Context₁ + Context₂".
  - That node has a No branch → "Answer₃".

  Red-outlined "Retrieve" boxes label each branch. Curved arrows tie each "Yes" to the node it
  feeds. Purpose: retrieval as a repeated decision, with context accumulating.
- **B78 · critique tokens.** Three green tags, IsREL, IsSUP and IsUSE, each with a one-line
  definition. A callout "A hallucination check" points at IsSUP.
- **B80 · no retrieval needed.** A small neural-net icon, a red box "Retrieve" tagged "No", and
  the start of a generated essay. The callout says no retrieval is required.
- **B81–B83 · checking each retrieved chunk.** The query at the top, a neural-net icon, a long
  arrow to a red box "Retrieve" tagged "Yes", then a dashed arrow to a magnifier. Three numbered
  grey balls 1, 2, 3 are labelled "Retrieve Chunks". Below, a grey bar "Query + ①" (② on B82, ③ on
  B83) feeds a second net icon, which produces a short answer with tags:
  - B81: ISREL Yes, "11 out of 50 state names come from persons", ISSUP Yes ("supported, no
    hallucination");
  - B82: ISREL No, "Texas was a part of Mexico from 1821 to 1836", discarded, no ISSUP check;
  - B83: ISREL Yes, a line about California's name and a 16th-century novel, ISSUP "Partially".
- **B85 · ISUSE scoring.** Three green headers "Response 1/2/3" over the three answers, each with
  an arrow down to a blue "ISUSE" box and a star rated 5 (orange), 1 (red) and 3 (lavender). A
  callout says an LLM produces ISUSE from the context, ISREL and ISSUP. Purpose: choose the best
  draft. Note that the discarded response 2 still gets a rating here.
- **B86–B88 · continue loop.** B86: Response 1 becomes "New Response": "US states got their names
  from a variety of sources" plus the persons fact. B88 is a flow:
  - "Current Response" → orange "Retrieve" → "New generated Response" → a second "Retrieve";
  - the second Retrieve loops up and back ("Continue", "Repeat") or exits down ("No") to the
    "Final Response".

  The final response adds a fact that none of the three chunks contained (26 states named after
  Native Americans, including Utah). So at least one more retrieval round happened off-slide.

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Retrieval-Augmented-Generation (RAG)" (hyphenated) | A7, A12 | README: "Retrieval-Augmented Generation (RAG)". |
| "Naïve RAG" | A15–A62, B3–B10 | The README never says "naive". Its five steps (Chunk, Embed, Load, Query, Chat) are naïve RAG. |
| "Advanced RAG" | B1, B68 | The README uses "Advanced RAG" only for semantic chunking (`README.md:220`). The deck's advanced RAG is much wider. |
| "Knowledge Base" | A16–A18, B6 | The tutorial's knowledge base is `input-datasets/books/` (11 cheese books). |
| "Documents" (the arrow after Chunking) | A16 | Means the chunks. The README and code say "chunks". |
| "Chunking"; "character splitting"; "chunk size" (50, 200) | A20–A22, B14–B18 | README: "Character splitting", `--chunk_type char-split`, chunk size 350 with overlap 20 (digest C2). **The slides never mention overlap or recursive splitting** (`recursive-split`, default overlap 200). |
| "semantic chunking" | B19–B34 | README: "Semantic Chunking (Semantic Splitting)", `semantic-split`. |
| "anchor sentence", "window size", "Group", "threshold" (0.8) | B21–B33 | **The rule differs.** The code (`semantic_splitter.py`) gives *every* sentence a window of ±1 (`buffer_size=1`, the slides' window size) and embeds each window. It measures the cosine *distance* between consecutive windows and cuts where the distance is above the **95th percentile** of all distances. There is no fixed 0.8 similarity threshold and no jumping anchor. The slides' version is the intuition; a scene that shows the code must name the percentile rule. |
| "Embedding Model" (BERT-like, aggregating word embeddings) | A25 | Tutorial: `gemini-embedding-001` on Vertex AI, asked for 256 dimensions. Same model for chunks and query, as in the slide's shared box. |
| "Document Embedding"; "Embedded Query" (A) / "Query Embedding" (B5) | A16, B5 | Same idea under two names. The code passes `embeddings=` and `query_embeddings=` to Chroma. |
| "Sentence Embedding" vs word embeddings | A28 | Not in the README. |
| "Index data": "Lexical", "Graphical", "Semantic" | A26 | Not in the README. The tutorial is semantic only, plus a lexical *filter* (`where_document={"$contains": …}`). |
| "Vector Database" | A30–A56 | README: "vector database" / "vector db", "ChromaDB", "collection". The slides never say "collection" or "record". |
| "Indexing" | A32–A38; B5–B10; B13–B34 | **Three meanings.** In A it is building a search structure over vectors. In B5–B10 it is the whole offline phase. In B13–B34 it is better chunking. The README calls the offline phase "Chunk -> Embed -> Load" and never says "indexing". |
| "Querying", "Post Processing" | A32, A39–A55 | README step 4 "Query the Vector Database" (`--query`). No post-processing in the tutorial. |
| "LSH", "PQ", "HNSW" | A38 | Chroma builds an HNSW index (`hnsw:space: cosine`, digest C4). The README does not name it. |
| "nearest vector neighbor"; "Similarity Score"; "top-K" | A39–A53 | Code: `n_results=10`. **Chroma returns cosine distances (1 − similarity), so smaller is closer**, the reverse of the slides' scores. |
| "Cosine Similarity", "Euclidian Distance" (A44; "Euclidean" on A45–A47), "Dot Product" | A42–A47 | The tutorial chooses cosine. Chroma's default space would be L2 (Euclidean). |
| "Metadata", "metadata filtering" (author, publication date, category) | A54–A55 | Tutorial metadata: `book`, `author`, `year`; filter `where={"book": …}`. **The slides put filtering in post-processing, after ranking. Chroma applies `where` before ranking**, and top-k is chosen among the survivors (digest C5). |
| "re-rank" | A54, B51–B65 | Not in the tutorial. |
| "Prompt" / "System Prompt", "Query" / "User Query", "Context", "Final Prompt", "Prompt + query + context" | A57–A60 | Code: `SYSTEM_INSTRUCTION` and `INPUT_PROMPT` (question + 10 chunks). **The system instruction is defined but never passed (digest E1)**, so the tutorial's real final prompt is query + context only. |
| "LLM", "LLM Response" | A16, A61–A62 | `gemini-3.1-flash-lite`; README step 5 "Chat" (`--chat`). |
| "Retrieval", "Augmentation & Generation", "Pre-Retrieval", "Post-Retrieval" | B5–B10 | README: "Query" and "Chat" steps; its two figures are "Step 1: Chunk -> Embed -> Load" and "Step 2: Query -> Embed -> Retrieve -> LLM -> Generate Answer". |
| "Query Manipulation", "cluttered", "ambiguous", "Rewritten query" | B35–B39 | Not in the tutorial. |
| "Retriever Optimization" (B2, B3, B11) / "Retrieval Optimization" (B40, B41, B49, B66) | — | Same section, two names in the deck. |
| "Hybrid Search", "keyword matching", "BM25", "TF-IDF", "TF", "IDF" | B42–B45 | Not in the tutorial. Its `$contains` filter is keyword *filtering*, not keyword *ranking*. |
| "rank fusion techniques", "Reciprocal Rank Fusion (RRF)", n, r_j(d), w_j, k ("ranking constant") | B46–B48 | Not in the tutorial. The deck's file name ("added_j_suffix_in_RRF") refers to the j subscripts in this formula. |
| "re-ranker", "bi-encoders", "cross-encoder", "BERT-like encoder/model", "topK" (25), "True relevant records", "information loss", "frontload" | B51–B65 | Not in the tutorial. B58 calls a re-ranker "just another LLM"; B62–B63 make it a BERT-like cross-encoder. Say "another model" rather than "an LLM". |
| "Self-RAG", "reflection tokens", "Retrieve token", "Critique token", "IsREL"/"ISREL" (also "ISSREL" on B81), "IsSUP"/"ISSUP", "IsUSE"/"ISUSE", "Continue" | B67–B88 | Not in the tutorial. The closest tutorial idea is the README's L06 **agent** (`--agent`), where the LLM decides which retrieval tool to call. That link is mine, not the slides'. |
| "open book exam" | B69–B71 | The digest's own analogy for RAG (C1) is also an open-book exam, so the series can reuse one image for both decks. |
| "Asai et al." | B80–B88 | Citation link for Self-RAG. |

Slips on the slides, so a scene does not copy them: A62's title says "Vector Database" but the
slide is about the LLM. "Euclidian" appears on A44. A54 calls re-ranking a "pre-processing step"
inside the Post Processing stage (it prepares input for generation). B33 says "till we reach the
end of the token" (meaning the document). On B16–B18 chunk 1's title does not match the paper's
title. B59's callout says one encoder for the query and another for the documents, while B60 says
they are the same encoder. B64 says the cross-encoder is fed "document and query vectors", while
B62–B63 show it reading the text pair. B79 promises a token summary that does not follow.

## Commands and code on the slides

There are no shell commands, Python, Docker or configuration on either deck. The only literal
code-like items are:

- A31 · SQL examples of what relational databases do well: `WHERE user_id = 123` and
  `WHERE price BETWEEN 10 AND 50`.
- A42 · cosine similarity: `cos(θ) = A·B / (‖A‖ ‖B‖) = Σ AᵢBᵢ / (√Σ Aᵢ² · √Σ Bᵢ²)`, for
  i = 1 … n.
- A45–A47 · formulas in the table: cosine `x·y / (|x||y|)`, Euclidean `‖x − y‖₂` (drawn as
  `√(x − y)²`), dot product `x·y`.
- A43 · results: `0.986`, `0.976`, `0.886`.
- A49–A53 · similarity scores `0.57`, `0.77`, `0.43`, `0.93`.
- A59 · a system prompt that opens "You are a Cheese Expert." (one line of a two-line quote).
- B15 · "character splitting of chunk size 50"; first chunk `"Machine learning is a subset of
  artificial intelli"`.
- B16 · "chunk size=200".
- B21 · sentence separators `(.,?,!)`.
- B25, B31, B32 · `Cosine similarity = 0.89`, `= 0.85`, `= 0.68`; threshold `0.8`.
- B46 · `RRF = Σ_{j=1}^{n} w_j · 1 / (k + r_j(d))`.
- B47 · `k = 0`, `w_j = 0.5`; e.g. `0.5 × 1/2 + 0.5 × 1/1 = 0.75`.
- B53 · `top_K = 25`.
- B76 · `Retrieve = Yes` / `Retrieve = No`.
- B85 · ISUSE rating `1–5` (5 highest).

## What the lecture stresses

- **Dumping everything into the prompt fails.** Too much context and the model "gives out
  garbage". (A8)
- **Fine-tuning is the slow road** for adding knowledge; RAG avoids changing the model. (A9, A62)
- **RAG addresses freshness and domain knowledge first** (A7). Deck B is frank that naïve and even
  advanced RAG can still hallucinate and retrieve irrelevant chunks (B4 meme, B68).
- **Chunk so the model can focus.** (A21)
- **A sentence embedding is not a word embedding.** It is a NOTE in bold on A28.
- **Relational databases do not do meaning.** Use a vector database or a database with a vector
  column type (PostgreSQL). (A31, A38)
- **Never scan millions of vectors one by one**; use an approximate index. (A33–A38)
- **The similarity measure is a design choice**, and it depends on whether magnitude carries
  meaning. Cosine for text embeddings. (A44–A47)
- **top-K is a fixed, predefined number.** (A53)
- **Post-processing (re-rank, metadata filter) is optional.** (A54)
- **A system prompt belongs in the final prompt** together with the query and the context.
  (A58–A59)
- **Fixed-size splitting cuts words and mixes sections.** "Do you think this is a good chunk?",
  "Do you see the problem here?" (B15, B17–B18)
- **Semantic chunking is the "optimal way"**, when the document has structure. (B19, B34)
- **Query rewriting by an LLM can hallucinate.** The expanded query had nothing to do with the
  source document. (B39)
- **Keyword and vector search have complementary strengths**: vectors disambiguate words, and
  keywords pin names and rare terms. (B42–B43)
- **RRF's weights and constant are hyper-parameters** that you choose. (B46)
- **Cosine similarity can rank the right chunks too low.** (B55)
- **Retrievers are fast and re-rankers are slow, so use both.** Retrieval frontloads the heavy
  computation and pays with information loss. Re-ranking spends time to recover accuracy. "Strong
  together." (B58–B65)
- **Bi-encoder vectors cannot know the query**, because they were made before it arrived. (B59)
- **Retrieving when it is not needed hurts**: slower answers, more confusion, wrong information
  pulled in. (B72)
- **IsSUP is the hallucination check.** (B78)

## Pointers

- **Course logistics (A2).** About 25% of students had groups; Milestone 1 is due 09/29. Form your
  own group and post ideas on Ed. Office hours are announced in two Ed posts; AWS credits in
  another. When a team forms, fill the group form (`bit.ly/ac215_2026_groups`, with a QR code).
- **Later lectures.** Fine-tuning "in upcoming lectures" (A9); in the series that is L08. LLMs were
  covered "in the previous sessions" (A62).
- **Forward references inside the lecture.** Vector databases "later in the slides" (A12 →
  A31–A55). Chunking methods "discussed later" (A22 → B14–B34).
- **BM25.** "To learn more about BM25: Click here" (B43). The link target is not in the extracted
  text.
- **Self-RAG source.** "Asai et al." links on B80–B88: the Self-RAG paper by Asai and colleagues
  (2023). The URL is not in the extracted text.
- **Uncredited figure.** The landscape map on A11/A63 carries no source on the slide.
- **No tutorial pointer.** Neither deck links the `llm-rag` repo, the Ed lesson, the web tools
  (`/chunkviz`, `/chromaui`, `/chat`) or any homework beyond Milestone 1. The pairing of these
  slides with the tutorial comes from the course site (see `digest.md`).
