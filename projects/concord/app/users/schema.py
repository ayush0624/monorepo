from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class Base(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(Base):
    password: str


class UserResponse(Base):
    model_config = ConfigDict(
        from_attributes=True,  # replaces orm_mode=True
        extra="ignore",
    )


class UserCreateResponse(UserResponse):
    id: int
    created_at: datetime


class UserJWTPayload(BaseModel):
    id: int


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
