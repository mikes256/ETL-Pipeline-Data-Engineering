import requests, yaml, pandas as pd
from pathlib import Path
from io import StringIO  # To handle CSV data in memory

def get_config():
    # Load the YAML file
    with open('config.yml', 'r') as file:
        config = yaml.safe_load(file)
    return config
config = get_config()

# Global constants
API_KEY = config['api']['api_key']

def auntenticate(API_KEY):
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

def dataFrame_head(df):
    df.columns = df.columns.str.strip()  # Strip any leading/trailing spaces from column names
    return df

def remove_delisting_col(df):
    df = df.drop('delistingDate', axis=1, errors='ignore')  # Avoid errors if column isn't found
    
    return df

def ipoDate_to_date(df):
    df['ipoDate'] = pd.to_datetime(df['ipoDate'], errors='coerce')
    
    return df


def csv_output(df):
    filepath = Path()
    filename = 'transformed_cleaned.csv'

    output_dir = df.to_csv(filepath / filename)

    return df, output_dir


def main():
    first_auth = auntenticate(API_KEY)
    requests_extract = run_request_extract(first_auth)
    see_df = dataFrame_head(requests_extract)
    remove_col = remove_delisting_col(see_df)
    to_date = ipoDate_to_date(remove_col)
    csv_excel = csv_output(to_date)
        
    #print df
    print(csv_excel)
    
if __name__ == "__main__":
    main()