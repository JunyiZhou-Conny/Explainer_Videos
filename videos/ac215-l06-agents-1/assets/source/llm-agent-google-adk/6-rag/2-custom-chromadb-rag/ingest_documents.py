"""
Document ingestion script for ChromaDB.

Loads documents from a directory and indexes them in ChromaDB.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "knowledge_base")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    split text into overlapping chunks

    args:
        text: input text to chunk
        chunk_size: approximate number of characters per chunk
        overlap: number of characters to overlap between chunks

    returns:
        list of text chunks
    """
    words = text.split()
    chunks = []

    words_per_chunk = chunk_size // 5
    overlap_words = overlap // 5

    for i in range(0, len(words), words_per_chunk - overlap_words):
        chunk = " ".join(words[i:i + words_per_chunk])
        if chunk:
            chunks.append(chunk)

    return chunks


def load_documents_from_directory(directory: str) -> List[Dict[str, str]]:
    """
    load all text files from a directory

    args:
        directory: path to directory containing documents

    returns:
        list of dicts with 'content' and 'metadata'
    """
    documents = []
    directory_path = Path(directory)

    if not directory_path.exists():
        print(f"Error: Directory '{directory}' does not exist")
        return documents

    supported_extensions = ['.txt', '.md', '.text']

    for file_path in directory_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                chunks = chunk_text(content)

                for i, chunk in enumerate(chunks):
                    documents.append({
                        'content': chunk,
                        'metadata': {
                            'source': str(file_path.name),
                            'path': str(file_path),
                            'chunk': i,
                            'total_chunks': len(chunks)
                        }
                    })

                print(f"✓ Loaded {len(chunks)} chunk(s) from {file_path.name}")

            except Exception as e:
                print(f"✗ Failed to load {file_path.name}: {e}")

    return documents


def ingest_documents(
    documents: List[Dict[str, str]],
    host: str = CHROMA_HOST,
    port: int = CHROMA_PORT,
    collection_name: str = COLLECTION_NAME,
    embedding_model_name: str = EMBEDDING_MODEL
):
    """
    ingest documents into ChromaDB with embeddings

    args:
        documents: list of documents with 'content' and 'metadata'
        host: chromadb host
        port: chromadb port
        collection_name: name of the collection
        embedding_model_name: sentence transformer model name
    """
    print(f"\nConnecting to ChromaDB at {host}:{port}...")

    try:
        client = chromadb.HttpClient(host=host, port=port)
        client.heartbeat()
        print("✓ Connected to ChromaDB")
    except Exception as e:
        print(f"✗ Failed to connect to ChromaDB: {e}")
        print("\nMake sure ChromaDB is running:")
        print("  docker compose up -d")
        sys.exit(1)

    try:
        client.delete_collection(name=collection_name)
        print(f"✓ Cleared existing collection: {collection_name}")
    except:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={"description": "RAG knowledge base"}
    )
    print(f"✓ Created collection: {collection_name}")

    print(f"\nLoading embedding model: {embedding_model_name}")
    embedding_model = SentenceTransformer(embedding_model_name)
    print("✓ Embedding model loaded")

    print(f"\nIngesting {len(documents)} document chunk(s)...")

    batch_size = 100
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]

        texts = [doc['content'] for doc in batch]
        metadatas = [doc['metadata'] for doc in batch]
        ids = [f"doc_{i + j}" for j in range(len(batch))]

        embeddings = embedding_model.encode(texts, convert_to_tensor=False).tolist()

        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

        print(f"  Processed {min(i + batch_size, len(documents))}/{len(documents)} chunks")

    print(f"\n✓ Successfully ingested {len(documents)} document chunk(s)")
    print(f"✓ Collection '{collection_name}' ready for querying")


def main():
    """interactive document ingestion"""
    print("=" * 80)
    print("ChromaDB Document Ingestion")
    print("=" * 80)
    print()

    default_dir = "./sample_documents"
    directory = input(f"Enter directory path (default: {default_dir}): ").strip()

    if not directory:
        directory = default_dir

    print(f"\nLoading documents from: {directory}")
    documents = load_documents_from_directory(directory)

    if not documents:
        print("\n✗ No documents found to ingest")
        print("\nSupported file types: .txt, .md, .text")
        print(f"Place your documents in: {directory}")
        sys.exit(1)

    print(f"\nFound {len(documents)} document chunk(s)")
    confirm = input("Proceed with ingestion? (yes/no): ").strip().lower()

    if confirm != 'yes':
        print("Cancelled.")
        sys.exit(0)

    ingest_documents(documents)

    print("\n" + "=" * 80)
    print("Ingestion complete! You can now run the agent:")
    print("  uv run adk web")
    print("=" * 80)


if __name__ == "__main__":
    main()
