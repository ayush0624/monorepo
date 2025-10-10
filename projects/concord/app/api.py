from fastapi import FastAPI, status, HTTPException, Response
from typing import Dict, List
from random import randrange

from projects.concord.app.models import Project

app = FastAPI()
all_projects = []
def find_idx_by_id(id: int):
    for idx, project in enumerate(all_projects):
        if project["id"] == id:
            return idx
    return -1

# Default ping function to test connectivity
@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping() -> Dict[str, str]:
    return {"message": "pong"}

# Get all of the projects available
@app.get("/projects")
def get_all_projects():
    return {"data": all_projects}

# Get the project based on a given ID
@app.get("/projects/{id}")
def get_project_by_id(id: int):
    idx = find_idx_by_id(id)
    if idx < 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"project with id={id} does not exist"
        )

    return {"data": all_projects[idx]}

# Create a new project
@app.post("/projects", status_code=status.HTTP_201_CREATED)
def create_new_project(new_project: Project):
    project_dict = new_project.model_dump()
    project_dict["id"] = randrange(0, 1000000)
    all_projects.append(project_dict)

    return {"data": project_dict}

# Delete a specific project based on a given ID
@app.delete("/projects/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_by_id(id: int):
    idx = find_idx_by_id(id)
    if idx < 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"project with id={id} does not exist"
        )
    
    all_projects.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update the information of a project by ID
@app.put("/projects/{id}")
def update_project_by_id(
    id: int,
    updated_project: Project
):
    idx = find_idx_by_id(id)
    if idx < 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail=f"project with id={id} does not exist"
        )
    
    project_dict = updated_project.model_dump()
    project_dict["id"] = id
    all_projects[idx] = project_dict

    return {"data": project_dict}
    
