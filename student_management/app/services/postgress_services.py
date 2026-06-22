from typing import Dict , List
from repositories.student_pg_repo import PostgressStudentRepository
from fastapi import HTTPException

def generate_unique_key(
    existing_ids : set , prefix : str = "STD"
) -> str:
    counter = 1
    while True:
        new_id = f"{prefix}{counter:03d}"
        if new_id not in existing_ids:
            return new_id
        counter += 1

class PostgressStudentService :
    def __init__(self , StudentRepo : PostgressStudentRepository = None):
        self.studentrepo = StudentRepo or PostgressStudentRepository()
        
        
   
    def get_all_student(self) -> List[Dict]:
        return self.studentrepo.get_all_student()
    
    def create_student(self , student_data : Dict)->Dict:
        if self.studentrepo.email_exists(student_data.get('email', '')):
            raise HTTPException(
                status_code=400,
                detail=f"Student with email '{student_data['email']}' already exists"
            )
        if 'bloodGroup' in student_data:
            student_data['blood_group'] = student_data.pop('bloodGroup')  # ✅ Convert

        if 'date_of_birth' in student_data:
            student_data['date_of_birth'] = str(student_data['date_of_birth'])
        
        student_data['status'] = 'active'
        
        
        existing_id = self.studentrepo.get_all_ids()
        
        new_id = generate_unique_key(existing_ids= existing_id , prefix="STD")
        student_data['student_id'] = new_id
        
        return self.studentrepo.create_student(studentId=new_id,StudentData=student_data)
    
    
    def updateStudent(self , student_id : str , student_data : Dict)-> Dict:
        exisiting_id = self.studentrepo.get_all_ids()
        if student_id not in exisiting_id :
            raise HTTPException(
                status_code=404,
                detail=f"Student '{student_id}' not found"
            )
        existing_student = self.studentrepo.get_student_by_ID(std_id=student_id)
        if existing_student.get("status") != "active":
            raise HTTPException(
            status_code=400,
            detail=f"Student '{student_id}' is inactive"
            )
        if 'date_of_birth' in student_data:
            student_data['date_of_birth'] = str(student_data['date_of_birth'])
    
        if 'bloodGroup' in student_data:
            student_data['blood_group'] = student_data.pop('bloodGroup')
    
        student_data.pop('student_status', None)
        student_data.pop('id', None)

        return self.studentrepo.update_student(
            studentId=student_id,
            StudentData= student_data
        )

 