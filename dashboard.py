import streamlit as st
import requests
import pandas as pd

# Configure the visual layout and browser tab metadata
st.set_page_config(page_title="E-Commerce Anomaly Tracker", page_icon="📊", layout="wide")

# --- SIDEBAR: Context & Purpose ---
with st.sidebar:
    st.header("Project Overview")
    st.info(
        "**Primary Purpose:**\n"
        "To autonomously monitor e-commerce platforms and detect irregular pricing behaviors—such as extreme inflation or artificial price drops—using machine learning."
    )
    st.markdown("### Technical Architecture")
    st.write("**Detection Model:** Scikit-Learn Isolation Forest")
    st.write("**Database:** Microsoft SQL Server")
    st.write("**Backend API:** FastAPI & Uvicorn")
    st.write("**Frontend:** Streamlit")

# --- MAIN DASHBOARD HEADER ---
st.title("📊 E-Commerce Price Anomaly Tracker")
st.markdown("### Real-Time Market Monitoring System")
st.write("This dashboard interfaces directly with the analytical backend to isolate and visualize critical pricing outliers within the daily scraped dataset.")

# Define the FastAPI endpoint (Update to Ngrok URL if sharing remotely)
API_URL = "http://127.0.0.1:8000/api/v1/anomalies"

# --- DATA RETRIEVAL & RENDERING ---
if st.button("Fetch Live Market Anomalies", type="primary"):
    with st.spinner("Executing machine learning predictions via FastAPI..."):
        try:
            response = requests.get(API_URL)
            
            if response.status_code == 200:
                payload = response.json()
                
                if payload.get("status") == "Success":
                    records = payload.get("data", [])
                    anomalies_count = payload.get("anomalies_detected", 0)

                    # KPI Metrics Row
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Anomalies Detected", anomalies_count)
                    col2.metric("Pipeline Status", "Live Detection Active")
                    col3.metric("Data Source", "Daraz Automated Extraction")

                    st.divider()

                    if records:
                        # Process data into a formatted Pandas DataFrame
                        df = pd.DataFrame(records)
                        df = df.rename(columns={
                            "fetch_date": "Timestamp",
                            "product_name": "Product Name",
                            "price": "Current Price (PKR)",
                            "daily_inflation_pct": "Price Fluctuation (%)"
                        })

                        # Analytical Visualization
                        st.subheader("Anomaly Magnitude Analysis")
                        st.write("Visual representation of percentage deviations from the market baseline.")
                        st.bar_chart(data=df, x="Product Name", y="Price Fluctuation (%)", color="#ff4b4b")

                        # Detailed Record Table
                        st.subheader("Detailed Anomaly Logs")
                        st.dataframe(df, use_container_width=True)
                        
                    else:
                        st.success("System scan complete. No pricing anomalies detected in the current dataset.")
                else:
                    st.error("The API returned an unexpected configuration payload.")
            else:
                st.error(f"Failed to retrieve data. HTTP Status Code: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Connection Error: The FastAPI server is currently offline. Please initiate the backend terminal.")