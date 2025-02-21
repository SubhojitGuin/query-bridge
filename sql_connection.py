# from mysql.connector import connect
import os
from dotenv import load_dotenv
import mysql.connector
import csv
import io
from sqlalchemy import create_engine
load_dotenv()

user = os.getenv("db_user")
pw = os.getenv("db_password")
host = os.getenv("db_host")
db = os.getenv("db_name")
port = os.getenv("db_port")

engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}",
                        pool_pre_ping=True,
                        pool_recycle=1800,    # ✅ Recycles connection every 30 minutes
                        pool_size=10,         # ✅ Maintains up to 10 connections
                        max_overflow=5)


# mydb = mysql.connector.connect(
#   host=localhost,
#   user=username,
#   password=password,
#   database=db_name
# )

# def reconnect_sql_connection():
#     global mydb
#     mydb = mysql.connector.connect(
#       host=localhost,
#       user=username,
#       password=password,
#       database=db_name
#     )

def sql_cursor():
    connection = engine.connect()  # Returns a SQLAlchemy connection object
    return connection



def format_results_as_list(rows):
    # # Create the header row as a list
    # header_row = [str(header) for header in headers]
    
    # Create the data rows as lists without padding for column width
    data_rows = [[str(value) for value in row] for row in rows]
    
    # Combine the header row and the data rows into a final list of lists
    # table_as_list = [header_row] + data_rows
    table_as_list = data_rows
    
    return table_as_list

def format_results_as_markdown(headers, rows):
    # Create the header row in Markdown format
    header_row = "|  " + "  |  ".join(str(header).replace('\n',' ') for header in headers) + "  |"
    
    # Create the separator row (--- between columns)
    separator_row = "| " + " | ".join("---" for _ in headers) + " |"
    
    # Create the data rows in Markdown format
    data_rows = ["| " + " | ".join(str(value).replace('\n' , ' ') for value in row) + " |" for row in rows]
    
    # Combine the header, separator, and data rows
    markdown_table = [header_row, separator_row] + data_rows
    
    # Join the rows with line breaks to create the final Markdown string
    markdown_output = "\n".join(markdown_table)
    
    return markdown_output

if __name__ == "__main__":
     mycursor = sql_cursor()
     mycursor.execute("SELECT * FROM `ground_water_level-2015-2022`")
     myresult = mycursor.fetchall()
     for x in myresult:
        print(x)
  


