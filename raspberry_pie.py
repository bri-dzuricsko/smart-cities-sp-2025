# -*- coding: utf-8 -*-

import time
import pandas as pd
import os
from datetime import datetime
from openpyxl import Workbook
import spidev

# ---- SETUP ----

# SPI Setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# MCP3008 analog channel where the soil sensor is connected
ADC_CHANNEL = 0

# Create folder for output
image_folder = "soil_images"
os.makedirs(image_folder, exist_ok=True)

# Locations
sensor_locations = [f"Location {i+1}" for i in range(4)]

# ---- READ SENSOR VIA SPI ----

def read_adc(channel):
    if not 0 <= channel <= 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    result = ((adc[1] & 3) << 8) + adc[2]
    return result

def read_soil_moisture():
    raw = read_adc(ADC_CHANNEL)
    moisture_percent = 100 - int((raw / 1023.0) * 100)
    return moisture_percent

# ---- DATA COLLECTION ----

moisture_data = []

def collect_soil_data():
    print("Soil moisture session begins...\n")
    for location in sensor_locations:
        print(f"\nNow probing {location}")
        for reading in range(4):  # 4 readings per location
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            moisture = read_soil_moisture()
            print(f"  [{timestamp}] Moisture: {moisture}%")

            moisture_data.append({
                "timestamp": timestamp,
                "location": location,
                "moisture": moisture,
                "vegetation_type": "",  # Optional
            })

            if reading < 3:
                time.sleep(15)

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
    try:
        collect_soil_data()
        export_data_to_excel()

        print("\nRunning idle loop. Press Ctrl+C to generate an Excel file.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        create_excel_file()
        print("Press Ctrl+C again to create another one or close the terminal to exit.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            create_excel_file()
