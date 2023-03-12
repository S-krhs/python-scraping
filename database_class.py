from sqlalchemy import Column, Integer, Float, String, JSON, Date, text
from database_setting import Base
from sqlalchemy.dialects.mysql import DATETIME as Datetime
from sqlalchemy.sql.functions import current_timestamp

# Class for ScrapingFormat Table
class ScrapingFormatTableClass(Base):
    __tablename__ = "ScrapingFormat"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    PageName = Column(String(255))
    TableName = Column(String(255))
    Format = Column(JSON)
    
# Create temporary table class referring to page-data
def create_tmp_table_class(page):
    format=page["Format"]

    # Define a new table
    class PageTable(Base):
        # Specify the table name
        __tablename__ = page["TableName"]
        
        # Define the columns: id, date, datetime
        id = Column("id", Integer, primary_key=True, autoincrement=True)
        date = Column("date", Date,nullable=False)
        datetime = Column("datetime", Datetime, server_default=current_timestamp(), nullable=False)

    # Add a new column for each feature     
    for feature in format["Features"]:
        if feature["FeatureType"]=="String":
            if feature["FeatureName"]=="Title":
                column_type=String(255)
                column_index=True
            else:
                column_type=String(255)
                column_index=False
        elif feature["FeatureType"]=="Integer":
            column_type=Integer
            column_index=False
        elif feature["FeatureType"]=="Float":
            column_type=Float
            column_index=False
        else:
            raise ValueError("Unexpected FeatureType")
        
        setattr(PageTable, feature["FeatureName"], Column(column_type,index=column_index))
    
    return PageTable