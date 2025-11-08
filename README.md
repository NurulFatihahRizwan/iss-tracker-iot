# ISS Tracker IoT

Simple ISS telemetry collector and live map dashboard.

## Files
- `server.py` - Flask backend + background collector
- `static/index.html` - Leaflet frontend dashboard
- `iss_data.csv` - runtime CSV (created automatically)
- `requirements.txt` - dependencies
- `Procfile` - start command for Render

## Run locally
1. Create virtualenv:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
