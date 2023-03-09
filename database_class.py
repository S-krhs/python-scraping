from sqlalchemy import Column, Integer, String, JSON, DateTime
from database_setting import Base

# Class for ScrapingFormat Table
class ScrapingFormatTableClass(Base):
    __tablename__ = "ScrapingFormat"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    PageName = Column(String(255))
    TableName = Column(String(255))
    Format = Column(JSON)
    
# Create temporary table class refer to page-data
def CreateTmpTableClass(page):
    format=page["Format"]

    # Define a new table
    class PageTable(Base):
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
        
        setattr(PageTable, feature["FeatureName"], Column(colmun_type))
    
    return PageTable