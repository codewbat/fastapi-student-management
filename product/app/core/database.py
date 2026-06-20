import json , os
from core.config import config
from typing import Dict , Any

class JSONDatabase : 
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({}, file, indent=4)

    def load(self) -> Dict:
        """Load data from JSON file"""
        if os.path.getsize(self.file_path) == 0:
            return {}
        with open(self.file_path, 'r') as file:
            return json.load(file)
    
    # ✅ ADD THIS METHOD (was missing!)
    def save(self, data: Dict):
        """Save data to JSON file"""
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)



    def load_product_data ( self ) -> Dict:
        if os.path.getsize(self.file_path) == 0:
            return{}
        
        with open(self.file_path,'r') as file:
            return json.load(file)
        
    
    def save_product_data (self , DBase : Dict):
        
        if os.path.getsize(self.file_path) ==0:
            return{}
        
        with open(self.file_path,'w') as file:
            json.dump(DBase,file,indent=4)
    
    def get_all(self) -> Dict:
        return self.load_product_data()
    
    def get_by_id(self, record_id: str) -> Dict | None:
        data = self.load()
        return data.get(record_id)
    
    def create(self, record_id: str, data: Dict) -> Dict:
        all_data = self.load()
        all_data[record_id] = data
        self.save(all_data)
        return data
    
    def update(self , record_id: str , data : Dict) -> Dict|None:
        all_data = self.load_product_data()
        
        if record_id not in all_data :
            return None
        all_data[record_id].update(data)
        self.save_product_data(all_data)
        return all_data[record_id]
    
    def delete(self, record_id: str) -> bool:
        all_data = self.load()
        if record_id not in all_data:
            return False
        del all_data[record_id]
        self.save(all_data)
        return True
    def get_all_records(self) -> list:
        data = self.load()
        return [{"id": key, **value} for key, value in data.items()]

product_DB = JSONDatabase(config.Prodcut_File_Path)
image_DB = JSONDatabase(config.Image_File_Path)

async def get_Product_DB():
    return product_DB
async def get_Image_DB():
    return image_DB