# expected, not a capture and not program output: the README's own description of what the step does, README.md:133-138 ("Generate Embeddings", dlops-io/llm-rag main @ e17a39f); command line(s) marked with $
$ python cli.py --embed --chunk_type char-split
$ python cli.py --embed --chunk_type recursive-split
This will:

- Reads the chunk files created in the previous section
- Uses the **Gemini Enterprise Agent Platform** (formerly Vertex AI) text embeddings API to generate embeddings for each chunk
- Saves the chunks with their embeddings as new JSONL files
- We use the `gemini-embedding-001` model to generate the embeddings (the older `text-embedding-004` model was retired on January 14, 2026)
