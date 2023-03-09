from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql
from dotenv import load_dotenv
import os

# Load database connection info from .env file
load_dotenv()
endpoint = os.getenv('DB_ENDPOINT')
port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

DATABASE=f"mysql+pymysql://{username}:{password}@{endpoint}:{port}/{db_name}?charset=utf8"

# Create database connection engine using sqlalchemy
Engine = create_engine(
    DATABASE,
    echo=False
)

# Create inspector
Inspector = inspect(Engine)

# Create session
Session = scoped_session(
    sessionmaker(
        autocommit = False,
	    autoflush = False,
	    bind = Engine
    )
)

# Create base model
Base = declarative_base()
Base.query = Session.query_property()

