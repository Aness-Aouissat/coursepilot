from fastapi import APIRouter, Response, Query, Body, Path

from app.models.courses_models import CourseCreate, CourseUpdate, CourseRead, CourseList
from app.dependencies import SessionDep, UserDep
from app.services.courses_services import (
    get_all_courses_service,
    get_course_service,
    create_course_service,
    update_course_service,
    delete_course_service
)

from typing import Annotated
import uuid

router = APIRouter(prefix = "v1/courses")

@router.get("/", response_model=CourseList)
async def get_all_courses(
    session: SessionDep, 
    user: UserDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):
    courses = await get_all_courses_service(user.id, limit, session)
    
    return courses

@router.get("/{course_id}", response_model=CourseRead)
async def get_course(
    session: SessionDep,
    user: UserDep,
    course_id: Annotated[uuid.UUID, Path()]
):
    course = await get_course_service(user.id, course_id, session)
    
    return course

@router.post("/", response_model=CourseRead)
async def create_course(
    session: SessionDep,
    user: UserDep, 
    course_details: Annotated[CourseCreate, Body()]
):
    course = await create_course_service(user.id, course_details, session)
    
    return course

@router.patch("/{course_id}", response_model=CourseRead)
async def update_course(
    session: SessionDep,
    course_id: Annotated[uuid.UUID, Path()],
    user: UserDep,
    course_details: Annotated[CourseUpdate, Body()]
):
    course = await update_course_service(user.id, course_id, course_details, session)
    
    return course

@router.delete("/{course_id}")
async def delete_course(
    session: SessionDep,
    course_id: Annotated[uuid.UUID, Path()],
    user: UserDep
):
    await delete_course_service(user.id, course_id, session)

    return Response(status_code=204)