from pydantic import BaseModel , Field
from typing import Optional , Annotated 

class Items(BaseModel):
    name: Annotated[
        str,
        Field(min_length=3,max_length=50)
    ]
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    
    
    class Config:
        from_attributes = True


class Create_Items(BaseModel):
    name : Annotated[
        str,
        Field(
            ...,
            description="Enter new Product name",
            min_length=3
        )
    ]
    description : Annotated[
        str,
        Field(
            ...,
            description="Enter product description",
            min_length=1,
            max_length=100
        )
    ]
    price: Annotated[
        float,
        Field(
            ...,
            description="Enter price"
        )
    ]
    tax: Annotated[
        float|None,
        Field(
            description="taxes to paid off"
        )
    ]
    
class Update_Product(BaseModel):
    id : Annotated[
        str,
        Field(
            ...,
            description="Enter new Product id",
        )
    ]
    name : Annotated[
        str|None,
        Field(
            description="Enter new Product name",
            min_length=3
        )
    ]
    description : Annotated[
        str|None,
        Field(
            description="Enter product description",
            min_length=1,
            max_length=100
        )
    ]
    price: Annotated[
        float|None,
        Field(
            description="Enter price",
            gt =0
        )
    ]
    tax: Annotated[
        float|None,
        Field(
            description="taxes to paid off"
        )
    ]

class Image_model(BaseModel):
    id : Annotated[
        str,
        Field(
            ...,
            description="Enter new Product id",
        )
    ]
    url : Annotated[
        str,
        Field(
            ...,
            description="Image URL"
        )
    ]