# AC215 · Lecture 5 — Introduction to RAG (follow-along: llm-rag)

## 00:00 — A model that never read the book
Here's the question this tutorial asks a language model: how is Tolminc cheese made? Tolminc is a real Alpine cheese, but the answer we want lives in one particular text.
The knowledge base is eleven books: ten old cheese books from Project Gutenberg, and the instructor's short story, a fictional tale. A model trained before that story existed has never read it, so it answers from somewhere else. How do we make it answer from this story, without retraining it?
The lecture lists four weaknesses: stale training data, no specialized knowledge, hallucination, and no sources. RAG, retrieval augmented generation, goes after the first two.
Paste all eleven books into the prompt, and you get garbage. Fine-tune the model, and it's slow; that's lecture 8. Or let a librarian hand it the ten most relevant pages: an open-book exam. That's RAG.
The lecture's map of RAG techniques is crowded, but it starts from four questions. What is an embedding, a vector database, a query, the context? This video answers all four.
Open the README beside this video. Top left, the tracker shows its step; top right, the gray tag points to the lecture slides. When the yellow your-turn tag appears, pause and run the command; extra commands aren't in the README.
We recorded without a Google key. Docker, chunking and the database ran for real; the embeddings are the staff's recorded vectors. Where the code calls Google, you see the command, the real error, and what to look for.

## 01:40 — Two lanes, one database
Here's RAG in four boxes. The user's question goes to the RAG code, which asks a vector database for related texts. The code joins question and texts into one full prompt, and the model's response goes back. The database never talks to the model.
Open the RAG box and you get two lanes. On top, books are cut into chunks, an embedding model turns each chunk into a vector, and the vectors go into the database. Below, the question goes through the same model, and only its vector reaches the database.
This is the pipeline slide from lecture, with three phases. Indexing is the whole top lane. Retrieval brings the context to the prompt, and the model does augmentation and generation.
The README calls the two lanes step 1 and step 2, and gives each box one flag of cli.py: chunk, embed and load on top, query and chat below.
Two rules. The top lane runs once, offline, and it's slow. The bottom lane runs for every question. And both lanes must use the same embedding model, or the question and the chunks don't live in the same space.
Where does each box run? The chunker runs in your own container. Both models run at Google: you pay for the text you send, with your key, and nothing keeps running there. The database runs in a second container, with its files on your laptop.
Every step is one python cli.py command, inside that first container. So first, let's get it running.

## 03:15 — Your key, your folders, your project
Prerequisites first: Docker. This extra check prints its versions; the script needs docker compose, with a space. On a Mac your prompt looks different; on Windows, use WSL or Git Bash.
The README links the repo but doesn't print the clone command, so here it is. Then, as an extra, make a secrets folder beside the clone, and keep the clone's name exactly L-L-M rag. Pause and do both, in your course folder.
Now the service account, in the Google Cloud console. Create one called L-L-M service account, and grant it two roles: Storage Admin, and Gemini Enterprise Agent Platform User. Open its keys tab, add a JSON key, and save it in secrets as L-L-M service account dot JSON.
That key spends your project's money; the git ignore file has no secrets line, so it's safe only beside the repo. Remember the three gates from lecture 4: the key says who you are, the role what you may do, and the API must be switched on.
Two small slips. Nothing here uses Cloud Storage, so the Agent Platform role is what matters. And the README never says to enable the Vertex AI API; without it, the first embedding call fails with service disabled, after 5 retries. Pause and do it all now: account, roles, key, and API.
Step 1 of the next section: cd L-L-M rag. An extra look shows the scripts, the compose file, cli.py, and the commit this video was recorded on.
Step 2: in your editor, set GCP project on line 7 to your own Project ID, the ID, not the name. Leave line 8 alone. Skip this, and your calls go to the course's project and fail. Pause and edit.

## 05:15 — One script, two containers
Lecture 4 put two containers on one network; lecture 3 brought a key in through a mount. Today: both at once, with one command.
The script, docker-shell.sh, exports three values: your project, the key's path inside the container, and the image name. Then it calls docker compose run, with dash dash r m, for that one service.
The compose file draws the whole picture: one network, by name, and the CLI service on it, with an image built from this folder if missing.
Two mounts put the repo onto slash app and secrets onto slash secrets. Two slots take the script's values, and the service depends on Chroma.
The Chroma service runs the database from Docker Hub, under a fixed name. It publishes port 8000 to your laptop, keeps its data in the docker volumes folder, and lets the course's web tools in.
From the Dockerfile: the virtual environment lives in slash dot venv, outside slash app, so the code mount can't hide it. Edit cli.py on your laptop and rerun; no rebuild.
Step 3: sh docker-shell.sh. Compose pulls Chroma's image, creates the network, and creates the Chroma container first.
Then this, which looks like an error but isn't. Compose first asks Docker Hub for an image called L-L-M rag CLI, finds none, and builds it instead.
The build took 81 seconds here. Its context was 112 megabytes. Most of it is git history, which still holds an old copy of the staff's database. With no docker ignore file, the image keeps it.
Then the banner: Python 3.12.15 and uv 0.13.1, at the time of recording. It says activated before it activates: cosmetic.
You're at the container's prompt. The part after the at sign is the container's ID; it changes every run. Pause, and get to this prompt.

## 07:19 — Names, mounts, and two traps
Check the picture with extras: open a second laptop terminal and cd into L-L-M rag. The docker ps command shows Chroma with port 8000 published. But the CLI container isn't called L-L-M rag CLI: compose run ignores that name.
And docker inspect, with the name from docker ps, lists the mounts. The repo is on slash app, secrets on slash secrets, and the docker volumes folder on Chroma's slash data.
Inside the container, your Project ID and the key's path arrived. Our secrets folder is empty, with no key; yours should list the JSON file.
The CLI finds Chroma by name, through the network's phone book. From your laptop, the heartbeat comes through localhost port 8000, the published door for you and your browser.
Docker already created Chroma's data folder on your laptop, owned by root, with the database file in it. On Linux, deleting it later will need sudo.
Now two traps, hit on purpose. Trap one: typing the compose command yourself. Both variables come out blank, and even chunking dies at startup, where cli.py creates its Google client, looking for a key file with no name. Always start through the script.
Trap two: a clone with another name, like the folder a zip download gives you. The compose file mounts a folder named L-L-M rag, so Docker creates an empty one, owned by root, over your code. Keep the name, and delete the stray folder.
One last oddity: the image tag called latest, and three version numbers that don't match; a team should pin a tag. Pause and try these checks; your key in slash secrets matters most.

## 09:09 — Cutting the books: a ruler
Indexing starts with chunking. One vector for a whole book averages its topics, so every question fetches the whole book. Sending 11 books each time is slow, costly, and gives garbage. A chunk is small enough to find, and to paste.
Step 1 is a link: the README's chunk visualizer. Open it in Chrome and play with the sliders; here's the idea it shows.
Character splitting is a ruler. Lines 185 and 186 set windows of 350 characters, overlapping by 20. The separator is empty, so it counts characters, not words, stepping 330 at a time.
The instructor's story is 7,808 characters long. Windows of 350 that overlap by 20: how many chunks?
The first window takes 350 characters, and each one after it adds 330 new ones. 7,458 more characters need 23 more windows: 24 chunks.
Step 2: python cli.py, dash dash chunk, chunk type char split. It reads 11 books and prints each book's chunk count; the story gets 24. No key needed: this branch never calls Google. Pause and run it.
An extra line count of the chunk files: 24 for the story, and 8,248 in total.
An extra look at the seam. Chunk 0 stops two letters into the word accomplish. Chunk 1 backs up 20 characters, to the last letter of things, so accomplish is whole again. The lecture's pieces sit end to end, with no overlap.
The chunk files land in outputs, on your laptop, and git ignores them. Row 0 of a Gutenberg book is the Project Gutenberg header: these books start with a header and end with a license, both chunked like the rest.

## 11:21 — Recursive split and its hidden overlap
Recursive splitting gets only a chunk size, the same 350. No overlap is given.
It works like scissors that look for the best gap. First a blank line between paragraphs, then a line break, then a space, and only as a last resort, a single character. So every cut falls between words.
Step 3: the same command with chunk type recursive split. The story now makes 35 chunks, and an extra line count gives 14,228 in total. Pause and run it.
Same chunk size, 350. So why 14,228 chunks instead of 8,248?
Look at the first chunks. Chunk 1 starts again with Chapter One, repeating the end of chunk 0. The splitter's library default is an overlap of up to 200 characters, which the README never mentions. Cutting at boundaries also makes chunks shorter.
Overlap is insurance against cutting an idea in half. But every repeated character is embedded, stored, and paid for. If you want a different value, set chunk overlap yourself.
The lecture's point is that ideal chunks follow the document's own structure. Recursive splitting goes part of the way, using paragraphs. Semantic chunking, in part 2, goes further.

## 12:59 — Meaning as direction: embeddings
Next, the embedding model. It turns each chunk into one vector, a list of numbers, so similar meanings point in similar directions: in this sketch, curd near curd, license text elsewhere.
The personality game from lecture makes this concrete: which of three candidates is most like the instructor? Five scores make each person a five-number vector. Cosine similarity compares only the angle, and picks the first candidate.
The dot product also counts length, and would pick the second candidate, whose arrow is longer. So a measure is a choice; for text, cosine is the usual one.
The tutorial's model, Gemini embedding 001, natively returns 3,072 numbers. The code asks for the first 256. The model is trained to make that prefix useful alone.
Chunks go to the model in batches of 100. On an API error, it retries up to 5 times, doubling the wait from 5 seconds.
Your question will use this same model, later. Chunks now, questions later: one model.
Step 1: python cli.py, dash dash embed, chunk type char split. It's the first call to Google. On our machine it reads the first book, then stops at the missing key file. On yours, it runs.
With your key, look for each book's file, a 5-second pause, a table with an embedding column, and new embeddings files beside the chunks.
If yours fails, or keeps retrying, read the error. Key file not found: check its name in secrets. Permission denied: fix the Project ID or the role, then exit and start the script again. Service disabled: switch on the API.
Step 2 does the same for recursive split. Pause and run both, with your key: about 89 and 148 calls, a few cents by our estimate. Check the current price list.
The video goes on with the staff's own outputs, once committed and still in every clone's history. Their chunk files match ours byte for byte, so their vectors are what this command makes.
An extra check on the story's vectors. 24 rows of 256 numbers. Their lengths run from 0.369 to 0.402, not 1.
When we load them, the database will compare by cosine, and these arrows are shorter than 1. Does that change which chunks count as nearest?
No: cosine only sees the angle. With straight-line distance, Chroma's default, or a dot product, length would leak into the ranking: the game's lesson.

## 15:56 — Load: records, an index, a folder on your disk
An ordinary database answers precise questions, like a price between 10 and 50, but it can't find rows whose meaning is like a question. A vector database can.
Each chunk becomes a record: an ID, the text, metadata with book, author and year, and the vector. The ID hashes the book's name plus the row number, so it's stable.
Records go into a collection, one per chunk type. The load step deletes it and creates it again, with cosine as its measure: every load is a full rebuild.
Comparing a question with every vector is slow at scale. So the database builds an index, in these slides' sense: a layered graph called H-N-S-W, where a search hops down in a few steps.
Step 1: python cli.py, dash dash load, chunk type char split. On our first run there were no embeddings yet: it made an empty collection and found 0 files. If you see 0, your embed step didn't finish.
On the staff's recorded vectors, the same command deletes that empty collection and reads 11 files with an embedding column. It inserts 8,248 records, in batches of 500.
Step 2 loads recursive split, 14,228 records. Pause and run both loads.
An extra check: both collections now have dimension 256, fixed by the first insert.
And one book has no author or year: a small slip cuts its file name at the first dot. Split off only the extension, delete that book's old files in outputs, then chunk, embed and load again.
The docker volumes folder on your laptop now holds a 60-megabyte SQLite file and two index folders, one per collection, owned by root. The README calls it persistent.
Step 3 is a link to the course's Chroma UI. Opened in Chrome, it reads your local database through port 8000; Chroma's settings let the course's site in.
The top lane is done: the index is built. In part 2, we ask it questions.

## 18:09 — Exit, and the index survives
In part 1, we built the index: chunk, embed, load. Part 2 puts it to work. But first, a test: does the index survive closing the laptop?
Leaving isn't in the README. Type exit, and on the laptop, list every container with docker ps dash a. The CLI container is gone, removed on exit, but Chroma is still up, and port 8000 is still taken.
To stop it, run docker compose down from the repo folder. Two warnings say the variables aren't set. They're harmless: only the script sets them, and the down command needs neither. Then Chroma and the network are removed.
Nothing is running now. But the docker volumes folder on your disk still holds the database file and both index folders, and your chunk files in outputs are untouched.
Back another day: sh docker-shell.sh again. No pull, no build: the image exists. After a git pull that changes the dependencies or the Dockerfile, run docker compose build first. Pause and restart.
Two extra checks: both collections are back, with dimension 256, and an extra command called get returns the same 10 record IDs. The container was disposable; the data never lived in it.

## 19:34 — Asking the database: rank and cut
Now the bottom lane. The question goes through the same embedding model and becomes a query vector, in the same space as the chunks. Querying means finding its nearest neighbors.
The lecture scores every stored vector against the query. 0.57, 0.77, 0.43, 0.93. Sort by score, and keep the top K, with K fixed in advance. This code uses 10.
One difference: the lecture ranks by similarity, where higher is better. Chroma reports cosine distance, one minus the similarity, where smaller is closer. Same order, opposite direction.
And a query returns K results whenever K chunks are available, relevant or not. Nothing in this code sets a distance threshold.
In the code, the query function sets the question, turns it into a vector with the same Google model, and opens the chunk type's collection.
Step 1: python cli.py, dash dash query, chunk type char split. A small slip first: it prints the word load, a label copied from the load code. Then it connects to Chroma, but stops at the key while embedding the question, before it searches.
The question must become a vector before the database can compare it, and only the same Google model makes one in the same space.
Step 2 runs it on recursive split. With your key, look for 256 embedding values, the query, and the results. The results are lists of lists: one list per query, holding IDs, distances, metadata and documents. Pause and run both.
That's why chat, later, reads documents, item zero. No results were recorded, so next we ask the loaded database directly.

## 21:27 — Filters come first
Here's the query the code sends: 10 results and two filters. The metadata filter keeps one book, The Complete Book of Cheese. The document filter keeps chunks that contain Italian.
The question is about Tolminc. What will the 10 results be about?
An extra check counts them in the loaded collection. Of 8,248 chunks, the book filter keeps 1,355. The word Italian keeps 64. How many mention Tolminc? None.
Now a search. The real question needs Google to become a vector, so we use a stand-in: the stored vector of one story chunk. Without filters, its 10 nearest are all from the story, at distances from 0, the chunk itself, up to 0.16.
With the code's filters, all 10 results come from The Complete Book of Cheese. Their distances run from 0.28 to 0.31. The filters act first, and top K fills its 10 places with whatever survives, however far.
The lecture puts metadata filtering after ranking: here, that would drop all 10 story chunks and return nothing. Chroma filters first, so you get 10 results, about the wrong cheese.
A small slip: the README promises various filters, but only variant 4 runs; variants 1 to 3 are commented out. Uncomment the first, with no filter, and every chunk competes. And contains is a keyword filter, not a keyword ranking.
The get command from the restart check uses the same book filter, but no question, so no distances. Its 10 records start with the Gutenberg header, then the title page and contents. That header, and each book's closing license, are indexed like any text: strip them before chunking.

## 23:31 — Chat: the prompt is the whole trick
Now generation. The lecture's final prompt has three parts: a system prompt that says how to behave, the user's query, and the context retrieved from the database.
In chat, the code queries again, this time with no filter, for 10 results.
Then it builds the input prompt: the question, followed by the 10 chunks, joined by newlines. The prompt goes to Gemini 3.1 Flash Lite.
So where's the system prompt? Line 40 defines one: answer only from the chunks, and say so when they don't contain enough. But look at the call. It's never sent.
A small slip, with a one-line fix: pass it in a config argument. The older pipenv branch did send it. Without it, the README's promise of grounded answers rests on the chunks alone.
And notice what didn't change: the model itself. No weights moved. Delete the collection, and the knowledge is gone.
Steps 1 and 2: python cli.py, dash dash chat, for char split and for recursive split. Without a key, both stop embedding the question. Each question costs one embedding call and one Gemini call.
With your key, look for the query, printed with two question marks, a harmless slip, and its 256 embedding values. Then the results, the number 10, the input prompt with your chunks, and the model's response.
Remember the opening question? The story is fiction, so an answer about Mara, her grandfather and the curd came from your chunks. Real-world rules for Tolminc came from the model's memory. Compare both chunk types.
Step 3 is a link to the course's chat tool, in Chrome. Pause: run both chat commands with your key, then try the tool. For your own question, change line 372 of cli.py.

## 25:30 — Semantic chunking: cut where meaning shifts
Back to chunking, with the lecture's best answer: cut where the meaning changes. On the slides, an anchor walks through the sentences and joins neighbors while their similarity stays above 0.8.
The code uses the same ingredients with a different rule. Every sentence gets a window, itself and one neighbor on each side, and each window is embedded.
Then it measures the distance between each window and the next, and plots it over the text, like a seismograph.
Next, it draws a line at the 95th percentile, and cuts at every spike above it. So the biggest 5 percent of gaps become chunk boundaries.
Char split ran the chunk step without a key. Can semantic split?
No. To find where the meaning shifts, it has to embed every sentence window first. Look at the function handed to the chunker: generate text embeddings, the same one the embed step uses.
The README's command runs all three steps with chunk type semantic split. On our machine it fails inside the chunk step, on the first book, before a single chunk is saved.
With your key, budget for it: by our estimate, about 528 embedding calls to chunk the corpus, about 90 more to embed the chunks, and 10 to 20 minutes. Try one book first, then put the others back and run it again. Look for a chunk count per book, and finally, finished inserting into the semantic split collection.
The chunks come out very uneven, and even a single-topic book gets cut at its biggest gaps. Afterwards, an extra: chat works the same way. Pause and try it, with your key.

## 27:23 — Beyond naïve RAG: what the lecture adds
The lecture goes further. Its frame adds a pre-retrieval stage and a post-retrieval stage. Semantic chunking sits in pre-retrieval: the one advanced lever this tutorial implements. Here are three more, as ideas only.
Also before retrieval: query rewriting. A model turns a cluttered question into a clean one, like where do dolphins live. But hand it a vague question, and the rewrite can invent details.
In retrieval: hybrid search. Keywords pin down names and rare words; vectors catch meaning. Take the question: Chester went to the bank of the river in the morning. The two rank three paragraphs differently.
Reciprocal rank fusion gives each paragraph one half divided by its rank, in each list, and adds them up. The near paraphrase wins with 0.75, ahead of 0.67 and 0.42.
After retrieval: re-ranking. A fast retriever, whose vectors were made before the question existed, returns 25 candidates with the right ones scattered. A slower model reads each question and chunk together and reorders them.
None of these is in cli.py. They're what you reach for when naive retrieval brings back the wrong chunks; our filtered query only needed its filter removed.

## 28:49 — Tear down, a stale index, recap
Time to tear down. Type exit, then docker compose down from the repo folder: the same harmless warnings, then Chroma and the network are gone.
The images stay: 2.11 gigabytes for the CLI image, its Python base included, and 826 megabytes for Chroma.
Now git status shows only your edit to docker-shell.sh. The outputs and docker volumes folders are ignored, and stay on your disk.
Nothing keeps running in Google Cloud; you paid only for what you sent. Keep the key beside the repo: inside it, git wouldn't ignore the key, and the image would copy it. Delete it when the course ends. Pause and tear down now, so port 8000 is free next time.
One last lesson, from the staff's recorded run of next lecture's agent. It retrieved text about transhumance from an older Tolminc book, replaced that same day. The database answers from what was loaded: when the books change, rebuild the index.
Next lecture runs this command with an agent. In the staff's run, the model chose which retrieval tool to call. The lecture's Self-RAG goes further: the model decides whether to retrieve at all, then checks what it found. Our chat opens the book for every question, and checks nothing.
And the four questions? An embedding is a direction for meaning. A vector database stores records, with an index to search them. A query finds the question's nearest neighbors. The context is the chunks you paste into the prompt.
Five questions to test yourself. One: which flags belong to each lane, and what must both lanes share? Two: why does the CLI reach the database by name, and who uses port 8000?
Three: what does overlap buy and cost? And why did the recursive splitter make more chunks? Four: why did the README's query return no Tolminc text? Five: what is the prompt missing, and what's the fix?
The answers are in the exercises, and every command is in the study guide, in the MLOps Learning repo. Next time: agents.
