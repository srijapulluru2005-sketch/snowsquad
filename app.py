import streamlit as st
import snowflake.connector
import pandas as pd

# -----------------------------
# Snowflake Connection
# -----------------------------
@st.cache_resource
def get_connection():
    conn = snowflake.connector.connect(
        user="YOUR_USERNAME",
        password="YOUR_PASSWORD",
        account="YOUR_ACCOUNT",
        warehouse="CITYRIDE_WH",
        database="CITYRIDE_DB",
        schema="CURATED"
    )
    return conn

conn = get_connection()

# -----------------------------
# Helper Function
# -----------------------------
def run_query(query):
    return pd.read_sql(query, conn)

# -----------------------------
# Title
# -----------------------------
st.title("🚴‍♂️ CityRide Analytics Dashboard")

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

total_revenue = run_query("SELECT SUM(revenue) AS val FROM fact_rentals").iloc[0,0]
avg_duration = run_query("SELECT AVG(duration_sec)/60 AS val FROM fact_rentals").iloc[0,0]
total_rides = run_query("SELECT COUNT(*) AS val FROM fact_rentals").iloc[0,0]

col1.metric("💰 Total Revenue", f"{total_revenue:.2f}")
col2.metric("⏱ Avg Duration (min)", f"{avg_duration:.2f}")
col3.metric("🚴 Total Rides", total_rides)

# -----------------------------
# Revenue Trend
# -----------------------------
st.subheader("📈 Revenue Trend")

query = """
SELECT DATE(start_time) AS date, SUM(revenue) AS revenue
FROM fact_rentals
GROUP BY date
ORDER BY date
"""
df = run_query(query)
st.line_chart(df.set_index("DATE"))

# -----------------------------
# Bike Type Usage
# -----------------------------
st.subheader("🚲 Bike Type Usage")

query = """
SELECT b.bike_type, COUNT(*) AS rides
FROM fact_rentals f
JOIN dim_bikes b ON f.bike_id = b.bike_id
GROUP BY b.bike_type
"""
df = run_query(query)
st.bar_chart(df.set_index("BIKE_TYPE"))

# -----------------------------
# Revenue by Channel
# -----------------------------
st.subheader("💳 Revenue by Channel")

query = """
SELECT booking_channel, SUM(revenue) AS revenue
FROM fact_rentals
GROUP BY booking_channel
"""
df = run_query(query)
st.bar_chart(df.set_index("BOOKING_CHANNEL"))

# -----------------------------
# Top Stations
# -----------------------------
st.subheader("📍 Top Stations")

query = """
SELECT s.station_name, SUM(f.revenue) AS revenue
FROM fact_rentals f
JOIN dim_stations s ON f.start_station_id = s.station_id
GROUP BY s.station_name
ORDER BY revenue DESC
LIMIT 10
"""
df = run_query(query)
st.dataframe(df)

# -----------------------------
# User Segment
# -----------------------------
st.subheader("👥 User Segments")

query = """
SELECT user_segment, COUNT(*) AS total
FROM dim_users
GROUP BY user_segment
"""
df = run_query(query)
st.bar_chart(df.set_index("USER_SEGMENT"))
