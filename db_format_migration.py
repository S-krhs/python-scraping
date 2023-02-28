from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

def format_migration():
    
    load_dotenv()
    endpoint = os.getenv('DB_ENDPOINT')
    port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    engine = create_engine(f"mysql+pymysql://{username}:{password}@{endpoint}:{port}/{db_name}?charset=utf8")

    Base = declarative_base()
    
    class CreateTable(Base):
        __tablename__ = "ScrapingFormat"
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        PageName = Column(String(255))
        TableName = Column(String(255))
        Format = Column(JSON)
        
    Base.metadata.create_all(engine)
    
    return

format_migration()