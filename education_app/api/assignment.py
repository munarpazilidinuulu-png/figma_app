from fastapi import APIRouter, Depends, HTTPException
from education_app.database.models import Assignment
from education_app.database.schema import (
    AssignmentInputSchema,
    AssignmentOutSchema
)
from education_app.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

assignment_router = APIRouter(
    prefix='/assignment',
    tags=['Assignment']
)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@assignment_router.post('/', response_model=AssignmentOutSchema)
async def create_assignment(
    assignment: AssignmentInputSchema,
    db: Session = Depends(get_db)
):
    assignment_db = Assignment(**assignment.dict())

    db.add(assignment_db)
    db.commit()
    db.refresh(assignment_db)

    return assignment_db


@assignment_router.get('/', response_model=List[AssignmentOutSchema])
async def list_assignments(
    db: Session = Depends(get_db)
):
    return db.query(Assignment).all()


@assignment_router.get('/{assignment_id}/',
                       response_model=AssignmentOutSchema)
async def detail_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    assignment_db = (
        db.query(Assignment)
        .filter(Assignment.id == assignment_id)
        .first()
    )

    if not assignment_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай тапшырма жок'
        )

    return assignment_db


@assignment_router.put('/{assignment_id}/',
                       response_model=dict)
async def update_assignment(
    assignment_id: int,
    assignment: AssignmentInputSchema,
    db: Session = Depends(get_db)
):
    assignment_db = (
        db.query(Assignment)
        .filter(Assignment.id == assignment_id)
        .first()
    )

    if not assignment_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай тапшырма жок'
        )

    for key, value in assignment.dict().items():
        setattr(assignment_db, key, value)

    db.commit()
    db.refresh(assignment_db)

    return {'message': 'Тапшырма өзгөртүлдү'}


@assignment_router.delete('/{assignment_id}/',
                          response_model=dict)
async def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    assignment_db = (
        db.query(Assignment)
        .filter(Assignment.id == assignment_id)
        .first()
    )

    if not assignment_db:
        raise HTTPException(
            status_code=404,
            detail='Мындай тапшырма жок'
        )

    db.delete(assignment_db)
    db.commit()

    return {'message': 'Тапшырма өчүрүлдү'}