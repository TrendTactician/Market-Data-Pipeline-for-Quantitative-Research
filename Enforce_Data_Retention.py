from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# Assuming your connection details remain the same
password = quote_plus("YourPass")
DATABASE_URI = f"postgresql://postgres:{password}@localhost:5432/market_data"
engine = create_engine(DATABASE_URI)

def enforce_data_retention():
    # Query to get table size (in bytes)
    query_size = "SELECT pg_total_relation_size('historical_data');"
    with engine.connect() as conn:
        result = conn.execute(text(query_size))
        table_size_bytes = result.scalar()

    one_gb = 1 * 1024 * 1024 * 1024  # 1GB in bytes
    print(f"Current table size: {table_size_bytes / (1024*1024):.2f} MB")
    
    if table_size_bytes > one_gb:
        # Example deletion: remove records older than a computed cutoff date
        delete_query = """
            DELETE FROM historical_data
            WHERE date < (
                SELECT MIN(date) FROM (
                    SELECT date FROM historical_data ORDER BY date DESC OFFSET 1000
                ) AS sub
            );
        """
        with engine.connect() as conn:
            conn.execute(text(delete_query))
        print("Old historical data purged to maintain the 1GB limit.")

# Call this function periodically (e.g., via a scheduler or Airflow)
enforce_data_retention()
