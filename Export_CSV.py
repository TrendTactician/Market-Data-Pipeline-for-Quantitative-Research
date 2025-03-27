from Historical_Data import fetch_historical_data
from PT_Data import process_data
import os

historical_df = fetch_historical_data(symbol='BTCUSDT')
processed_df = process_data(historical_df, 'BTCUSDT')
processed_df.to_csv("historical_data.csv", index=False)
print("CSV saved to:", os.getcwd())
