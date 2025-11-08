from flask import Flask, jsonify, render_template_string
import requests, csv, time, threading, os

app = Flask(__name__)

DATA_FILE = "iss_data.csv"

# Function to fetch and save ISS data
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

# Run data collection in background thread
threading.Thread(target=collect_data, daemon=True).start()

@app.route("/")
def dashboard():
    html = """
    <html><head><title>ISS Tracker</title></head>
    <body style='font-family:Arial;background:#001F3F;color:white;text-align:center'>
        <h1>🌍 ISS Live Tracker</h1>
        <p>Data is being collected automatically every minute.</p>
        <p><a href="/data" style="color:cyan">View Latest Data</a></p>
    </body></html>
    """
    return render_template_string(html)

@app.route("/data")
def data():
    rows = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            for row in csv.reader(f):
                rows.append(row)
    return jsonify(rows[-10:])  # show last 10 records

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

