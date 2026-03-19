import streamlit as st
import snowflake.connector

st.title("Snowflake Test ✅")

# Test Snowflake connection
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
