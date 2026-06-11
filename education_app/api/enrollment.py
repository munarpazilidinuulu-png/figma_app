from fastapi import APIRouter, Depends, HTTPException
from education_app.database.models import Enrollment
from education_app.database.schema import (
    EnrollmentInputSchema,
    EnrollmentOutSchema
)
from education_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

enrollment_router = APIRouter(
    prefix='/enrollment',
    tags=['Enrollment']
)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@enrollment_router.post('/', response_model=EnrollmentOutSchema)
async def create_enrollment(
    enrollment: EnrollmentInputSchema,
    db: Session = Depends(get_db)
):
    enrollment_db = Enrollment(**enrollment.dict())

    db.add(enrollment_db)
    db.commit()
    db.refresh(enrollment_db)

    return enrollment_db


@enrollment_router.get('/', response_model=List[EnrollmentOutSchema])
async def list_enrollments(
    db: Session = Depends(get_db)
):
    return db.query(Enrollment).all()


@enrollment_router.get('/{enrollment_id}/',
                       response_model=EnrollmentOutSchema)
async def detail_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    enrollment_db = (
        db.query(Enrollment)
        .filter(Enrollment.id == enrollment_id)
        .first()
    )

    if not enrollment_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай enrollment жок'
        )

    return enrollment_db


@enrollment_router.put('/{enrollment_id}/',
                       response_model=dict)
async def update_enrollment(
    enrollment_id: int,
    enrollment: EnrollmentInputSchema,
    db: Session = Depends(get_db)
):
    enrollment_db = (
        db.query(Enrollment)
        .filter(Enrollment.id == enrollment_id)
        .first()
    )

    if not enrollment_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай enrollment жок'
        )

    for key, value in enrollment.dict().items():
        setattr(enrollment_db, key, value)

    db.commit()
    db.refresh(enrollment_db)

    return {'message': 'Enrollment өзгөртүлдү'}


@enrollment_router.delete('/{enrollment_id}/',
                          response_model=dict)
async def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    enrollment_db = (
        db.query(Enrollment)
        .filter(Enrollment.id == enrollment_id)
        .first()
    )

    if not enrollment_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай enrollment жок'
        )

    db.delete(enrollment_db)
    db.commit()

    return {'message': 'Enrollment өчүрүлдү'}