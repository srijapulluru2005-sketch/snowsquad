import streamlit as st

# Only import Snowflake to test
try:
    import snowflake.connector
    st.success("✅ Snowflake connector imported successfully")
except ModuleNotFoundError:
    st.error("❌ Snowflake connector NOT found")
