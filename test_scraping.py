import json
import asyncio
import traceback
import scraping_functions as sc
from bs4 import BeautifulSoup


# Main function
def main():

    # Get Scraping Pages List
    try:
        pageName=""
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
            
            # Output Data
            with open("./Output/test","w",encoding='utf-8') as f:
                tmp_soup=BeautifulSoup(page_data.html.html,"lxml")
                f.write(tmp_soup.prettify())

            # Create DataFrame and Input Data"
            df = sc.shaping(page_data, format)
            print("Data shaping completed successfully.")
            
            # Output Data
            path="./Output/"+page["PageName"]+".csv"
            df.to_csv(path)
            print("Data saved to file successfully.\n")
   
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
