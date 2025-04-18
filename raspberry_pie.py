import RPi.GPIO as GPIO
import time
import pandas as pd
from datetime import datetime
import signal
import sys
import os
import picamera

# --- Setup ---
MOISTURE_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOISTURE_PIN, GPIO.IN)

image_folder = "images"
os.makedirs(image_folder, exist_ok=True)

moisture_data = []

camera = picamera.PiCamera()
camera.resolution = (1024, 768)

# --- Functions ---

def read_soil_status():
    value = GPIO.input(MOISTURE_PIN)
    return "WET" if value == 0 else "DRY"

def capture_image():
    filename


