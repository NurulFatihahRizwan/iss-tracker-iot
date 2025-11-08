from flask import Flask, jsonify, send_file
import requests, csv, time, threading, os

app = Flask(__name__)

DATA_FILE = "iss_data.csv"

# -------------------------------
# Background data collection
# -------------------------------
def collect_data():
    while True:
        try:
            url = "https://api.wheretheiss.at/v1/satellites/25544"
            data = requests.get(url).json()
            with open(DATA_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    data["timestamp"],
                    data["latitude"],
                    data["longitude"],
                    data["altitude"]
                ])
            print("Data saved:", data)
        except Exception as e:
            print("Error:", e)
        time.sleep(60)

# Start data collection in a background thread
threading.Thread(target=collect_data, daemon=True).start()

# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def home():
    return send_file("index.html")  # index.html is in the same folder as server.py

@app.route("/data")
def data():
    rows = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            for row in csv.reader(f):
                rows.append(row)
    return jsonify(rows[-10:])  # last 10 records

# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
