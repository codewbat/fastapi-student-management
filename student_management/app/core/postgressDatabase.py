from sqlalchemy import create_engine , text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import Config

engine = create_engine(
    Config.Postgres_Database_URL_SYNC,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush= False,
    bind= engine
)

Base = declarative_base()


def get_Postgress_DB():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
def init_db():
    from model.db_model import StudentTable
    Base.metadata.create_all(bind = engine)
    print("Postgress table created")
    
def check_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ PostgreSQL connected successfully!")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
