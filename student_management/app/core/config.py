import os 

class Config:
    Student_File_Path = "C:/kanishk_pratice/student_management/data/student.json"
    
    Postgres_Database_URL ="postgresql+asyncpg://postgres:2419@localhost:5432/StudentDB"
    
    Postgres_Database_URL_SYNC = "postgresql://postgres:2419@localhost:5432/StudentDB"
    
    STORAGE_MODE = "postgres"
    STUDENT_ID_PREFIX: str = "STD"
    STUDENT_ID_DIGITS: int = 3

    @classmethod
    def init_dicectories(cls):
        os.makedirs(os.path.dirname(cls.Student_File_Path), exist_ok=True)
        
    @classmethod
    def is_postgres(cls) -> bool:
        return cls.STORAGE_MODE == "postgres"
    
    @classmethod
    def is_json(cls) -> bool:
        return cls.STORAGE_MODE == "json"

        
config = Config()
config.init_dicectories()