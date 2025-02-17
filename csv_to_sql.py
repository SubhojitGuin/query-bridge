import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import glob

# Load environment variables
load_dotenv()
username = os.getenv("db_user")
password = os.getenv("db_password")
localhost = os.getenv("db_host")
db_name = os.getenv("db_name")

# Define database connection
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{localhost}:3306/{db_name}')

# Define folder path
folder_path = 'ergastf1_data'

# Get all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

def format_table_name(filename):
    """Convert filename to table name by removing underscores and capitalizing the next letter."""
    name_without_ext = os.path.splitext(filename)[0]  # Remove .csv extension
    # parts = name_without_ext.split('_')
    # formatted_name = parts[0] + ''.join(word.capitalize() for word in parts[1:])
    return name_without_ext

# Iterate over each CSV file and load it into MySQL
for file in csv_files:
    table_name = format_table_name(os.path.basename(file))  # Generate table name
    df = pd.read_csv(file)  # Load CSV into DataFrame
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)  # Store in MySQL
    print(f"Loaded {file} into table {table_name}")
