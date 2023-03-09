from sqlalchemy import create_engine, Column, Integer, String, JSON
from database_setting import Engine, Base
from database_class import ScrapingFormatTable

# This program is designed to be executed only once when building the environment.
# In most cases, you will not need to execute it. 
def main():
    Base.metadata.create_all(Engine)
    return

# Execution
if __name__ == '__main__':
    main()