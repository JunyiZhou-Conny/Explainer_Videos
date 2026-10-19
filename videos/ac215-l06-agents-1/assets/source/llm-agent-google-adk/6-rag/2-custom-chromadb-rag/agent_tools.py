"""
Agent tools for RAG retrieval with ChromaDB.

Defines function calling tools for the agent to query the knowledge base.
"""

from google.genai import types


# define the tool for querying the knowledge base
knowledge_base_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="search_knowledge_base",
            description=(
                "searches the knowledge base for relevant information. "
                "use this tool when you need to find specific information to answer the user's question."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "the search query to find relevant documents"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "number of results to return (default: 5, max: 10)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        types.FunctionDeclaration(
            name="search_by_source",
            description=(
                "searches the knowledge base with filtering by document source. "
                "use this when you need to find information from a specific document."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "the search query to find relevant documents"
                    },
                    "source": {
                        "type": "string",
                        "description": "the document source name to filter by"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "number of results to return (default: 5, max: 10)",
                        "default": 5
                    }
                },
                "required": ["query", "source"]
            }
        )
    ]
)


def execute_function_calls(function_calls, collection, embed_func):
    """
    execute function calls from the LLM.

    args:
        function_calls: list of function calls from the LLM
        collection: chromadb collection to query
        embed_func: function to generate embeddings for queries

    returns:
        list of function response parts
    """
    function_responses = []

    for function_call in function_calls:
        function_name = function_call.name
        function_args = function_call.args

        print(f"executing function: {function_name}")
        print(f"arguments: {function_args}")

        # execute the appropriate function
        if function_name == "search_knowledge_base":
            result = search_knowledge_base(
                query=function_args.get("query"),
                num_results=function_args.get("num_results", 5),
                collection=collection,
                embed_func=embed_func
            )
        elif function_name == "search_by_source":
            result = search_by_source(
                query=function_args.get("query"),
                source=function_args.get("source"),
                num_results=function_args.get("num_results", 5),
                collection=collection,
                embed_func=embed_func
            )
        else:
            result = {"error": f"unknown function: {function_name}"}

        # create function response
        function_response = types.Part(
            function_response=types.FunctionResponse(
                name=function_name,
                response={"result": result}
            )
        )
        function_responses.append(function_response)

    return function_responses


def search_knowledge_base(query, num_results, collection, embed_func):
    """
    search the knowledge base for relevant documents.

    args:
        query: search query
        num_results: number of results to return
        collection: chromadb collection
        embed_func: embedding function

    returns:
        dict with search results
    """
    # generate query embedding
    query_embedding = embed_func(query)

    # query chromadb
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(num_results, 10)
    )

    print(results)
    # format results
    documents = []
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"][0] else {
            }
            distance = results["distances"][0][i] if results["distances"][0] else None

            documents.append({
                "content": doc,
                "source": metadata.get("source", "unknown"),
                "similarity": 1 - distance if distance is not None else None
            })

    return {
        "query": query,
        "num_results": len(documents),
        "documents": documents
    }


def search_by_source(query, source, num_results, collection, embed_func):
    """
    search the knowledge base filtered by document source.

    args:
        query: search query
        source: document source to filter by
        num_results: number of results to return
        collection: chromadb collection
        embed_func: embedding function

    returns:
        dict with search results
    """
    # generate query embedding
    query_embedding = embed_func(query)

    # query chromadb with metadata filter
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(num_results, 10),
        where={"source": source}
    )

    # format results
    documents = []
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"][0] else {
            }
            distance = results["distances"][0][i] if results["distances"][0] else None

            documents.append({
                "content": doc,
                "source": metadata.get("source", "unknown"),
                "similarity": 1 - distance if distance is not None else None
            })

    return {
        "query": query,
        "source": source,
        "num_results": len(documents),
        "documents": documents
    }
