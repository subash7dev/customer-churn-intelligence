import sys
import os

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT / "src")
)

# ============================================================
# ADD PROJECT SRC TO PYTHON PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SRC_PATH = os.path.join(
    PROJECT_ROOT,
    "src"
)

sys.path.append(SRC_PATH)


from analytics_queries import (
    get_kpis,
    get_contract_churn,
    get_internet_churn,
    get_payment_churn,
    get_tenure_churn,
    get_revenue_by_contract
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title(
    "📊 Customer Churn Intelligence"
)

st.markdown(
    """
    **PostgreSQL-powered customer analytics dashboard**
    """
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data(ttl=300)
def load_kpis():

    return get_kpis()


@st.cache_data(ttl=300)
def load_contract():

    return get_contract_churn()


@st.cache_data(ttl=300)
def load_internet():

    return get_internet_churn()


@st.cache_data(ttl=300)
def load_payment():

    return get_payment_churn()


@st.cache_data(ttl=300)
def load_tenure():

    return get_tenure_churn()


@st.cache_data(ttl=300)
def load_revenue():

    return get_revenue_by_contract()


kpis = load_kpis()

contract_df = load_contract()

internet_df = load_internet()

payment_df = load_payment()

tenure_df = load_tenure()

revenue_df = load_revenue()


# ============================================================
# KPI CARDS
# ============================================================

row1 = st.columns(5)

with row1[0]:

    st.metric(
        "Total Customers",
        f"{int(kpis.loc[0, 'total_customers']):,}"
    )

with row1[1]:

    st.metric(
        "Churned Customers",
        f"{int(kpis.loc[0, 'churned_customers']):,}"
    )

with row1[2]:

    st.metric(
        "Churn Rate",
        f"{kpis.loc[0, 'churn_rate']:.2f}%"
    )

with row1[3]:

    st.metric(
        "Monthly Revenue",
        f"${kpis.loc[0, 'monthly_revenue']:,.0f}"
    )

with row1[4]:

    st.metric(
        "Revenue at Risk",
        f"${kpis.loc[0, 'revenue_at_risk']:,.0f}"
    )


st.divider()


# ============================================================
# CONTRACT + INTERNET
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader(
        "Churn by Contract"
    )

    fig, ax = plt.subplots(
        figsize=(7, 5)
    )

    ax.bar(
        contract_df["contract"],
        contract_df["churn_rate"]
    )

    ax.set_ylabel(
        "Churn Rate (%)"
    )

    ax.set_xlabel(
        "Contract"
    )

    ax.set_title(
        "Churn Rate by Contract"
    )

    plt.xticks(
        rotation=15
    )

    st.pyplot(fig)


with col2:

    st.subheader(
        "Churn by Internet Service"
    )

    fig, ax = plt.subplots(
        figsize=(7, 5)
    )

    ax.bar(
        internet_df["internetservice"],
        internet_df["churn_rate"]
    )

    ax.set_ylabel(
        "Churn Rate (%)"
    )

    ax.set_xlabel(
        "Internet Service"
    )

    ax.set_title(
        "Churn Rate by Internet Service"
    )

    st.pyplot(fig)


# ============================================================
# TENURE
# ============================================================

st.subheader(
    "Churn by Customer Tenure"
)

fig, ax = plt.subplots(
    figsize=(11, 5)
)

ax.bar(
    tenure_df["tenure_group"],
    tenure_df["churn_rate"]
)

ax.set_ylabel(
    "Churn Rate (%)"
)

ax.set_xlabel(
    "Tenure"
)

ax.set_title(
    "Churn Rate by Tenure Group"
)

plt.xticks(
    rotation=20
)

st.pyplot(fig)


# ============================================================
# PAYMENT
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader(
        "Churn by Payment Method"
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.bar(
        payment_df["paymentmethod"],
        payment_df["churn_rate"]
    )

    ax.set_ylabel(
        "Churn Rate (%)"
    )

    ax.set_xlabel(
        "Payment Method"
    )

    ax.set_title(
        "Churn by Payment Method"
    )

    plt.xticks(
        rotation=35,
        ha="right"
    )

    st.pyplot(fig)


with col2:

    st.subheader(
        "Revenue by Contract"
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.bar(
        revenue_df["contract"],
        revenue_df["monthly_revenue"]
    )

    ax.set_ylabel(
        "Monthly Revenue"
    )

    ax.set_xlabel(
        "Contract"
    )

    ax.set_title(
        "Monthly Revenue by Contract"
    )

    plt.xticks(
        rotation=15
    )

    st.pyplot(fig)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.divider()

st.header(
    "💡 Business Insights"
)


highest_contract = contract_df.iloc[0]

highest_internet = internet_df.iloc[0]

highest_payment = payment_df.iloc[0]


col1, col2, col3 = st.columns(3)


with col1:

    st.info(
        f"""
        **Contract**

        {highest_contract['contract']}
        shows the highest observed churn rate:

        **{highest_contract['churn_rate']:.2f}%**
        """
    )


with col2:

    st.info(
        f"""
        **Internet Service**

        {highest_internet['internetservice']}
        shows the highest observed churn rate:

        **{highest_internet['churn_rate']:.2f}%**
        """
    )


with col3:

    st.info(
        f"""
        **Payment Method**

        {highest_payment['paymentmethod']}
        shows the highest observed churn rate:

        **{highest_payment['churn_rate']:.2f}%**
        """
    )


# ============================================================
# RAW ANALYTICS TABLE
# ============================================================

st.divider()

st.subheader(
    "Contract Analysis"
)

st.dataframe(
    contract_df,
    use_container_width=True
)