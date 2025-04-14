# -*- coding: utf-8 -*-

import time
import random
import pandas as pd
import os

# ---- SETUP ----

# Create image folder
image_folder = "soil_images"
os.makedirs(image_folder, exist_ok=True)

# Simulated soil moisture sensor reading (replace with actual code)
def read_soil_moisture():
    return round(random.uniform(0, 100), 2)

# ---- DATA COLLECTION ----

moisture_data = []

print("🌱 Soil moisture session begins...\n")

for location in sensor_locations:
    print(f"\n📍 Now probing location: {location}")
    for reading in range(4):  # 4 readings every 30 seconds
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        moisture = read_soil_moisture()

        print(f"   ⏱️ [{timestamp}] Moisture: {moisture}%")

        # Save everything
        moisture_data.append({
            "timestamp": timestamp,
            "location": location,
            "moisture": moisture,
            "vegetation_type": "",  # To be filled manually
        })

        if reading < 3:
            time.sleep(30)

print("\n✅ Data collection complete!")

# ---- EXPORT TO EXCEL ----

def create_excel_file():
    now = datetime.now()
    filename = f"interrupted_{now.strftime('%Y%m%d_%H%M%S')}.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"
    ws['A1'] = "This Excel file was created on interrupt."
    ws['A2'] = now.strftime("%Y-%m-%d %H:%M:%S")
    wb.save(filename)
    print(f"Excel file '{filename}' created.")

if __name__ == "__main__":
    print("Running. Press Ctrl+C to generate an Excel file.")
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

df = pd.DataFrame(moisture_data)
excel_filename = "soil_moisture_with_images.xlsx"
df.to_excel(excel_filename, index=False)

print(f"\n📁 Excel saved as '{excel_filename}'")
