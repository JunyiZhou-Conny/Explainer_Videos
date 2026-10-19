# Vertex AI RAG Engine Implementation

Use Google's managed RAG Engine service with ADK for production-ready knowledge retrieval.

## Overview

This implementation uses **Vertex AI RAG Engine**, a fully managed service for:

- Automatic document processing and chunking
- Managed vector embeddings
- Scalable retrieval infrastructure
- Built-in optimization and caching

## Prerequisites

- Google Cloud project with billing enabled
- Vertex AI API enabled
- Python 3.10+
- uv package manager

## Setup

### 1. Enable Vertex AI API

```bash
gcloud services enable aiplatform.googleapis.com
```

### 2. Create Service Account (Recommended)

**Option A: Using gcloud CLI**

```bash
# create service account
gcloud iam service-accounts create vertex-rag-agent \
    --display-name="Vertex RAG Agent" \
    --project=your-project-id

# grant necessary permissions
gcloud projects add-iam-policy-binding your-project-id \
    --member="serviceAccount:vertex-rag-agent@your-project-id.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# create and download key
gcloud iam service-accounts keys create service-account-key.json \
    --iam-account=vertex-rag-agent@your-project-id.iam.gserviceaccount.com
```

**Option B: Using Google Cloud Console**

1. Navigate to **IAM & Admin** > **Service Accounts**
2. Click **Create Service Account**
3. Name: `vertex-rag-agent`
4. Grant role: **Vertex AI User**
5. Click **Create Key** → **JSON** → Download
6. Save as `service-account-key.json` in this directory

**Alternative: User Credentials (Development Only)**

```bash
gcloud auth application-default login
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=true

# service account key path
GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json

GEMINI_MODEL=gemini-2.0-flash
```

**Important**: Add `service-account-key.json` to `.gitignore`:

```bash
echo "service-account-key.json" >> .gitignore
```

### 5. Create RAG corpus

```bash
uv run python setup_corpus.py
```

Follow the interactive menu to:
1. Create a new corpus
2. Import documents from Google Cloud Storage or Google Drive
3. Copy the corpus name to your `.env` file

**Example workflow:**

```
Select option: 1
Enter corpus display name: my-knowledge-base
Enter description: Product documentation corpus

✓ Corpus created: projects/12345/locations/us-central1/ragCorpora/67890

Add this to your .env file:
RAG_CORPUS=projects/12345/locations/us-central1/ragCorpora/67890
```

Then add to `.env`:

```bash
RAG_CORPUS=projects/12345/locations/us-central1/ragCorpora/67890
```

## Running the Agent

### Programmatic Usage (Recommended)

Run queries directly using the agentic RAG pattern:

```bash
cd 6-rag/1-vertex-rag-engine
uv run python agent.py
```

Or in your own code:

```python
from agent import run_agent_query

response = run_agent_query(
    "What information do you have in your knowledge base?",
    top_k=5  # number of documents to retrieve
)
print(response)
```

### Web UI (Alternative)

From the **repository root**:

```bash
uv run adk web
```

Open http://localhost:8000, navigate to `6-rag/1-vertex-rag-engine/agent.py`, and start chatting.

### Example Queries

Try asking:

- "What information do you have available?"
- "Tell me about [topic from your documents]"
- "Find details about [specific concept]"
- "Compare [A] and [B] based on the documentation"
- "Summarize the main themes in the knowledge base"

## How It Works

### Agentic RAG Architecture

This implementation uses **Vertex AI RAG Engine** with a programmatic retrieval flow:

```
User Query
    ↓
Step 1: Retrieve from Vertex RAG Engine
    ↓
  • Query RAG corpus with semantic search
  • Vertex AI handles embeddings automatically
  • Return top-K documents with sources
    ↓
Step 2: Format retrieved contexts
    ↓
Step 3: LLM generates response with context
    ↓
  • System instruction guides grounding
  • LLM synthesizes answer from retrieved docs
  • Citations included in response
```

### Three-Step Retrieval Process

**agent.py:52-140**: Main agentic query function

```python
def run_agent_query(user_prompt: str, top_k: int = 5):
    # step 1: retrieve documents using Vertex RAG
    rag_retrieval = rag.retrieval_query(
        rag_resources=[rag_resource],
        text=user_prompt,
        similarity_top_k=top_k,
        vector_distance_threshold=0.6
    )

    # step 2: format contexts for LLM
    formatted_contexts = format_retrieved_docs(contexts)

    # step 3: generate response with retrieved context
    response = llm_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=augmented_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION
        )
    )
```

### Key Components

**agent.py:33-49**: System instruction guiding the agent

**agent.py:90-95**: Vertex RAG retrieval with `rag.retrieval_query()`

- Automatic embedding generation
- Managed similarity search
- Built-in ranking and filtering

**agent.py:118-126**: Augmented prompt with retrieved context

## Document Import Options

### Option 1: Google Cloud Storage

1. Upload documents to GCS:

```bash
gsutil cp ./documents/*.pdf gs://your-bucket/documents/
```

2. Import in `setup_corpus.py`:

```
Select option: 3
Enter corpus name: projects/.../ragCorpora/...
Enter GCS URIs:
gs://your-bucket/documents/doc1.pdf
gs://your-bucket/documents/doc2.pdf
[empty line]
```

### Option 2: Google Drive

1. Upload documents to a Google Drive folder
2. Get the folder ID from the URL: `https://drive.google.com/drive/folders/FOLDER_ID`
3. Import in `setup_corpus.py`:

```
Select option: 4
Enter corpus name: projects/.../ragCorpora/...
Enter Google Drive folder ID: FOLDER_ID
```

## Supported File Types

Vertex AI RAG Engine supports:

- **Documents**: PDF, DOCX, TXT, HTML, MD
- **Spreadsheets**: XLSX, CSV
- **Presentations**: PPTX

## Configuration Parameters

### similarity_top_k

Number of documents to retrieve (agent.py:28)

- **Default**: 5
- **Range**: 1-100
- **Higher**: More context, slower
- **Lower**: Faster, less context

### vector_distance_threshold

Minimum similarity score (agent.py:29)

- **Default**: 0.6
- **Range**: 0.0-1.0
- **Higher**: Stricter matching
- **Lower**: More permissive

### chunk_size and chunk_overlap

Document splitting parameters (setup_corpus.py:72-73)

- **chunk_size**: Tokens per chunk (default: 1024)
- **chunk_overlap**: Overlapping tokens (default: 200)

## Monitoring and Debugging

### View corpus in Cloud Console

```bash
echo "https://console.cloud.google.com/vertex-ai/generative/rag?project=${GOOGLE_CLOUD_PROJECT}"
```

### List corpora programmatically

```bash
uv run python setup_corpus.py
# Select option: 2
```

### Check imported files

Via Cloud Console or API:

```python
from vertexai.preview import rag
corpus_name = "projects/.../ragCorpora/..."
files = rag.list_files(corpus_name=corpus_name)
for f in files:
    print(f.name, f.display_name)
```

## Cost Considerations

Vertex AI RAG Engine pricing:

- **Storage**: Per GB per month
- **Queries**: Per 1000 queries
- **Embeddings**: Included in query cost

See [Vertex AI Pricing](https://cloud.google.com/vertex-ai/pricing) for details.

**Cost optimization tips:**

- Start with smaller corpus for testing
- Use appropriate `top_k` (5-10 typical)
- Monitor usage in Cloud Console
- Delete unused corpora

## Troubleshooting

### Error: "Corpus not found"

**Solution**:
- Verify `RAG_CORPUS` in `.env` matches created corpus
- Run `setup_corpus.py` option 2 to list corpora
- Check corpus exists in Cloud Console

### Error: "Permission denied" or "Unauthorized"

**Solution with Service Account**:

1. Verify service account has correct permissions:
```bash
gcloud projects get-iam-policy $GOOGLE_CLOUD_PROJECT \
    --flatten="bindings[].members" \
    --filter="bindings.members:serviceAccount:vertex-rag-agent*"
```

2. Grant missing permissions:
```bash
gcloud projects add-iam-policy-binding your-project-id \
    --member="serviceAccount:vertex-rag-agent@your-project-id.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# for GCS imports
gcloud projects add-iam-policy-binding your-project-id \
    --member="serviceAccount:vertex-rag-agent@your-project-id.iam.gserviceaccount.com" \
    --role="roles/storage.objectViewer"
```

3. Verify key file path is correct in `.env`:
```bash
GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json
```

**Solution with User Credentials** (Development):

```bash
gcloud auth application-default login
```

### Error: "Could not load credentials"

**Solution**:
- Check `GOOGLE_APPLICATION_CREDENTIALS` path in `.env` is correct
- Verify `service-account-key.json` file exists
- Ensure JSON file is valid (not corrupted)

```bash
# verify key file exists
ls -la service-account-key.json

# test credentials
gcloud auth activate-service-account --key-file=service-account-key.json
```

### Error: "API not enabled"

**Solution**:
```bash
gcloud services enable aiplatform.googleapis.com
```

### Poor retrieval quality

**Solutions**:

1. **Adjust threshold**:
   ```python
   vector_distance_threshold=0.5  # More permissive
   ```

2. **Increase top_k**:
   ```python
   similarity_top_k=10  # More results
   ```

3. **Improve documents**:
   - Add more documents
   - Better formatting (headings, structure)
   - Remove noise (boilerplate, footers)

4. **Smaller chunks**:
   ```python
   chunk_size=512  # Smaller, more precise chunks
   ```

### No results returned

**Possible causes**:

1. **Threshold too high**: Lower `vector_distance_threshold`
2. **No relevant documents**: Verify corpus contains expected content
3. **Import failed**: Check import status in Cloud Console
4. **Query mismatch**: Rephrase query or add more documents

## Best Practices

### 1. Document Preparation

- **Clean documents**: Remove headers/footers, formatting
- **Structured content**: Use headings, bullet points
- **Metadata**: Include titles, dates, categories

### 2. Corpus Organization

- **Single topic per corpus**: Better retrieval accuracy
- **Regular updates**: Keep documents current
- **Version control**: Track corpus changes

### 3. Agent Instructions

- **When to retrieve**: Clear guidance on tool usage
- **Citation**: Encourage source attribution
- **Fallback**: Handle no-results gracefully

Example instruction (agent.py:36):

```python
instruction=(
    "Use retrieve_documents when user asks factual questions. "
    "Always cite sources. "
    "If no relevant documents found, say 'I don't have information on that.'"
)
```

### 4. Testing

Test with:
- **Known answers**: Verify correct retrieval
- **Edge cases**: Out-of-domain queries
- **Synonyms**: Check semantic understanding
- **Multi-hop**: Questions requiring multiple documents

## Advanced Usage

### Multiple Corpora

Combine multiple corpora:

```python
rag_resources=[
    rag.RagResource(rag_corpus="projects/.../ragCorpora/corpus1"),
    rag.RagResource(rag_corpus="projects/.../ragCorpora/corpus2"),
]
```

### Custom Embeddings

Use specific embedding models (requires Vertex AI configuration):

```python
rag.create_corpus(
    display_name="my-corpus",
    embedding_model_config=rag.EmbeddingModelConfig(
        publisher_model="textembedding-gecko@003"
    ),
)
```

### Metadata Filtering

Add metadata during import and filter at query time:

```python
# During import (requires API/SDK)
metadata = {"category": "technical", "year": "2024"}

# During retrieval (future feature)
# Currently not directly supported in ADK wrapper
```

## Migration to Production

### 1. Separate Corpora

- **Dev/Test/Prod**: Different corpora per environment
- **Environment variables**: Switch via `.env`

### 2. CI/CD Integration

```bash
# In CI pipeline
gcloud auth activate-service-account --key-file=${KEY_FILE}
python setup_corpus.py --create --name="prod-corpus"
python import_docs.py --corpus=${CORPUS_NAME} --source=${GCS_PATH}
```

### 3. Monitoring

- Set up Cloud Monitoring alerts
- Track query latency and errors
- Monitor corpus size and costs

### 4. Security

- Use service accounts with minimal permissions
- Enable VPC Service Controls
- Audit access logs

## Next Steps

**Compare approaches**: Try [Custom ChromaDB](../2-custom-chromadb-rag/) implementation

**Production deployment**: See [Tutorial 4: Production Ready](../../4-production-ready/)

**Advanced agents**: Combine with [Tutorial 5: Custom Agents](../../5-custom-agent/)

## Resources

- [Vertex AI RAG Engine Docs](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/rag)
- [RAG API Reference](https://cloud.google.com/python/docs/reference/aiplatform/latest/vertexai.preview.rag)
- [ADK RAG Tools](https://google.github.io/adk-docs/tools/rag-tools/)
- [Original ADK Sample](https://github.com/google/adk-samples/tree/main/python/agents/RAG)
