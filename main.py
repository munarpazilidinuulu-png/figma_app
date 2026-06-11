from fastapi import FastAPI
import uvicorn

from education_app.api import (
    student,
    Instructor,
    course,
    enrollment,
    assignment
)

education_app = FastAPI(title='Education App')

education_app.include_router(student.student_router)
education_app.include_router(Instructor.instructor_router)
education_app.include_router(course.course_router)
education_app.include_router(enrollment.enrollment_router)
education_app.include_router(assignment.assignment_router)





if __name__ == '__main__':
    uvicorn.run(education_app, host='127.0.0.1', port=8001)