import os

class Settings:
    """Application configuration."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    Prodcut_File_Path = os.path.join(DATA_DIR, "product.json")
    Image_File_Path = os.path.join(DATA_DIR, "image.json")

config = Settings()
