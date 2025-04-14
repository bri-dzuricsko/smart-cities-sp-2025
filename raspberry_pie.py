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
    print("Soil moisture session begins...\n")
    for location in sensor_locations:
        print(f"\nNow probing location: {location}")
        for reading in range(4):  # 4 readings every 30 seconds
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            moisture = read_soil_moisture()

            print(f"   [Time: {timestamp}] Moisture: {moisture}%")

            moisture_data.append({
                "timestamp": timestamp,
                "location": location,
                "moisture": moisture,
                "vegetation_type": "",  # To be filled manually
            })

            if reading < 3:
                time.sleep(30)

    print("\nData collection complete!")

# ---- EXPORT TO EXCEL ----

def export_data_to_excel():
    df = pd.DataFrame(moisture_data)
    excel_filename = os.path.join(image_folder, "soil_moisture_with_images.xlsx")
    df.to_excel(excel_filename, index=False)
    print(f"\nExcel saved as '{excel_filename}'")

def create_excel_file():
    now = datetime.now()
    filename = os.path.join(image_folder, f"interrupted_{now.strftime('%Y%m%d_%H%M%S')}.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws['A1'] = "This Excel file was created on interrupt."
    ws['A2'] = now.strftime("%Y-%m-%d %H:%M:%S")
    wb.save(filename)
    print(f"Excel file '{filename}' created.")

# ---- MAIN ----

if __name__ == "__main__":
    collect_soil_data()
    export_data_to_excel()

    print("\nRunning idle loop. Press Ctrl+C to generate an Excel file.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        create_excel_file()
        print("You can press Ctrl+C again to create another one, or press Ctrl+Break (or close the window) to exit.")
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                create_excel_file()
