from config.gemini_config import gemini_client
from core.retrieve import retrieve_relevant_docs


async def generate_with_rag(query: str, top_k: int = 5):
    """
    Generates an answer using RAG by retrieving documents and then calling the LLM.
    """
    # 1. Retrieve relevant documents from Pinecone
    search_results = await retrieve_relevant_docs(query_text=query, top_k=top_k)

    # 2. Extract text from results to build the context
    hits = search_results.get("result", {}).get("hits", [])
    context_chunks = [
        hit.get("fields", {}).get("chunk_text", "") for hit in hits if hit
    ]
    context = "\n\n---\n\n".join(context_chunks)

    # Handle cases where no context is found
    if not context.strip():
        return "I could not find any relevant information in the documents to answer your question."

    # 3. Create a detailed prompt for the LLM
    prompt = f"""
    You are an expert assistant. Your task is to answer the user's question based exclusively on the provided context.
    Do not use any external knowledge. If the answer is not found within the context, state that clearly.

    Provided Context:
    ---
    {context}
    ---

    User's Question: {query}

    Answer:
    """

    # 4. Generate the answer using the LLM
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
