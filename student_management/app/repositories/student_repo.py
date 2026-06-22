from typing import Dict
from core.database import studentDB

class StudentRepository:
    
    def get_all_student_data(self)->Dict:
        return studentDB.get_all_data()
    
    def create_student(self , std_id : str , data : Dict) -> Dict :
        return studentDB.create_student_data(datarecord=data , student_id=std_id)
    
    def get_student_by_ID(self , std_id : str)->Dict|None:
        studentsbyID = studentDB.get_student_by_ID(studentID=std_id)
        if studentsbyID:
            studentsbyID["id"] = std_id
            return studentsbyID
        return None
    
    def update_data (self , std_id : str , student_data : Dict) -> Dict:
        return studentDB.update_student(studentID=std_id, studentData=student_data)
    
    def soft_delete_student(self , student_id : str , student_Data:Dict) ->Dict:
        return studentDB.soft_delete(studentID=student_id , studentData=student_Data)
        
    
    
    
    
    