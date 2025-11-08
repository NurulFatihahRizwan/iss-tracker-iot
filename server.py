# server.py
from flask import Flask, jsonify, send_from_directory
import requests
import csv
import time
import threading
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_ROOT, "iss_data.csv")
STATIC_DIR = os.path.join(APP_ROOT, "static")

app = Flask(__name__, static_folder="static")

ISS_API = "https://api.wheretheiss.at/v1/satellites/25544"
COLLECTION_INTERVAL_SECONDS = 60  # collect every 60 seconds

def ensure_csv_header():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "latitude", "longitude", "altitude"])

def collect_once():
    """Fetch one reading and append to CSV"""
    try:
        resp = requests.get(ISS_API, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        row = [
            data.get("timestamp"),
            data.get("latitude"),
            data.get("longitude"),
            data.get("altitude")
        ]
        with open(DATA_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        print("Collected:", row)
    except Exception as e:
        print("Collection error:", str(e))

def collector_loop():
    """Background loop to collect data periodically"""
    ensure_csv_header()
    while True:
        collect_once()
        time.sleep(COLLECTION_INTERVAL_SECONDS)

# Start collector thread as daemon so it won't block shutdown
threading.Thread(target=collector_loop, daemon=True).start()

@app.route("/")
def index():
    # Serve static/index.html
    return send_from_directory(STATIC_DIR, "index.html")

@app.route("/data")
def get_data():
    """Return recent data rows as JSON (list of rows)."""
    rows = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, newline="") as f:
            reader = csv.reader(f)
            for r in reader:
                rows.append(r)
    # Optionally skip header if present
    if rows and rows[0] == ["timestamp", "latitude", "longitude", "altitude"]:
        rows = rows[1:]
    return jsonify(rows)

@app.route("/download")
def download_csv():
    """Optional: let user download the full CSV."""
    if os.path.exists(DATA_FILE):
        return send_from_directory(APP_ROOT, os.path.basename(DATA_FILE), as_attachment=True)
    return ("No data yet", 404)

if __name__ == "__main__":
    # For local testing only; Render will use this entry command too.
    app.run(host="0.0.0.0", port=5000)


