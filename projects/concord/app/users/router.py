from projects.concord.app.users.schema import (
    UserCreate,
    UserResponse,
    UserCreateResponse,
)
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from projects.concord.app.common.db import get_db
from projects.concord.app.common.utils import hash
from projects.concord.app.common.models import User
from projects.concord.app.common.oath2 import get_current_user_id
from sqlalchemy.exc import SQLAlchemyError

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
def get_user_by_id(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)
):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id={id} does not exist",
        )

    if db_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"this user belongs to: {db_user.email}, you cannot view it.",
        )

    return db_user


# Delete a specific user based on a given ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)
):
    db_query = db.query(User).filter(User.id == id)
    db_user = db_query.first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id={id} does not exist",
        )
    if db_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"this user belongs to: {db_user.email}, you cannot delete it.",
        )

    try:
        db_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from DB : {e}",
        )


# Update the information of a user by ID
@router.put("/{id}", response_model=UserResponse)
def update_user_by_id(
    id: int,
    updated_user: UserCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    db_query = db.query(User).filter(User.id == id)
    db_user = db_query.first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id={id} does not exist",
        )
    if db_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"this user belongs to: {db_user.email}, you cannot delete it.",
        )

    try:
        hashed_password = hash(updated_user.password)
        updated_user.password = hashed_password
        db_query.update(
            updated_user.model_dump(exclude_unset=True),  # type: ignore[arg-type]
            synchronize_session=False,
        )

        db.commit()
        return db_query.first()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from DB : {e}",
        )
