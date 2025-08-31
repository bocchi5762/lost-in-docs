from pinecone import Pinecone
import os

api_key = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=api_key)

index = pc.Index(
    name="lost-in-docs",
    host="https://lost-in-docs-1wsfn2s.svc.aped-4627-b74a.pinecone.io",
)
