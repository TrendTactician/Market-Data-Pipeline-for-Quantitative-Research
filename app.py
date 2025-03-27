import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Configure your database connection
password = quote_plus("YourPass")  # Encode special characters if needed
DATABASE_URI = f"postgresql://postgres:{password}@localhost:5432/market_data"
engine = create_engine(DATABASE_URI)

# Function to load data directly from PostgreSQL
@st.cache_data
def load_data():
    query = "SELECT * FROM historical_data ORDER BY date"
    df = pd.read_sql(query, engine)
    return df

# Set up the Streamlit dashboard
st.set_page_config(page_title="Market Data Dashboard", layout="wide")
st.title("Market Data Pipeline & Visualization Dashboard")

# Load data from PostgreSQL
data = load_data()

# Option to show raw data
if st.checkbox("Show Raw Data"):
    st.write(data)

# Display interactive Plotly chart (example for closing price)
import plotly.express as px

st.subheader("Interactive Price Trend")
fig = px.line(data, x="date", y="close", title="Closing Price Trend", 
              labels={"close": "Closing Price", "date": "Date"})
st.plotly_chart(fig, use_container_width=True)

# Sidebar filter example: Date range filter
st.sidebar.subheader("Filter Data by Date")
min_date = pd.to_datetime(data["date"]).min()
max_date = pd.to_datetime(data["date"]).max()
start_date, end_date = st.sidebar.date_input("Select date range", [min_date, max_date],
                                              min_value=min_date, max_value=max_date)

filtered_data = data[(pd.to_datetime(data["date"]) >= pd.to_datetime(start_date)) & 
                     (pd.to_datetime(data["date"]) <= pd.to_datetime(end_date))]

st.subheader("Filtered Price Trend")
fig_filtered = px.line(filtered_data, x="date", y="close", title="Filtered Closing Price Trend")
st.plotly_chart(fig_filtered, use_container_width=True)
