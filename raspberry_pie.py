import RPi.GPIO as GPIO
import time
import pandas as pd
from datetime import datetime
import signal
import sys
import os
import subprocess

# --- GPIO Setup ---
MOISTURE_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOISTURE_PIN, GPIO.IN)

# --- Folder for photos ---
image_folder = "images"
os.makedirs(image_folder, exist_ok=True)

# --- Data storage ---
moisture_data = []

# --- Functions ---

def read_soil_status():
    value = GPIO.input(MOISTURE_PIN)
    return "WET" if value == 0 else "DRY"

def capture_image():
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(image_folder, filename)
    try:
        subprocess.run([
            "libcamera-still",
            "-o", filepath,
            "--width", "1024",
            "--height", "768",
            "--timeout", "1000",
            "--nopreview"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error capturing image: {e}")
        return None
    return filename

def save_to_excel():
    df = pd.DataFrame(moisture_data, columns=["timestamp", "status", "image"])
    filename = f"soil_log_{datetime.now().


