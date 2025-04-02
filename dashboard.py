import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

# Set custom styles using Markdown (Navbar & Background)
st.markdown(
    """
    <style>
    /* Change whole background */
    .stApp {
        background-color: #1E3A8A; /* Dark Blue */
        color: white;
    }
    
    /* Change top navbar (Deploy bar) */
    header[data-testid="stHeader"] {
        background-color: #222831 !important; /* Dark Gray/Black */
    }
    
    /* Change Deploy button & three dots to white */
    header[data-testid="stHeader"] button, 
    header[data-testid="stHeader"] svg {
        color: white !important;
    }

    /* Change sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #12326B;
    }
    
    /* Style for DataFrame */
    .stDataFrame {
        background-color: white;
        color: black;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fetch logs from SQLite database
def fetch_logs():
    conn = sqlite3.connect('api_logs.db')
    query = "SELECT timestamp, response_time FROM logs ORDER BY timestamp DESC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Display Dashboard Title
st.title("📊 API Monitoring Dashboard")

# Fetch data from logs
df = fetch_logs()

if df.empty:
    st.warning("⚠️ No logs available. Run the API and generate logs.")
else:
    # Show response times
    st.subheader("📈 API Response Times")
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'], df['response_time'], marker='o', linestyle='-', color='cyan')
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Response Time (s)")
    ax.set_title("API Response Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Detect and display anomalies
    st.subheader("🔴 Detected Anomalies")

    anomaly_file = "anomaly_detection.log"

    if os.path.exists(anomaly_file):
        df_anomalies = pd.read_csv(anomaly_file, delimiter="\t", header=None, names=["Timestamp", "Anomaly"])
        st.dataframe(df_anomalies.style.applymap(
            lambda x: "background-color: red; color: white" if "Anomalous" in str(x) else "",
            subset=["Anomaly"]
        ))
    else:
        st.warning("⚠️ No anomaly data available. Run the AI anomaly detection model.")

# Footer
st.markdown("<h5 style='text-align: center; color: white;'>🚀 AI-Powered API Monitoring </h5>", unsafe_allow_html=True)
