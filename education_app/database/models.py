from education_app.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, Text, Boolean
from enum import Enum as PyEnum
from typing import Optional, List
from datetime import date


class LevelChoices(str, PyEnum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class EnrollmentStatus(str, PyEnum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String, unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, unique=True)
    date_registered: Mapped[date] = mapped_column(Date, default=date.today)

    enrollments: Mapped[List['Enrollment']] = relationship(
        back_populates='student',
        cascade='all, delete-orphan'
    )


class Instructor(Base):
    __tablename__ = 'instructors'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    specialization: Mapped[str] = mapped_column(String(100))
    experience_level: Mapped[LevelChoices] = mapped_column(Enum(LevelChoices))

    courses: Mapped[List['Course']] = relationship(
        back_populates='instructor',
        cascade='all, delete-orphan'
    )


class Course(Base):
    __tablename__ = 'courses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    instructor_id: Mapped[int] = mapped_column(ForeignKey('instructors.id'))
    instructor: Mapped[Instructor] = relationship(
        back_populates='courses'
    )

    enrollments: Mapped[List['Enrollment']] = relationship(
        back_populates='course',
        cascade='all, delete-orphan'
    )


class Assignment(Base):
    __tablename__ = 'assignments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    due_date: Mapped[date] = mapped_column(Date)

    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))

    course: Mapped[Course] = relationship()


class Enrollment(Base):
    __tablename__ = 'enrollments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    enrollment_date: Mapped[date] = mapped_column(Date, default=date.today)
    status: Mapped[EnrollmentStatus] = mapped_column(
        Enum(EnrollmentStatus),
        default=EnrollmentStatus.active
    )

    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    student: Mapped[Student] = relationship(
        back_populates='enrollments'
    )

    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    course: Mapped[Course] = relationship(
        back_populates='enrollments'
    )