-- Database: MarketTracker
-- Table: daily_prices

CREATE TABLE daily_prices (
    id INT IDENTITY(1,1) PRIMARY KEY,
    fetch_date DATETIME DEFAULT GETDATE(),
    product_name NVARCHAR(255),
    price FLOAT,
    location NVARCHAR(100)
);