import RPi.GPIO as GPIO
import time
import pandas as pd
from datetime import datetime
import signal
import sys
import os
from picamera2 import Picamera2

# --- Setup ---
MOISTURE_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOISTURE_PIN, GPIO.IN)

image_folder = "images"
os.makedirs(image_folder, exist_ok=True)

moisture_data = []

camera = Picamera2()
camera.configure(camera.create_still_configuration())
camera.start()

# --- Functions ---

def read_soil_status():
    value = GPIO.input(MOISTURE_PIN)
    return "WET" if value == 0 else "DRY"

def capture_image():
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(image_folder, filename)
    camera.capture_file(filepath)
    return filename

def save_to_excel():
    df = pd.DataFrame(moisture_data, columns=["timestamp", "status", "image"])
    filename = f"soil_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    print(f"\n📁 Excel file saved: {filename}")

def handle_exit(sig, frame):
    print("\n🛑 Ctrl+C detected. Saving data...")
    save_to_excel()
    GPIO.cleanup()
    camera.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

# --- Main Loop ---
print("🌱 Logging soil moisture & capturing photos every 15 seconds.")
print("Press Ctrl+C to stop and save.\n")

try:
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = read_soil_status()
        image = capture_image()

        print(f"[{timestamp}] Moisture: {status} | Image: {image}")

        moisture_data.append((timestamp, status, image))

        time.sleep(15)

except Exception as e:
    print(f"❌ Error: {e}")
    handle_exit(None, None)


