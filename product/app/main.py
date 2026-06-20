from fastapi import FastAPI , Depends , Header , Query
#from fastapi.responses import JSONResponse
#from pydantic import BaseModel , Field
#from typing import Optional , Annotated 
#import json , os
from routes.product_route import routes


"""
def generate_unique_id(Dbase: dict, prefix: str = "P") -> str:
    
    existing_ids = set(Dbase.keys())
    counter = 1
    while True:
        new_id = f"{prefix}{counter:03d}"
        if new_id not in existing_ids:
            return new_id
        counter += 1

async def save_product(Dbase : dict):
    if not os.path.exists(File_path):
        raise FileNotFoundError(f"File '{File_path}' not found.")
    with open(File_path,'w') as file:
        json.dump(Dbase,file,indent=4)

async def load_product():
    
    if not os.path.exists(File_path):
        raise FileNotFoundError(f"File '{File_path}' not found.")
    
    with open(File_path,'r') as file:
        data = json.load(file)
        yield data
    
DBsession = Annotated[dict,Depends(load_product)]    

async def load_image():
        if not os.path.exists(image_File_path):
            raise FileNotFoundError(f"File '{image_File_path}' not found.")
        with open(image_File_path,'r') as file:
            data = json.load(file)
            yield data

async def save_image_data(ImageDBase : dict):
    if not os.path.exists(image_File_path):
        raise FileNotFoundError(f"File '{image_File_path}' not found.")
    with open(image_File_path,'w') as file:
        json.dump(ImageDBase,file,indent=4)

ImageDBsession = Annotated[dict,Depends(load_image)]
    
@app.get('/getproduct')
async def getproduct(
    Dbase :DBsession,
    token : Annotated[Optional[str],Header()]  = None,
    price : Optional[bool] = Query(
        default =None,
        description="Sort by price"
    ),
    tax : Optional[bool] = Query(
        default=None,
        description="Sort by tax"
    ),
    name : Optional[bool] = Query(
        default=None,
        description="Sort by name"
    ),
    sort_by : Optional[str] = Query(
        default=None,
        description="Sort order"
    ),
):
    products = []
    for id,value in Dbase.items():
        products.append({
            'id':id,
            'name':value['name'],
            'description':value['description'],
            'price':value['price'],
            'tax':value['tax']
        })
    
    if tax == True:
        products.sort(key=lambda x:x['tax'], reverse=(sort_by == 'desc'))
    elif price == True:
        products.sort(key=lambda x:x['price'], reverse=(sort_by == 'desc'))
    elif name == True:
        products.sort(key=lambda x:x['name'], reverse=(sort_by == 'desc'))
        
        
    return JSONResponse(
        status_code=200,
        content={
            "message": "Here Your Product ",
            "data": products,
        }
    )

@app.get('/product_Field')
async def get_product_by(
    Dbase :DBsession,
    token : Annotated[Optional[str],Header()]  = None,
    price : Optional[float] = Query(
        default =None,
        description="Sort by price"
    ),
    min_tax : Optional[float] = Query(
        default=None,
        description="Range of tax"
    ),
    max_tax : Optional[float] = Query(
        default=None,
        description="Range of tax"
    ),
    name : Optional[str] = Query(
        default=None,
        description="Sort by name"
    ),
    product_id : Optional[str] = Query(
        default=None,
        description="Sort order"
    ),
    sort_by : Optional[str] = Query(
        default=None,
        description="Sort order"
    ),
):
    products = []
    for key,value in Dbase.items():
        products.append({
            'id':key,
            'name':value['name'],
            'description':value['description'],
            'price':value['price'],
            'tax':value['tax']
        })
    
    if name :
        starts_with  = [product for product in products if product['name'].lower().startswith(name.lower())]
        contains = [product for product in products if name.lower() in product['name'].lower()]
        products = starts_with+ [x for x in contains if x not in starts_with]
    elif price :
        products = [product for product in products if product['price'] == price]
    elif min_tax and max_tax:
        products = sorted([product for product in products if min_tax <= product['tax'] <= max_tax],key=lambda x:x['tax'], reverse=(sort_by == 'desc'))
    elif product_id :
        products = [product for product in products if product['id'] == product_id]
    else :
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Please provide at least one filter: name, price, min_tax+max_tax, or product_id",
                "example": "/getProduct_by_Field?name=keyboard"
            }
        )
    return JSONResponse(
        status_code=200,
        content={
            "message": "Here Your Product ",
            "data": products,
        }
    )

@app.post('/create_product')
async def create_product(
    Dbase :DBsession,
    item : Create_Items,
    token : Annotated[Optional[str],Header()]  = None,
):
    
    product_data = item.model_dump()
    for pid , value in Dbase.items():
        if value['name'].lower() == item.name.lower():
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": f"Product '{item.name}' already exists"
                }
            )
    product_id = generate_unique_id(Dbase=Dbase)
    
    Dbase[product_id] = product_data
    
    await save_product(Dbase)
    
    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "message": f"Product created successfully",
            "product_id": product_id,
            "data": product_data
        }
    )

@app.put('/Update_product')
async def update_product(
    Dbase :DBsession,
    item : Update_Product,
    token : Annotated[Optional[str],Header()]  = None,
):
    existing_ids = set(Dbase.keys()) 
    if item.id not in existing_ids:
        return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": f"Product '{item.id}' not  exists"
                }
        ) 
    
    update_data = item.model_dump(exclude_none=True)  
    
    update_data.pop('id',None)
    Dbase[item.id].update(update_data)
    
    await save_product(Dbase)

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f"Product {item.id} updated successfully",
            "updated_fields": list(update_data.keys()),
            "data": Dbase[item.id]
        }
    )

@app.delete('/delete_product')
async def delete_product(
    Dbase :DBsession,
    product_id : str,
    token : Annotated[Optional[str],Header()]  = None,
):
    existing_ids = set(Dbase.keys()) 
    if product_id not in existing_ids:
        return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": f"Product '{product_id}' not  exists"
                }
        ) 
    del Dbase[product_id]
    await save_product(Dbase=Dbase)
    return 0

@app.post('/saveImages')
async def save_images(
    ImageDbase :ImageDBsession,
    product_image : Image_model,
    token : Annotated[Optional[str],Header()]  = None,

):
    image_product = product_image.model_dump(exclude_unset=True)
    new_id = generate_unique_id(Dbase=ImageDbase)
     
    ImageDbase[new_id] = image_product
    await save_image_data(ImageDbase)
    
    print(product_image)
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message":'image saved',
            "image" : image_product
        }
    )

@app.get('/getImages')
async def get_images(
    ImageDbase :ImageDBsession,
    token : Annotated[Optional[str],Header()]  = None,

):
    image_data = []
    for key , value in ImageDbase.items():
        image_data.append({
            'id':value.get('id',key),
            'url':value.get('url','')
        })
    
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "images":image_data
        }
    )
"""  

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Product API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes)

