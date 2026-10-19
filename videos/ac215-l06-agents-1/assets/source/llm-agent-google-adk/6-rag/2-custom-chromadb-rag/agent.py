# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Custom ChromaDB RAG Agent

Demonstrates agentic RAG with function calling using ChromaDB and Google ADK.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import chromadb
from sentence_transformers import SentenceTransformer
from agent_tools import search_knowledge_base, search_by_source

load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "knowledge_base")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# initialize chromadb and embedding model
chromadb.api.client.SharedSystemClient.clear_system_cache()
chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
collection = chroma_client.get_collection(name=COLLECTION_NAME)
embedding_model = SentenceTransformer(EMBEDDING_MODEL)


def generate_query_embedding(query: str):
    """generate embedding for a query string"""
    return embedding_model.encode(query, convert_to_tensor=False).tolist()


# system instruction for the RAG agent
SYSTEM_INSTRUCTION = """
you are a helpful AI assistant with access to a knowledge base. your responses are based on the information in the knowledge base accessed through your search tools.

when answering a query:
1. use the search_kb_tool to find relevant information
2. if the user asks about a specific document or source, use the search_source_tool
3. base your responses only on the information retrieved from the knowledge base
4. if the retrieved information doesn't contain enough to answer the query, state this clearly
5. always cite which sources you're drawing information from
6. be concise but comprehensive in your responses

remember:
- your knowledge is limited to what's in the knowledge base
- do not invent information beyond what the tools return
- if there are contradictions in the retrieved information, mention them
- maintain a helpful and professional tone
"""


# define ADK-compatible tool functions
def search_kb_tool(query: str, num_results: int = 5):
    """
    searches the knowledge base for relevant information.
    use this tool when you need to find specific information to answer the user's question.

    Args:
        query: the search query to find relevant documents
        num_results: number of results to return (default: 5, max: 10)

    Returns:
        dict with search results
    """
    return search_knowledge_base(
        query=query,
        num_results=num_results,
        collection=collection,
        embed_func=generate_query_embedding
    )


def search_source_tool(query: str, source: str, num_results: int = 5):
    """
    searches the knowledge base with filtering by document source.
    use this when you need to find information from a specific document.

    Args:
        query: the search query to find relevant documents
        source: the document source name to filter by
        num_results: number of results to return (default: 5, max: 10)

    Returns:
        dict with search results
    """
    return search_by_source(
        query=query,
        source=source,
        num_results=num_results,
        collection=collection,
        embed_func=generate_query_embedding
    )


# create the ADK agent with tools
root_agent = Agent(
    model=GEMINI_MODEL,
    name='chromadb_rag_agent',
    instruction=SYSTEM_INSTRUCTION,
    tools=[search_kb_tool, search_source_tool]
)


if __name__ == "__main__":
    import asyncio

    async def main():
        # Create session service
        session_service = InMemorySessionService()

        # Define session parameters
        APP_NAME = "chromadb_rag_app"
        USER_ID = "user_1"
        SESSION_ID = "session_001"

        # Create session
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )

        # Create runner
        runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=session_service
        )

        # Prepare user message
        query = "What the name of the teacher in machine learning?"
        content = types.Content(
            role='user',
            parts=[types.Part(text=query)]
        )

        print(f"Query: {query}\n")

        # Run agent
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=content
        ):
            if event.is_final_response() and event.content:
                print(f"Response: {event.content.parts[0].text}")

    asyncio.run(main())
