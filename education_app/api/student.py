from fastapi import APIRouter, Depends, HTTPException
from education_app.database.models import Student
from education_app.database.schema import StudentInputSchema, StudentOutSchema
from education_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

student_router = APIRouter(prefix='/student', tags=['Student'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@student_router.post('/', response_model=StudentOutSchema)
async def create_student(student: StudentInputSchema,
                         db: Session = Depends(get_db)):
    student_db = Student(**student.dict())
    db.add(student_db)
    db.commit()
    db.refresh(student_db)
    return student_db


@student_router.get('/', response_model=List[StudentOutSchema])
async def list_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@student_router.get('/{student_id}/', response_model=StudentOutSchema)
async def detail_student(student_id: int,
                         db: Session = Depends(get_db)):
    student_db = db.query(Student).filter(Student.id == student_id).first()

    if not student_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай студент жок'
        )

    return student_db


@student_router.put('/{student_id}/', response_model=dict)
async def update_student(student_id: int,
                         student: StudentInputSchema,
                         db: Session = Depends(get_db)):
    student_db = db.query(Student).filter(Student.id == student_id).first()

    if not student_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай студент жок'
        )

    for key, value in student.dict().items():
        setattr(student_db, key, value)

    db.commit()
    db.refresh(student_db)

    return {'message': 'Студент өзгөртүлдү'}


@student_router.delete('/{student_id}/', response_model=dict)
async def delete_student(student_id: int,
                         db: Session = Depends(get_db)):
    student_db = db.query(Student).filter(Student.id == student_id).first()

    if not student_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай студент жок'
        )

    db.delete(student_db)
    db.commit()

    return {'message': 'Студент өчүрүлдү'}