from config.pinecone_config import index


def retrieve_relevant_docs(
    query_text: str, top_k: int = 5, namespace: str = "__default__"
):
    return index.search(
        namespace=namespace,
        query={"inputs": {"text": query_text}, "top_k": top_k},
        fields=["chunk_text", "doc_id", "filename"],
    )
