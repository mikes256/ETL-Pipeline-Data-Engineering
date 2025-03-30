import requests
import yaml
import logging
import pandas as pd
from supabase import create_client
from pathlib import Path
from io import StringIO  # To handle CSV data in memory

# Create logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Load the YAML config file
def get_config():
    """ Load the YAML config file """
    try:
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logger.error(f"Error loading config file: {e}")
        raise

config = get_config()

def authenticate():
    """ Authenticate Alpha Vantage URL """
    try:
        # Request for S&P 500 list
        url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={config['api']['api_key']}"
        response = requests.get(url)  # Make the API request
        if response.status_code != 200:
            logger.error(f"Failed to get data from Alpha Vantage. Status code: {response.status_code}")
            raise ValueError(f"Error: Received status code {response.status_code}")
        return response
    except Exception as r:
        logger.error(f"Error authenticating Alpha Vantage URL: {r}")
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
        logger.error(f"Error reading CSV: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during extraction: {e}")
        raise

def transformation(df):
    """ Transformation in ETL """
    try:
        df.columns = df.columns.str.strip()  # Strip any leading/trailing spaces from column names
        df = df.drop('delistingDate', axis=1, errors='ignore')  # Avoid errors if column isn't found
        df['ipoDate'] = pd.to_datetime(df['ipoDate'], errors='coerce')  # Convert ipoDate to datetime
        df['LastRun_Timestamp'] = pd.Timestamp.now()
        df['LastRun_Timestamp'] = df['LastRun_Timestamp'].astype(str)  # Convert to string
        return df
    except Exception as e:
        logger.error(f"Error in transformation occurred: {e}")
        raise

def csv_output(df):
    """ Save to CSV output """
    try:
        filepath = Path('output')  # Use a dedicated folder for output
        filepath.mkdir(parents=True, exist_ok=True)  # Ensure the folder exists
        filename = 'transformed_cleaned.csv'
        df.to_csv(filepath / filename, index=False)
        logger.info(f"Transformed data saved to {filepath / filename}")
        return df
    except Exception as e:
        logger.error(f"Error with the .csv output: {e}")
        raise

def load_supabase(df):
    """ Authenticate Supabase and load into table """
    try:
        supabase = create_client(config['supabase']['url'], config['supabase']['anon_public'])
        logger.info("Connected to Supabase!\n")
        df = df.astype(str)  # Ensure all data is in string format for insertion
        data_list = df.to_dict(orient="records")  # Convert DataFrame to a list of dictionaries
        return supabase, data_list
    except Exception as e:
        logger.error(f"Failed to authenticate Supabase: {e}")
        raise

def batch_supabase_insert(data_list, supabase):
    """ Batch insert into Supabase """
    batch_size = 2500  # Adjust batch size based on performance
    try:
        for i in range(0, len(data_list), batch_size):
            batch = data_list[i:i + batch_size]
            logger.info(f"Inserting rows {i} to {i + batch_size}")
            response = supabase.table("practice_etl_mike").upsert(batch).execute()
            if response.status_code != 200:
                logger.error(f"Error inserting batch {i} to {i + batch_size}: {response.text}")
            else:
                logger.info(f"Batch {i} to {i + batch_size} inserted successfully")
        logger.info("✅ Data loaded into Supabase successfully!")
    except Exception as e:
        logger.error(f"Error inserting data into Supabase: {e}")
        raise

def main():
    """ Main function to run all steps """
    try:
        # Run the ETL pipeline
        first_auth = authenticate()
        extracted_data = run_request_extract(first_auth)
        transformed_data = transformation(extracted_data)
        csv_data = csv_output(transformed_data)
        supabase, data_list = load_supabase(csv_data)
        batch_supabase_insert(data_list, supabase)

        # Print a sample of the data
        print(csv_data.sample(3))
        logger.info("\nETL process completed successfully!")
    except Exception as e:
        logger.error(f"ETL process failed: {e}")
        raise

if __name__ == "__main__":
    logger.info("\nStarting script...\n")
    main()
    logger.info("\nScript completed successfully!")
