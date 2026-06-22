from pydantic import BaseModel , Field ,EmailStr , field_validator , computed_field
from typing import Annotated ,Literal , Optional ,Dict
from datetime import date , datetime
from enum import Enum


class StudentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Address(BaseModel):
    pt_no : Annotated[
        str,
        Field(
            ...,
            description="house number"
        )
    ]
    city : Annotated[
        str,
        Field(
            ...,
            description="city"
        )
    ]
    state : Annotated[
        str,
        Field(
            ...,
            description="state"
        )
    ]
    country : Annotated[
        str,
        Field(
            ...,
            description="country"
        )
    ]
    
class Create_Student(BaseModel):
    first_name : Annotated[
        str,
        Field(
            ...,
            description= " Enter student first name ",
            min_length=1,
            max_length=20
        )
    ]
    middle_name : Annotated[
        Optional[str],
        Field(
            default=None,
            description= " Enter student middle name ",
            max_length=20
        )
    ]
    last_name : Annotated[
        str,
        Field(
            ...,
            description= " Enter student last name ",
            min_length=1,
            max_length=20
        )
    ]

    date_of_birth : Annotated[
        date,
        Field(
            ...,
            description="Enter date of birth"
        )    
    ]
    gender : Annotated[
        Literal["male" , "female" , "other"],
        Field(
            ...,
            description="Select gender"
        )
    ]
    bloodGroup : Annotated[
        Optional[str] ,
        Field(
            default=None,
            description="Enter blood group"
        )
    ]
    email : Annotated[
        EmailStr,
        Field(
            ...,
            description="Enter student e-mail"
        )
    ]
    phone : Annotated[
        str,
        Field(
            ...,
            description="Enter mobile number",
            pattern=r'^\d{10}$'
        )
    ]
    address : Annotated[
        Address,
        Field(
            ...,
            description="User Address"
        )
    ]
    
    @field_validator('email')
    @classmethod
    def validate_email(cls,value):
        validate_email = ["gmail.com","skit.ac.in"]
        domain = value.split('@')[-1]
        if domain not in validate_email :
            raise ValueError("Email domain must be one of {allowed_domains}")
        return value
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls,value):
        if value.startswith('0'):
            raise ValueError("phone number cannot be started with 0")
        
        if len(value)!=10 :
            raise ValueError("phone number cannot be less that 10")
        
        if not value.isdigit():
            raise ValueError("phone number can only be a digit")
        return value
        
    @computed_field
    @property
    def age(self) ->int:
        today = date.today()
        if not self.date_of_birth :
            raise ValueError("enter date of birth to calculate age ")
        dob = self.date_of_birth
        age = today.year - dob.year
        
        if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
            age -= 1
        
        return age
    
    @computed_field
    @property
    def student_status(self) -> StudentStatus:
        return StudentStatus.ACTIVE
    
class Update_Student(BaseModel):

    first_name : Annotated[
        Optional[str],
        Field(
            ...,
            description= " Enter student first name ",
            min_length=1,
            max_length=20
        )
    ]
    middle_name : Annotated[
        Optional[str],
        Field(
            default=None,
            description= " Enter student middle name ",
            max_length=20
        )
    ]
    last_name : Annotated[
        Optional[str],
        Field(
            ...,
            description= " Enter student last name ",
            min_length=1,
            max_length=20
        )
    ]

    date_of_birth : Annotated[
        Optional[date],
        Field(
            ...,
            description="Enter date of birth"
        )    
    ]
    gender : Annotated[
        Optional[Literal["male" , "female" , "other"]],
        Field(
            ...,
            description="Select gender"
        )
    ]
    bloodGroup : Annotated[
        Optional[str] ,
        Field(
            default=None,
            description="Enter blood group"
        )
    ]
    email : Annotated[
        Optional[EmailStr],
        Field(
            ...,
            description="Enter student e-mail"
        )
    ]
    phone : Annotated[
        Optional[str],
        Field(
            ...,
            description="Enter mobile number",
            pattern=r'^\d{10}$'
        )
    ]
    address : Annotated[
        Optional[Address],
        Field(
            default=None,
            description="User Address"
        )
    ]


