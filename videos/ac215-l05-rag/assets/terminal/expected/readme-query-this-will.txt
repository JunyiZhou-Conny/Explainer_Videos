# expected, not a capture and not program output: the README's own description of what the step does, README.md:182-186 ("Query the Vector Database", dlops-io/llm-rag main @ e17a39f); command line(s) marked with $
$ python cli.py --query --chunk_type char-split
$ python cli.py --query --chunk_type recursive-split
This will:

- Generate an embedding for a sample query: "How is tolminc cheese made?"
- Perform similarity searches in the vector database
- Apply various types of filters on the queries
