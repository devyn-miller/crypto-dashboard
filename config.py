import os
import streamlit as st

# Try to get API key from Streamlit secrets in production, fall back to environment variable
API_KEY = st.secrets.get("CRYPTOCOMPARE_API_KEY", os.getenv("CRYPTOCOMPARE_API_KEY", ""))
BASE_URL = "https://min-api.cryptocompare.com/data"