import RPi.GPIO as GPIO
import time
import pandas as pd
from datetime import datetime
import signal
import sys

# --- GPIO Setup ---
MOISTURE_PIN = 17  # GPIO pin connected to DO pin of the sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOISTURE_PIN, GPIO.IN)

# --- Data storage ---
moisture_data = []

# --- Functions ---

def read_soil_status():
    value = GPIO.input(MOISTURE_PIN)
    return "WET" if value == 0 else "DRY"

def save_to_excel():
    df = pd.DataFrame(moisture_data, columns=["timestamp", "status"])
    filename = f"soil_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"\n📁 Excel file saved: {filename}")

def handle_exit(sig, frame):
    print("\n🛑 Ctrl+C detected. Saving data...")
    save_to_excel()
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# --- Main Loop ---
print("🌱 Logging soil moisture every 15 seconds.")
print("Press Ctrl+C to stop and save.\n")

try:
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = read_soil_status()

        print(f"[{timestamp}] Moisture: {status}")

        moisture_data.append((timestamp, status))

        time.sleep(15)

except Exception as e:
    print(f"❌ Error: {e}")
    handle_exit(None, None)

