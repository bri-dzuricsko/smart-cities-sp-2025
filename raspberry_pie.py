# -*- coding: utf-8 -*-

import time
import random
import pandas as pd
import os
from datetime import datetime
from openpyxl import Workbook

# ---- SETUP ----

# Create image folder
image_folder = "soil_images"
os.makedirs(image_folder, exist_ok=True)

# Simulated sensor locations
sensor_locations = [f"Location {i+1}" for i in range(4)]

# Simulated soil moisture sensor reading (replace with actual code)
def read_soil_moisture():
    return round(random.uniform(0, 100), 2)

# ---- DATA COLLECTION ----

moisture_data = []

def collect_soil_data():
    print("🌱 Soil moisture session begins...\n")
    for location in sensor_locations:
        print(f"\n📍 Now probing location: {location}")
        for reading in range(4):  # 4 readings every 30 seconds
            timestamp = time.strftime('%
