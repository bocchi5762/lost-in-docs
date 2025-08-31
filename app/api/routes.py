from fastapi import APIRouter, UploadFile, File, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from core.parser import parse_pdf
from core.generate import generate_with_rag
from config.pinecone_config import index
from database import crud
from database.config import get_db


router = APIRouter(prefix="")


# Health check endpoint
@router.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}


# Upload document endpoint
@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Create a record in the database first to get a doc_id
    db_doc = crud.create_document(db, filename=file.filename, chunk_count=0)
    doc_id = db_doc.doc_id

    # 2. Read file content
    content = await file.read()
    # 3. Parse and split into chunks
    chunks = parse_pdf(content)

    # 4. Prepare records for Pinecone upsert
    records = []
    for i, chunk in enumerate(chunks):
        chunk_id = f"{doc_id}_{i}"
        if isinstance(chunk, dict) and "content" in chunk:
            chunk_text = chunk["content"]
        elif hasattr(chunk, "page_content"):
            chunk_text = chunk.page_content
        else:
            chunk_text = str(chunk)
        records.append(
            {
                "id": chunk_id,
                "chunk_text": chunk_text,
                "doc_id": doc_id,
                "filename": file.filename,
            }
        )
    # 5. Upsert records to Pinecone
    if records:
        index.upsert_records(records=records, namespace="__default__")
        # Update the chunk count in the database
        db_doc.chunk_count = len(chunks)
        db.commit()

    return {"filename": file.filename, "chunks": len(chunks), "doc_id": doc_id}


# Query endpoint
@router.post("/query")
async def query_rag(query: str = Body(..., embed=True)):
    answer = generate_with_rag(query)
    return {"query": query, "answer": answer}


# List documents endpoint
@router.get("/documents")
async def list_documents(db: Session = Depends(get_db)):
    documents = crud.get_documents(db)
    return {"documents": documents}


# Delete document endpoint
@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str, db: Session = Depends(get_db)):
    # 1. Check if document exists in DB
    db_document = crud.get_document(db, doc_id=doc_id)
    if not db_document:
        raise HTTPException(status_code=404, detail="Document not found")

    # 2. Delete vectors from Pinecone
    await index.delete(filter={"doc_id": doc_id}, namespace="__default__")

    # 3. Delete the document record from the database
    crud.delete_document(db, doc_id=doc_id)

    return {
        "status": "success",
        "message": f"Document {doc_id} and its vectors have been deleted.",
    }
