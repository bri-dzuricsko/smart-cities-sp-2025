import RPi.GPIO as GPIO
import smbus
import time
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
import signal
import sys

# ========== SETUP ==========

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

address = 0x48  # I2C device address (from Keyestudio docs)
A0 = 0x40       # Analog channel 0
bus = smbus.SMBus(1)  # Use I2C bus 1

moisture_data = []
excel_file = ""

# ========== FUNCTIONS ==========

def read_soil_value():
    bus.write_byte(address, A0)         # Select A0 channel
    value = bus.read_byte(address)      # Read analog value (0–255)
    return value

def classify_moisture(value, threshold=80):
    # You can adjust threshold if needed
    return "WET" if value < threshold else "DRY"

def save_to_excel():
    df = pd.DataFrame(moisture_data)
    filename = f"soil_moisture_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"\n📁 Excel file saved: {filename}")

def handle_exit(sig, frame):
    print("\n🛑 Ctrl+C detected. Saving data...")
    save_to_excel()
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# ========== MAIN LOOP ==========

print("🌱 Soil moisture logging started. Reading from I²C ADC (A0).")
print("Press Ctrl+C to stop and save.\n")

try:
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        raw_value = read_soil_value()
        status = classify_moisture(raw_value)

        print(f"[{timestamp}] Raw: {raw_value} → Moisture: {status}")

        moisture_data.append({
            "timestamp": timestamp,
            "raw_value": raw_value,
            "status": status
        })

        time.sleep(15)

except Exception as e:
    print(f"❌ Error: {e}")
    save_to_excel()
    GPIO.cleanup()
    sys.exit(1)

