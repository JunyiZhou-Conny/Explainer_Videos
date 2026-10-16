# expected, not a capture and not program output: the README's own description of what the step does, README.md:155-160 ("Load Embeddings into Vector Database", dlops-io/llm-rag main @ e17a39f); command line(s) marked with $
$ python cli.py --load --chunk_type char-split
$ python cli.py --load --chunk_type recursive-split
This will:

- Connects to your ChromaDB instance
- Creates a new collection (or clears an existing one)
- Loads the embeddings and associated metadata into the collection
- Writes the data to `docker-volumes/chromadb`, which is bind-mounted into the ChromaDB container at `/data` (see `docker-compose.yml`). This makes the vector database **persistent** — it survives restarting or rebuilding the container, so you don't have to re-run the chunk → embed → load steps every time.
