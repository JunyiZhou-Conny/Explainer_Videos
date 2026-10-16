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

## This video and the slides

**Basis.** The video is planned but not scripted. This folder has:
- `BRIEF.md`: 16 scenes, S01–S16, in two parts. Each scene names a `Lecture:` slide range, and the
  BRIEF asks this pass to check them.
- `video.yaml`, with the same scene ids and titles;
- `ASSETS.md` and the captures in `assets/terminal/` (2026-10-16).

There is no `script.md` and no scene file yet. The nine-chapter plan in `digest.md` §8 is older,
and the BRIEF replaces it. So the map below uses the BRIEF's scenes. The study guide is
`MLOps_Learning/guides/L05-rag.md`. For this section I re-read all eighteen contact sheets and both
decks' text. I also re-checked these at the source:
- **The README's promises.** "small, overlapping" chunks (`README.md:17`, `:93`). Answers
  "grounded in your documents, not its own training data" (`:21`, again at `:194`). The two step
  titles (`:5`, `:9`).
- **`cli.py`.**
  - The cheese-specialist `SYSTEM_INSTRUCTION` (`:40-58`).
  - `chat()`: it pastes only `results["documents"][0]` into the prompt (`:390`) and sends no
    `config` (`:394-396`).
  - The four query variants (`:325-361`). The active one is commented "lexical search filter"
    (`:352`).
  - The agent's forced tool call, `mode="any"` (`:449`).
- **`semantic_splitter.py`.** `buffer_size: int = 1` (`:113`). The sentence regex (`:118`) and its
  comment "by default on '.', '?', and '!'" (`:216`). `distance = 1 - similarity` (`:74`). The
  95th-percentile default (`:92`).
- **The captures.**
  - `cli-container/12`, `15`, `40` and `60`;
  - `recorded-embeddings/04`, `06`, `08` and `09`;
  - `laptop/17`, the collection listing. It shows the HNSW settings (`"space":"cosine"`,
    `max_neighbors` 16, `ef_search` 100). It also shows that each collection carries Chroma's own
    `"embedding_function"` named `"default"`, which the tutorial never uses.

Where the slides and the captures disagree, the captures decide what the video shows.

### 1. Map: planned scenes ↔ slides

| Scene (BRIEF) | Slides on the same ground | Relation |
|---|---|---|
| S01 · A model that never read the book | A6–A11 (BRIEF); A17 (where a knowledge base comes from) | Same concept: the lecture's motivation. That is A6's four weaknesses, A8–A10's three roads and A11's four questions. The cold open on the Tolminc story and the how-to-follow beats are tutorial-only. The BRIEF also cites B69 for "an open-book exam", which deck B uses for another point (Common 18). |
| S02 · Two lanes, one database | A12–A16, B5–B6 (BRIEF); B59–B60 would add the shared-encoder rule (Gap 1) | Same concept, and the tutorial applies it. V1 is A16 redrawn with B5's numbers and phases, with the README's steps pinned under it. Conflicts 6, 7. |
| S03 · Your key, your folders, your project | none | Tutorial-only (service account, key, `GCP_PROJECT`). Neither deck mentions Google Cloud. |
| S04 · One script, two containers | none | Tutorial-only (Compose, the image build). The slides draw the vector database as one cylinder and never say where it runs. |
| S05 · Names, mounts, and two traps | none | Tutorial-only. |
| S06 · Cutting the books: a ruler | A19–A22, B14–B15 (BRIEF); B13 (the two pre-retrieval levers) | The tutorial applies it. `cli-container/12` captures B15's mid-word cut on the real book. Conflict 5. |
| S07 · Recursive split and its hidden overlap | B16–B19 (BRIEF) | The tutorial applies part of it. Cutting at blank lines moves toward B19's chunks, one per section. The 200-character default overlap is tutorial-only (Conflict 5). |
| S08 · Meaning as direction: embeddings | A24–A28, A40–A47 (BRIEF); B59–B60 | Same concept. The 256 numbers, `output_dimensionality` and the measured vector lengths are tutorial-only. |
| S09 · Load: records, an index, a folder on your disk | A30–A38 (BRIEF); A26 (three ways to index data) | Same concept for why a vector database and why an index. A38's HNSW is the index Chroma builds. Records, collections, `load`'s full rebuild and the files on disk are tutorial-only. Conflict 6. |
| S10 · Exit, and the index survives | none | Tutorial-only (persistence across a restart). |
| S11 · Asking the database: rank and cut | A39, A48–A53 (BRIEF); A44–A45 | Same concept, with the numbers running the other way (Conflict 1). Conflict 7 shows up in the no-key failure. |
| S12 · Filters come first | A54–A55 (BRIEF); A32 (the four-stage strip that V6 reuses) | Same concept, opposite order (Conflict 2). The `$contains` filter is not B42's keyword matching (Conflict 9). |
| S13 · Chat: the prompt is the whole trick | A57–A62 (BRIEF); A6–A7, B68, B78 | Same concept. The tutorial applies it with one block missing (Conflict 3). The README promises more than the lecture does (Conflict 8). |
| S14 · Semantic chunking: cut where meaning shifts | B13–B34 (BRIEF; the walk itself is B19–B33); A22 (the forward reference "discussed later") | Same concept, same ingredients, a different rule (Conflict 4). The API calls at `--chunk` are tutorial-only. |
| S15 · Beyond naïve RAG: what the lecture adds | B6–B10, B35–B65 (BRIEF) | Lecture-only: the tutorial has no code for it. The tutorial's semantic chunking is the one lever it implements (B13). |
| S16 · Tear down, a stale index, recap | B68–B76, A63 (BRIEF); B69–B72, B78 | Teardown and the stale index are tutorial-only. Self-RAG is lecture-only. The link to L06's agent is the series' own, and it needs a correction (Common 17). The recap answers the four questions of A11/A63. |
| S06–S14 · the mini-map | A18, A19, A23, A24, A29, A30, A56, A57, A60, A61 (the pipeline, one box lit each time) | The tutorial applies it. The BRIEF's corner copy of V1 lights the active box, as the deck does. |
| — not in the video | A1–A5, A15, A64; B1–B4, B11–B12, B35, B40–B41, B49–B50, B66–B67, B89 (title, logistics, outlines, dividers, closing pictures); B17, B20, B54, B56, B65, B71 (memes); B77, B79–B88 (Self-RAG's critique tokens at work and the worked example) | Lecture-only. B78's IsSUP is worth one tag in S13 (Gap 2). |

### 2. Already in common

| # | Concept | Scenes ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | LLMs have four weaknesses, and RAG targets two | S01 ↔ A6–A7 | Yes: four chips, two lit. The lecture claims less than the README (Conflict 8). S13 and S16 should come back to the two chips left dim (Gap 2). |
| 2 | Three roads: paste everything, fine-tune, use RAG | S01 ↔ A8–A10 | Yes. "Garbage" for the overfull prompt is A8's own word. "That's lecture 8" fills in A9's "upcoming lectures". |
| 3 | RAG sits between the user and the LLM, and the model does not change | S02, S13 ↔ A12–A14, A61–A62 | Yes. S13's "no weights move; delete the collection and the knowledge is gone" goes one step past A62's "nothing new to be added". A12's arrow takes the question itself to the database, which the code does not do (Conflict 7). |
| 4 | Two lanes share one embedding model and one database, in six numbered steps | S02 and the mini-map ↔ A16, B5 | Yes. V1 is A16 with B5's numbers 1–6, and like the deck it lights one box at a time. The BRIEF's rule "same model, same 256 numbers, both lanes" is A16's single tall box; B60 says it in words (Gap 1). |
| 5 | Three phases, and the video's two parts | Parts 1–2, S02 ↔ B5–B6 | Yes. Part 1 is B5's red Indexing box; part 2 is its Retrieval and Augmentation & Generation boxes. "Indexing" must say which sense it means (Conflict 6). |
| 6 | Why chunk at all | S06 ↔ A20–A21 | Yes. "So the model can focus" is A21's reason. The BRIEF adds the tutorial's second reason: a chunk is also what gets pasted into the prompt. |
| 7 | Character splitting is the default, and it cuts words | S06 ↔ B14–B15 | Yes. B14 calls character splitting the default, and it is the README's first chunk command. The captured `…intended to ac` / `s she intended to accomplish…` is B15's `intelli` / `gence` on the real book. What happens at the cut differs (Conflict 5). |
| 8 | Chunks should follow the document's own structure | S07, S14 ↔ B16–B19, B34 | Yes. The BRIEF's ladder (a ruler, then paragraph-aware scissors, then meaning) climbs toward B19's "optimal way". |
| 9 | One vector per chunk; a sentence embedding is not a word embedding; close means similar | S08 ↔ A25, A27–A28 | Yes. The slides' bars of six to ten cells become the tutorial's 256 numbers. A25 describes a "BERT-like" encoder. Here the model is Google's `gemini-embedding-001` behind an API, and the video need not name an architecture. |
| 10 | Cosine similarity, the personality game, and choosing a measure | S08 ↔ A40–A47 | Yes, and the tutorial makes the lecture's advice concrete. A45 recommends cosine for text embeddings, and `load()` asks for `hnsw:space: cosine` where Chroma's default would be L2. The captured vectors have lengths 0.369–0.402, not 1 (`recorded-embeddings/06`). That is exactly when A44–A47's choice matters: cosine ignores length, while L2 and the dot product do not (ponder 3). |
| 11 | Relational databases can't search by meaning | S09 ↔ A31 | Yes. The BRIEF uses A31's own SQL line. |
| 12 | Scanning every vector is slow, so build an index (HNSW) | S09 ↔ A33–A38 | Yes. V5's pointer walking 8,248 rows is A33–A36. The layered graph is our illustration of HNSW, the third of A38's three algorithms, which Chroma builds. The captured listing gives the real index's settings (`laptop/17`), and each loaded collection gets one index folder (`recorded-embeddings/04`). A37 shows no mechanism, so the BRIEF's "our illustration" label is right. |
| 13 | Nearest neighbours, a ranking, a fixed K | S11 ↔ A39, A48–A53 | Yes on the mechanism: A53's "K is a predefined number" is `n_results=10`. The numbers run the other way (Conflict 1). The BRIEF's "every query returns exactly K results, relevant or not" goes past A53. B68's first limit, no guarantee of relevance, backs it. |
| 14 | What metadata is | S09, S12 ↔ A54–A55 | Yes on what it is: A55's author, publication date and category match `book`, `author` and `year`. No on when filtering happens (Conflict 2). |
| 15 | The final prompt has three parts, with a cheese expert behind it | S13 ↔ A57–A59 | Yes on the design. The tutorial's `SYSTEM_INSTRUCTION` (`cli.py:40-58`) is the same idea as A59's system prompt: a cheese specialist who answers from the text it is given. The tutorial puts the question first and the chunks after it. That is A59's order without the first block. The BRIEF's ghost card is A58's "Prompt" block, unplugged (Conflict 3). |
| 16 | Semantic chunking's ingredients | S14 ↔ B21–B33 | Yes on the ingredients, no on the rule (Conflict 4). The ingredients match: sentences split at `.`, `?` and `!` (B21 ↔ `semantic_splitter.py:216`), a window of one sentence on each side (B23 ↔ `buffer_size=1`, `:113`), and cosine on embeddings (B21 ↔ `:56-85`). |
| 17 | Deciding whether to retrieve | S16 ↔ B68, B72–B76 | Partly. The BRIEF shows L06's agent choosing a retrieval tool and calls Self-RAG "the same idea taken further". But the agent is forced to call a tool (`mode="any"`, `cli.py:449`). It always retrieves and only chooses *how*. Self-RAG's Retrieve token decides *whether* to retrieve, and whether to fetch more (B75–B76). Its critique tokens then check what came back (B78). The link is the series' own, since the slides never mention agents. Keep it, but say which one decides what. |
| 18 | The open-book exam | S01 (the BRIEF cites B69), S16 ↔ B69–B72 | Partly. The series uses the open-book exam for RAG itself: a librarian hands over ten pages (digest C1). Deck B uses the same exam for another point. Student A looks things up only for unfamiliar topics. Student B looks up every topic, which is slower and invites confusion (B70, B72). This tutorial's `chat()` is student B. It retrieves ten chunks for every question, even an off-topic one (guide Ex 4). The image is fine for the opening, but don't tag it B69 in S01. Pay it off in S16 instead (Proposals). |
| 19 | Advanced RAG's map and levers | S15 ↔ B6–B10, B13, B35–B65 | Yes. The BRIEF tags them "concept · not in the tutorial's code". Its re-ranking beat ties B59's bi-encoder vectors to the tutorial's 8,248 stored vectors. |
| 20 | The four questions | S01, S16 ↔ A11, A63 | Yes. The BRIEF opens and closes on A11/A63's map, blurred, as the deck does. |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **One encoder, used at two different times (B59–B61).** B60's red box says outright what A16
   only draws: the same encoder embeds the documents ahead of time and the query when it arrives.
   B61 says why retrieval is fast: the heavy work is done up front, and a question costs one
   embedding plus a comparison with the stored vectors. B61 also names the price: "information
   loss", because the stored vectors never saw the question. That motivates re-ranking in S15.
   For a student, this one idea explains three tutorial facts:
   - the query and the chunks must use the same model and the same 256 numbers (guide Ex 6);
   - `--embed` is the slow, paid step, while `--query` makes one call;
   - the index can be reused after a restart.

   The BRIEF uses B59–B60 only in S15. **Carry it in** S02 (the shared box's label) and S08 (the
   moment `generate_query_embedding` lights the shared box from the query lane).
2. **What RAG fixes and what it doesn't (A6–A7, B68, B78).**
   - A7 claims two of A6's four problems for RAG: stale training data and missing domain knowledge.
   - B68 lists what even advanced RAG does not guarantee: relevant chunks, an answer supported by
     them, and retrieval only when it is needed.
   - B78 names the check for the second one: IsSUP, "a hallucination check".

   All of these show up in this tutorial:
   - The README's `--query` returns ten chunks without the word "Tolminc" (S12).
   - The system instruction that would keep the answer inside the chunks is never sent (S13).
   - A6's fourth problem stays open. `chat()` pastes only the chunk texts (`cli.py:390`), not their
     `metadatas`, so the model cannot say which book a fact came from.

   The BRIEF shows A6–A7 as chips in S01 and B68–B76 in S16, but it never ties them to the
   tutorial's own output. **Carry it in** S13 and S16. In S13, the grounding test is an IsSUP check
   done by eye, and the prompt has no sources. S16 closes the recap with B68's three limits.
3. **Rare words carry the most weight (B42–B43).** B43 gives the TF-IDF intuition: a word frequent
   everywhere ("the") says little, and a rare one ("GPT-3") says a lot. BM25 builds on it. The
   tutorial's own question has such a word. Only 3 of the 8,248 char-split chunks contain "Tolminc"
   (`recorded-embeddings/08`). A keyword retriever would very likely rank those three near the top
   (our expectation, not run). The vector side instead finds cheese-making passages that share no
   word with the question. The BRIEF's S15 uses only the lecture's Chester example and never names
   TF-IDF. **Carry it in** S15's hybrid-search beat.
4. **Three ways to index data (A26): lexical, graph, semantic.** The tutorial is semantic, plus a
   lexical *filter* (`where_document`, S12). Naming the routes gives S12's `$contains` a place,
   and keeps it apart from hybrid search (Conflict 9). **Carry it in** S09 (a GREY chip beside the
   index) or S12.
5. **What a knowledge base can be (A17): websites, PDFs, Word files.** The tutorial's knowledge base
   is eleven `.txt` books. Ten of them are still wrapped in Project Gutenberg's licence text (guide
   E18). A team's Milestone 2 corpus will look like A17, and every format needs extracting and
   cleaning before chunking. **Carry it in** S01 (a GREY strip beside the eleven books) or S06,
   where the licence text first appears.
6. **A vector column in an ordinary database (A38's callout).** PostgreSQL and others now offer a
   vector type. That helps later, when a team picks a store for its project; the tutorial does not
   need it. **Carry it in** S09 as a GREY note on the index beat, with no narration.

### 4. Conflicts

| # | The slides say | The tutorial and the captures | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **Scores vs distances.** A48–A53 give each stored vector a similarity score (0.57, 0.77, 0.43, 0.93); higher is better, and the list sorts from high to low. A45 gives cosine a range of −1 to 1. | With `hnsw:space: cosine`, Chroma returns `distances`: 1 − cosine similarity, from 0 to 2, where smaller is closer. A chunk's own vector comes back at 0.0000 and its neighbours at 0.0804–0.1627 (`recorded-embeddings/09`). `semantic_splitter.py:74` does the same conversion. | Both. They give the same ranking, read in opposite directions. | S11, as the BRIEF plans: after A53's sort, each score flips to 1 − score and the "better" arrow turns upside down. "The lecture ranks by similarity: higher is closer. Chroma reports distance, one minus the similarity: lower is closer. Same order, read the other way." |
| 2 | **When filtering happens.** A54–A55 put metadata filtering in Post Processing, after Querying. A32's strip shows that order. | `where` and `where_document` apply before the nearest-neighbour search. Top-k then fills its 10 slots from whatever survives: 8,248 → 1,355 → 64 candidates, none containing "Tolminc" (`recorded-embeddings/08`). With a stand-in query vector, the filtered top 10 sit at 0.2833–0.3123, against 0.0000–0.1627 unfiltered (`09`). | Chroma's order, for this tutorial | S12, as the BRIEF plans: on V6's strip, the filter box slides from Post Processing to before Querying. "In the lecture, filtering tidies up the results. In Chroma it comes first, and top-k picks among what's left, however far away." |
| 3 | **The system prompt.** A58–A59: the final prompt is a system prompt, the query and the context. A59's system prompt makes the model a cheese expert. | The tutorial defines a cheese-specialist `SYSTEM_INSTRUCTION` (`cli.py:40-58`). But `generate_content(model=…, contents=INPUT_PROMPT)` sends no `config` (`:394-396`), so the model gets only the question and ten chunks. Last year's branch sent it (`pipenv-branch/cli.py:62-64`). No capture shows a chat: without a key, `--chat` stops at the question's embedding (`cli.py:373`). | The code, as it runs today. The slides show the intended design, and the fix is one argument. | S13, as planned (V7's unplugged cable). "The lecture's final prompt has three parts. This code writes the first one, and then never sends it." Then the fix, tagged "not in the repo". |
| 4 | **The semantic-chunking rule.** B21–B33: an anchor sentence with a window of size 1. Cosine similarity between the anchor and each neighbour. Neighbours above a fixed 0.8 join the chunk (0.89 and 0.85 join; 0.68 does not), then the anchor jumps ahead. | `SemanticChunker` (`cli.py:209-210`) gives *every* sentence a window of ±1 (`buffer_size=1`) and embeds each three-sentence window. It measures the cosine *distance* between consecutive windows (`semantic_splitter.py:56-85`). It cuts wherever that distance is above the 95th percentile of all of them (`:92`, `:137-141`, `:239-243`). So about 5 % of the gaps become cuts, whatever their size. It needs the embedding API already during `--chunk` (`cli-container/60`). | The code. The slides teach the intuition. | S14, as planned (V8): the anchor walk plays small, then the code's rule replaces it. "The slides join sentences while their similarity stays above 0.8. This code measures every gap and cuts the widest five percent." In the code's units, B25's similarity of 0.89 is a distance of 0.11. |
| 5 | **Overlap.** On B14–B18 the character-split pieces sit end to end: `"…artificial intelli"`, then `"gence…"`. The 200-character paper chunks do the same. Neither deck mentions overlap. | `char-split` repeats 20 characters at each cut. Chunk 0 ends `…intended to ac`, and chunk 1 starts `s she intended to accomplish…`, so the cut word is whole in the next chunk (`cli-container/12`). `recursive-split` inherits a hidden overlap of up to 200 characters: chunk 1 starts again at the chapter heading (`15`). The README says "small, overlapping" (`README.md:17`, `:93`) and gives no numbers. | The captures | S06 (the 20-character band) and S07 (the 200). "The lecture's pieces sit end to end. This splitter repeats twenty characters at each cut, so a word cut off at the end of one chunk is whole in the next." |
| 6 | **"Indexing" means three things.** On A32–A38 it is building a search structure over the vectors. On B5–B10 it is the whole offline phase. On B13–B34 it is better chunking. | The README calls the offline phase "Chunk -> Embed -> Load" (`README.md:5`) and never says "indexing". Chroma's index is HNSW (`hnsw:space`, `laptop/17`). | All three senses; the README doesn't use the word | Name the sense each time, as the BRIEF does in S02 and S09. S02: "indexing = the whole top lane (B5)". S09: "the index = HNSW, A37's search structure". S14: "the lecture files semantic chunking under indexing (B13)". |
| 7 | **Who embeds the question.** On A12, the RAG box sends the *question* to the vector database and gets texts back. | The code embeds the question at Google first (`generate_query_embedding`, `cli.py:318-319`) and passes Chroma only numbers (`query_embeddings=`). Without a key, `--query` stops at that step, before it ever reaches Chroma (`cli-container/40`). Chroma could embed text itself: each collection carries its own default embedding function (`laptop/17`). That is a different model, so passing `query_texts` would put the question in the wrong space (guide Ex 6). | A16 and the code. A12 is a first sketch, and A16 refines it. | S02: as V1 grows out of A12, the BLUE embedding box slides in between the question and the cylinder, labelled "Chroma gets numbers, not words". S11 repeats it at the no-key stop. |
| 8 | **How much RAG guarantees.** A7 claims two of the four problems: stale data and missing domain knowledge. B68 says even advanced RAG guarantees neither relevant chunks nor a supported answer. | The README promises answers "grounded in your documents, not its own training data" (`README.md:21`; also `:194`). The code sends no instruction to stay inside the chunks (Conflict 3) and sets no distance threshold. It also leaves the sources out of the prompt (`cli.py:390`). | The lecture's modest claim describes what this code does | S13: "Retrieval hands the model your text. Whether it sticks to it is a separate question; the lecture calls that check IsSUP." (Gap 2) |
| 9 | **Keywords: ranking vs filtering.** On B42–B48, hybrid search *ranks* with a keyword retriever (BM25) and a vector retriever, then fuses the two rankings (RRF). | The active variant is commented "embedding value + lexical search filter" (`cli.py:352`). `where_document={"$contains": "Italian"}` is a case-sensitive substring *mask*, applied before the vector ranking. It never ranks by keywords. | Both exist. They are different tools with similar names. | S12 says it in one clause; the BRIEF already has "a keyword filter, not keyword ranking". S15's hybrid beat starts from it: "The tutorial uses a word to filter. Hybrid search uses words to rank." |

Not counted as conflicts:
- **Lecture number.** The slides say "Lecture 5"; the course schedule says "Lecture 4" (digest E17).
  The series follows the slides.
- **B59 vs B60.** B59's callout says one encoder for the query and another for the documents. B60
  says the two are the same encoder, used at different times. The tutorial follows B60: one model,
  with no `task_type` (digest E16). Draw B60's version.
- **The logo on A12.** A12's LLM box carries an OpenAI-style logo, but the tutorial's LLM is
  `gemini-3.1-flash-lite`. Draw a plain BLUE box.
- **"BERT-like" (A25).** This is a general picture of an embedding model, not a claim about
  `gemini-embedding-001`.
- **A45's "normalised embeddings" row.** The tutorial's vectors are not normalised (0.369–0.402).
  The row still recommends cosine, which is what the tutorial uses (Common 10).
- **B21's separators "(.,?,!)".** They read as period, question mark and exclamation mark, the same
  three as the code's regex and its comment (`semantic_splitter.py:118`, `:216`).
- **B53's `top_K = 25` vs `n_results=10`.** The 25 is an example size, not a default.
- **Slips listed under Terms.** A62's title, "Euclidian", A54's "pre-processing step", B33's
  "token" and B79's missing summary are not copied.

### 5. Proposals

Each item is marked **do** (clear value, low risk) or **nice**.

**General**
- **Tags.** `lecture_ref(5, "A16–A19")` prints "Lecture 5 · slides A16–A19"
  (`explainer/devops.py:176`). S01 says once that A is the main deck and B the supplement.
  - Below I use the form this task asked for, "Lecture 05 · slides …". The series should pick one
    form for all lectures, as L03's SLIDES.md also noted.
  - Use one tag per scene. Show it from the beat's first words for at least 3 s.
  - Never show a slide, a meme, or A11's chart itself; redraw them.
- **Corrections to the BRIEF (do), for its mapping pass.**
  1. S01: drop "B69" from the open-book line, or move it to S16's payoff (Common 18).
  2. S16: keep the agent → Self-RAG link, but sharpen it. The agent picks *which* retrieval to
     make: it must call a tool (`mode="any"`, `cli.py:449`). Self-RAG also decides *whether* to
     retrieve, and then checks the result (B75–B78) (Common 17).
  3. Widen these ranges:
     - S02 + B59–B60;
     - S08 + B60;
     - S12 + A32;
     - S13 + A6, B68, B78;
     - S15 + B43, for the Tolminc beat.
  4. The BRIEF's own list of differences between the slides and the tutorial has five entries.
     Add Conflict 5 (overlap; S06–S07), Conflict 7 (A12's arrow; S02, S11), Conflict 8 (the README's
     promise; S13) and Conflict 9 (filter vs ranking; S12, S15).
- **Narration budget.** The BRIEF plans ~4,240 words against a cap of 4,300, which leaves about 60
  words for bridges.
  - Keep at most three: S06 (overlap, ~20 words), S13 (sources and grounding, ~18) and S16 (whether
    vs which, ~17).
  - Each bridge needs its line in `i18n/zh/narration/`.
  - Tags and diagram labels need no narration.
- **Terms (do).** Use the lecture's names where the tutorial has none, and the tutorial's where
  they are more exact.
  - **Knowledge base:** the 11 books.
  - **Chunking.**
    - Chunk, chunking.
    - Character splitting (`char-split`), semantic chunking (`semantic-split`).
    - "Overlap" is the tutorial's word; the slides have no word for it.
  - **Embedding.**
    - Embedding model.
    - Sentence embedding (not a word embedding).
    - Query vector. Deck A says "embedded query", B5 "query embedding".
  - **Database.**
    - Vector database (Chroma).
    - Collection and record are tutorial-only words; say so once.
    - Index (HNSW). Say "indexing" only with its sense (Conflict 6).
  - **Retrieval.**
    - Nearest neighbour.
    - Top-K = `n_results=10`.
    - Similarity (the lecture) vs distance (Chroma) (Conflict 1).
    - Metadata, metadata filtering. Post-processing is optional, and this tutorial has none.
  - **Prompt.** Final prompt = system prompt + query + context.
  - **The bigger picture.**
    - Naïve RAG = the README's five steps. Advanced RAG, pre-retrieval, post-retrieval.
    - Bi-encoder, cross-encoder, re-ranker ("another model", not B58's "just another LLM").
    - Hybrid search, BM25, TF-IDF, RRF.
    - Self-RAG, Retrieve token, critique tokens (IsREL, IsSUP, IsUSE).
  - Spell it "Euclidean", not A44's "Euclidian".
- **Recap card (nice).** The five recap questions can each carry a slide number: Q1 A16, B5; Q2
  none; Q3 B14–B18; Q4 A54–A55; Q5 A58–A59.

**Per scene.** S03–S05 and S10 have no lecture ground and get no tag.
- **S01.**
  - do · "Lecture 05 · slides A6–A10", at the four chips and the three roads.
  - Diagram:
    - light only A7's two chips (stale data, domain knowledge);
    - leave "hallucination" and "no sources" dim: S13 and S16 come back to them (Gap 2);
    - keep the open-book exam as the series' image, untagged (Common 18).
  - nice · A17's three source icons as a GREY strip beside the eleven `.txt` books, captioned "a
    project's knowledge base: websites, PDFs, Word files" (Gap 5).
- **S02.**
  - do · "Lecture 05 · slides A12–A16, B5", as V1 grows out of A12.
  - Diagram do · A12's arrow takes the question straight to the database. As V1 replaces it, the
    BLUE embedding box slides in between, labelled "Chroma gets numbers, not words" (Conflict 7).
  - do · Label the shared box with B60's point in our words: "one model · chunks before,
    questions later" (Gap 1).
  - Say "indexing = the whole top lane", in B5's sense.
- **S06.**
  - do · "Lecture 05 · slides B14–B15", at the mid-word cut.
  - Diagram do · B15's five 50-character pieces, small and end to end, beside the captured cut
    with its 20-character band (Conflict 5).
  - nice, a bridge (~20 words): "The lecture's pieces sit end to end. This splitter repeats twenty
    characters, so the cut word is whole in the next chunk."
- **S07.**
  - do · "Lecture 05 · slides B16–B19", at "follow the document's own structure".
  - Diagram nice, in three steps:
    - B18's two red marks: a word cut in half, and one section running into the next section's
      heading;
    - then recursive's cuts landing on blank lines;
    - B19's section-shaped chunks as a GREY ghost target.
- **S08.**
  - do · "Lecture 05 · slides A40–A47", at the personality game.
  - nice · A second tag, "Lecture 05 · slide B60", when `generate_query_embedding` lights the
    shared box from the query lane (Gap 1).
  - Ponder 3's answer can point back to A45–A47's "magnitude" column: the vectors' lengths,
    0.369–0.402, are where that column matters (Common 10).
  - Keep A28's NOTE: a sentence embedding, not a word embedding.
- **S09.**
  - do · "Lecture 05 · slides A33–A38", from the slow scan to the index.
  - Diagram nice · After "our illustration of HNSW", a small GREY card tagged `recorded` with the
    real index's settings from `laptop/17`: `space cosine · max_neighbors 16 · ef_search 100`. It is
    the one place where a viewer sees A38's HNSW as Chroma actually configures it.
  - nice · A26's three routes as a chip, "lexical · graph · semantic", with "this tutorial:
    semantic, plus a lexical filter in S12" (Gap 4).
  - nice · A38's PostgreSQL note as a GREY line (Gap 6).
- **S11.**
  - do · "Lecture 05 · slides A48–A53", at the rank and cut.
  - Diagram do · The planned flip, with both scales: similarity from −1 to 1 (A45), and distance
    from 0 to 2, where 0 means the same direction (the captured 0.0000) (Conflict 1).
  - At the no-key stop, say "it fails before it reaches Chroma: Chroma only takes vectors"
    (Conflict 7).
- **S12.**
  - do · "Lecture 05 · slides A54–A55", at the filter beat.
  - Diagram: V6's A32 strip, as planned (Conflict 2).
  - Say A54's definition once: metadata is data about the data.
  - One clause, already planned: `$contains` filters by a word; ranking by words comes in S15
    (Conflict 9).
- **S13.**
  - do · "Lecture 05 · slides A57–A59", at the three blocks.
  - Diagram do · On the ghost card, write the tutorial's own persona in a few words ("specialized
    in cheese knowledge", `cli.py:41`), beside A59's "Cheese Expert": the same idea, unplugged
    (Conflict 3).
  - do · At the grounding test, a GREY tag "IsSUP · slide B78", captioned "a hallucination check,
    done by eye" (Gap 2).
  - nice · Draw each chunk card with its `book` label, greyed out as the card enters the prompt:
    "the prompt drops the source" (`cli.py:390`). S01's "no sources" chip stays dim (Gap 2).
  - nice, a bridge (~18 words): "Retrieval hands the model your books. Nothing here makes it stick
    to them, or say which book it used."
- **S14.**
  - do · "Lecture 05 · slides B21–B33", at the anchor walk.
  - Diagram do · Three GREEN ticks for what the slides and the code share: the split at `.`, `?`
    and `!`; window size 1 = `buffer_size=1`; cosine on embeddings. Then two swaps for what
    differs: a fixed 0.8 becomes the 95th percentile, and a jumping anchor becomes every gap
    (Common 16, Conflict 4).
  - nice · Convert B25's similarity of 0.89 to the code's distance of 0.11 on screen.
- **S15.**
  - do · "Lecture 05 · slides B6–B10", at the frame. The three beats can carry small inline
    numbers (B36–B39, B42–B48, B51–B65) instead of more tags.
  - Hybrid beat, do · Open with the tutorial's own rare word: "Tolminc" is in 3 of 8,248 chunks
    (`recorded-embeddings/08`). B43's IDF says that rarity is what makes it a strong keyword. The
    vectors, meanwhile, find cheese-making text that never uses the word (Gap 3). Then the Chester
    example and RRF, as planned.
  - nice, verify first · The captured collection schema contains a `sparse_vector_index` with
    `"bm25": false` (`laptop/17`). That suggests newer Chroma servers can index keywords; the
    tutorial's client, 1.1.0, does not use this. Check Chroma's documentation before saying more
    than "there's a switch, and it's off".
  - Re-ranking beat: B53's 25 candidates against the tutorial's 10 is a choice of K, not a rule.
- **S16.**
  - do · "Lecture 05 · slides B68–B76", at Self-RAG. The recap's map carries "slide A63".
  - Framing do (Common 17, 18): "Our chat looks things up for every question, like student B in
    the lecture's open-book exam (B69–B72)." Then a bridge (~17 words): "The L06 agent picks which
    lookup to make; Self-RAG also decides whether to look, and checks the result."
  - do · B68's three limits as three ticks on the recap, each pointing to a scene:
    - relevance: S12's ten Italian-cheese chunks;
    - support: S13's IsSUP check;
    - needless retrieval: every question retrieves.
