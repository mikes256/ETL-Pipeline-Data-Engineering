import requests
import pandas as pd
import yaml
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
            print(df.head())
        
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
    df.head()
    return df

def main():
    first_auth = auntenticate(API_KEY)
    requests_extract = run_request_extract(first_auth)
    see_df = dataFrame_head(requests_extract)
    
    #print df
    print(see_df)
    
if __name__ == "__main__":
    main()


"""
1. Create updated: pip freeze > requirements.txt
    
"""