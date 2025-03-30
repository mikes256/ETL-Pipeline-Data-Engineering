import requests, yaml, logging, pandas as pd
from supabase import create_client, Client
from pathlib import Path
from io import StringIO  # To handle CSV data in memory

logger = logging.getLogger()
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger.setLevel(logging.INFO)


def get_config():
    """ Load the YAML config file """
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config
config = get_config()


def auntenticate():
    #ADD A TRY BLOCK. 

    # Request for S&P 500 list (this endpoint gives you the entire listing)
    url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={config['api']['api_key']}"

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
            logging.error(f"Error reading CSV:", {e})
            raise
        except Exception as m:
            logging.error("Response text:", response.text,f"\nErr: {m}")  # Inspect the actual response content
            raise
    else:
        print(f"Error: Received status code {response.status_code}")
        print("Response content:", response.text)  # Inspect the raw response content
    return df

def transformation(df):
    df.columns = df.columns.str.strip()  # Strip any leading/trailing spaces from column names
    df = df.drop('delistingDate', axis=1, errors='ignore')  # Avoid errors if column isn't found
    df['ipoDate'] = pd.to_datetime(df['ipoDate'], errors='coerce') # Turns ipoDate from a str into a datetime
    df['LastRun_Timestamp'] = pd.Timestamp.now()#.strftime("%d/%m/%Y-%I:%M:%S")

    return df

def csv_output(df):
    filepath = Path()
    filename = 'transformed_cleaned.csv'
    df.to_csv(filepath / filename, index=False)
    return df


def load_supabase(df):
    # Supabase credentials
    url = config['supabase']['url']
    key = config['supabase']['anon_public']    

    # Create Supabase client
    supabase = create_client(url, key)
    print("Connected to Supabase!\n")

    # Define the CREATE TABLE query to ensure the table exists
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS practice_etl_mike (
        assetType TEXT,
        ipoDate DATE,
        name TEXT,
        status TEXT,
        LastRun_Timestamp TIMESTAMP,
        symbol TEXT,
        exchange TEXT
    );
    """
    try:
        # Execute the SQL query to create the table if it doesn't exist
        supabase.rpc(create_table_sql).execute()
        print("Table 'practice_etll' is ready or already exists.")
    except Exception as e:
        print(f"Error while creating table: {e}")

    df = df.astype(str) 
    data_list = df.to_dict(orient="records")
     
    return data_list, supabase

def batch_supabase_insert(data_list, supabase):
    # Batch insert into Supabase
    batch_size = 2000  # Adjust batch size based on performance
    for i in range(0, len(data_list), batch_size):
        batch = data_list[i:i + batch_size]
        print(f"Inserted rows {i} to {i + batch_size}")
        response = supabase.table("practice_etl").insert(batch).execute()
    print("✅ Data loaded into Supabase successfully!")

    return response


def main():
    first_auth = auntenticate()
    requests_extract = run_request_extract(first_auth)
    t_etl = transformation(requests_extract)
    csv_excel = csv_output(t_etl)
    supabase, response = load_supabase(csv_excel)
    insert_supabase = batch_supabase_insert(supabase, response)
    
    print(csv_excel.head(3))
    
if __name__ == "__main__":
    print("\nStarting script...\n")
    main()
    print("\nScript completed successfully!")