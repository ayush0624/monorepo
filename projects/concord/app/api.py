from fastapi import FastAPI, status, HTTPException, Response, Depends
from typing import Dict, List
from random import randrange
from sqlalchemy.orm import Session

from projects.concord.app.models import Base, Project
from projects.concord.app.db import engine, get_db
from projects.concord.app.schema import (
    ProjectCreate,
    ProjectCreateResponse,
    ProjectResponse,
)

app = FastAPI()
Base.metadata.create_all(engine)


# Default ping function to test connectivity
@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping() -> Dict[str, str]:
    return {"message": "pong"}


# Get all of the projects available
@app.get("/projects", response_model=List[ProjectResponse])
def get_all_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects


# Get the project based on a given ID
@app.get("/projects/{id}", response_model=ProjectResponse)
def get_project_by_id(id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"project with id={id} does not exist",
        )

    return db_project


# Create a new project
@app.post(
    "/projects",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectCreateResponse,
)
def create_new_project(new_project: ProjectCreate, db: Session = Depends(get_db)):
    project_entry = Project(**new_project.model_dump())
    db.add(project_entry)
    db.commit()
    db.refresh(project_entry)

    return project_entry


# Delete a specific project based on a given ID
@app.delete("/projects/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_by_id(id: int, db: Session = Depends(get_db)):
    db_query = db.query(Project).filter(Project.id == id)
    db_project = db_query.first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"project with id={id} does not exist",
        )

    db_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update the information of a project by ID
@app.put("/projects/{id}", response_model=ProjectResponse)
def update_project_by_id(
    id: int, updated_project: ProjectCreate, db: Session = Depends(get_db)
):
    db_query = db.query(Project).filter(Project.id == id)
    db_project = db_query.first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"project with id={id} does not exist",
        )

    db_query.update(
        updated_project.model_dump(exclude_unset=True),  # type: ignore[arg-type]
        synchronize_session=False,
    )

    db.commit()
    return db_query.first()
