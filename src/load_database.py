import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# ============================================================
# DATABASE CONNECTION
# ============================================================

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# ============================================================
# LOAD CLEAN DATA
# ============================================================

file_path = (
    "data/processed/"
    "telco_customer_churn_clean.csv"
)

df = pd.read_csv(file_path)

print(f"Loaded rows: {len(df):,}")
print(f"Loaded columns: {len(df.columns)}")


# ============================================================
# NORMALIZE COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)

print("\nDatabase columns:")

for column in df.columns:
    print("-", column)


# ============================================================
# LOAD INTO POSTGRESQL
# ============================================================

df.to_sql(
    "customers",
    engine,
    if_exists="replace",
    index=False,
    method="multi"
)

print(
    "\nCustomer data successfully loaded "
    "into PostgreSQL."
)


# ============================================================
# VERIFY DATABASE
# ============================================================

with engine.connect() as connection:

    result = connection.execute(
        text(
            "SELECT COUNT(*) FROM customers"
        )
    )

    count = result.scalar()

    print(
        f"Customers in database: {count:,}"
    )


# ============================================================
# VERIFY IMPORTANT COLUMNS
# ============================================================

with engine.connect() as connection:

    result = connection.execute(
        text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'customers'
            ORDER BY ordinal_position;
        """)
    )

    columns = result.fetchall()

print("\nPostgreSQL columns:")

for column in columns:
    print("-", column[0])