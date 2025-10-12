from projects.concord.app.projects.schema import (
    ProjectCreate,
    ProjectCreateResponse,
    ProjectResponse,
)
from typing import List
from projects.concord.app.common.models import Project
from projects.concord.app.common.db import get_db
from projects.concord.app.common.oath2 import get_current_user_id
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Define the API routes for projects
router = APIRouter(prefix="/projects", tags=["projects"])


# Get all of the projects available
@router.get("/", response_model=List[ProjectResponse])
def get_all_projects(
    db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)
):
    projects = db.query(Project).filter(Project.owner_id == user_id).all()
    return projects


# Get the project based on a given ID
@router.get("/{id}", response_model=ProjectResponse)
def get_project_by_id(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)
):
    db_project = db.query(Project).filter(Project.id == id).first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"project with id={id} does not exist",
        )
    if db_project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"this project belongs to: {db_project.owner.email}, you cannot view it.",
        )

    return db_project


# Create a new project
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectCreateResponse,
)
def create_new_project(
    new_project: ProjectCreate,
    db: Session = Depends(get_db),
    owner_id: int = Depends(get_current_user_id),
):
    project_entry = Project(**new_project.model_dump())
    project_entry.owner_id = owner_id
    try:
        db.add(project_entry)
        db.commit()
        db.refresh(project_entry)
        return project_entry
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from DB : {e}",
        )


# Delete a specific project based on a given ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_by_id(
    id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)
):
    db_query = db.query(Project).filter(Project.id == id)
    db_project = db_query.first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"project with id={id} does not exist",
        )
    if db_project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"this project belongs to: {db_project.owner.email}, you cannot delete it.",
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


# Update the information of a project by ID
@router.put("/{id}", response_model=ProjectResponse)
def update_project_by_id(
    id: int,
    updated_project: ProjectCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    db_query = db.query(Project).filter(Project.id == id)
    db_project = db_query.first()
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"project with id={id} does not exist",
        )
    if db_project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"this project belongs to: {db_project.owner.email}, you cannot delete it.",
        )

    try:
        db_query.update(
            updated_project.model_dump(exclude_unset=True),  # type: ignore[arg-type]
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
