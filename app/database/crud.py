from sqlalchemy.orm import Session
from . import models
import uuid


def create_document(db: Session, filename: str, chunk_count: int) -> models.Document:
    """
    Create a new document record in the database.
    """
    db_document = models.Document(
        doc_id=str(uuid.uuid4()), filename=filename, chunk_count=chunk_count
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document


def get_documents(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all document records.
    """
    return db.query(models.Document).offset(skip).limit(limit).all()


def get_document(db: Session, doc_id: str):
    """
    Retrieve a single document by its doc_id.
    """
    return db.query(models.Document).filter(models.Document.doc_id == doc_id).first()


def delete_document(db: Session, doc_id: str):
    """
    Delete a document record by its doc_id.
    """
    db_document = (
        db.query(models.Document).filter(models.Document.doc_id == doc_id).first()
    )
    if db_document:
        db.delete(db_document)
        db.commit()
        return db_document
    return None
