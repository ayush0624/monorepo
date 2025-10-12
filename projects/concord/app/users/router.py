from projects.concord.app.users.schema import (
    UserCreate,
    UserResponse,
    UserCreateResponse,
)
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from projects.concord.app.common.db import get_db
from projects.concord.app.common.utils import hash
from projects.concord.app.users.models import User

# Define the API routes for users
router = APIRouter(prefix="/users", tags=["users"])


# Create a new user
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreateResponse,
)
def create_new_user(new_user: UserCreate, db: Session = Depends(get_db)):
    # Hash the password using passlib
    hashed_password = hash(new_user.password)
    new_user.password = hashed_password

    user_entry = User(**new_user.model_dump())
    db.add(user_entry)
    db.commit()
    db.refresh(user_entry)

    return user_entry


# Get a specific user by ID
@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id={id} does not exist",
        )

    return db_user
