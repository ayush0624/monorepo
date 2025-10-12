from jose import jwt, JWTError
from typing import Dict
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, ValidationError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from projects.concord.app.common.config import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oath2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class JWTPayload(BaseModel):
    user_id: int


class JWTToken(JWTPayload):
    exp: datetime


class JWTResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def create_access_token(data: Dict):
    to_encode = data.copy()
    expires_in = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration_time = datetime.now(timezone.utc) + expires_in
    to_encode.update({"exp": expiration_time})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


class CredentialsException(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(token: str = Depends(oath2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jwt_token = JWTToken(**payload)
    except JWTError as e:
        raise CredentialsException(f"Invalid JWT Token: {e}")
    except ValidationError as e:
        raise CredentialsException(f"Malformed Token Payload: {e}")

    return jwt_token.user_id
