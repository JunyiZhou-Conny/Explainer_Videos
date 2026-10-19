# expected, not a capture and not program output: the README's own description of what the step does, README.md:203-209 ("Chat with LLM", dlops-io/llm-rag main @ e17a39f); command line(s) marked with $
$ python cli.py --chat --chunk_type char-split
$ python cli.py --chat --chunk_type recursive-split
This will:

Takes a sample query: "How is tolminc cheese made?"

- Retrieves relevant context from the vector database
- Sends the query and context to the LLM
- Displays the LLM's response
