from config.pinecone_config import index


async def retrieve_relevant_docs(
    query_text: str, top_k: int = 5, namespace: str = "__default__"
):
    return await index.search(
        namespace=namespace,
        query={"inputs": {"text": query_text}, "top_k": top_k},
        fields=["chunk_text", "doc_id", "filename"],
    )
