from fastapi import FastAPI, status, HTTPException, Response, Depends
from typing import Dict, List
from random import randrange
from sqlalchemy.orm import Session

from projects.concord.app.common.models import Base
from projects.concord.app.common.db import engine
from projects.concord.app.projects.router import router as projects_router
from projects.concord.app.users.router import router as users_router

app = FastAPI()
app.include_router(projects_router)
app.include_router(users_router)
Base.metadata.create_all(engine)


# Default ping function to test connectivity
@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping() -> Dict[str, str]:
    return {"message": "pong"}
