import requests, yaml, logging, pandas as pd
from supabase import create_client, Client
from pathlib import Path
from io import StringIO  # To handle CSV data in memory

logger = logging.getLogger()
FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger.setLevel(logging.INFO)




def get_config():
    """ Load the YAML config file """
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config
config = get_config()


def auntenticate(API_KEY):
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
    return df

def csv_output(df):
    filepath = Path()
    filename = 'transformed_cleaned.csv'

    output_dir = df.to_csv(filepath / filename)

    return df, output_dir


def load_supabase():
    # Supabase credentials
    url = config['supabase']['url']
    key = config['supabase']['anon_public']
    supabase: Client = create_client(url, key)
    print("Connected to Supabase!")

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