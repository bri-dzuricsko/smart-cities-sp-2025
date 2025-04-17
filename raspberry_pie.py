import RPi.GPIO as GPIO
import time
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
import signal
import sys

# ==== CONFIGURATION ====

MOISTURE_PIN = 17  # GPIO17 (physical pin 11)

# ==== GPIO SETUP ====

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOISTURE_PIN, GPIO.IN)

moisture_data = []
excel_file = ""

# ==== FUNCTIONS ====

def read_soil_status():
    value = GPIO.input(MOISTURE_PIN)
    return "WET" if value == 0 else "DRY"

def save_to_excel():
    global excel_file
    df = pd.DataFrame(moisture_data)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_file = f"soil_moisture_log_{timestamp}.xlsx"
    df.to_excel(excel_file, index=False)
    print(f"\n📁 Excel file saved: {excel_file}")

def handle_exit(sig, frame):
    print("\n🛑 Ctrl+C detected. Saving data...")
    save_to_excel()
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# ==== MAIN LOOP ====

print("🌱 Soil sensor is running. Press Ctrl+C to stop and save.\n")

try:
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = read_soil_status()
        print(f"[{timestamp}] Moisture: {status}")

        moisture_data.append({
            "timestamp": timestamp,
            "status": status
        })

        time.sleep(15)
except Exception as e:
    print(f"❌ Error: {e}")
    handle_exit(None, None)

