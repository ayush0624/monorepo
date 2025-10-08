from fastapi import FastAPI, status
from typing import Dict
from projects.bookshelf.main.books import router as books_router

app = FastAPI()
app.include_router(books_router)

@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping() -> Dict[str, str]:
    return {"message": "pong"}
