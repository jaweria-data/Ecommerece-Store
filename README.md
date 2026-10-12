# E-Commerce Inflation & Price Anomaly Tracker

## Project Overview
This project is an end-to-end data science and machine learning pipeline designed to track live e-commerce pricing data, calculate time-series inflation metrics, and automatically detect irregular price fluctuations. Built with a focus on business intelligence and market monitoring, the system utilizes unsupervised machine learning to isolate statistical outliers (sudden price surges or crashes) and serves these insights through a live RESTful API.

## Tech Stack
* **Language:** Python 3.x
* **Database:** Microsoft SQL Server, `pyodbc`
* **Data Engineering:** `pandas` (Time-series analysis, feature engineering)
* **Machine Learning:** `scikit-learn` (Isolation Forest)
* **Backend API:** FastAPI, Uvicorn
* **Deployment & Tunneling:** Ngrok
* **Version Control:** Git, GitHub

## Data Pipeline Architecture
The system operates on a 5-step automated architecture:
1. **Data Extraction:** Extracts live pricing data for targeted products (e.g., Daraz).
2. **Database Storage:** Ingests raw data into a localized SQL Server database (`MarketTracker`) utilizing the `daily_prices` schema.
3. **Time-Series Preprocessing:** Uses Pandas to dynamically format temporal data, sort chronologically, and calculate daily inflation percentages (`pct_change`).
4. **Machine Learning Anomaly Detection:** Deploys an Isolation Forest algorithm (`contamination=0.05`) to mathematically flag suspicious pricing behavior without manual thresholding.
5. **API Deployment:** Exposes the processed data and ML flags via a FastAPI backend, enabling secure public access through an Ngrok tunnel.

## API Endpoints
**Base URL:** `http://localhost:8000` (Local) / Ngrok Forwarding URL (Public)

* `GET /` 
  * Returns API status and health check.
* `GET /api/v1/anomalies`
  * Executes the database query, runs the machine learning model, and returns a JSON payload of all detected pricing anomalies.

### Example API Response
```json
{
  "status": "Success",
  "anomalies_detected": 2,
  "data": [
    {
      "fetch_date": "2026-10-10 15:51:57.300",
      "product_name": "Golden Pearl Healthy White Moisturizing Lotion",
      "price": 115.0,
      "daily_inflation_pct": 10.5769
    }
  ]
}
Local Installation & Execution
1. Clone the Repository

Bash
git clone [https://github.com/your-username/E-Commerce-Inflation-Tracker.git](https://github.com/your-username/E-Commerce-Inflation-Tracker.git)
cd E-Commerce-Inflation-Tracker
2. Install Dependencies
Ensure you have Python installed, then run:

Bash
pip install -r requirements.txt
3. Database Configuration

Ensure Microsoft SQL Server is running locally (.\SQLEXPRESS).

Execute the provided database_schema.sql (if applicable) to generate the MarketTracker database and daily_prices table.

4. Launch the Server

Bash
uvicorn task_5_api:app --reload
The API will be accessible at http://127.0.0.1:8000.

5. Launch Public Tunnel (Optional)
To expose the local API to the internet for external review:

Bash
python start_tunnel.py
Author
Jaweria Iqbal

Data Scientist & Analyst
