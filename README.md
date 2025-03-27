# Market Data Pipeline & Visualization Dashboard for Quantitative Research

An end-to-end project that fetches, processes, stores, and visualizes historical market data from Binance. This project is designed for quantitative research and backtesting trading strategies. It includes a robust data pipeline, an API built with FastAPI, and an interactive dashboard built with Streamlit.


## Table of Contents

- **Project Overview**

- **Project Structure**

- **Features**

- **Installation & Setup**

- **Usage**

   **1. Data Pipeline & API**

   **2. Streamlit Dashboard**

   **3. Job Scheduling & Automation**

- **Deployment**

- **Tech Stack**

- **Contributing**

- **License**


## Project Overview

**This project demonstrates an end-to-end solution for quantitative market research:**

- Data Ingestion: Historical OHLCV data is fetched from the Binance API.

- Data Processing: The raw data is cleaned, processed, and enriched with additional information (such as the trading symbol).

- Data Storage: Processed data is stored in a PostgreSQL database.

- API Services: A FastAPI backend exposes endpoints to process, store, and retrieve data on demand.

- Visualization: An interactive dashboard built with Streamlit displays real-time and historical market trends, with filtering options and interactive charts using Plotly and Matplotlib.


## Project Structure
    ├── Historical_data.py  # Fetches raw historical data from Binance API

    ├── PT_Data.py          # Processes and transforms the raw data

    ├── Data_Storage.py     # Stores processed data into a PostgreSQL database

    ├── api.py              # FastAPI application with endpoints for processing, storing and retrieving data

    ├── app.py              # Streamlit dashboard for data visualization from PostgressSQL

    └── README.md           # Project documentation (this file)


## Features

- **Data Ingestion:** Fetch up to 10,000 data points from Binance with configurable parameters.

- **Data Processing:** Convert timestamps, enforce numeric types, and add essential metadata like the trading symbol.

- **Database Integration:** Store the cleaned data into a PostgreSQL database using SQLAlchemy.

- **API Endpoints:**

     ```/process-data:``` Fetch and process data, then return the result.

     ```/store-data:``` Fetch, process, and store new data in PostgreSQL.

     ```/get-data:``` Retrieve stored data for analysis.

- **Dashboard Visualization:** Interactive dashboard with Streamlit for real-time visualization, including filtering by date and plotting price trends with Plotly and Matplotlib.

- **Backtesting Potential:** With the stored historical data, you can backtest trading strategies and compute performance metrics.


## Installation & Setup

**1. Clone the Repository:**
   
       git clone https://github.com/yourusername/yourrepo.git
   
       cd yourrepo
   
**2. Install Dependencies:**

       pip install fastapi uvicorn sqlalchemy psycopg2-binary pandas streamlit plotly matplotlib
       
**3. Configure PostgreSQL:**

- Ensure PostgreSQL is installed and running.

- Create a database called market_data (or update the connection string in data_storage.py).

- Verify that the historical_data table is created (you can use SQL scripts provided in the documentation).


## Usage

**1. Data Pipeline & API**

- **Run the FastAPI Server:**

      uvicorn api:app --reload

- **Visit http://127.0.0.1:8000/ to see the root endpoint.**

- **Access interactive API documentation at ```http://127.0.0.1:8000/docs``` to test endpoints like ```/process-data```, ```/store-data```, and ```/get-data```.**

- **Example cURL Command to Store Data:**

      curl -X POST "http://127.0.0.1:8000/store-data?symbol=BTCUSDT" -H "accept: application/json"

  
**2. Streamlit Dashboard**

- **Run the Streamlit App:**

If you have created a dashboard (e.g., in ```app.py```) that pulls data directly from PostgreSQL:

       streamlit run app.py

   - Access the dashboard (typically at ```http://localhost:8501```).
   - Explore interactive visualizations and filters to analyze market trends.

- **Dashboard Features:**

   **1. Interactive charts showing market trends.**

   **2. Date range filters to refine displayed data.**

   **3. Option to view raw data and visual insights.**


**3. Job Scheduling & Automation**

To ensure your data is regularly updated without manual intervention, you can schedule jobs that trigger your data update process:

- **Using Cron (Linux/macOS):**

   - Create a cron job that calls the /store-data endpoint periodically. For example, to run every hour:

         0 * * * * curl -X POST "http://127.0.0.1:8000/store-data?symbol=BTCUSDT" -H "accept: application/json"
     
   - ```0 * * * *:``` Runs the command at minute 0 of every hour.

   - ```curl -X POST "http://127.0.0.1:8000/store-data?symbol=BTCUSDT" -H "accept: application/json":``` Sends a POST request to your API endpoint with the query parameter symbol=BTCUSDT and specifies that the client accepts JSON responses.

 - **Important Considerations:**

   - **Server Availability:**
     - Ensure your FastAPI server is running and accessible at http://127.0.0.1:8000 when this cron job executes.

   - **Environment:**
     - This command runs on your local machine. If you're deploying on a remote server, make sure the endpoint URL reflects the correct host.

   - **Path to curl:**
     - Depending on your system’s configuration, you might need to specify the full path to curl or ensure it’s available in the cron environment.


- **Using Apache Airflow:**
  
   - Set up an Airflow DAG that calls the endpoint on a defined schedule. This is especially useful for more complex workflows.

- **Windows Task Scheduler:**
  
   - On Windows, you can use Task Scheduler to run a script (or cURL command) at scheduled intervals.

By setting up a scheduler, your system will automatically fetch and update new data into PostgreSQL, ensuring your API and dashboard always have the latest information.


## Deployment

- **API Deployment:**

     - You can deploy your FastAPI application to ```Heroku```, ```AWS```, or any other cloud provider.

- **Dashboard Deployment:**

     - Host Streamlit dashboard on platforms like ```Streamlit Sharing``` or deploy via ```Docker``` on cloud services.

 
## 🔥 Summary Table of Tech Stack

| Component	| Technology |
| :---: | :---: |
| `Programming Languag` |	Python |
| `Data Fetching`	|	Binance API, Requests, Pandas |
| `Data Processing`	|	Pandas, Python Standard Library |
| `Database`	|	PostgreSQL, SQLAlchemy |
| `API Framework`	|	FastAPI, Uvicorn |
| `Visualization`	|	Streamlit, Plotly, Matplotlib |
| `Job Scheduling`	| Cron / Apache Airflow / Windows Task Scheduler |
| `Deployment`	|	Heroku / AWS / Streamlit Sharing |


## License

**Distributed under the MIT License. See LICENSE for more information.**
