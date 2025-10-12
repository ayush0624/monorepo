from jose import jwt
from typing import Dict
from datetime import datetime, timedelta, timezone

SECRET_KEY = "e5022c455d31efcf1d834409726e916fb6772547014e1216b9141033d488d34f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: Dict):
    to_encode = data.copy()
    expires_in = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration_time = datetime.now(timezone.utc) + expires_in
    to_encode.update({"exp": expiration_time})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token
