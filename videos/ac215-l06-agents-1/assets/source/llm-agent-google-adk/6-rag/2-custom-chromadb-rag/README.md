# Custom ChromaDB RAG Implementation

Build your own RAG system with ChromaDB vector database and custom Python tools.

## Overview

This implementation shows how to build RAG from scratch using:

- **ChromaDB**: Open-source vector database
- **Docker Compose**: Container orchestration
- **Sentence Transformers**: Open-source embeddings
- **Custom FunctionTool**: Full control over retrieval

## Prerequisites

- Docker and Docker Compose installed
- Python 3.10+
- uv package manager
- Google AI API key

## Setup

### 1. Start ChromaDB service

```bash
docker compose up -d
```

Verify it's running:

```bash
docker ps
curl http://localhost:8000/api/v1/heartbeat
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```bash
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash

CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_COLLECTION_NAME=knowledge_base

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### 4. Ingest documents

```bash
uv run python ingest_documents.py
```

This will:
1. Load documents from `sample_documents/`
2. Split them into chunks
3. Generate embeddings
4. Store in ChromaDB

**Example output:**

```
Connecting to ChromaDB at localhost:8000...
✓ Connected to ChromaDB
✓ Created collection: knowledge_base
✓ Embedding model loaded
Ingesting 15 document chunk(s)...
✓ Successfully ingested 15 document chunk(s)
```

## Running the Agent

Run queries directly using Google ADK Agent:

```bash
cd 6-rag/2-custom-chromadb-rag
uv run python agent.py
```

### Example Queries

Try asking:

- "What is machine learning?"
- "Explain the types of machine learning"
- "Tell me about Python programming"
- "What are the cloud computing service models?"
- "Compare supervised and unsupervised learning"
- "What does the python_programming document say about frameworks?"

## How It Works

### Agentic RAG Architecture

This implementation uses **Google ADK Agent** with custom tools for agentic RAG:

```
User Query
    ↓
ADK Agent determines which tools to call
    ↓
Execute tool(s) to retrieve from ChromaDB
    ↓
  • Generate query embedding
  • Search ChromaDB with semantic similarity
  • Return top-K documents with metadata
    ↓
ADK Agent synthesizes final response with retrieved context
```

### Key Components

**agent.py**: ADK Agent with custom ChromaDB tools

```python
root_agent = Agent(
    model=GEMINI_MODEL,
    name='chromadb_rag_agent',
    instruction=SYSTEM_INSTRUCTION,
    tools=[search_kb_tool, search_source_tool]
)
```

**Tools:**
- `search_kb_tool` - semantic search across all documents
- `search_source_tool` - search with source filtering

**agent_tools.py**: Helper functions for ChromaDB operations

- `search_knowledge_base` - core search implementation
- `search_by_source` - source-filtered search implementation

## Adding Your Own Documents

### Option 1: Add to sample_documents/

1. Place `.txt` or `.md` files in `sample_documents/`
2. Run ingestion script:

```bash
uv run python ingest_documents.py
```

### Option 2: Ingest from custom directory

```bash
uv run python ingest_documents.py
# When prompted, enter your directory path
```

### Supported File Types

- `.txt` - Plain text
- `.md` - Markdown
- `.text` - Text files

**Note**: For PDF, DOCX, etc., you'll need to add parsers (e.g., PyPDF2, python-docx).

## Configuration

### Embedding Models

Change in `.env`:

```bash
# Fast and lightweight (default)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Higher quality, slower
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2

# Multilingual
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### Chunk Size and Overlap

Edit `ingest_documents.py:26-27`:

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    # adjust chunk_size and overlap as needed
```

**Guidelines:**
- **chunk_size**: 300-1000 characters
- **overlap**: 10-20% of chunk_size
- Smaller chunks = more precise, but more storage
- Larger chunks = more context, but less precise

### Retrieval Parameters

Edit `agent.py:21`:

```python
top_k=5  # number of results to return
```

**Guidelines:**
- `top_k=3`: Fast, minimal context
- `top_k=5`: Balanced (default)
- `top_k=10`: More context, slower

## Managing ChromaDB

### View collections

```python
import chromadb
client = chromadb.HttpClient(host="localhost", port=8000)
print(client.list_collections())
```

### Collection info

```python
collection = client.get_collection("knowledge_base")
print(f"Documents: {collection.count()}")
```

### Delete collection

```python
client.delete_collection("knowledge_base")
```

### Restart with fresh data

```bash
docker compose down -v  # removes volume
docker compose up -d
uv run python ingest_documents.py
```

## Troubleshooting

### Error: "Failed to connect to ChromaDB"

**Solution:**

```bash
# check if docker is running
docker ps

# restart chromadb
docker compose restart

# check logs
docker compose logs chromadb
```

### Error: "Collection not found"

**Solution:**
Run the ingestion script first:

```bash
uv run python ingest_documents.py
```

### Poor retrieval quality

**Solutions:**

1. **Try different embedding model** (.env):
   ```bash
   EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
   ```

2. **Adjust chunk size** (ingest_documents.py):
   ```python
   chunk_size=300  # smaller for precise matching
   ```

3. **Increase top_k** (agent.py):
   ```python
   top_k=10  # retrieve more documents
   ```

4. **Add more documents**: More diverse content improves coverage

### Slow performance

**Solutions:**

1. **Use smaller embedding model**:
   ```bash
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   ```

2. **Reduce top_k**:
   ```python
   top_k=3
   ```

3. **Limit document size**: Remove very large documents

### No results returned

**Possible causes:**

1. **Empty collection**: Run ingestion script
2. **Query mismatch**: Rephrase query
3. **Wrong collection name**: Check `.env` settings

## Advanced Usage

### Custom Document Processing

Extend `ingest_documents.py` to handle PDFs:

```python
from PyPDF2 import PdfReader

def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
```

### Metadata Filtering

Add metadata during ingestion:

```python
metadata = {
    'source': filename,
    'category': 'technical',
    'date': '2024-01-01'
}
```

Query with filters (requires ChromaDB where clause):

```python
results = collection.query(
    query_embeddings=[embedding],
    where={"category": "technical"},
    n_results=5
)
```

### Hybrid Search

Combine vector search with keyword search:

```python
# vector search
vector_results = collection.query(...)

# keyword search (requires implementation)
keyword_results = full_text_search(query)

# merge results
combined = merge_and_rank(vector_results, keyword_results)
```

### Re-ranking

Improve results with cross-encoder re-ranking:

```python
from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# re-rank top-K results
scores = cross_encoder.predict([(query, doc) for doc in results])
reranked = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
```

## Production Deployment

### 1. Use Remote ChromaDB

Deploy ChromaDB to cloud and update `.env`:

```bash
CHROMA_HOST=chromadb.example.com
CHROMA_PORT=443
```

### 2. Authentication

Add authentication to ChromaDB (requires ChromaDB auth setup):

```python
client = chromadb.HttpClient(
    host=host,
    port=port,
    headers={"Authorization": f"Bearer {token}"}
)
```

### 3. Persistent Storage

Update `docker-compose.yml` for production:

```yaml
volumes:
  - /mnt/data/chromadb:/chroma/chroma
```

### 4. Monitoring

Add health checks and logging:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def query_with_logging(query):
    logger.info(f"Query: {query}")
    results = retriever.query(query)
    logger.info(f"Found {len(results)} results")
    return results
```

## Performance Optimization

### Batch Processing

Process multiple queries efficiently:

```python
embeddings = model.encode(queries, batch_size=32)
```

### Caching

Cache embeddings for frequent queries:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_embedding(text: str):
    return model.encode(text)
```

### Async Operations

Use async for concurrent queries:

```python
import asyncio

async def query_async(query):
    # async implementation
    pass
```

## Cost Comparison

| Component | ChromaDB | Vertex RAG |
|-----------|----------|------------|
| **Vector DB** | Free | $$ |
| **Embeddings** | Free (self-hosted) | $$ |
| **Compute** | Your infrastructure | Pay-per-query |
| **Storage** | Your disk | Pay-per-GB |
| **Total** | Infrastructure only | Per-usage pricing |

## Best Practices

1. **Document Quality**: Clean, well-structured documents improve retrieval
2. **Chunk Appropriately**: Balance precision vs context
3. **Monitor Performance**: Track query latency and quality
4. **Version Control**: Track embedding model and document versions
5. **Regular Updates**: Keep documents current
6. **Test Queries**: Build query test suite
7. **Backup Data**: Regular ChromaDB backups

## Next Steps

**Compare approaches**: Try [Vertex RAG Engine](../1-vertex-rag-engine/) for comparison

**Production deployment**: See [Tutorial 4: Production Ready](../../4-production-ready/)

**Advanced patterns**: Explore [Tutorial 5: Custom Agents](../../5-custom-agent/)

## Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [ADK Tools Guide](https://google.github.io/adk-docs/tools/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
