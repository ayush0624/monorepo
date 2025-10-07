from fastapi import FastAPI, Path, Request, status
from typing import Optional, Any, Dict
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from projects.bookshelf.tutorial.errors import EntityDoesNotExistError, EntityAlreadyExistsError

app = FastAPI()

@app.exception_handler(EntityDoesNotExistError)
async def entity_not_found_handler(_: Request, exc: EntityDoesNotExistError) -> JSONResponse:
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {
            "error": "EntityDoesNotExistError",
            "message": exc.message
        },
    )

@app.exception_handler(EntityAlreadyExistsError)
async def entity_already_exists_handler(_: Request, exc: EntityAlreadyExistsError) -> JSONResponse:
    return JSONResponse(
        status_code = status.HTTP_409_CONFLICT,
        content = {
            "error": "EntityAlreadyExistsError",
            "message": exc.message
        },
    )


students: Dict[int, Any] = {
    0: {
        "name": "john",
        "age": 17,
        "year": "year 12"
    },
    1: {
        "name": "bob",
        "age": 12,
        "year": "year 10"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping() -> Dict[str, str]:
    return {"message": "pong"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(
    description="The id of the student to view",
    ge = 0,
)) -> JSONResponse:
    if student_id not in students:
        raise EntityDoesNotExistError(message = "Could Not Find Student ID")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content = students[student_id]
    )


@app.get("/get-by-name")
def get_student_name(name: Optional[str] = None) -> JSONResponse:
    for _, data in students.items():
        if data["name"] == name:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content = data
            )
    raise EntityDoesNotExistError(message = "Could Not Find Student with Name")

@app.post("/new-student/{student_id}")
def new_student(student_id: int, student: Student) -> JSONResponse:
    if student_id in students:
        raise EntityAlreadyExistsError("Found another Student with Same ID")

    students[student_id] = student.model_dump()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content = students[student_id]
    )

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent) -> JSONResponse:
    if student_id not in students:
        raise EntityDoesNotExistError(message = "Could Not Find Student ID")
    
    student_data = students[student_id]
    new_student_data = student.model_dump()
    for field, value in new_student_data.items():
        if value is not None:
            student_data[field] = value
    
    students[student_id] = student_data
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content = students[student_id]
    )
    
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int) -> JSONResponse:
    if student_id not in students:
        raise EntityDoesNotExistError(message = "Could Not Find Student ID")

    del students[student_id]
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content = {
            "message": "successfully deleted student"
        }
    )
