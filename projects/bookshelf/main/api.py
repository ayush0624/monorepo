from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from typing import Dict
from projects.bookshelf.main.books import router as books_router
from projects.bookshelf.main.errors import EntityDoesNotExistError
from projects.bookshelf.main.db import init_db

app = FastAPI()
app.include_router(books_router)

@app.on_event("startup")
def on_startup():
    init_db()

@app.exception_handler(EntityDoesNotExistError)
async def entity_not_found_handler(_: Request, exc: EntityDoesNotExistError) -> JSONResponse:
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {
            "error": "EntityDoesNotExistError",
            "message": exc.message
        },
    )

@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping() -> Dict[str, str]:
    return {"message": "pong"}
