from fastapi import APIRouter, Path, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, Sequence
from projects.bookshelf.main.db import get_db, Bookshelf

# Define Pydantic Data Models for Books
class Create(BaseModel):
    name: str
    author: str

class Update(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None

class Response(BaseModel):
    id: int
    name: str
    author: str

    class Config:
        orm_mode = True

# Define the API routes for books
router = APIRouter(prefix="/books", tags = ["books"])

# GET endpoint for retreiving all books
@router.get("/", response_model=Sequence[Response])
def get_all_books(
    db: Session = Depends(get_db)
) -> Sequence[Response]:
    books = db.query(Bookshelf).all()
    return books

# GET endpoint for retrieving a book by ID
@router.get("/{id}", response_model=Response)
def get_book_by_id(
    id: int = Path(description="the UUID for a respective book"),
    db: Session = Depends(get_db)
) -> Response:
    book = db.query(Bookshelf).filter(Bookshelf.id == id).first()
    if not book:
        # TODO: handle errors better here
        raise
    return book

# POST endpoint for creating a new book
@router.post("/", response_model=Response)
def create_new_book(
    input_book: Create,
    db: Session = Depends(get_db)
) -> Response:
    new_book = Bookshelf(**input_book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

# PUT endpoint for updating the information for an existing book
@router.put("/{id}", response_model=Response)
def update_existing_book(
    input_book: Update,
    id: int = Path(description="the UUID of the book to update"),
    db: Session = Depends(get_db)
) -> Response:
    existing_book = db.query(Bookshelf).filter(Bookshelf.id == id).first()
    if not existing_book:
        # TODO : handle errors better here
        raise

    if input_book.name:
        existing_book.name = input_book.name
    if input_book.author:
        existing_book.author = input_book.author
    
    db.commit()
    db.refresh(existing_book)

    return existing_book

# DELETE endpoint for deleting an existing book
@router.delete("/{id}", response_model=Response)
def delete_existing_book(
    id: int = Path(description="the UUID of the book to delete"),
    db: Session = Depends(get_db)
) -> Response:
    existing_book = db.query(Bookshelf).filter(Bookshelf.id == id).first()
    if not existing_book:
        # TODO : handle errors better here
        raise

    db.delete(existing_book)
    db.commit()
    return existing_book
