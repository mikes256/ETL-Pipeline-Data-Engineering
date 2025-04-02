import requests, yaml, logging, pandas as pd
from supabase import create_client
from pathlib import Path
from io import StringIO

""" Create logger """
logger = logging.getLogger()
FORMAT = 'Msg: %(message)s\nFunc: %(funcName)s\nLogLevel: %(levelname)s\nTimestamp: %(asctime)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger.setLevel(logging.INFO)

def get_config():
    """ Load the config file """
    try:
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logging.error(f"Error loading config file: {e}")
        raise 
config = get_config()

def auntenticate():
    """ Authenticate Alpha Vantage URL """
    try:
        # Request for S&P 500 list
        url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={config['api']['api_key']}"
        response = requests.get(url)
        if response.status_code != 200:
            logging.error(f"Failed to get data from Alpha Vantage. Status code: {response.status_code}")
            raise ValueError(f"Error: Received status code {response.status_code}")
        return response
    except Exception as r:
        logging.error(f"Error authenticating Alpha Vantage URL: {r}")
        raise

def run_request_extract(response):
    """ Extract API request & read request as a pd.df """
    try:
        if response.status_code == 200:
            csv_data = StringIO(response.text)  # Convert the string response to a file-like object
            df = pd.read_csv(csv_data)
            return df
        else:
            raise ValueError(f"Error: Received status code {response.status_code}")
    except ValueError as e:
        logging.error(f"Error reading CSV: {e}")
        raise
    except Exception as e:
        logging.error(f"Error during extraction: {e}")
        raise   

def transformation(df):
    """ Transormation in ETL """
    try:
        df.columns = df.columns.str.strip()  # Strip any leading/trailing spaces from column names
        df = df.drop('delistingDate', axis=1, errors='ignore')  # Avoid errors if column isn't found
        df['ipoDate'] = pd.to_datetime(df['ipoDate'], errors='coerce')
        df['lastrun_timestamp'] = pd.Timestamp.now()
        df['lastrun_timestamp'] = df['lastrun_timestamp'].astype(str)
        df.columns = df.columns.str.lower()
        return df
    except Exception as m:
        logging.error(f"Err in transformation occurred due to: {m}")

def csv_output(df):
    """ Save df as .csv output """
    try:
        filepath = Path('cleaned_output_csv')
        filepath.mkdir(parents=True, exist_ok=True)
        filename = 'transformed_cleaned.csv'
        df.to_csv(filepath / filename, index=False)
        logger.info(f"Transformed data saved to {filepath / filename}\n")
        return df
    except Exception as s:
        logging.warning(f"Error with the .csv output: {s}")

def load_supabase(df):
    """ Authenticate Supabase and load into table """
    try:
        supabase = create_client(config['supabase']['url'], config['supabase']['anon_public'])
        logging.info("Connected to Supabase!\n")
        df = df.astype(str)
        data_list = df.to_dict(orient="records")  # Convert DataFrame to a list of dictionaries
        return supabase, data_list
    except Exception as e:
        logging.error(f"Failed to authenticate Supabase: {e}")
        raise

def batch_supabase_insert(data_list, supabase):
    """ Batch insert into Supabase """
    batch_size = 2500  # Adjust batch size based on performance
    try:
        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i + batch_size]
            logging.info(f"Inserted rows {i} to {i + batch_size}")
            response = supabase.table("practice_etl_mike").upsert(batch).execute()
        logging.info("✅ Data loaded into Supabase successfully!")
        return response
    except Exception as k:
        logging.error(f"Failed to insert rows into supabase: {k}")

def main():
    """ Call every function into a main() """
    try:
        first_auth = auntenticate()
        requests_extract = run_request_extract(first_auth)
        t_etl = transformation(requests_extract)
        csv_excel = csv_output(t_etl)
        supabase, data_list = load_supabase(csv_excel)
        batch_supabase_insert(data_list, supabase)
        print(csv_excel.sample(3))
        logging.info("\nETL process completed successfully!")
    except Exception as e:
        logging.error(f"ETL process failed: {e}")
        raise

if __name__ == "__main__":
    logging.critical("\nStarting script...\n")
    main()
    logging.critical("\nScript completed successfully!")