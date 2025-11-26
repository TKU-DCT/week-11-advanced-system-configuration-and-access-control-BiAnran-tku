# import streamlit as st
# import sqlite3
# import pandas as pd
# import os

# DB_NAME = "log.db"

# st.set_page_config(page_title="Advanced Dashboard", layout="wide")

# # TODO: Initialize session state for login status
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# # TODO: Create login form (username/password)
# if not st.session_state.logged_in:
#     st.title("🔐 Login to Access Dashboard")

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     # TODO: Replace with simple check (e.g., admin / admin123)
#     if st.button("Login"):
#         pass
# else:
#     # Navigation
#     st.sidebar.title("📂 Navigation")
#     page = st.sidebar.radio("Select Page", ["Dashboard", "Configuration", "Logout"])

#     if page == "Dashboard":
#         st.title("🌐 Secure Data Center Dashboard")
#         if not os.path.exists(DB_NAME):
#             st.warning("Database not found. Please ensure 'log.db' exists.")
#         else:
#             conn = sqlite3.connect(DB_NAME)
#             df = pd.read_sql_query("SELECT * FROM system_log", conn)
#             st.dataframe(df.tail(10), use_container_width=True)
#             st.line_chart(df.set_index("timestamp")[["cpu", "memory", "disk"]])
#             conn.close()

#     elif page == "Configuration":
#         st.title("⚙️ Configuration Panel")
#         # TODO: Add sliders to adjust thresholds dynamically
#         # Example: CPU_THRESHOLD = st.slider("CPU Alert Threshold (%)", 0, 100, 80)
#         pass

#     elif page == "Logout":
#         # TODO: Log out and reset session
#         pass
import streamlit as st
import sqlite3
import pandas as pd
import os

DB_NAME = "log.db"

st.set_page_config(page_title="Advanced Dashboard", layout="wide")

# Initialize session state for login status and thresholds
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "cpu_threshold" not in st.session_state:
    st.session_state.cpu_threshold = 80

if "memory_threshold" not in st.session_state:
    st.session_state.memory_threshold = 80

if "disk_threshold" not in st.session_state:
    st.session_state.disk_threshold = 80

# Create login form (username/password)
if not st.session_state.logged_in:
    st.title("🔐 Login to Access Dashboard")
    
    # Add some styling to the login page
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f2f6;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        # Simple authentication check
        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid username or password. Please try again.")
                st.info("Hint: Username: admin, Password: admin123")
    
    # Add footer to login page
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray;'>Secure Data Center Monitoring System</p>", 
                unsafe_allow_html=True)

else:
    # Navigation sidebar
    st.sidebar.title("📂 Navigation")
    st.sidebar.markdown(f"**Welcome, Admin!**")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio("Select Page", ["📊 Dashboard", "⚙️ Configuration", "🚪 Logout"])

    if page == "📊 Dashboard":
        st.title("🌐 Secure Data Center Dashboard")
        
        # Display current thresholds
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("CPU Threshold", f"{st.session_state.cpu_threshold}%")
        with col2:
            st.metric("Memory Threshold", f"{st.session_state.memory_threshold}%")
        with col3:
            st.metric("Disk Threshold", f"{st.session_state.disk_threshold}%")
        
        st.markdown("---")
        
        if not os.path.exists(DB_NAME):
            st.warning("⚠️ Database not found. Please ensure 'log.db' exists.")
            st.info("The system requires a SQLite database named 'log.db' with a 'system_log' table.")
        else:
            try:
                conn = sqlite3.connect(DB_NAME)
                df = pd.read_sql_query("SELECT * FROM system_log ORDER BY timestamp DESC", conn)
                
                if df.empty:
                    st.warning("No data found in the database.")
                else:
                    # Display last 10 entries
                    st.subheader("📋 Recent System Logs (Last 10 Entries)")
                    st.dataframe(df.tail(10).reset_index(drop=True), use_container_width=True)
                    
                    # Display charts
                    st.subheader("📈 System Metrics Over Time")
                    
                    # Prepare data for visualization
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    chart_data = df.set_index("timestamp")[["cpu", "memory", "disk"]]
                    
                    # Add threshold lines to the chart
                    st.line_chart(chart_data)
                    
                    # Show threshold indicators
                    st.subheader("🚨 Current Status")
                    latest_data = df.iloc[-1]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        cpu_status = "🔴 Critical" if latest_data['cpu'] > st.session_state.cpu_threshold else "🟢 Normal"
                        st.metric("CPU Usage", f"{latest_data['cpu']}%", cpu_status)
                    
                    with col2:
                        mem_status = "🔴 Critical" if latest_data['memory'] > st.session_state.memory_threshold else "🟢 Normal"
                        st.metric("Memory Usage", f"{latest_data['memory']}%", mem_status)
                    
                    with col3:
                        disk_status = "🔴 Critical" if latest_data['disk'] > st.session_state.disk_threshold else "🟢 Normal"
                        st.metric("Disk Usage", f"{latest_data['disk']}%", disk_status)
                
                conn.close()
                
            except Exception as e:
                st.error(f"Error reading database: {str(e)}")

    elif page == "⚙️ Configuration":
        st.title("⚙️ Configuration Panel")
        st.markdown("Adjust the alert thresholds for system monitoring:")
        
        # Create configuration sliders
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Threshold Settings")
            
            # CPU Threshold Slider
            cpu_threshold = st.slider(
                "CPU Alert Threshold (%)",
                min_value=0,
                max_value=100,
                value=st.session_state.cpu_threshold,
                step=5,
                help="Alert when CPU usage exceeds this percentage"
            )
            
            # Memory Threshold Slider
            memory_threshold = st.slider(
                "Memory Alert Threshold (%)",
                min_value=0,
                max_value=100,
                value=st.session_state.memory_threshold,
                step=5,
                help="Alert when Memory usage exceeds this percentage"
            )
            
            # Disk Threshold Slider
            disk_threshold = st.slider(
                "Disk Alert Threshold (%)",
                min_value=0,
                max_value=100,
                value=st.session_state.disk_threshold,
                step=5,
                help="Alert when Disk usage exceeds this percentage"
            )
            
            # Save button
            if st.button("💾 Save Configuration", use_container_width=True):
                st.session_state.cpu_threshold = cpu_threshold
                st.session_state.memory_threshold = memory_threshold
                st.session_state.disk_threshold = disk_threshold
                st.success("✅ Configuration saved successfully!")
                st.balloons()
        
        with col2:
            st.subheader("📋 Current Settings")
            st.info(f"""
            **CPU Threshold:** {cpu_threshold}%  
            **Memory Threshold:** {memory_threshold}%  
            **Disk Threshold:** {disk_threshold}%
            """)
            
            st.markdown("---")
            st.markdown("**💡 Tips:**")
            st.markdown("""
            - Lower thresholds = more sensitive alerts
            - Higher thresholds = fewer false positives
            - Recommended range: 70-90%
            """)
        
        # Reset to defaults button
        st.markdown("---")
        if st.button("🔄 Reset to Defaults", use_container_width=False):
            st.session_state.cpu_threshold = 80
            st.session_state.memory_threshold = 80
            st.session_state.disk_threshold = 80
            st.warning("Thresholds reset to default values (80%)")
            st.rerun()

    elif page == "🚪 Logout":
        st.title("🚪 Logout")
        
        st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h2>Are you sure you want to logout?</h2>
            <p>You will need to login again to access the dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🚪 Confirm Logout", use_container_width=True):
                # Reset session state
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                
                # Re-initialize default values
                st.session_state.logged_in = False
                st.session_state.cpu_threshold = 80
                st.session_state.memory_threshold = 80
                st.session_state.disk_threshold = 80
                
                st.success("Logged out successfully!")
                st.info("Redirecting to login page...")
                st.rerun()
            
            if st.button("❌ Cancel", use_container_width=True):
                st.info("Logout cancelled. Returning to dashboard...")
                st.rerun()
        
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: gray;'>Thank you for using the Secure Data Center Monitoring System</p>", 
                    unsafe_allow_html=True)