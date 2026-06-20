from fastapi import APIRouter, Depends, Header, Query
from fastapi.responses import JSONResponse
from typing import Optional, Annotated

from services.service import ProductService
from repositories.product_repo import ProductRepository
from model.models import Create_Items, Update_Product, Image_model
from core.database import image_DB


routes = APIRouter(prefix="/products", tags=["Products"])


# ── Dependency ──────────────────────────────────────────────
def get_product_service() -> ProductService:
    repo = ProductRepository()
    return ProductService(repository=repo)


# ── GET all products (with sorting & pagination) ────────────
@routes.get("/getproduct")
async def get_products(
    services: ProductService = Depends(get_product_service),
    token: Annotated[Optional[str], Header()] = None,
    price: Optional[bool] = Query(default=None, description="Sort by price"),
    tax: Optional[bool] = Query(default=None, description="Sort by tax"),
    name: Optional[bool] = Query(default=None, description="Sort by name"),
    sort_by: Optional[str] = Query(default=None, description="Sort order: asc or desc"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
):
    products = services.get_all_products()

    # Sorting
    if tax:
        products.sort(key=lambda x: x.get("tax", 0), reverse=(sort_by == "desc"))
    elif price:
        products.sort(key=lambda x: x.get("price", 0), reverse=(sort_by == "desc"))
    elif name:
        products.sort(key=lambda x: x.get("name", ""), reverse=(sort_by == "desc"))

    # Pagination
    total = len(products)
    start = (page - 1) * limit
    end = start + limit
    paginated = products[start:end]

    return JSONResponse(
        status_code=200,
        content={
            "message": "Here Your Product",
            "total": total,
            "page": page,
            "limit": limit,
            "data": paginated,
        },
    )


# ── GET product by field (search / filter) ──────────────────
@routes.get("/product_field")
async def get_product_by_field(
    services: ProductService = Depends(get_product_service),
    token: Annotated[Optional[str], Header()] = None,
    name: Optional[str] = Query(default=None, description="Search by name"),
    price: Optional[float] = Query(default=None, description="Filter by exact price"),
    min_tax: Optional[float] = Query(default=None, description="Min tax range"),
    max_tax: Optional[float] = Query(default=None, description="Max tax range"),
    product_id: Optional[str] = Query(default=None, description="Filter by product ID"),
    sort_by: Optional[str] = Query(default=None, description="Sort order: asc or desc"),
):
    if name:
        products = services.search_products(name)
    elif price is not None:
        products = services.filter_by_price(price)
    elif min_tax is not None and max_tax is not None:
        products = services.filter_by_tax_range(min_tax, max_tax)
        if sort_by == "desc":
            products.reverse()
    elif product_id:
        product = services.get_product_by_id(product_id)
        products = [product] if product else []
    else:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Please provide at least one filter: name, price, min_tax+max_tax, or product_id",
                "example": "/products/product_field?name=keyboard",
            },
        )

    return JSONResponse(
        status_code=200,
        content={
            "message": "Here Your Product",
            "data": products,
        },
    )


# ── POST create product ────────────────────────────────────
@routes.post("/create_product")
async def create_product(
    item: Create_Items,
    services: ProductService = Depends(get_product_service),
    token: Annotated[Optional[str], Header()] = None,
):
    # Check for duplicate name
    existing = services.get_all_products()
    for p in existing:
        if p["name"].lower() == item.name.lower():
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": f"Product '{item.name}' already exists",
                },
            )

    product_data = item.model_dump()
    result = services.create_product(product_data)

    return JSONResponse(
        status_code=201,
        content={
            "status": "success",
            "message": "Product created successfully",
            "data": result,
        },
    )


# ── PUT update product ─────────────────────────────────────
@routes.put("/update_product")
async def update_product(
    item: Update_Product,
    services: ProductService = Depends(get_product_service),
    token: Annotated[Optional[str], Header()] = None,
):
    # Check existence
    existing = services.get_product_by_id(item.id)
    if not existing:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": f"Product '{item.id}' does not exist",
            },
        )

    update_data = item.model_dump(exclude_none=True)
    update_data.pop("id", None)

    result = services.update_product(item.id, update_data)

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f"Product {item.id} updated successfully",
            "updated_fields": list(update_data.keys()),
            "data": result,
        },
    )


# ── DELETE product ──────────────────────────────────────────
@routes.delete("/delete_product")
async def delete_product(
    product_id: str = Query(..., description="Product ID to delete"),
    services: ProductService = Depends(get_product_service),
    token: Annotated[Optional[str], Header()] = None,
):
    deleted = services.delete_product(product_id)
    if not deleted:
        return JSONResponse(
            status_code=404,
            content={
                "status": "error",
                "message": f"Product '{product_id}' does not exist",
            },
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": f"Product '{product_id}' deleted successfully",
        },
    )


# ── POST save image ────────────────────────────────────────
@routes.post("/saveImages")
async def save_images(
    product_image: Image_model,
    token: Annotated[Optional[str], Header()] = None,
):
    image_data = product_image.model_dump(exclude_unset=True)
    # Generate a unique ID for the image record
    all_images = image_DB.load()
    existing_ids = set(all_images.keys())
    counter = 1
    while True:
        new_id = f"I{counter:03d}"
        if new_id not in existing_ids:
            break
        counter += 1

    all_images[new_id] = image_data
    image_DB.save(all_images)

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Image saved",
            "image_id": new_id,
            "image": image_data,
        },
    )


# ── GET all images ──────────────────────────────────────────
@routes.get("/getImages")
async def get_images(
    token: Annotated[Optional[str], Header()] = None,
):
    all_images = image_DB.load()
    image_list = []
    for key, value in all_images.items():
        image_list.append(
            {
                "id": value.get("id", key),
                "url": value.get("url", ""),
            }
        )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "images": image_list,
        },
    )
