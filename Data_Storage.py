import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from PT_Data import processed_df


password = quote_plus("YourPass")
DATABASE_URI = f"postgresql://postgres:{password}@localhost:5432/market_data"
engine = create_engine(DATABASE_URI)

def store_data(df):
    df.to_sql('historical_data', engine, if_exists='append', index=False)
    print("Data stored successfully!")

store_data(processed_df)

