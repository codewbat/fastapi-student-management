from typing import Dict
from repositories.student_repo import StudentRepository
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


class StudentService :
    
    
    def __init__(self , StudentRepo : StudentRepository):
        self.repo = StudentRepo
    
    def get_all_student(self)->Dict:
        student_data = self.repo.get_all_student_data()
        activeStudent ={}
        for student_id , student in student_data.items() :
            if student.get("student_status") == "active":
                activeStudent[student_id] = student
        return activeStudent
    
    def create_student(self, student_data: Dict) -> Dict:
        all_students = self.repo.get_all_student_data()
        for student in all_students.values():
            if student['email'] == student_data['email']:
                raise ValueError(f"Student with email '{student_data['email']}' already exists")
    
        student_data['date_of_birth'] = str(student_data['date_of_birth'])
    
        existing_ids = set(all_students.keys())
        new_id = generate_unique_key(existing_ids, prefix="STD")
        return self.repo.create_student(new_id, student_data)
    
    
    def getStudentByID(self, studentID: str):

        student_data = self.repo.get_student_by_ID(std_id=studentID)

        if not student_data:
            raise HTTPException(
                status_code=404,
                detail=f"Student '{studentID}' not found"
            )

        if student_data.get("student_status") != "active":
            raise HTTPException(
                status_code=400,
                detail=f"Student '{studentID}' is inactive"
            )

        return student_data


    
    def updateStudent (self ,student_id : str  , student_data : Dict) -> Dict:
        student = self.repo.get_all_student_data()
        ex_id = set(student.keys())
        if student_id not in ex_id:
            raise ValueError(f"Student '{student_data['id']}' not found")
        
        existing_student = student[student_id]

        if existing_student.get("student_status") != "active":
            raise HTTPException(
            status_code=400,
            detail=f"Student '{student_id}' is inactive"
            )
        
        student_data["date_of_birth"] = str(student_data["date_of_birth"])
        student_data["student_status"] = "active"
        return self.repo.update_data(std_id=student_id , student_data=student_data)
    
    
    def soft_delete(self , studentID : str)->Dict:
        student = self.repo.get_all_student_data()
        ex_id = set(student.keys())
        if studentID not in ex_id:
            raise ValueError(f"Student '{studentID}' not found")
        
        if student[studentID].get("student_status") != "active":
            raise HTTPException(
            status_code=400,
            detail=f"Student '{studentID}' is already inactive"
            )
        student[studentID]["student_status"] = "inactive"
        return self.repo.soft_delete_student(student_id= studentID ,student_Data=student[studentID])


    
    