from typing import Dict , List , Optional
from sqlalchemy.orm import Session
from model.db_model import StudentTable
from core.postgressDatabase import SessionLocal
from fastapi import HTTPException
class PostgressStudentRepository:
    
    def __init__(self , postgressDB : Session =None):
        self.postgressDB = postgressDB or SessionLocal()
    
    def get_all_student(self) -> Dict:
        students = self.postgressDB.query(StudentTable).filter(
            StudentTable.status == "active"
        ).all()
        
        return [student.to_dict() for student in students]
    
    def email_exists(self, email: str) -> bool:
        student = self.postgressDB.query(StudentTable).filter(
            StudentTable.email == email
        ).first()
        return student is not None

    def get_all_ids(self) -> set:
        students = self.postgressDB.query(StudentTable.student_id).all()
        return {s[0] for s in students}
    
    def get_student_by_ID(self, std_id: str) -> Optional[Dict]:
        student = self.postgressDB.query(StudentTable).filter(
            StudentTable.student_id == std_id
        ).first()
        if student:
            return student.to_dict()
        return None

    def create_student(self , studentId : str , StudentData : Dict)->Dict:
        StudentData.pop('student_status', None)
        
        StudentData.pop('id', None)
        
        if 'address' in StudentData :
            address = StudentData.pop('address')
            StudentData['house_no'] = address.get('pt_no')
            StudentData['city'] = address.get('city')
            StudentData['state'] = address.get('state')
            StudentData['country'] = address.get('country')
        
        db_student = StudentTable(**StudentData)
        self.postgressDB.add(db_student)
        self.postgressDB.commit()
        self.postgressDB.refresh(db_student)
        return db_student.to_dict()
    
    def update_student(self,studentId : str , StudentData : Dict )->Dict:
        
        StudentData.pop('student_status', None)
        
        StudentData.pop('id', None)
        if 'bloodGroup' in StudentData:
            StudentData['blood_group'] = StudentData.pop('bloodGroup')
       
        if 'address' in StudentData :
            address = StudentData.pop('address')
            StudentData['house_no'] = address.get('pt_no')
            StudentData['city'] = address.get('city')
            StudentData['state'] = address.get('state')
            StudentData['country'] = address.get('country')
            
        student = self.postgressDB.query(StudentTable).filter(
            StudentTable.student_id == studentId
        ).first()
        
        if not student : 
            return HTTPException(
                status_code=404,
                detail="Student not found in database"
            )
        for key , value in StudentData.items():
            if hasattr(student,key) : setattr(student,key,value)
            
        self.postgressDB.commit()
        self.postgressDB.refresh(student)
        return student.to_dict()
        
        
    