import requests
import pandas as pd
from datetime import datetime

def fetch_historical_data(symbol='BTCUSDT', interval='1d', limit=10000):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        raw_data = response.json()
        # Binance returns data as a list of lists.
        columns = [
            'open_time', 'open', 'high', 'low', 'close', 'volume', 
            'close_time', 'quote_asset_volume', 'num_trades', 
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ]
        df = pd.DataFrame(raw_data, columns=columns)
        return df
    else:
        print("Error fetching data:", response.status_code)
        return pd.DataFrame()

def process_data(df, symbol="BTCUSDT"):
    # Convert timestamp columns from milliseconds to datetime
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    
    # Convert numeric columns to proper data types
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Add the symbol column BEFORE selecting final columns
    df['symbol'] = symbol
    
    # Select only the necessary columns including symbol
    df = df[['open_time', 'open', 'high', 'low', 'close', 'volume', 'symbol']]
    
    # Rename and sort as needed
    df.rename(columns={'open_time': 'date'}, inplace=True)
    df.sort_values('date', inplace=True)
    return df

if __name__ == "__main__":
    # Fetch data (Step 1)
    historical_df = fetch_historical_data(symbol='BTCUSDT')
    if historical_df.empty:
        print("No data fetched.")
    else:
        # Process data (Step 2) and verify the symbol column
        processed_df = process_data(historical_df, symbol='BTCUSDT')
        print(processed_df.head())
        print("Columns:", processed_df.columns.tolist())
