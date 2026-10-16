# expected, not a capture and not program output: the README's own description of what the step does, README.md:230-236 ("Advanced RAG: Semantic Chunking", dlops-io/llm-rag main @ e17a39f); command line(s) marked with $
$ python cli.py --chunk --embed --load --chunk_type semantic-split
This will:

- Read each text file in the `input-datasets/books` directory
- Split the text into chunks using semantic splitting method
- Save the chunks as JSONL files in the `outputs` directory
- Reads each JSONL file of chunks and converts to embeddings and saves them
- Loads each JSONL file with embeddings into the vector db
