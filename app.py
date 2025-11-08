import streamlit as st
import sqlite3
import pandas as pd
import os

DB_NAME = "log.db"

st.set_page_config(page_title="Advanced Dashboard", layout="wide")

# TODO: Initialize session state for login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# TODO: Create login form (username/password)
if not st.session_state.logged_in:
    st.title("🔐 Login to Access Dashboard")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # TODO: Replace with simple check (e.g., admin / admin123)
    if st.button("Login"):
        pass
else:
    # Navigation
    st.sidebar.title("📂 Navigation")
    page = st.sidebar.radio("Select Page", ["Dashboard", "Configuration", "Logout"])

    if page == "Dashboard":
        st.title("🌐 Secure Data Center Dashboard")
        if not os.path.exists(DB_NAME):
            st.warning("Database not found. Please ensure 'log.db' exists.")
        else:
            conn = sqlite3.connect(DB_NAME)
            df = pd.read_sql_query("SELECT * FROM system_log", conn)
            st.dataframe(df.tail(10), use_container_width=True)
            st.line_chart(df.set_index("timestamp")[["cpu", "memory", "disk"]])
            conn.close()

    elif page == "Configuration":
        st.title("⚙️ Configuration Panel")
        # TODO: Add sliders to adjust thresholds dynamically
        # Example: CPU_THRESHOLD = st.slider("CPU Alert Threshold (%)", 0, 100, 80)
        pass

    elif page == "Logout":
        # TODO: Log out and reset session
        pass
