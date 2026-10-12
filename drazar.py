import requests
import pyodbc

# --- PHASE 1: DATA EXTRACTION ---
url = "https://www.daraz.pk/catalog/?ajax=true&isFirstRequest=true&page=1&q=lotion"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

print("Live data is fetching from Daraz.pk...")
response = requests.get(url, headers=headers)
data = response.json()
products = data['mods']['listItems']

# --- PHASE 2: DATABASE CONNECTION & INSERTION ---
print("SQL is connecting to the server and saving data into the database...")

# Connection string (Aapke local server aur database ka pata)
conn_str = (
    r'DRIVER={SQL Server};'
    r'SERVER=.\SQLEXPRESS;'
    r'DATABASE=MarketTracker;'
    r'Trusted_Connection=yes;'
)

# Database se connect karna
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

print("Data table mein save ho raha hai...")

# Testing ke liye pehle 5 products save kar rahe hain
for item in products[:5]:
    name = item.get('name')
    price = float(item.get('price')) # Text ko number mein convert kiya
    location = item.get('location')
    
    # SQL mein data insert karne ki command
    cursor.execute('''
        INSERT INTO daily_prices (product_name, price, location)
        VALUES (?, ?, ?)
    ''', (name, price, location))

# Changes ko save (commit) karna aur connection band karna
conn.commit()
cursor.close()
conn.close()

print("Task 2 Complete! Data scucessfully save in the database.")