from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Import functions from your modules
from Historical_Data import fetch_historical_data
from PT_Data import process_data  # function to process and transform the data
from Data_Storage import engine, store_data

app = FastAPI()

# Optional: Create a SQLAlchemy session (for more advanced querying)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Root endpoint to verify API is running
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# Endpoint to process data and return it (without storing)
@app.get("/process-data")
async def process_data_endpoint(symbol: str = "BTCUSDT"):
    try:
        # Fetch historical data using the function from Historical_data.py
        df = fetch_historical_data(symbol=symbol)
        if df.empty:
            raise HTTPException(status_code=404, detail="No historical data fetched.")
        # Process the data using the process_data function from PT_data.py
        processed_df = process_data(df, symbol)
        # Convert DataFrame to a JSON-friendly format (list of dictionaries)
        return processed_df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {e}")

# Endpoint to store processed data in PostgreSQL
@app.post("/store-data")
async def store_data_endpoint(symbol: str = "BTCUSDT"):
    try:
        # Fetch and process data
        df = fetch_historical_data(symbol=symbol)
        if df.empty:
            raise HTTPException(status_code=404, detail="No historical data fetched.")
        processed_df = process_data(df, symbol)
        # Store the processed data in PostgreSQL using the function from data_storage.py
        store_data(processed_df)
        return {"message": "Data stored successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Storage error: {e}")

# Endpoint to retrieve stored data from PostgreSQL
@app.get("/get-data")
async def get_data_endpoint(symbol: str = "BTCUSDT"):
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM historical_data WHERE symbol = :symbol ORDER BY date DESC LIMIT 100")
            result = conn.execute(query, {"symbol": symbol})
            # Use row._mapping to convert each row to a dictionary
            rows = [dict(row._mapping) for row in result]
            return {"data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval error: {e}")

# Optional: Global exception handler for debugging (can be removed in production)
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {exc}"}
    )
