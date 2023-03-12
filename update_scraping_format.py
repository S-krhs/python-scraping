from sqlalchemy import Column, Integer, String, JSON, DateTime
from database_setting import Engine, Base, Session, Inspector
from database_class import ScrapingFormatTableClass, create_tmp_table_class

import json
import asyncio
import traceback
import shutil
import scraping_functions as sc

# formatの型の変更はSQLで直接する必要あり

# Registration new page
def main():
    # Get registration data from "ScrapingFormat.json"
    try:
        pageName=""
        with open("./FormatsArchive/"+pageName+"Format.json","r") as f:
            page=json.load(f)
        print("Scraping format JSON loaded successfully.\n")
    except Exception as e:
        print("FileOpenError:", e)
        return
    
    # Check if a table for the data already exists
    try:
        # Create an inspector object to access the database metadata
        if Inspector.has_table(page['TableName']):
            pass
        else:
            raise ValueError("Specified table name does not exist.")
    except Exception as e:
        print("Error occurred:", e)
        print("StackTrace:", traceback.format_exc())
        return
    
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
            print("Are you sure to execute the migration? Prease press 'Y' or 'n' to select an option. If you want to preview whole data, enter 'd'.")
            input_=input("[Y/n/d] >> ").lower()
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
    
    # Migration, Registration and Archive
    try:      
        # Migration datatable
        create_tmp_table_class(page)
        
        # Registration format
        Session.query(ScrapingFormatTableClass).filter(ScrapingFormatTableClass.PageName == page["PageName"]).delete()
        replace_data = ScrapingFormatTableClass(PageName=(page["PageName"]),TableName=(page["TableName"]),Format=json.dumps(page["Format"]))
        Session.add(replace_data)
        
        # Commit
        print("Datatable migration completed.")
        Session.commit()
        print("Scraping format registration completed.")
        
    except Exception as e:
        print("Error occurred:", e)
        print("StackTrace:", traceback.format_exc())
    
    print("Program closed.")
    return

# Execution
if __name__ == '__main__':
    main()
