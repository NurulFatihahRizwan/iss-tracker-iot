from flask import Flask, jsonify
import requests, csv, time, threading, os

app = Flask(__name__, static_folder="static")

DATA_FILE = "iss_data.csv"

# -------------------------------
# Function to fetch and save ISS data
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
        time.sleep(60)  # collect every 1 minute

# Start data collection in a background thread
threading.Thread(target=collect_data, daemon=True).start()

# -------------------------------
# Routes
# -------------------------------

# Serve the static dashboard HTML
@app.route("/")
def home():
    return app.send_static_file("index.html")

# Return latest 10 records as JSON
@app.route("/data")
def data():
    rows = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            for row in csv.reader(f):
                rows.append(row)
    return jsonify(rows[-10:])  # show last 10 records

# -------------------------------
# Run the app
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
