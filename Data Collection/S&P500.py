import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import requests
from bs4 import BeautifulSoup
import os
from time import time

# Generalized scraper for tickers
def scrape_market_tickers(url, ticker_column_index):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    tickers = []
    
    for row in soup.select('table tbody tr'):
        cells = row.find_all('td')
        if cells and len(cells) > ticker_column_index:
            ticker = cells[ticker_column_index].text.strip()
            tickers.append(ticker)
    
    return tickers

# URLs for different markets
market_sources = {
    "sp500": {
        "url": "https://stockanalysis.com/list/sp-500-stocks/",
        "ticker_column_index": 1  # Adjust based on the table structure
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
    }
}

start_time = time()

# Fetch tickers for all markets
tickers_by_market = {}
for market, config in market_sources.items():
    print(f"Scraping {market.upper()} tickers...")
    tickers_by_market[market] = scrape_market_tickers(config["url"], config["ticker_column_index"])
    print(f"Found {len(tickers_by_market[market])} tickers for {market.upper()}.")




day_range = 1000 # about 4-5 years, though not all stocks will have data that far back
end_date = datetime.now()
start_date = end_date - timedelta(days=day_range)
missing_stocks = []

# Function to fetch EOD data
def fetch_eod_prices(tickers, start_date, end_date):
    data = {}
    tickerCount = len(tickers)
    currTicker = 1
    for ticker in tickers:
        ticker = ticker.replace(".","-")
        try:
            print(f"Fetching data for {ticker}...")
            stock_data = yf.download(ticker, start=start_date, end=end_date)
            if not stock_data.empty:  # Ensure we only add tickers with data
                data[ticker] = stock_data['Close']
            else:
                print(f"No data for {ticker}. Skipping...")
                missing_stocks.append(ticker)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
        print(f"{currTicker}/{tickerCount}")
        currTicker += 1
    #print(pd.DataFrame(data))
    #print(data.get('AMZN'))
    df = []
    if data:  # Ensure the data dictionary is not empty
        for tick in tickers:
            df.append( pd.DataFrame(data.get(tick)) )
            
        return df
    else:
        print("No valid data fetched. Returning an empty DataFrame.")
        return pd.DataFrame()


# Fetch and save EOD prices for each market
output_dir = "Data/dataset 1"
os.makedirs(output_dir, exist_ok=True)

for market, tickers in tickers_by_market.items():
    print(f"Fetching EOD prices for {market.upper()}...")
    eod_prices = fetch_eod_prices(tickers, start_date, end_date)
    file_path = f"Data/dataset 1/{market}"
    os.makedirs(file_path, exist_ok=True)
    if len(eod_prices)>0:
        for eod_price in eod_prices:
            ticker = ""
            for label, data in eod_price.items():
                if not label == "Date":
                    ticker = label
                    break
            eod_price.to_csv(file_path + "/" + ticker + ".csv")
        print(f"Saved EOD prices for {market.upper()} to {file_path}")

totalTime = int(time()-start_time)
print(f"total time taken: {totalTime//60} minutes, {totalTime%60} seconds")

print(f"\nTotal missing stocks: ({len(missing_stocks)}: \n{missing_stocks}")