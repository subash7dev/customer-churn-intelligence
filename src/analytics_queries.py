import pandas as pd

from sqlalchemy import text

from database import engine


# ============================================================
# KPI QUERY
# ============================================================
def get_kpis():
    query = """
        SELECT
            COUNT(*) AS total_customers,

            SUM(churn) AS churned_customers,

            ROUND(
                (100.0 * SUM(churn) / COUNT(*))::numeric,
                2
            ) AS churn_rate,

            ROUND(
                SUM(monthlycharges)::numeric,
                2
            ) AS monthly_revenue,

            ROUND(
                SUM(
                    CASE
                        WHEN churn = 1
                        THEN monthlycharges
                        ELSE 0
                    END
                )::numeric,
                2
            ) AS revenue_at_risk

        FROM customers;
    """

    with engine.connect() as connection:
        return pd.read_sql(query, connection)

# ============================================================
# CONTRACT ANALYSIS
# ============================================================

def get_contract_churn():

    query = text("""
        SELECT
            contract,

            COUNT(*) AS customers,

            SUM(churn) AS churned_customers,

            ROUND(
                100.0 * SUM(churn) / COUNT(*),
                2
            ) AS churn_rate

        FROM customers

        GROUP BY contract

        ORDER BY churn_rate DESC;
    """)

    with engine.connect() as connection:

        return pd.read_sql(
            query,
            connection
        )


# ============================================================
# INTERNET SERVICE
# ============================================================

def get_internet_churn():

    query = text("""
        SELECT
            internetservice,

            COUNT(*) AS customers,

            SUM(churn) AS churned_customers,

            ROUND(
                100.0 * SUM(churn) / COUNT(*),
                2
            ) AS churn_rate

        FROM customers

        GROUP BY internetservice

        ORDER BY churn_rate DESC;
    """)

    with engine.connect() as connection:

        return pd.read_sql(
            query,
            connection
        )


# ============================================================
# PAYMENT METHOD
# ============================================================

def get_payment_churn():

    query = text("""
        SELECT
            paymentmethod,

            COUNT(*) AS customers,

            SUM(churn) AS churned_customers,

            ROUND(
                100.0 * SUM(churn) / COUNT(*),
                2
            ) AS churn_rate

        FROM customers

        GROUP BY paymentmethod

        ORDER BY churn_rate DESC;
    """)

    with engine.connect() as connection:

        return pd.read_sql(
            query,
            connection
        )


# ============================================================
# TENURE ANALYSIS
# ============================================================

def get_tenure_churn():

    query = text("""
        SELECT

            CASE

                WHEN tenure <= 6
                    THEN '0-6 Months'

                WHEN tenure <= 12
                    THEN '7-12 Months'

                WHEN tenure <= 24
                    THEN '13-24 Months'

                WHEN tenure <= 48
                    THEN '25-48 Months'

                ELSE '49-72 Months'

            END AS tenure_group,

            COUNT(*) AS customers,

            SUM(churn) AS churned_customers,

            ROUND(
                100.0 * SUM(churn) / COUNT(*),
                2
            ) AS churn_rate

        FROM customers

        GROUP BY tenure_group

        ORDER BY
            MIN(tenure);
    """)

    with engine.connect() as connection:

        return pd.read_sql(
            query,
            connection
        )


# ============================================================
# PAYMENT REVENUE
# ============================================================
def get_revenue_by_contract():
    query = """
        SELECT
            contract,

            COUNT(*) AS customers,

            ROUND(
                SUM(monthlycharges)::numeric,
                2
            ) AS monthly_revenue,

            ROUND(
                AVG(monthlycharges)::numeric,
                2
            ) AS average_monthly_charge

        FROM customers

        GROUP BY contract

        ORDER BY monthly_revenue DESC;
    """

    with engine.connect() as connection:
        return pd.read_sql(query, connection)