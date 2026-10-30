from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest
import warnings
SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# Suppress pandas SQL execution warnings
warnings.filterwarnings('ignore')

app = FastAPI()

# Browser ki CORS Blockage ko bypass karne ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Yeh sabhi sources ko permission dega
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "message": "Welcome to the E-commerce Inflation API. Use /api/v1/anomalies to fetch data."
    }

@app.get("/api/v1/anomalies")
def get_anomalies():
    # 1. Database Connection
    conn_str = (
        r'DRIVER={SQL Server};'
        r'SERVER=.\SQLEXPRESS;'
        r'DATABASE=MarketTracker;'
        r'Trusted_Connection=yes;'
    )
    conn = pyodbc.connect(conn_str)
    query = "SELECT * FROM daily_prices"
    df = pd.read_sql(query, engine)
   

    # 2. Time-Series Preprocessing & Inflation Logic (Pandas)
    df['fetch_date'] = pd.to_datetime(df['fetch_date'])
    df = df.sort_values(by=['product_name', 'fetch_date'])
    df['daily_inflation_pct'] = df.groupby('product_name')['price'].pct_change() * 100
    df['daily_inflation_pct'] = df['daily_inflation_pct'].fillna(0)

    # 3. Anomaly Detection (Isolation Forest)
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly_flag'] = iso_forest.fit_predict(df[['daily_inflation_pct']])
    
    # Filter for anomalies
    anomalies_df = df[df['anomaly_flag'] == -1]

    # Convert datetime to string so it can be sent as JSON over the web
    anomalies_df['fetch_date'] = anomalies_df['fetch_date'].astype(str)

    # 4. Return the processed Data as a REST API JSON response
    return {
        "status": "Success",
        "anomalies_detected": len(anomalies_df),
        "data": anomalies_df[['fetch_date', 'product_name', 'price', 'daily_inflation_pct']].to_dict(orient="records")
    }