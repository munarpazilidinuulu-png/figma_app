from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

from .models import LevelChoices, EnrollmentStatus



class StudentInputSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None


class StudentOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str]
    date_registered: date

    class Config:
        from_attributes = True



class InstructorInputSchema(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    experience_level: LevelChoices


class InstructorOutSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    specialization: str
    experience_level: LevelChoices

    class Config:
        from_attributes = True


class CourseInputSchema(BaseModel):
    title: str
    description: str
    price: int
    is_available: bool = True
    instructor_id: int


class CourseOutSchema(BaseModel):
    id: int
    title: str
    description: str
    price: int
    is_available: bool
    instructor_id: int

    class Config:
        from_attributes = True



class AssignmentInputSchema(BaseModel):
    title: str
    description: str
    due_date: date
    course_id: int


class AssignmentOutSchema(BaseModel):
    id: int
    title: str
    description: str
    due_date: date
    course_id: int

    class Config:
        from_attributes = True



class EnrollmentInputSchema(BaseModel):
    student_id: int
    course_id: int
    status: EnrollmentStatus = EnrollmentStatus.active


class EnrollmentOutSchema(BaseModel):
    id: int
    enrollment_date: date
    status: EnrollmentStatus
    student_id: int
    course_id: int

    class Config:
        from_attributes = True