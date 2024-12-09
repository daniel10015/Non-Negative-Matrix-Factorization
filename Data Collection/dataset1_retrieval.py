import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from time import time
from requests import JSONDecodeError
from random import random

starting_time = time()

# Global cache for storing ticker data
ticker_cache = {}

# Helper function for retry logic
def retry(func, ticker, start, end, retries=3, delay=2):
    for i in range(retries):
        try:
            dat = func(ticker, start, end)
            #print(dat)
            return dat
        except JSONDecodeError as e:
            print(f"JSONDecodeError on attempt {i + 1}: {e}")
            sleep(delay*i*(1+random()))
        except Exception as e:
            print(f"Error on attempt {i + 1}: {e}")
            wait_time_seconds = 5
            print(f"sleeping for {wait_time_seconds} seconds...")
            starting_thread_timer = time()
            curr_time = 0
            while int(time()-starting_thread_timer) < wait_time_seconds:
                sleep(1)
                if int(curr_time) < int(time()):
                    curr_time = time()
                    print(f"{int(curr_time-starting_thread_timer)}/{wait_time_seconds} seconds")
            print("waiting another few seconds...")
            sleep(delay*i*(1+random()))
    return None

# Function to fetch data for a single ticker
def fetch_ticker_data(ticker, start_date, end_date):
    # Check cache first
    if ticker in ticker_cache:
        #print(f"Using cached data for ticker: {ticker}")
        return ticker, ticker_cache[ticker]

    # Fetch data if not in cache
    try:
        ticker_formatted = ticker.replace(".", "-")
        #print(f"ticker: {ticker_formatted}")
        stock_data = retry(
            yf.download,
            ticker=ticker_formatted,  # First argument as keyword
            start=start_date,
            end=end_date,
            retries=3,
            delay=2,
        )
        
        if stock_data is None or stock_data.empty:
            #print(f"No data for {ticker}. Skipping...")
            return ticker, None

        # Store in cache
        ticker_cache[ticker] = stock_data['Close']
        #print(f"Successfully fetched data for: {ticker}")
        return ticker, stock_data['Close']

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return ticker, None


# Fetch and process data with multithreading
def fetch_all_data(tickers, start_date, end_date):
    data = {}
    failed_tickers = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        results = executor.map(fetch_ticker_data, tickers, [start_date] * len(tickers), [end_date] * len(tickers))
    for ticker, close_data in results:
        if close_data is not None:
            data[ticker] = close_data
        else:
            failed_tickers.append(ticker)
    return data, failed_tickers

# Scrape tickers for all markets
def scrape_market_tickers(url, ticker_column_index):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    return [
        row.find_all('td')[ticker_column_index].text.strip()
        for row in soup.select('table tbody tr')
        if len(row.find_all('td')) > ticker_column_index
    ]

# URLs for different markets
market_sources = {
    "sp500": {
        "url": "https://stockanalysis.com/list/sp-500-stocks/",
        "ticker_column_index": 1
    },
    "nasdaq": {
        "url": "https://stockanalysis.com/list/nasdaq-stocks/",
        "ticker_column_index": 1
    },
    "nyse": {
        "url": "https://stockanalysis.com/list/nyse-stocks/",
        "ticker_column_index": 1
    },
    "penny": {
        "url": "https://stockanalysis.com/list/penny-stocks/",
        "ticker_column_index": 1
    },
    "mutual fund": {
        "url": "https://stockanalysis.com/list/mutual-funds/",
        "ticker_column_index": 1
    },
    "large cap stocks": {
        "url": "https://stockanalysis.com/list/large-cap-stocks/",
        "ticker_column_index": 1
    },
    "mid cap stocks": {
        "url": "https://stockanalysis.com/list/mid-cap-stocks/",
        "ticker_column_index": 1
    },
    "small cap stocks": {
        "url": "https://stockanalysis.com/list/small-cap-stocks/",
        "ticker_column_index": 1
    },
    "micro cap stocks": {
        "url": "https://stockanalysis.com/list/small-cap-stocks/",
        "ticker_column_index": 1    
    },
    "australian ase": {
        "url": "https://stockanalysis.com/list/australian-securities-exchange/",
        "ticker_column_index": 1
    }
}

# Main script execution
if __name__ == "__main__":
    day_range = 1000 # 1000  # About 4-5 years of data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=day_range)

    # Fetch tickers for all markets
    tickers_by_market = {
        market: scrape_market_tickers(config["url"], config["ticker_column_index"])
        for market, config in market_sources.items()
    }

    store_tickers = True
    if store_tickers:
        # Transform the dictionary into a DataFrame
        df = pd.DataFrame.from_dict(tickers_by_market, orient="index").transpose()

        # Rename columns for better readability
        df.columns.name = "Market"
        df.index.name = "Row"

        # Save to CSV (optional)
        df.to_csv("Data/tickers.csv", index=True)

        # Print DataFrame to console then quit
        print(df)
        exit(0)
    
    
    # Process each market
    output_dir = "Data/Dataset1_MoreMarkets_MoreTime"
    os.makedirs(output_dir, exist_ok=True)

    all_market_data = {}
    all_failed_tickers = {}
    first_market = True
    market_down_time = int(5*60) # wait 5 minutes between market
    for market, tickers in tickers_by_market.items():
        print(f"Processing market: {market.upper()}")
        if not first_market:
            print(f"wait {market_down_time//60} minutes, {market_down_time%60} seconds")
            curr_time = 0
            starting_thread_timer = time()
            wait_time_seconds = market_down_time
            while int(time()-starting_thread_timer) < wait_time_seconds:
                sleep(1)
                if int(curr_time) < int(time()):
                    curr_time = time()
                    print(f"{int(curr_time-starting_thread_timer)}/{wait_time_seconds} seconds")
        first_market = False
        
        market_data, failed_tickers = fetch_all_data(tickers, start_date, end_date)
        print(f"failed tickers ({len(failed_tickers)}): {failed_tickers}")

        # Filter valid data
        valid_data = {ticker: data for ticker, data in market_data.items() if data is not None}

        # Debugging: Print invalid entries
        # Ensure TSLA is in market_data before accessing it
        """
        if 'TSLA' in market_data:
            print(f"tesla data: {market_data['TSLA']}")
        else:
            print("TSLA data is not present in market_data.")
        for ticker, data in market_data.items():
            if not isinstance(data, pd.Series):
                print(f"Invalid data for ticker: {ticker}, type: {type(data)}")
            elif data.empty:
                print(f"Empty data for ticker: {ticker}")
        """

        valid_data = {}
        for ticker, data in market_data.items():
            # If the data is already a pd.Series, use it
            #print(f"ticker: {type(data)} ;\n{data}")
            valid_data[ticker] = data 
            """
            if isinstance(data, pd.Series) and not data.empty:
                valid_data[ticker] = data
            # If the data is a DataFrame, extract the relevant column (e.g., 'Close')
            elif isinstance(data, pd.DataFrame) and 'Close' in data.columns:
            # If the data is scalar, convert it to a pd.Series
            elif isinstance(data, (int, float, str)):
                valid_data[ticker] = pd.Series([data])
            else:
                print(f"Invalid data for ticker: {ticker}, type: {type(data)}")
            """

        # Check if there is valid data before creating DataFrame
        # Concatenate all DataFrames in valid_data
        if valid_data:
            # Concatenate all DataFrames along columns (axis=1)
            all_market_data[market] = pd.concat(valid_data.values(), axis=1)
            
            # If you want to reset the index and make Date a regular column (optional)
            all_market_data[market].reset_index(inplace=True)
        else:
            print(f"No valid data available for market: {market}")

        
        # Create DataFrame
        # print(f"valid_data: {valid_data}")
        # print(f"market: {market}")
        # all_market_data[market] = pd.DataFrame(valid_data) 
        # all_failed_tickers[market] = failed_tickers

    # Truncate data to the greatest lower bound (GLB)
    min_days = min(df.shape[0] for df in all_market_data.values() if not df.empty)
    print(f"minimum days: {min_days}")
    all_market_data = {market: df.iloc[-min_days:] for market, df in all_market_data.items() if not df.empty}

    # Save consolidated data
    for date in pd.date_range(start=start_date, end=end_date):
        date_str = date.strftime('%Y-%m-%d')
        # print(date)
        print(f"date string: {date_str}")
        for market, df in all_market_data.items():
            print(f"df:\n{df['Date']}")
            rows = df.query(f'Date == "{date_str}"')
            print(f"row: {type(rows)}")
        filtered_data = {
            market: df.query(f'Date == "{date_str}"') for market, df in all_market_data.items() if not df.query(f'Date == "{date_str}"').empty
        }

        # stock market not open
        if not filtered_data:
            continue
        print(f"filtered data: {filtered_data}")

        # Remove the `Date` column and transpose to get rows as stock prices
        aligned_data = {
            market: df.drop(columns=['Date']).T.reset_index(drop=True) for market, df in filtered_data.items()
        }

        # Combine into a single DataFrame where each column is a market
        combined_df = pd.concat(aligned_data, axis=1)
        combined_df.columns = aligned_data.keys()  # Set market names as column headers

        print(f"before dropping NaN's {combined_df.to_string()}")

        combined_df = combined_df.dropna(how='any')
        
        #print(f"after dropping NaN's {combined_df.to_string()}")



        if not combined_df.empty:
            print(f"writing {combined_df}\n-----\nto {output_dir}/{date_str}.csv")
            combined_df.to_csv(os.path.join(output_dir, f"{date_str}.csv"), index_label="Ticker")

    # Output failed tickers for debugging
    print("\nFailed to fetch data for the following tickers:")
    for market, tickers in all_failed_tickers.items():
        print(f"{market.upper()}: {tickers}")

    print("Processing complete. Data saved.")

total_time = int(time() - starting_time) 
print(f"----------\nTime taken: {total_time//60} minutes, {total_time%60} seconds.")