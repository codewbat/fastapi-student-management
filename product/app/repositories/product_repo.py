from typing import List , Dict , Optional
from core.database import product_DB , image_DB

class ProductRepository:
    
    def get_all(self) -> List[Dict] :
        return product_DB.get_all_records()
    
    def get_by_id(self , product_id : str) -> Optional[Dict]:
        product = product_DB.get_by_id(product_id)
        if product:
            product["id"] = product_id
        return product
    
    def create(self , product_id : str , data: Dict) -> Dict:
        return product_DB.create(product_id,data)
    
    def update(self, product_id: str, data: Dict) -> Optional[Dict]:
        return product_DB.update(product_id, data)
    
    def delete(self, product_id: str) -> bool:
        return product_DB.delete(product_id)
    
    def search_by_name(self, search_term: str) -> List[Dict]:
        products = self.get_all()
        return [p for p in products if search_term.lower() in p['name'].lower()]
    
    def filter_by_price(self, price: float) -> List[Dict]:
        products = self.get_all()
        return [p for p in products if p['price'] == price]
    
    def filter_by_tax_range(self, min_tax: float, max_tax: float) -> List[Dict]:
        products = self.get_all()
        return [p for p in products if min_tax <= p['tax'] <= max_tax]
    
    def get_total_count(self) -> int:
        return len(product_DB.load())

class ImageRepository:
    """Handles image database operations"""
    
    def get_all(self) -> List[Dict]:
        return image_DB.get_all_records()
    
    def get_by_id(self, image_id: str) -> Optional[Dict]:
        image = image_DB.get_by_id(image_id)
        if image:
            image["id"] = image_id
        return image
    
    def create(self, image_id: str, data: Dict) -> Dict:
        return image_DB.create(image_id, data)
    
    def delete(self, image_id: str) -> bool:
        return image_DB.delete(image_id)
