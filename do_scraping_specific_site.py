from database_setting import Engine, Base, Session
from database_class import ScrapingFormatTableClass
import json
import asyncio
import traceback
import scraping_functions as sc


# Main function
def main():

    # Get Scraping Pages List
    try:
        pageName="9anime"
        with open("./FormatsArchive/"+pageName+"Format.json","r") as f:
            page=json.load(f)
        print("Scraping format JSON loaded successfully.\n")
        pages=[page]
        # print(pages)
    except Exception as e:
        print("Error occurred:", e)
        print("StackTrace:", traceback.format_exc())
        return

    # Scraping per page
    for page in pages:
        # Scraping with Exception Handling
        try:  
            # Start Scraping
            print("Scraping process started on ",page["PageName"])
            format = page["Format"]
            
            # Get HTML
            print("HTML request started...")
            loop = asyncio.new_event_loop()
            page_data = loop.run_until_complete(sc.getHTML(format))
            page_data.raise_for_status()
            print("HTML data retrieved successfully.")
                    
            # Create DataFrame and Input Data"
            df = sc.shaping(page_data, format)
            print("Data shaping completed successfully.")
            
            # Output Data
            df.to_sql(name = page["TableName"], con = Engine, if_exists='append', index= False)
            print("Data saved to database successfully.\n")
            
            # path="./Output/"+page["PageName"]+".csv"
            # df.to_csv(path)
            # print("Data saved to file successfully.\n")
   
        except Exception as e:
            print("Error occurred:", e)
            print("StackTrace:", traceback.format_exc())
            # If error occurred go to next page
            continue
            
    print("All scraping process completed.")

    return

# Execution
if __name__ == '__main__':
    main()
