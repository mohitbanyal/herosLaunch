from streamlit_gsheets import GSheetsConnection
import streamlit as st
import os

def _conn():
    return st.connection("gsheets",type=GSheetsConnection)

@st.cache_data(ttl=60)
def load_data(_conn,sheet_name):
    sheet_url = os.getenv("GOOGLE_SHEET_URL")
    return _conn.read(
        spreadsheet=sheet_url,
        worksheet=sheet_name
    )

