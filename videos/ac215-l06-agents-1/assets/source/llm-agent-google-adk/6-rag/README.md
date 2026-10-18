# Tutorial 6: RAG - Retrieval-Augmented Generation

Learn how to build RAG (Retrieval-Augmented Generation) agents with Google ADK using two different approaches: managed Vertex AI RAG Engine and a custom ChromaDB solution.

## Overview

In this tutorial, you'll learn:

- What is RAG and why it's essential for AI agents
- Using Vertex AI RAG Engine (managed service)
- Building custom RAG with ChromaDB and Docker
- When to use each approach
- Best practices for document retrieval
- Embeddings and vector search fundamentals

## What is RAG?

**Retrieval-Augmented Generation (RAG)** enhances LLM responses by:

1. **Retrieving** relevant documents from a knowledge base
2. **Augmenting** the LLM prompt with retrieved context
3. **Generating** responses grounded in your data

### Why RAG?

- **Reduce hallucinations**: Ground responses in factual documents
- **Up-to-date knowledge**: Add recent documents without retraining
- **Domain expertise**: Inject specialized knowledge
- **Citations**: Provide source attribution
- **Cost-effective**: Cheaper than fine-tuning for many use cases

### Agentic RAG

Both implementations use an **agentic RAG pattern** with:

- **Function calling** - LLM decides when and how to query the knowledge base
- **System instructions** - Guide the agent to ground responses in retrieved information
- **Two-step process** - Retrieve → Generate with context
- **Source attribution** - Always cite where information comes from

See [AGENT_USAGE.md](./AGENT_USAGE.md) for detailed usage examples.

## Tutorial Structure

This tutorial provides **two implementations** to choose from:

### [1. Vertex AI RAG Engine](./1-vertex-rag-engine/)

**Managed service approach**

- Uses Google Cloud's Vertex AI RAG Engine
- Fully managed infrastructure
- Automatic scaling and optimization
- Built-in document processing

**Best for**: Production deployments, enterprise use cases, teams wanting managed infrastructure

### [2. Custom ChromaDB RAG](./2-custom-chromadb-rag/)

**Self-hosted approach**

- Uses ChromaDB vector database
- Docker Compose deployment
- Full control over implementation
- Custom embedding models

**Best for**: Learning, prototyping, custom requirements, cost optimization

## Comparison

| Feature | Vertex RAG Engine | Custom ChromaDB |
|---------|------------------|-----------------|
| **Setup Complexity** | Low | Medium |
| **Infrastructure** | Fully managed | Self-hosted (Docker) |
| **Cost** | Pay-per-query | Free (hosting cost only) |
| **Scalability** | Automatic | Manual |
| **Customization** | Limited | Full control |
| **Embeddings** | Google managed | Your choice |
| **Document Processing** | Automatic | Manual |
| **Best For** | Production | Learning/Prototyping |

## Prerequisites

### Required for Both

- Python 3.10+
- uv package manager
- Google AI API key or Vertex AI access
- Completed Tutorials 1-3

### Additional for Vertex RAG Engine

- Google Cloud project with billing enabled
- Vertex AI API enabled
- `gcloud` CLI authenticated

### Additional for Custom ChromaDB

- Docker and Docker Compose installed
- Basic understanding of embeddings

## Quick Start

### Option 1: Vertex RAG Engine

```bash
cd 1-vertex-rag-engine
uv sync
cp .env.example .env
# edit .env with your Google Cloud project details and service account

# create RAG corpus and import documents
uv run python setup_corpus.py

# run queries (recommended)
uv run python agent.py

# or use web UI
uv run adk web
```

### Option 2: Custom ChromaDB

```bash
cd 2-custom-chromadb-rag

# start ChromaDB service
docker compose up -d

uv sync
cp .env.example .env

# ingest documents (assumes RAG is already populated)
uv run python ingest_documents.py

# run queries (recommended)
uv run python agent.py

# or use web UI
uv run adk web
```

## Key Concepts

### Vector Embeddings

Convert text into numerical vectors that capture semantic meaning:

```python
"What is RAG?" → [0.23, -0.45, 0.67, ...]
"Explain RAG" → [0.21, -0.43, 0.69, ...]  # Similar vector
```

### Similarity Search

Find documents with vectors closest to the query vector:

1. User query: "How does RAG work?"
2. Convert query to vector
3. Find top-K similar document vectors
4. Return matching documents

### Retrieval Parameters

- **top_k**: Number of documents to retrieve (e.g., 3-10)
- **similarity_threshold**: Minimum similarity score (e.g., 0.6-0.8)
- **chunk_size**: Document split size (e.g., 500-1000 tokens)

## Architecture Comparison

### Vertex RAG Engine

```
User Query
    ↓
Agent (Gemini)
    ↓
VertexAiRagRetrieval Tool
    ↓
Vertex RAG Engine (managed)
    ↓
Retrieved Documents
    ↓
Agent Response
```

### Custom ChromaDB

```
User Query
    ↓
Agent (Gemini)
    ↓
Custom RAG Tool
    ↓
ChromaDB (Docker)
    ↓
Retrieved Documents
    ↓
Agent Response
```

## Use Cases

### When to Use Vertex RAG Engine

- **Production applications** requiring reliability and scale
- **Enterprise deployments** with GCP infrastructure
- **Compliance needs** (data governance, audit trails)
- **Automatic document processing** pipelines
- **Limited ML expertise** on team

### When to Use Custom ChromaDB

- **Learning and experimentation**
- **Custom embedding models** or processing
- **Cost optimization** for smaller deployments
- **On-premises** or specific hosting requirements
- **Full control** over RAG pipeline

## Learning Path

**New to RAG?** Start with **Custom ChromaDB** to understand the fundamentals.

**Ready for production?** Move to **Vertex RAG Engine** for managed infrastructure.

**Both!** Try both implementations to compare approaches.

## Example Queries

Once you have either implementation running, try:

- "What information do you have about [topic]?"
- "Find documents related to [keyword]"
- "Summarize what you know about [subject]"
- "Compare [concept A] and [concept B] based on the documents"

## Common Challenges

### Challenge 1: Low Quality Retrieval

**Symptoms**: Agent retrieves irrelevant documents

**Solutions**:
- Adjust similarity threshold
- Improve document chunking
- Use better embedding models
- Add metadata filtering

### Challenge 2: Context Window Limits

**Symptoms**: Too many/large documents exceed context

**Solutions**:
- Reduce top_k parameter
- Smaller chunk sizes
- Implement re-ranking
- Summarize retrieved content

### Challenge 3: Slow Performance

**Symptoms**: Queries take too long

**Solutions**:
- Reduce top_k
- Optimize embeddings (smaller model)
- Cache frequent queries
- Index optimization

## Best Practices

### 1. Document Preparation

- **Clean text**: Remove formatting, normalize
- **Chunk appropriately**: 500-1000 tokens per chunk
- **Add metadata**: Source, date, category
- **Overlap chunks**: 50-100 tokens overlap

### 2. Embedding Strategy

- **Consistent model**: Same model for indexing and querying
- **Quality over size**: Smaller models can be faster
- **Domain-specific**: Use specialized models when available

### 3. Retrieval Tuning

- **Start conservative**: top_k=5, threshold=0.7
- **Iterate**: Adjust based on results
- **Combine signals**: Mix vector search with keyword/metadata

### 4. Agent Instructions

- **Be specific**: Tell agent when to use retrieval
- **Handle no results**: Graceful fallback behavior
- **Citation**: Encourage source attribution

## Exercises

### Exercise 1: Compare Both Approaches

1. Set up both Vertex RAG and ChromaDB implementations
2. Use the same documents in both
3. Ask the same queries
4. Compare: response quality, speed, cost

### Exercise 2: Custom Domain RAG

1. Choose a domain (e.g., your company docs, academic papers)
2. Prepare 10-20 documents
3. Implement RAG using ChromaDB
4. Test various query types

### Exercise 3: Hybrid Search

Extend ChromaDB implementation with:
- Keyword search (BM25)
- Metadata filtering
- Combine with vector search

## Troubleshooting

### Vertex RAG Engine Issues

**Error: "RAG corpus not found"**
- Run `setup_corpus.py` first
- Verify `RAG_CORPUS` environment variable
- Check corpus exists in Google Cloud Console

**Error: "Permission denied"**
- Enable Vertex AI API
- Verify IAM permissions
- Run `gcloud auth application-default login`

### ChromaDB Issues

**Error: "Cannot connect to ChromaDB"**
- Check Docker is running: `docker ps`
- Verify port 8000 is available
- Restart: `docker compose restart`

**Error: "Collection not found"**
- Run `ingest_documents.py` first
- Check collection name matches in code

**Poor retrieval quality**
- Try different embedding models
- Adjust chunk size
- Increase top_k parameter

## Key Takeaways

- ✅ **RAG** = Retrieval + Augmentation + Generation
- ✅ **Vertex RAG Engine** = Managed, production-ready
- ✅ **ChromaDB** = Flexible, self-hosted
- ✅ **Embeddings** = Semantic search foundation
- ✅ **Tuning** = Adjust top_k and threshold iteratively
- ✅ **Documents** = Quality preparation matters

## Next Steps

**Master RAG**: Work through both implementations

**Production**: Deploy to Cloud Run (see Tutorial 4)

**Advanced**: Combine with custom agents (Tutorial 5)

**Explore**: Try different embedding models and retrieval strategies

## Resources

- [Vertex AI RAG Engine Docs](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/rag)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [RAG Pattern Overview](https://python.langchain.com/docs/use_cases/question_answering/)
- [Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [ADK RAG Sample](https://github.com/google/adk-samples/tree/main/python/agents/RAG)

---

**Ready to add knowledge to your agents?** Choose your path:
- [Vertex RAG Engine →](./1-vertex-rag-engine/)
- [Custom ChromaDB →](./2-custom-chromadb-rag/)
