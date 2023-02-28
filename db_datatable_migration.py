from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql
from dotenv import load_dotenv
import os
import json
import asyncio
import traceback
import scraping as sc

# Create database connection engine using sqlalchemy
def db_conn_engine():
    # Load database connection info from .env file
    load_dotenv()
    endpoint = os.getenv('DB_ENDPOINT')
    port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

    # Connect to database using sqlalchemy create_engine function
    engine = create_engine(f"mysql://{username}:{password}@{endpoint}:{port}/{db_name}",echo=True)
    return engine

# Migrate data table refer to Imput-ScrapingFormat
def db_datatable_migration(Base,page,engine):
    format=page["Format"]

    # Define a new table
    class CreateTable(Base):
        # Specify the table name
        __tablename__ = page["TableName"]
        
        # Define the columns, id, date, some features
        id = Column(Integer, primary_key=True, autoincrement=True)
        datetime = Column(DateTime)

    # Add a new column for each feature        
    for feature in format["Features"]:
        if feature["FeatureType"]=="Integer":
            colmun_type=Integer
        elif feature["FeatureType"]=="String":
            colmun_type=String(255)
        else:
            raise ValueError("Unexpected FeatureType")
        
        setattr(CreateTable, feature["FeatureName"], Column(colmun_type))
    
    # create all tables in the database
    Base.metadata.create_all(bind=engine)
    


# Registrate data format refer to Imput-ScrapingFormat
def db_format_registration(Base,page,engine):
    
    class ScrapingFormat(Base):
        # table name
        __tablename__ = "ScrapingFormat"
        
        # information of the columns
        id = Column(Integer, primary_key=True, autoincrement=True)
        PageName = Column(String)
        TableName = Column(String)
        Format = Column(String)

    Session = sessionmaker(bind=engine)
    session = Session()
        
    add_data = ScrapingFormat(PageName=(page["PageName"]),TableName=(page["TableName"]),Format=json.dumps(page["Format"]))
    session.add(add_data)
    session.commit()



def newSiteRegistration():
    try:
        with open("./ScrapingFormat.json","r") as imput:
            page=json.load(imput)
        print("JSON file loaded successfully\n")
    except Exception as e:
        print("FileOpenError:", e)
        return
    
    # Verify JSON format is correct
        # --ToDo
    
    # Test run to verify correct behavior
    try:  
        # Start Scraping
        print("Scraping test process started on ",page["PageName"])
        format = page["Format"]
        
        # Get HTML
        print("HTML request started...")
        loop = asyncio.new_event_loop()
        page_data = loop.run_until_complete(sc.getHTML(format))
        page_data.raise_for_status()
        print("HTML data retrieved successfully")
                
        # Create DataFrame and Input Data"
        df = sc.shaping(page_data, format)
        print("Data shaping completed successfully")
        print("All scraping process completed\n")
        
        # Preview data and Choose Execute Migration or Cancel
        print("DataFrame Output\n",df,"\n")
        while True:
            input_=input("Are you sure to execute the migration? Prease press 'Y' or 'n' to select an option. If you want to preview whole data, enter 'd'.\n[Y/n] >> ").lower()
            print(input_)

            if input_ in ["Y","y"]:
                print("Execute migration...")
                break
            elif input_ in ["D","d"]:
                #Output Data
                path="./Output/"+page["PageName"]+".csv"
                df.to_csv(path)
                
                print("Data saved to file at ",path)
            else:
                print("Migration canceled.")
                return
    except Exception as e:
        print("Error occurred:", e)
        print("StackTrace:", traceback.format_exc())
        return
    
    # Migration and Registration
    try:
        # DB connection
        print("DB connection started...")
        engine = db_conn_engine()
        print("DB connection succeeded.")
        
        # Create a declarative base object
        Base = declarative_base()
        
        # Migration datatable
            # --ToDo if exist??
        db_datatable_migration(Base,page,engine)
        print("Datatable migration completed.")
        
        # Registration format
            # --ToDo Transaction
        db_format_registration(Base,page,engine)
        print("Scraping format registration completed.")
        
    except Exception as e:
        print("Error occurred:", e)
        print("StackTrace:", traceback.format_exc())
    
    print("Program closed.")
    return

newSiteRegistration()