from fastapi import APIRouter, UploadFile, File, Body
from typing import List
from core.parser import parse_pdf
from config.pinecone_config import index
from config.gemini_config import gemini_client
import uuid


router = APIRouter(prefix="")


# Health check endpoint
@router.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}


# Upload document endpoint
@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    # 1. Read file content
    content = await file.read()
    # 2. Parse and split into chunks
    chunks = parse_pdf(content)

    # 3. Prepare records for Pinecone upsert
    doc_id = str(uuid.uuid4())

    records = []
    for i, chunk in enumerate(chunks):
        chunk_id = f"{doc_id}_{i}"
        # Extract the actual text content from the chunk
        if isinstance(chunk, dict) and "content" in chunk:
            chunk_text = chunk["content"]
        elif hasattr(chunk, "page_content"):
            chunk_text = chunk.page_content
        else:
            chunk_text = str(chunk)
        records.append(
            {
                "_id": chunk_id,
                "chunk_text": chunk_text,
                "doc_id": doc_id,  # stored as metadata
                "filename": file.filename,  # add filename as metadata
            }
        )
    # 4. Upsert records to Pinecone (using default namespace)
    if records:
        index.upsert_records("__default__", records)
    return {"filename": file.filename, "chunks": len(chunks), "doc_id": doc_id}


# Query endpoint
@router.post("/query")
async def query_rag(query: str = Body(..., embed=True)):
    # TODO: Retrieve relevant context and generate answer
    return {"query": query, "answer": "This is a placeholder answer."}


# List documents endpoint
@router.get("/documents")
async def list_documents():
    # TODO: Return list of documents
    return {"documents": []}


# Delete document endpoint
@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    # TODO: Remove document and its vectors
    return
