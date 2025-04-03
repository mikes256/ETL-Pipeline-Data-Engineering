# Project: Building an ETL Pipeline for S&P 500 Data (Alpha Vantage API → Python ETL → Supabase db)
## Purpose

#### Extract
![alt text](image001.png)


#### Transform
![alt text](pypy.avif)

#### Load
![alt text](logo-light.png)

This ETL project automates the extraction, transformation, and loading (ETL) of S&P 500 data from Alpha Vantage into the Supabase cloud database for further querying and analysis.

- **_E_**: The data is fetched via an API request from Alpha Vantage.
- **_T_**: It is transformed in Python using Pandas to clean, structure, and enhance data quality.
- **_L_**: The final dataset is stored in Supabase for analytics and visualization.
- A .csv backup is saved in a local subdirectory for redundancy and disaster recovery.

This repository provides a reproducible and scalable ETL workflow, allowing future developers to fork, modify, and extend the project for their own use cases.


## Prerequisite
To run this script successfully you must have the following:
1. [Alpha Vantage API token](https://www.alphavantage.co/documentation/)
2. [Supabase API token & URL](https://supabase.com/docs/guides/api)


## Config file
Modify the content of your config file accordingly. I have listed the relevant values required to fill in to run the script.    

Below is for further guidance on how to fill out your config file. Anything wrapped in "<input:...>" required data to be parsed in:
```yml
api:
    api_key: <input: YOUR ALPHA VANTAGE API TOKEN>

supabase:
    api_name: <input: YOUR SUPABASE API NAME>
    api: <input: YOUR SUPABASE API>
    url: <input: YOUR SUPABASE PROJECT URL>
    anon_public: <input: YOUR SUPABASE PROJECT API>
```


## End to End Automation
While this project does not currently use full end to end automation, the ETL script can still be automated using:
- Apache Airflow
- Cron Jobs
- Task Scheduler
- Cloud-based scheduling tools


## Virtual Environment
Please use a virtual environment when running this script. This helps contain your code in a safer, organised, optimised environment with better security controls and reduces conflicts with other projects.


Your virtual environment should look like this, if set up correctly.
```
TERMINAL: >source venv/bin/activate
(venv) TERMINAL: >
```
### venv/myenv
![alt text](python-conda.png)   
To run a conda virtual environment [click here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).  
To run a python virtual environment [click here](https://docs.python.org/3/library/venv.html).


## Functionality
Alpha Vantage have a list of different api endpoints you can connect to. These can be instantiated by coupling your Alpha Vantage username and API token.   
The output is a cleaned transformed ```.csv``` you can use for further analytics and have stored for safe keeping on your local pc/environment.

The code improves reporting and gets close to real time reporting as possible, if there are any updates or new rows, the code will be refreshed. By eliminating the need to extract a sizeable excel file and manually transform the S&P 500 data to fit your reporting critera, then ingest the data into your BI tool or database of choice.     
This script replaces all of these mundane steps at either the click of one button or you can programme the script with ```cron```, ```task scheduler``` or ```apache airflow``` to run on a particular cadence. 


## Library Dependecy Update
To install all necessary packages listed in the [requirements.txt](https://github.com/mikes256/ETL-Pipeline-Data-Engineering/blob/main/requirements.txt) follow the below terminal/command line prompts.
```ruby
(venv) TERMINAL: >pip install -r requirements.txt
(venv) TERMINAL: >pip install pip-tools
(venv) TERMINAL: >pip sync     #helps with package dependencies
```
### Conflicting packages update 
Step by step instructions for managing package dependencies and ensuring there are no conflicting libraries, ultimately futureproofing this ETL project.    
Follow [this link](https://github.com/mikes256/ETL-Pipeline-Data-Engineering/blob/main/Updating_Libraries.md) for detailed instructions.

## Who can run the code
Anyone interested in running and understanding the code behind this ETL project or thinks they can improve the code.    
Additionally, this code is tailored for data analysts, junior data engineers, analytics engineers, data scientists and programmers who are intersted in ETL projects. 

You are strongly advised to run the code in a virtual environment and install all packages in the [requirements.txt](https://github.com/mikes256/ETL-Pipeline-Data-Engineering/blob/main/requirements.txt) in a venv/myenv for dependencies and optimal processing speed by only installing the necessary packages.



### Features
- Automates the ETL Process: Extracts, transforms, and loads S&P 500 data from the Alpha Vantage API endpoint
- Near-Real-Time Reporting: Provides batch reporting and updates into the cloud database Supabase
- Cleaned and Transformed Data: Outputs processed data in a structured format for easy analysis.
- Simplifies Reporting: Reduces manual data preparation by automating the entire process with a single command or scheduled run.

## Data Quality
**1. Column Name Standardisation**
- Trimmed leading and trailing spaces from column names.
- Converted all column names to lowercase to maintain consistency and avoid schema conflicts.

**2. Handling Missing & Invalid Data**
- Used ```errors='coerce'``` while converting ipoDate to datetime, ensuring invalid dates were handled gracefully.
- Dropped the ['delistingDate'] column, preventing unnecessary processing of outdated records and this column was filled with NaN.

**3. Ensuring Data Type Consistency**
 - Converted ['ipoDate'] to pd.datetime to allow proper date filtering and analysis.
- Converted the entire dataset to string format before inserting into Supabase to prevent type mismatches.

**4. Tracking Data Refreshes**
- Added a ['LastRun_Timestamp'] column to track when the data was last updated.
- Ensured every ETL run adds a new timestamp to monitor data freshness.

**5. Uniqueness & Constraint Handling**
- Added a primary key (id) to uniquely identify records.
- Created a unique constraint on (symbol, exchange) to prevent duplicate stock entries.
- Used ```on_conflict=['symbol', 'exchange']``` in Supabase to update records when needed instead of duplicating data.

**6. Error Handling & Logging**
- Implemented try-except blocks in all major functions to catch errors gracefully.
- Used logging (logger.info, etc.) to track script execution and debug issues.

**7. Efficient Data Loading**
- Converted the dataframe to a list of dictionaries for optimized batch inserts into Supabase.
- Implemented batch inserts (2500 rows per batch) to improve performance and avoid API rate limits.


## Security Reminder
- Never share your ```config``` file publicly or commit it to ```git```
- Use ```.gitignore``` to exclude ```config``` from being staged and tracked by ```git```
- Keep your API token encrypted and safely kept, do not share your API token with anyone.


## Tech Stack Used
✅ Python (requests, pandas, yaml)
✅ SQL (PostgreSQL for creating Supabase tables)  
✅ Supabase (storage & querying)   
✅ Apache Airflow (Optional) (for orchestration)