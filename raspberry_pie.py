import RPi.GPIO as GPIO
import time
import pandas as pd
from datetime import datetime
import signal
import sys

# --- GPIO Setup ---
MOISTURE_PIN = 17  # Connect your sensor's DO pin here (GPIO17 = Pin 11)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOISTURE_PIN, GPIO.IN)

# --- Data Storage ---
moisture_data = []

# --- Functions ---

def read_soil_status():
    """Reads the GPIO pin and returns WET or DRY."""
    value = GPIO.input(MOISTURE_PIN)
    return "WET" if value == 0 else "DRY"

def save_to_excel():
    """Saves the collected moisture data to an Excel file."""
    df = pd.DataFrame(moisture_data, columns=["timestamp", "status"])
    filename = f"soil_moisture_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"\n📁 Excel file saved: {filename}")

def handle_exit(sig, frame):
    """Handles Ctrl+C to clean up and save data."""
    print("\n🛑 Ctrl+C detected. Saving data and exiting...")
    save_to_excel()
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# --- Main Loop ---
print("🌱 Soil moisture logger running (WET/DRY readings every 15 seconds).")
print("Press Ctrl+C to stop and export data to Excel.\n")

try:
    while True:
        for i in range(4):  # 4 readings per minute
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            status = read_soil_status()
            print(f"[{timestamp}] Soil Status: {status}")

            moisture_data.append((timestamp, status))

            time.sleep(15)  # 15 seconds between readings

except Exception as e:
    print(f"❌ Error: {e}")
    handle_exit(None, None)


