# Agentic RAG Usage Guide

This guide shows how to use the agentic RAG pattern implemented in both tutorial options.

## What is Agentic RAG?

Agentic RAG uses **function calling** to give the LLM tools for querying the knowledge base. Instead of directly embedding retrieval in the prompt, the LLM:

1. Decides when to use retrieval tools
2. Calls the appropriate functions
3. Receives retrieved context
4. Synthesizes a final response

## ChromaDB Implementation

### Running Queries

```python
from agent import run_agent_query

# basic query
response = run_agent_query("What is machine learning?")
print(response)
```

### How It Works

The agent has two tools available:

1. **search_knowledge_base** - semantic search across all documents
2. **search_by_source** - search filtered by source document

The LLM automatically chooses which tool(s) to use based on your query.

### Example Output

```
================================================================================
user query: What is machine learning?
================================================================================

executing function: search_knowledge_base
arguments: {'query': 'machine learning', 'num_results': 5}

generating final response with retrieved context...
================================================================================

response:
Machine learning is a subset of artificial intelligence that enables systems
to learn and improve from experience without being explicitly programmed...
[Based on document: machine_learning.txt]
```

## Vertex RAG Engine Implementation

### Running Queries

```python
from agent import run_agent_query

# basic query
response = run_agent_query(
    "What information do you have?",
    top_k=5  # retrieve top 5 documents
)
print(response)
```

### How It Works

The agent:

1. Retrieves relevant documents from Vertex RAG corpus
2. Formats the retrieved context
3. Generates a response grounded in the retrieved information

Vertex AI handles embeddings and similarity search automatically.

### Example Output

```
================================================================================
user query: What information do you have?
================================================================================

retrieving top 5 documents from RAG corpus...
retrieved 5 context(s)

generating response with retrieved context...
================================================================================

response:
Based on the knowledge base, I have information about...
[Sources: doc1.pdf, doc2.pdf]
```

## Key Differences

| Feature | ChromaDB | Vertex RAG |
|---------|----------|------------|
| **Tool Selection** | LLM decides which tool | Direct retrieval |
| **Embeddings** | Sentence Transformers | Vertex AI (automatic) |
| **Filtering** | Multiple tools for different filters | Single retrieval call |
| **Setup** | Docker + ChromaDB | Google Cloud + RAG Engine |
| **Cost** | Infrastructure only | Per-query pricing |

## System Instructions

Both implementations use detailed system instructions to guide the agent:

```python
SYSTEM_INSTRUCTION = """
you are a helpful AI assistant with access to a knowledge base...

when answering a query:
1. use the retrieval tools to find relevant information
2. base responses only on retrieved information
3. cite sources clearly
4. state when information is insufficient
...
"""
```

This ensures the agent:
- Only uses retrieved information
- Provides citations
- Handles edge cases appropriately

## Advanced Usage

### ChromaDB: Multiple Tool Calls

```python
# the agent can call multiple tools in sequence
query = "Compare what python_programming and machine_learning documents say about applications"

# the LLM might call search_by_source twice:
# 1. search_by_source(query="applications", source="python_programming")
# 2. search_by_source(query="applications", source="machine_learning")

response = run_agent_query(query)
```

### Vertex RAG: Adjusting Retrieval

```python
# retrieve more context
response = run_agent_query(
    "Detailed explanation of cloud computing",
    top_k=10  # retrieve 10 documents instead of 5
)

# the agent gets more context to work with
```

## Best Practices

### 1. Clear Queries

**Good**: "What are the types of machine learning?"
**Better**: "Explain supervised vs unsupervised learning based on the documents"

### 2. Source Attribution

The agent is instructed to cite sources. Ask explicitly if needed:

"What does the python_programming document say about frameworks?"

### 3. Verification

When accuracy is critical:

```python
query = "What is the exact process for making cheese? Include sources."
response = run_agent_query(query)
```

### 4. Handling No Results

The agent will tell you when retrieved information is insufficient:

```
"I don't have enough information in the knowledge base to answer that question completely."
```

## Integration Examples

### Batch Processing

```python
queries = [
    "What is machine learning?",
    "Explain Python's use cases",
    "What are cloud service models?"
]

for query in queries:
    print(f"\nQuery: {query}")
    response = run_agent_query(query)
    print(f"Response: {response}\n")
```

### API Endpoint

```python
from fastapi import FastAPI
from agent import run_agent_query

app = FastAPI()

@app.post("/query")
async def query_knowledge_base(query: str):
    response = run_agent_query(query)
    return {"query": query, "response": response}
```

### Streaming (Advanced)

For long responses, you can modify the agent to stream:

```python
# this would require modifying agent.py to use streaming
config = types.GenerateContentConfig(
    stream=True,
    ...
)
```

## Debugging

### Enable Verbose Logging

Both implementations print execution steps:

```
llm initial response received
executing 1 function call(s)
executing function: search_knowledge_base
arguments: {'query': '...', 'num_results': 5}
generating final response with retrieved context...
```

### Common Issues

**No function calls made**:
- Check that tools are properly configured
- Ensure `mode="any"` forces tool use (ChromaDB)

**Empty results**:
- Verify ChromaDB is running: `docker ps`
- Check Vertex RAG corpus exists
- Confirm documents were ingested

**Poor responses**:
- Try different queries (more specific)
- Adjust `top_k` parameter
- Check system instruction alignment

## Next Steps

- Integrate with your application
- Customize system instructions
- Add custom tools (ChromaDB)
- Deploy to production (see Tutorial 4)
- Combine with other agent patterns (Tutorial 5)
