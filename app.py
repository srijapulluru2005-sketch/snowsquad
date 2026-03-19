
import streamlit as st
import snowflake.connector
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="CityRide Dashboard",
    layout="wide"
)

st.title("🚴‍♂️ CityRide Analytics Dashboard")

# -----------------------------
# Snowflake Connection
# -----------------------------
@st.cache_resource
def get_connection():
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
        role=st.secrets["snowflake"]["role"]
    )
    return conn

conn = get_connection()
st.success("✅ Connected to Snowflake!")

# -----------------------------
# Query Function
# -----------------------------
@st.cache_data
def run_query(query):
    cur = conn.cursor()
    cur.execute(query)
    df = pd.DataFrame(cur.fetchall(), columns=[col[0] for col in cur.description])
    cur.close()
    return df

# -----------------------------
# Example KPIs
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

# Replace with your actual table/columns
total_revenue = run_query("SELECT SUM(revenue) AS val FROM fact_rentals").iloc[0,0]
avg_duration = run_query("SELECT AVG(duration_sec)/60 AS val FROM fact_rentals").iloc[0,0]
total_rides = run_query("SELECT COUNT(*) AS val FROM fact_rentals").iloc[0,0]

col1.metric("💰 Total Revenue", f"{total_revenue:.2f}")
col2.metric("⏱ Avg Duration (min)", f"{avg_duration:.2f}")
col3.metric("🚴 Total Rides", int(total_rides))
