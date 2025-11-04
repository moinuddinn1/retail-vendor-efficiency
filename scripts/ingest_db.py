
# -------------------------------------------------------------------
#  MAIN SCRIPT — Iterate and Ingest
# -------------------------------------------------------------------
if __name__ == "__main__":
    logging.info("Starting full bulk ingestion process...")
    start_all = time.time()

    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            file_path = os.path.join(DATA_DIR, file)
            table_name = os.path.splitext(file)[0]
            bulk_load_mysql(file_path, table_name, engine)

    logging.info(f"All CSVs ingested in {time.time() - start_all:.2f}s total.")

import os
import time
import logging
import pandas as pd
from sqlalchemy import create_engine, text

logging.basicConfig(
    level=logging.INFO,           # or DEBUG for more verbosity
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]  # print to console
)

#Credentials

DB_NAME = "vendor_db"
DB_USER = "root"
DB_PASS = "1234"
DB_HOST = "localhost"
DB_PORT = 3306
DATA_DIR = "data"
CHUNKSIZE = 50_000

# Database Setup (Auto-create if Missing)

try:
    root_engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}")
    with root_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        logging.info(f"🛠️ Ensured database '{DB_NAME}' exists.")
except SQLAlchemyError as e:
    logging.critical(f"Database connection/setup failed: {e}")
    raise SystemExit(e)

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# -------------------------------------------------------------------
#  CONFIGURATION
# -------------------------------------------------------------------
DATA_DIR = "data"
LOG_DIR = "logs"
#DB_URI = "mysql+pymysql://root:1234@localhost:3306/vendor_db"
DB_URI = "mysql+pymysql://root:1234@localhost:3306/vendor_db?local_infile=1"

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "bulk_ingestion.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)        


engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?local_infile=1"
)


# -------------------------------------------------------------------
# ⚙️ Utility: Infer MySQL-compatible data types from CSV sample
# -------------------------------------------------------------------
def infer_mysql_dtypes(csv_path, sample_size=5000):
    """
    Read a small CSV sample and infer column data types for MySQL.
    """
    sample = pd.read_csv(csv_path, nrows=sample_size)

    dtype_map = {
        "int64": "BIGINT",
        "float64": "DOUBLE",
        "object": "VARCHAR(255)",
        "bool": "BOOLEAN",
        "datetime64[ns]": "DATETIME"
    }

    inferred = {}
    for col, dtype in sample.dtypes.items():
        inferred[col] = dtype_map.get(str(dtype), "VARCHAR(255)")
    return inferred

# -------------------------------------------------------------------
# ⚙️ Utility: Create table schema if it doesn’t exist
# -------------------------------------------------------------------
def ensure_table_exists(table_name: str, csv_path: str, engine):
    """
    Creates a table in MySQL if it does not already exist,
    using inferred schema from CSV headers and sample dtypes.
    """
    conn = engine.raw_connection()
    cursor = conn.cursor()

    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    exists = cursor.fetchone()
    if exists:
        conn.close()
        return

    inferred_dtypes = infer_mysql_dtypes(csv_path)
    columns_sql = ", ".join([f"`{col}` {dtype}" for col, dtype in inferred_dtypes.items()])
    create_stmt = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_sql});"

    cursor.execute(create_stmt)
    conn.commit()
    conn.close()

    logging.info(f" Created table `{table_name}` automatically with inferred schema.")


# -------------------------------------------------------------------
#  FUNCTION: Bulk Load CSV into MySQL
# -------------------------------------------------------------------
def bulk_load_mysql(file_path: str, table_name: str, engine):
    """
    Load CSV data directly into MySQL using LOAD DATA LOCAL INFILE.
    """
    logging.info(f" Starting bulk load for table: {table_name}")
    start = time.time()
    conn = None

    try:
        # Ensure table exists before ingestion
        ensure_table_exists(table_name, file_path, engine)

        conn = engine.raw_connection()
        cursor = conn.cursor()

        abs_path = os.path.abspath(file_path).replace("\\", "\\\\")  # for Windows compatibility

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
        logging.info(f" Bulk loaded {table_name} in {elapsed:.2f}s")

    except Exception as e:
        logging.error(f" Failed to load {table_name}: {e}")

    finally:
        if conn:
            conn.close()
