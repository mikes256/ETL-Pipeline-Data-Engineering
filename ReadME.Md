# Project: Building an ETL Pipeline for Stock Market Data (Yahoo Finance → Snowflake)

## Goal: Extract stock market data, transform it in Python, and load it into Snowflake for analytics.

## Project Outline
## 1. Extract Data (Yahoo Finance API)
Use yfinance to fetch historical stock data (e.g., Apple, Tesla).
Save raw data in a structured format (CSV or DataFrame).
## 2. Transform Data (Python & Pandas)
Clean column names, handle missing data, and standardize date formats.
Normalize data into different tables:
stocks (ticker, company name)
date_dimension (date, year, quarter, month)
stock_prices (ticker, date, open, close, volume)
## 3. Load Data (Snowflake Python Connector)
Connect to Snowflake using Python.
Create necessary tables in Snowflake (if they don’t exist).
Load transformed data into Snowflake.
## 4. Automate the Pipeline
Schedule the ETL job using Apache Airflow or a simple cron job.
## 5. Optional - Query & Analyze in Snowflake
Write SQL queries to analyze trends (e.g., moving averages, daily returns).

## Tech Stack Used
✅ Python (requests, pandas, yfinance)  
✅ Snowflake (storage & querying)   
✅ Snowflake Python Connector (to load data)    
✅ Airflow (Optional) (for orchestration)


### Why This Project?

Teaches real-world ETL concepts.
Helps you practice data modeling (normalizing stock data).
Uses Python for both data transformation & loading (AE + DE skills).
Gets you comfortable with Snowflake + Python connectors before dbt.


## Purpose


## Prerequisite

## Automation

## Config file

## 