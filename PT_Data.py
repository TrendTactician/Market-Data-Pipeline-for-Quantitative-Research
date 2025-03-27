from datetime import datetime
from Historical_Data import fetch_historical_data
import pandas as pd

def process_data(df, symbol):
    # Convert timestamp columns from milliseconds to datetime
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
    
    # Convert price and volume columns to numeric types
    numeric_cols = ['open', 'high', 'low', 'close', 'volume', 
                    'quote_asset_volume', 'taker_buy_base_asset_volume', 
                    'taker_buy_quote_asset_volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Add the 'symbol' column with the provided value
    df['symbol'] = symbol
    
    # Select only the necessary columns
    df = df[['open_time', 'symbol', 'open', 'high', 'low', 'close', 'volume']]
    df.rename(columns={'open_time': 'date'}, inplace=True)
    
    # Sort data by date (ascending order)
    df.sort_values('date', inplace=True)
    
    return df

# Fetch the historical data
historical_df = fetch_historical_data()  # Ensure this function is defined and returns a DataFrame

# Process the data with the specified symbol
processed_df = process_data(historical_df, 'BTCUSDT')

print(processed_df.head())
print(processed_df.dtypes)
