from sqlalchemy import Column , String , Integer , Date
from core.postgressDatabase import Base

class StudentTable (Base):
    __tablename__ = "student"
    
    student_id = Column(
        String(10),
        primary_key=True,
        index=True
    )
    
    first_name = Column(
        String(50),
        nullable=False
    )
    
    middle_name = Column(
        String(50),
        nullable=True
    )
    
    last_name = Column(
        String(50),
        nullable=False
    )
    
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    blood_group = Column(String(10), nullable=True)
    
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(10), unique=True, nullable=False)
    
    status = Column(String(10), default="active")
    
    age = Column(Integer, nullable=True)
    
    house_no = Column(String(20), nullable=True)     
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    
    
    def __repr__(self):
        return f"<Student {self.student_id}: {self.first_name} {self.last_name}>"
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "address": {
                "pt_no": self.house_no,
                "city": self.city,
                "state": self.state,
                "country": self.country,
            },
            "date_of_birth": str(self.date_of_birth) if self.date_of_birth else None,
            "gender": self.gender,
            "bloodGroup": self.blood_group,
            "email": self.email,
            "phone": self.phone,
            "status": self.status,
            "age": self.age,
        }
