from fastapi import Depends, FastAPI, Path, Request, status
from typing import Optional, Dict
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from projects.bookshelf.tutorial.errors import (
    EntityDoesNotExistError,
    EntityAlreadyExistsError,
)
from projects.bookshelf.tutorial.db import get_db, Student

app = FastAPI()


@app.exception_handler(EntityDoesNotExistError)
async def entity_not_found_handler(
    _: Request, exc: EntityDoesNotExistError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "EntityDoesNotExistError", "message": exc.message},
    )


@app.exception_handler(EntityAlreadyExistsError)
async def entity_already_exists_handler(
    _: Request, exc: EntityAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": "EntityAlreadyExistsError", "message": exc.message},
    )


class StudentCreate(BaseModel):
    name: str
    age: int
    year: str


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    year: str


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping() -> Dict[str, str]:
    return {"message": "pong"}


@app.get("/get-student/{id}", response_model=StudentResponse)
def get_student(
    id: int = Path(description="The id of the student to view"),
    db: Session = Depends(get_db),
) -> StudentResponse:
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise EntityDoesNotExistError(message="Could Not Find Student ID")
    return student


@app.post("/new-student/", response_model=StudentResponse)
def new_student(
    student: StudentCreate, db: Session = Depends(get_db)
) -> StudentResponse:
    if db.query(Student).filter(Student.name == student.name).first():
        raise EntityAlreadyExistsError("Found another Student with Same Name")

    new_student = Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@app.get("/get-by-name", response_model=StudentResponse)
def get_student_name(
    name: Optional[str] = None, db: Session = Depends(get_db)
) -> StudentResponse:
    student = db.query(Student).filter(Student.name == name).first()
    if not student:
        raise EntityDoesNotExistError(message="Could Not Find Student with Name")
    return student


@app.put("/update-student/{id}", response_model=StudentResponse)
def update_student(
    id: int, student: StudentUpdate, db: Session = Depends(get_db)
) -> StudentResponse:
    db_student = db.query(Student).filter(Student.id == id).first()
    if not db_student:
        raise EntityDoesNotExistError(message="Could Not Find Student ID")

    new_student_data = student.model_dump()
    for field, value in new_student_data.items():
        if value is not None:
            setattr(db_student, field, value)

    db.commit()
    db.refresh(db_student)
    return db_student


@app.delete("/delete-student/{id}", response_model=StudentResponse)
def delete_student(id: int, db: Session = Depends(get_db)) -> StudentResponse:
    db_student = db.query(Student).filter(Student.id == id).first()
    if not db_student:
        raise EntityDoesNotExistError(message="Could Not Find Student ID")

    db.delete(db_student)
    db.commit()
    return db_student
