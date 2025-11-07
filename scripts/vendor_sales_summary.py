# vendor_summary.py
"""
Create Vendor Summary Table, clean it, and ingest into MySQL database.
"""

import pandas as pd
import logging
import numpy as np
from db_creation import engine  # import SQLAlchemy engine

# -----------------------------
# LOGGING
# -----------------------------
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# -----------------------------
# INGEST DATAFRAME TO MYSQL
# -----------------------------
def ingest_db(df, table_name, engine):
    """Ingest dataframe into MySQL table (replace if exists)."""
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    logging.info(f"Data ingested into table `{table_name}` successfully.")

# -----------------------------
# CREATE VENDOR SUMMARY
# -----------------------------
def create_vendor_summary(engine):
    """Merge multiple tables to create vendor summary."""
    query = """
    WITH FreightSummary AS (
        SELECT VendorNumber, SUM(Freight) AS FreightCost 
        FROM vendor_invoice 
        GROUP BY VendorNumber
    ), 
    PurchaseSummary AS (
        SELECT 
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
    ),
    SalesSummary AS (
        SELECT 
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )
    SELECT 
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss 
        ON ps.VendorNumber = ss.VendorNo 
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs 
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """
    df = pd.read_sql(query, con=engine)
    return df

# -----------------------------
# CLEAN DATA
# -----------------------------
def clean_data(df):
    """Clean vendor summary and create new metrics safely for MySQL."""
    df['Volume'] = df['Volume'].astype('float')
    df.fillna(0, inplace=True)
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']

    # Avoid division by zero / inf for MySQL
    df['ProfitMargin'] = np.where(df['TotalSalesDollars'] != 0,
                                  (df['GrossProfit'] / df['TotalSalesDollars']) * 100, 0)
    df['StockTurnover'] = np.where(df['TotalPurchaseQuantity'] != 0,
                                   df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'], 0)
    df['SalesToPurchaseRatio'] = np.where(df['TotalPurchaseDollars'] != 0,
                                          df['TotalSalesDollars'] / df['TotalPurchaseDollars'], 0)
    return df

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    logging.info("Creating Vendor Summary Table.....")
    summary_df = create_vendor_summary(engine)
    logging.info(summary_df.head())

    logging.info("Cleaning Data.....")
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info("Ingesting data into MySQL.....")
    ingest_db(clean_df, 'vendor_sales_summary', engine)
    logging.info("Completed")
