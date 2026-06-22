import json , os
from core.config import config
from typing import Dict , Any

class JSONDatabase : 
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file, indent=4)
                
    def load(self)->Dict:
        if os.path.getsize(self.file_path) == 0:
            return{}
        with open(self.file_path,'r') as file:
            data = json.load(file)
            return data
    
    def save(self, data : Dict) :
        with open(self.file_path,'w') as file:
            json.dump(data,file,indent=4,default=str)
            
    def get_all_data (self) -> Dict:
        data = self.load()
        return data 
    
    def create_student_data (self , datarecord : Dict , student_id : str) -> Dict:
        studentdata = self.load()
        studentdata[student_id] = datarecord
        self.save(studentdata)
        return datarecord
    
    def get_student_by_ID(self , studentID : str)-> Dict:
        student = self.load()
        return student.get(studentID)        
    
    def update_student(self , studentID : str , studentData : Dict) -> Dict:
        student = self.load()
        student[studentID] = studentData
        self.save(student)
        return studentData
    
    def soft_delete(self , studentID:str , studentData : Dict) -> Dict :
        students = self.load()
        students[studentID] = studentData
        self.save(students)
        return students[studentID]  
        
    
studentDB = JSONDatabase(config.Student_File_Path)
async def get_database():
    return studentDB