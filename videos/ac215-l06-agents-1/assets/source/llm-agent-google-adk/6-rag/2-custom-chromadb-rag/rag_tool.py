"""
Custom RAG tool using ChromaDB for retrieval.
"""

import os
from typing import Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer


class ChromaDBRetriever:
    """handles document retrieval from ChromaDB"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        collection_name: str = "knowledge_base",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.host = host
        self.port = port
        self.collection_name = collection_name

        self.client = chromadb.HttpClient(host=host, port=port)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "RAG knowledge base"}
        )

        self.embedding_model = SentenceTransformer(embedding_model)

    def query(self, query_text: str, top_k: int = 5) -> Dict[str, Any]:
        """
        retrieve relevant documents from ChromaDB

        args:
            query_text: user's query
            top_k: number of results to return

        returns:
            dict with retrieved documents and metadata
        """
        try:
            query_embedding = self.embedding_model.encode(
                query_text,
                convert_to_tensor=False
            ).tolist()

            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )

            if not results["documents"] or not results["documents"][0]:
                return {
                    "success": True,
                    "documents": [],
                    "message": "No relevant documents found."
                }

            documents = []
            for i, doc in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"][0] else {}
                distance = results["distances"][0][i] if results["distances"][0] else None

                documents.append({
                    "content": doc,
                    "metadata": metadata,
                    "distance": distance,
                    "similarity": 1 - distance if distance is not None else None
                })

            return {
                "success": True,
                "documents": documents,
                "count": len(documents),
                "query": query_text
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to retrieve documents: {str(e)}"
            }


def create_rag_retrieval_function(
    host: str = "localhost",
    port: int = 8000,
    collection_name: str = "knowledge_base",
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    top_k: int = 5
):
    """
    creates a RAG retrieval function that can be used as a FunctionTool
    """
    retriever = ChromaDBRetriever(
        host=host,
        port=port,
        collection_name=collection_name,
        embedding_model=embedding_model
    )

    def retrieve_documents(query: str) -> str:
        """
        retrieve relevant documents from the knowledge base.

        use this tool when you need factual information from stored documents.
        the tool will return the most relevant passages based on semantic similarity.

        args:
            query: the search query or question to find relevant documents for

        returns:
            formatted string with retrieved documents and their sources
        """
        result = retriever.query(query, top_k=top_k)

        if not result["success"]:
            return f"Error retrieving documents: {result.get('message', 'Unknown error')}"

        if not result["documents"]:
            return "No relevant documents found in the knowledge base."

        response_parts = [f"Found {result['count']} relevant document(s):\n"]

        for i, doc in enumerate(result["documents"], 1):
            response_parts.append(f"\n--- Document {i} ---")
            response_parts.append(f"Content: {doc['content']}")

            if doc.get("metadata"):
                response_parts.append(f"Source: {doc['metadata'].get('source', 'Unknown')}")

            if doc.get("similarity") is not None:
                similarity_pct = doc["similarity"] * 100
                response_parts.append(f"Relevance: {similarity_pct:.1f}%")

        return "\n".join(response_parts)

    return retrieve_documents
