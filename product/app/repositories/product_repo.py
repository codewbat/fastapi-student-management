from typing import List, Dict, Optional
from core.database import JSONDatabase, product_DB


class ProductRepository:
    """Repository layer for product data access."""

    def __init__(self, db: JSONDatabase = None):
        self.db = db or product_DB

    def get_all(self) -> List[Dict]:
        """Return all products as a list of dicts with 'id' included."""
        data = self.db.load()
        return [{"id": key, **value} for key, value in data.items()]

    def get_by_id(self, product_id: str) -> Optional[Dict]:
        """Return a single product by its ID, or None."""
        record = self.db.get_by_id(product_id)
        if record is not None:
            return {"id": product_id, **record}
        return None

    def create(self, product_id: str, data: Dict) -> Dict:
        """Create a new product and return it."""
        self.db.create(product_id, data)
        return {"id": product_id, **data}

    def update(self, product_id: str, data: Dict) -> Optional[Dict]:
        """Update an existing product. Returns updated product or None."""
        updated = self.db.update(product_id, data)
        if updated is not None:
            return {"id": product_id, **updated}
        return None

    def delete(self, product_id: str) -> bool:
        """Delete a product by ID. Returns True if deleted."""
        return self.db.delete(product_id)

    def search_by_name(self, search_term: str) -> List[Dict]:
        """Search products whose name starts with or contains the term."""
        all_products = self.get_all()
        starts_with = [p for p in all_products if p["name"].lower().startswith(search_term.lower())]
        contains = [p for p in all_products if search_term.lower() in p["name"].lower()]
        # starts_with first, then remaining contains matches
        return starts_with + [x for x in contains if x not in starts_with]

    def filter_by_price(self, price: float) -> List[Dict]:
        """Return products matching exact price."""
        return [p for p in self.get_all() if p.get("price") == price]

    def filter_by_tax_range(self, min_tax: float, max_tax: float) -> List[Dict]:
        """Return products within a tax range, sorted by tax."""
        return sorted(
            [p for p in self.get_all() if min_tax <= (p.get("tax") or 0) <= max_tax],
            key=lambda x: x.get("tax", 0),
        )

    def get_total_count(self) -> int:
        """Return total number of products."""
        return len(self.db.load())
