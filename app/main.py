from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="lost-in-docs",
    description="A FastAPI project - lost-in-docs",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"Project": "lost-in-docs", "description": "A FastAPI project - lost-in-docs"}


app.include_router(router)
