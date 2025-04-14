# -*- coding: utf-8 -*-

import time
import random
import pandas as pd
import os

# ---- SETUP ----

# Create image folder
image_folder = "soil_images"
os.makedirs(image_folder, exist_ok=True)

# Define all 31 sensor locations
sensor_locations = []

# Quadrant points
for i in range(1, 7):
    sensor_locations.append(f"Northeast_{i}")
    sensor_locations.append(f"Northwest_{i}")
    sensor_locations.append(f"Southeast_{i}")
    sensor_locations.append(f"Southwest_{i}")

# Cardinal and center points
sensor_locations.extend([
    "North", "South", "East", "West", "Center_0",
    "Center_1", "Center_2"
])

# Simulated soil moisture sensor reading (replace with actual code)
def read_soil_moisture():
    return round(random.uniform(0, 100), 2)

# ---- DATA COLLECTION ----

moisture_data = []

print("🌱 Soil moisture + image session begins...\n")

for location in sensor_locations:
    print(f"\n📍 Now probing location: {location}")
    for reading in range(4):  # 4 readings every 30 seconds
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        moisture = read_soil_moisture()

        # Generate filename for image
        image_filename = f"img_{location}_{reading+1}.jpg"
        image_path = os.path.join(image_folder, image_filename)

        # Try to take a photo
        safe_image_filename = capture_image(image_path)

        print(f"   ⏱️ [{timestamp}] Moisture: {moisture}%")

        # Save everything
        moisture_data.append({
            "timestamp": timestamp,
            "location": location,
            "moisture": moisture,
            "vegetation_type": "",  # To be filled manually
            "image_filename": safe_image_filename
        })

        if reading < 3:
            time.sleep(30)

print("\n✅ Data collection complete!")

# ---- EXPORT TO EXCEL ----

df = pd.DataFrame(moisture_data)
excel_filename = "soil_moisture_with_images.xlsx"
df.to_excel(excel_filename, index=False)

print(f"\n📁 Excel saved as '{excel_filename}'")
print(f"🖼️ Images saved in folder: {image_folder}")
