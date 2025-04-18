import RPi.GPIO as GPIO
import time
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
import signal
import sys

# ===== CONFIGURATION =====

MOISTURE_PIN = 17  # GPIO17 (Pin 11)
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOISTURE_PIN, GPIO.IN)

moisture_data = []

# ===== FUNCTIONS =====

def read_soil_status():
    value = GPIO.input(MOISTURE_PIN)
    return "WET" if value == 1 else "DRY"  # Most modules: LOW = WET

def save_to_excel():
    df = pd.DataFrame(moisture_data)
    filename = f"soil_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"\n📁 Data saved: {filename}")

def handle_exit(sig, frame):
    print("\n🛑 Ctrl+C detected. Saving data...")
    save_to_excel()
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# ===== MAIN LOOP =====

print("🌱 Monitoring soil moisture. Press Ctrl+C to stop and save.\n")

try:
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = read_soil_status()
        print(f"[{timestamp}] Moisture: {status}")

        moisture_data.append({
            "timestamp": timestamp,
            "status": status
        })

        time.sleep(15)  # Every 15 seconds

except Exception as e:
    print(f"❌ Error: {e}")
    handle_exit(None, None)
