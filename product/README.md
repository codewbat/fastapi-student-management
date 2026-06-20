# Product API

A small FastAPI service for managing products and product image links with JSON file persistence.

## What it does

- List products with sorting and pagination
- Search products by name, exact price, tax range, or product ID
- Create, update, and delete products
- Save and list image URLs
- Store data in local JSON files instead of a database

## Tech Stack

- FastAPI
- Uvicorn
- Pydantic
- Local JSON files for storage

## Project Structure

```text
product/
|-- app/
|   |-- main.py
|   |-- core/
|   |   |-- config.py
|   |   `-- database.py
|   |-- model/
|   |   `-- models.py
|   |-- repositories/
|   |   `-- product_repo.py
|   |-- routes/
|   |   `-- product_route.py
|   `-- services/
|       `-- service.py
`-- data/
    |-- product.json
    `-- image.json
```

## Data Storage

- `data/product.json` stores product records
- `data/image.json` stores image records
- Product IDs are generated as `P001`, `P002`, and so on
- Image IDs are generated as `I001`, `I002`, and so on

## Setup

### 1. Install Python dependencies

From the project root:

```bash
pip install fastapi uvicorn pydantic
```

### 2. Run the API

The imports in this project are written to run from `product/app`.

```bash
cd product/app
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Open the docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

All routes are mounted under `/products`.

### Products

#### `GET /products/getproduct`

Returns all products.

Query params:
- `price=true` sort by price
- `tax=true` sort by tax
- `name=true` sort by name
- `sort_by=asc|desc`
- `page=1`
- `limit=10`

Example:

```bash
curl "http://127.0.0.1:8000/products/getproduct?price=true&sort_by=desc&page=1&limit=5"
```

#### `GET /products/product_field`

Searches by one of the supported filters.

Supported filters:
- `name=keyboard`
- `price=29.99`
- `min_tax=2&max_tax=6`
- `product_id=P001`

Example:

```bash
curl "http://127.0.0.1:8000/products/product_field?name=keyboard"
```

#### `POST /products/create_product`

Creates a new product.

Example body:

```json
{
  "name": "Bluetooth Mouse",
  "description": "Compact wireless mouse",
  "price": 24.99,
  "tax": 2.0
}
```

#### `PUT /products/update_product`

Updates an existing product.

Example body:

```json
{
  "id": "P001",
  "price": 44.99
}
```

#### `DELETE /products/delete_product`

Deletes a product by query parameter.

Example:

```bash
curl -X DELETE "http://127.0.0.1:8000/products/delete_product?product_id=P001"
```

### Images

#### `POST /products/saveImages`

Saves an image record.

Example body:

```json
{
  "id": "P001",
  "url": "https://example.com/image.png"
}
```

#### `GET /products/getImages`

Returns all saved image URLs.

## Notes

- The `token` header is accepted by the routes but is not validated yet.
- `GET /products/product_field` requires at least one filter.
- `price`, `tax`, and `name` sorting only applies when those query flags are set to `true`.
- CORS is configured to allow all origins for local development.

## Sample Data

The repository already includes example entries in:

- `data/product.json`
- `data/image.json`

You can edit those files directly to seed or reset the API data.
