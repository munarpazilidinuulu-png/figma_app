from fastapi import APIRouter, Depends, HTTPException
from education_app.database.models import Instructor
from education_app.database.schema import (
    InstructorInputSchema,
    InstructorOutSchema
)
from education_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

instructor_router = APIRouter(
    prefix='/instructor',
    tags=['Instructor']
)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@instructor_router.post('/', response_model=InstructorOutSchema)
async def create_instructor(
        instructor: InstructorInputSchema,
        db: Session = Depends(get_db)
):
    instructor_db = Instructor(**instructor.dict())

    db.add(instructor_db)
    db.commit()
    db.refresh(instructor_db)

    return instructor_db


@instructor_router.get('/', response_model=List[InstructorOutSchema])
async def list_instructors(
        db: Session = Depends(get_db)
):
    return db.query(Instructor).all()


@instructor_router.get('/{instructor_id}/',
                       response_model=InstructorOutSchema)
async def detail_instructor(
        instructor_id: int,
        db: Session = Depends(get_db)
):
    instructor_db = db.query(Instructor).filter(
        Instructor.id == instructor_id
    ).first()

    if not instructor_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай инструктор жок'
        )

    return instructor_db


@instructor_router.put('/{instructor_id}/',
                       response_model=dict)
async def update_instructor(
        instructor_id: int,
        instructor: InstructorInputSchema,
        db: Session = Depends(get_db)
):
    instructor_db = db.query(Instructor).filter(
        Instructor.id == instructor_id
    ).first()

    if not instructor_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай инструктор жок'
        )

    for key, value in instructor.dict().items():
        setattr(instructor_db, key, value)

    db.commit()
    db.refresh(instructor_db)

    return {'message': 'Инструктор өзгөртүлдү'}


@instructor_router.delete('/{instructor_id}/',
                          response_model=dict)
async def delete_instructor(
        instructor_id: int,
        db: Session = Depends(get_db)
):
    instructor_db = db.query(Instructor).filter(
        Instructor.id == instructor_id
    ).first()

    if not instructor_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай инструктор жок'
        )

    db.delete(instructor_db)
    db.commit()

    return {'message': 'Инструктор өчүрүлдү'}