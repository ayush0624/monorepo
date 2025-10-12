from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Dict
from projects.concord.app.common.models import User
from projects.concord.app.common.db import get_db
from projects.concord.app.common.utils import verify
from projects.concord.app.common.oath2 import (
    JWTPayload,
    JWTResponse,
    create_access_token,
)
from projects.concord.app.projects.router import router as projects_router
from projects.concord.app.users.router import router as users_router
from sqlalchemy.orm import Session

app = FastAPI()
app.include_router(projects_router)
app.include_router(users_router)


# Default ping function to test connectivity
@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping() -> Dict[str, str]:
    return {"message": "pong"}


@app.post("/login", response_model=JWTResponse)
def login(
    attempted_login: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.email == attempted_login.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials",
        )

    if not verify(attempted_login.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials",
        )

    payload = JWTPayload(user_id=db_user.id)
    access_token = create_access_token(data=payload.model_dump())

    return JWTResponse(access_token=access_token)
