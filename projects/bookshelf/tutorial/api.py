from fastapi import FastAPI, Path
from typing import Optional, Any, Dict
from pydantic import BaseModel

app = FastAPI()

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

@app.get("/")
def index():
    return {"name": "First Data"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(
    description="The id of the student to view",
    ge = 0,
)) -> Dict[str, Any]:
    return students[student_id]


@app.get("/get-by-name")
def get_student_name(name: Optional[str] = None) -> Dict[str, Any]:
    for _, data in students.items():
        if data["name"] == name:
            return data
    
    return {"Data": "Not Found"}

@app.post("/new-student/{student_id}")
def new_student(student_id: int, student: Student) -> Dict[str, Any]:
    if student_id in students:
        return {"Error": "Student Already Exists"}

    students[student_id] = student.model_dump()
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent) -> Dict[str, Any]:
    if student_id not in students:
        return {"Error": "Student Does Not Exist"}
    
    student_data = students[student_id]
    new_student_data = student.model_dump()
    for field, value in new_student_data.items():
        if value is not None:
            student_data[field] = value
    
    students[student_id] = student_data
    return students[student_id]
    
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int) -> Dict[str, Any]:
    if student_id not in students:
        return {"Error": "Student Does Not Exist"}

    del students[student_id]
    return {"Message": "Student Successfully Deleted"}
