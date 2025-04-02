import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
import logging

logging.basicConfig(filename='anomaly_detection.log', level=logging.INFO)

# Fetch logs from DB
def fetch_logs():
    conn = sqlite3.connect('api_logs.db')
    df = pd.read_sql_query("SELECT id, response_time FROM logs", conn)
    conn.close()
    return df

# Apply Isolation Forest for anomaly detection
def detect_anomalies():
    df = fetch_logs()
    if df.empty:
        print("No logs found")
        return

    model = IsolationForest(contamination=0.1, random_state=42)
    df['anomaly'] = model.fit_predict(df[['response_time']])

    # Mark anomalies (-1 means anomaly)
    df['anomaly'] = df['anomaly'].apply(lambda x: "Anomalous" if x == -1 else "Normal")
    
    # Log anomalies
    anomalies = df[df['anomaly'] == "Anomalous"]
    if not anomalies.empty:
        logging.warning(f"Detected {len(anomalies)} anomalies:\n{anomalies}")

    return df

if __name__ == "__main__":
    result = detect_anomalies()
    print(result)
