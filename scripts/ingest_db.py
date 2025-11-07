# bulk_ingest.py
"""
Bulk ingestion of CSV files into MySQL.
Requires `engine` from db_creation.py.
"""

import os
import time
import logging
import pandas as pd
from db_creation import engine  # import your pre-created engine

# -----------------------------
# CONFIGURATION
# -----------------------------
DATA_DIR = "../data"    # folder containing CSV files
LOG_DIR = "logs"
CHUNKSIZE = 50_000

# Create log folder if missing
os.makedirs(LOG_DIR, exist_ok=True)

# File logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "bulk_ingestion.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------
# UTILITY: Infer MySQL column types from CSV
# -----------------------------
def infer_mysql_dtypes(csv_path, sample_size=5000):
    """Infer MySQL-compatible data types from a sample of CSV."""
    sample = pd.read_csv(csv_path, nrows=sample_size)
    dtype_map = {
        "int64": "BIGINT",
        "float64": "DOUBLE",
        "object": "VARCHAR(255)",
        "bool": "BOOLEAN",
        "datetime64[ns]": "DATETIME"
    }
    inferred = {col: dtype_map.get(str(dtype), "VARCHAR(255)") for col, dtype in sample.dtypes.items()}
    return inferred

# -----------------------------
# UTILITY: Ensure table exists
# -----------------------------
def ensure_table_exists(table_name: str, csv_path: str, engine):
    """
    Creates a table in MySQL if it does not exist,
    using inferred schema from CSV headers and sample dtypes.
    """
    conn = engine.raw_connection()
    cursor = conn.cursor()

    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    if cursor.fetchone():
        conn.close()
        return

    inferred_dtypes = infer_mysql_dtypes(csv_path)
    columns_sql = ", ".join([f"`{col}` {dtype}" for col, dtype in inferred_dtypes.items()])
    create_stmt = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_sql});"

    cursor.execute(create_stmt)
    conn.commit()
    conn.close()
    logging.info(f"Created table `{table_name}` automatically with inferred schema.")

# -----------------------------
# FUNCTION: Bulk load CSV into MySQL
# -----------------------------
def bulk_load_mysql(file_path: str, table_name: str, engine):
    """Load CSV data directly into MySQL using LOAD DATA LOCAL INFILE."""
    logging.info(f"Starting bulk load for table: {table_name}")
    start = time.time()
    conn = None

    try:
        # Ensure table exists before ingestion
        ensure_table_exists(table_name, file_path, engine)

        conn = engine.raw_connection()
        cursor = conn.cursor()

        abs_path = os.path.abspath(file_path).replace("\\", "\\\\")  # Windows-safe path

        sql = f"""
            LOAD DATA LOCAL INFILE '{abs_path}'
            INTO TABLE `{table_name}`
            FIELDS TERMINATED BY ',' 
            ENCLOSED BY '"'
            LINES TERMINATED BY '\\n'
            IGNORE 1 ROWS;
        """
        cursor.execute(sql)
        conn.commit()

        elapsed = time.time() - start
        logging.info(f"Bulk loaded {table_name} in {elapsed:.2f}s")

    except Exception as e:
        logging.error(f"Failed to load {table_name}: {e}")

    finally:
        if conn:
            conn.close()

# -----------------------------
# MAIN SCRIPT: Iterate over CSVs
# -----------------------------
if __name__ == "__main__":
    logging.info("Starting full bulk ingestion process...")
    start_all = time.time()

    if not os.path.exists(DATA_DIR):
        logging.warning(f"Data folder '{DATA_DIR}' does not exist.")
    else:
        for file in os.listdir(DATA_DIR):
            if file.endswith(".csv"):
                file_path = os.path.join(DATA_DIR, file)
                table_name = os.path.splitext(file)[0]
                bulk_load_mysql(file_path, table_name, engine)

    logging.info(f"All CSVs ingested in {time.time() - start_all:.2f}s total.")
