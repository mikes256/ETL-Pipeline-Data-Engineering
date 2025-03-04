import requests, yaml, pandas as pd
from pathlib import Path
import snowflake.connector
from io import StringIO  # To handle CSV data in memory

def get_config():
    """ Load the YAML config file """
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config
config = get_config()

# Global constants
API_KEY = config['api']['api_key']

def auntenticate(API_KEY):
    #ADD A TRY BLOCK. 

    # Request for S&P 500 list (this endpoint gives you the entire listing)
    url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}"

    # Make the API request
    response = requests.get(url)
    
    return response

def run_request_extract(response):
    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Since the data is CSV, we'll use StringIO to read it into a DataFrame
            csv_data = StringIO(response.text)  # Convert the string response to a file-like object
            
            # Load the CSV data into a DataFrame
            df = pd.read_csv(csv_data)
            
            # Display the first few rows of the DataFrame
            #print(df.head())
        
        except ValueError as e:
            # Handle error if unable to read the CSV
            print("Error reading CSV:", e)
            print("Response text:", response.text)  # Inspect the actual response content
    else:
        print(f"Error: Received status code {response.status_code}")
        print("Response content:", response.text)  # Inspect the raw response content
    return df

def transformation(df):
    df.columns = df.columns.str.strip()  # Strip any leading/trailing spaces from column names
    df = df.drop('delistingDate', axis=1, errors='ignore')  # Avoid errors if column isn't found
    df['ipoDate'] = pd.to_datetime(df['ipoDate'], errors='coerce') # Turns ipoDate from a str into a datetime
    return df
"""
def remove_delisting_col(df):
    
    return df

def ipoDate_to_date(df):
    
    return df

"""
def csv_output(df):
    filepath = Path()
    filename = 'transformed_cleaned.csv'

    output_dir = df.to_csv(filepath / filename)

    return df, output_dir


def load_snowflake():
    # Snowflake credentials
    conn = snowflake.connector.connect(
        user="YOUR_USERNAME",
        password="YOUR_PASSWORD",
        account="YOUR_ACCOUNT",  # E.g., 'xyz123.snowflakecomputing.com'
        warehouse="YOUR_WAREHOUSE",
        database="YOUR_DATABASE",
        schema="YOUR_SCHEMA"
    )

    print("Connected to Snowflake!")

    """
    create_table_query = 
    # three " here
    CREATE TABLE IF NOT EXISTS your_table_name (
        symbol STRING,
        name STRING,
        exchange STRING,
        assetType STRING,
        ipoDate DATE,
        delistingDate DATE,
        status STRING
    );
    # three " here
    cur = conn.cursor()
    cur.execute(create_table_query)
    conn.commit()
    print("Table checked/created.")

    """
    pass

def main():
    first_auth = auntenticate(API_KEY)
    requests_extract = run_request_extract(first_auth)
    t_etl = transformation(requests_extract)
    csv_excel = csv_output(t_etl)

    #csv_excel = csv_output(to_date)
        
    #print df
    print(csv_excel)
    
if __name__ == "__main__":
    main()