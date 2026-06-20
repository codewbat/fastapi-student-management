import os 

class Config:
    Prodcut_File_Path = 'C:/kanishk_pratice/product/data/product.json'
    Image_File_Path = 'C:/kanishk_pratice/product/data/image.json'
    
    @classmethod
    def init_dicectories(cls):
        os.makedirs(os.path.dirname(cls.Prodcut_File_Path),exist_ok=True)
        os.makedirs(os.path.dirname(cls.Image_File_Path),exist_ok=True)
        

config = Config()
config.init_dicectories()