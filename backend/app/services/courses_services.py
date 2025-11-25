from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.courses_db import Courses
from app.models.courses_models import CourseCreate, CourseUpdate

import uuid

async def get_all_courses_service(
    user_id: uuid.UUID,
    limit: int,
    session: AsyncSession
):
    result = await session.execute(select(Courses).order_by(Courses.created_at).limit(limit).where(Courses.user_id == user_id))
    courses = result.scalars().all() 

    return courses

async def get_course_service(
    user_id: uuid.UUID,
    course_id: uuid.UUID,
    session: AsyncSession
):
    course = await session.get(Courses, course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if user_id != course.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized user")
    
    return course

async def create_course_service(
    user_id: uuid.UUID,
    course_details: CourseCreate,
    session: AsyncSession
):
    course = Courses(user_id=user_id, title=course_details.title, description=course_details.description)

    session.add(course)
    await session.commit()
    await session.refresh(course)

    return course

async def update_course_service(
    user_id: uuid.UUID,
    course_id: uuid.UUID, 
    course_details: CourseUpdate,
    session: AsyncSession
):
    course = await session.get(Courses, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if user_id != course.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized user")

    course_dict = course_details.model_dump(exclude_unset=True)

    protected = {"id", "created_at", "updated_at"}
    [setattr(course, key, value) for key, value in course_dict.items() if key not in protected]

    await session.commit()
    await session.refresh(course)

    return course

async def delete_course_service(
    user_id: uuid.UUID, 
    course_id: uuid.UUID,
    session: AsyncSession
):
    course = await session.get(Courses, course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if user_id != course.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized user")
    
    await session.delete(course)
    await session.commit()