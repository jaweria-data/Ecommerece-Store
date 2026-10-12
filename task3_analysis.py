import pandas as pd
import pyodbc
import warnings

# Suppress pandas SQL execution warnings for a cleaner terminal output
warnings.filterwarnings('ignore')

print("Phase 1: Ingesting Data from SQL Server...")

# 1. Database Connection String
# Update the SERVER name if your local SQL instance has a different name
conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=.\SQLEXPRESS;'
    r'DATABASE=MarketTracker;'
    r'Trusted_Connection=yes;'
)

# Establish the connection
conn = pyodbc.connect(conn_str)

# 2. Data Ingestion
# Read the entire daily_prices table directly into a Pandas DataFrame
query = "SELECT * FROM daily_prices"
df = pd.read_sql(query, conn)
print("Success: Data loaded into Pandas DataFrame.\n")

print("Phase 2: Time-Series Preprocessing...")

# 3. Data Type Formatting
# Convert the 'fetch_date' column from standard text into datetime objects
df['fetch_date'] = pd.to_datetime(df['fetch_date'])

# 4. Chronological Sorting
# Sort the data first by product name, then by date, to ensure chronological order
df = df.sort_values(by=['product_name', 'fetch_date'])


print("Phase 3: Feature Engineering (Inflation Logic)...")

# 5. Calculate Daily Percentage Change
# Group the data by product, look at the price, and calculate the difference from the previous row
df['daily_inflation_pct'] = df.groupby('product_name')['price'].pct_change() * 100

# 6. Handle Null Values
# The first day of data will show 'NaN' (Not a Number) because there is no previous day to compare it to. Fill these with 0.
df['daily_inflation_pct'] = df['daily_inflation_pct'].fillna(0)

# Close the database connection to free up system resources
conn.close()

# 7. Validation
# Print the first 15 rows of specific columns to verify the logic worked
print("\n--- Processed DataFrame Output ---")
print(df[['fetch_date', 'product_name', 'price', 'daily_inflation_pct']].head(15))



from sklearn.ensemble import IsolationForest

print("\nPhase 4: Machine Learning - Anomaly Detection (Isolation Forest)...")

# 8. Model Initialization
# 'contamination' tells the model what percentage of the data we expect to be abnormal (e.g., 5%)
iso_forest = IsolationForest(contamination=0.05, random_state=42)

# 9. Model Training and Prediction
# We feed the daily_inflation_pct column into the model.
# Sklearn requires a 2D array, so we use double brackets [['daily_inflation_pct']]
df['anomaly_flag'] = iso_forest.fit_predict(df[['daily_inflation_pct']])

# 10. Filter the Results
# Isolation Forest labels normal data as '1' and anomalies (spikes/crashes) as '-1'
anomalies_df = df[df['anomaly_flag'] == -1]

# 11. Final Output validation
print("--- Detected Anomalies (Suspicious Price Surges) ---")
print(anomalies_df[['fetch_date', 'product_name', 'price', 'daily_inflation_pct']])