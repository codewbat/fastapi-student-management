from fastapi import APIRouter ,Depends ,Query
from fastapi.responses import JSONResponse
from model.student_models import Create_Student , Update_Student
from services.StudentService import StudentService
from repositories.student_repo import StudentRepository
from typing import Optional, Annotated
from services.postgress_services import PostgressStudentService
from repositories.student_pg_repo import PostgressStudentRepository
student_routes = APIRouter(prefix="/student",tags=["Student"])

def get_productservice()->StudentService:
    repo = StudentRepository()
    return StudentService(repo)

@student_routes.get('/getstudent')
def get_all_student(
    service : StudentService = Depends(get_productservice),
):
    student_data = service.get_all_student()
    
    students = []
    for keys , values in student_data.items():
        students.append({
            "id":keys,
            **values
        })
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "Here Your Product",
            "data": students,
        },
    )

@student_routes.post('/create_student')
def create_student(
    service : StudentService = Depends(get_productservice),
    item : Create_Student = Depends()
):
    
    new_student = item.model_dump()
    service.create_student(new_student)
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "message": "Student add successfully",
            "data": new_student,
        },
    )
    
    
@student_routes.get('/getstudentByID/{stdID}')
def get_student_byID(
    stdID : str,
    service : StudentService = Depends(get_productservice),
):
    student = service.getStudentByID(studentID=stdID)
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "Here Your Product",
            "data": student,
        },
    )
    
@student_routes.put('/update_student/{stdId}')
def update_student(
    stdID : str,
    updateStudent : Update_Student,
    service : StudentService = Depends(get_productservice),
):
    student_data = updateStudent.model_dump()
    service.updateStudent(student_id=stdID,student_data=student_data)
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "Here Your Product",
            "data": student_data,
        },
    )

@student_routes.delete('/delete_student/{stdId}')
def delete_student(
    stdId : str,
    service : StudentService = Depends(get_productservice)
):
    service.soft_delete(studentID=stdId)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Student '{student_id}' deleted"
        }
    )
    
def get_postgress_student_service() -> PostgressStudentService:
    postgress_repo = PostgressStudentRepository()
    return PostgressStudentService(postgress_repo)
  
@student_routes.get('/postgress_get_allstudent')
def get_postgress_student(
    service : PostgressStudentService = Depends(get_postgress_student_service)
):
    
    students = service.get_all_student()
    
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "data": students
        }
    )

@student_routes.post('/postgress_create_student')
def postgress_create_student(
    std_item :Create_Student,
    service : PostgressStudentService = Depends(get_postgress_student_service)
):
    student_data = std_item.model_dump()
    service.create_student(student_data=student_data)
    
    
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "message": "Student add successfully",
            "data": student_data,
        },
    )

@student_routes.patch('/postgress_update-students/{std_id}')
def postgress_update_student(
    std_id : str,
    updated_data : Update_Student,
    service : PostgressStudentService = Depends(get_postgress_student_service)
):
    student_data = updated_data.model_dump()
    service.updateStudent(student_id=std_id,student_data=student_data)
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "Here Your Product",
            "data": student_data,
        },
    )
    
@student_routes.put('/postgressput_update_student/{std_id}')
def put_postgress_update_student(
    std_id : str,
    updated_data : Update_Student,
    service : PostgressStudentService = Depends(get_postgress_student_service)
):
    student_data = updated_data.model_dump()
    service.updateStudent(student_id=std_id,student_data=student_data)
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "Here Your Product",
            "data": student_data,
        },
    )

    