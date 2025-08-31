from config.pinecone_config import index
from typing import List, Optional


def retrieve_relevant_docs(
    query_text: str,
    doc_ids: Optional[List[str]] = None,
    top_k: int = 5,
    namespace: str = "__default__",
):
    """
    Retrieves relevant document chunks from Pinecone, with an optional filter for specific doc_ids.
    """
    # The query dictionary will hold all search parameters
    search_query = {
        "inputs": {"text": query_text},
        "top_k": top_k,
    }

    # If doc_ids are provided, add the filter to the query dictionary
    if doc_ids:
        search_query["filter"] = {"doc_id": {"$in": doc_ids}}

    return index.search(
        namespace=namespace,
        query=search_query,
        fields=["chunk_text", "doc_id", "filename"],
    )
