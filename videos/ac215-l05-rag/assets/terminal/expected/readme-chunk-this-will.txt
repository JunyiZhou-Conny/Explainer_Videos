# expected, not a capture and not program output: the README's own description of what the step does, README.md:112-116 ("Chunk Documents", dlops-io/llm-rag main @ e17a39f); command line(s) marked with $
$ python cli.py --chunk --chunk_type char-split
$ python cli.py --chunk --chunk_type recursive-split
This will:

- Read each text file in the `input-datasets/books` directory
- Split the text into chunks using the specified method (character-based or recursive)
- Save the chunks as JSONL files in the `outputs` directory
