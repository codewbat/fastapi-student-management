from typing import List, Dict, Optional
from repositories.product_repo import ProductRepository

def generate_unique_key(
    existing_ids : set , prefix : str = "P"
) -> str:
    counter = 1
    while True:
        new_id = f"{prefix}{counter:03d}"
        if new_id not in existing_ids:
            return new_id
        counter += 1

class ProductService:
    
    def __init__(self , repository : ProductRepository):
        self.repo = repository
        
    def get_all_products(self) -> List[Dict]:
        return self.repo.get_all()
    
    def get_product_by_id(self,product_id : str)-> Optional[Dict]:
        return self.repo.get_by_id(product_id)
    
    def create_product(self , data : Dict)-> Dict:
        exisiting_product = self.repo.get_all()
        exisiting_id = {p['id'] for p in exisiting_product}
        new_id = generate_unique_key(existing_ids=exisiting_id,prefix="P")
        
        return self.repo.create(new_id,data)
    
    def update_product(self, product_id: str, data: Dict) -> Optional[Dict]:
        return self.repo.update(product_id, data)
    
    def delete_product(self, product_id: str) -> bool:
        return self.repo.delete(product_id)
    
    def search_products(self, search_term: str) -> List[Dict]:
        return self.repo.search_by_name(search_term)
    
    def filter_by_price(self, price: float) -> List[Dict]:
        return self.repo.filter_by_price(price)
    
    def filter_by_tax_range(self, min_tax: float, max_tax: float) -> List[Dict]:
        return self.repo.filter_by_tax_range(min_tax, max_tax)
    
    def get_total_count(self) -> int:
        return self.repo.get_total_count()
    
