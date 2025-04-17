# -*- coding: utf-8 -*-

import time
import pandas as pd
import os
from datetime import datetime
from openpyxl import Workbook
import spidev

# =======================
# SPI + MCP3008 SETUP
# =======================

spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, CE0
spi.max_speed_hz = 1350000

ADC_CHANNEL = 1  # MCP3008 CH1 (A1) where the sensor is now connected

def read_adc(channel):
    """Reads analog value from MCP3008 channel (0–7)"""
    if not 0 <= channel <= 7:
        raise ValueError("MCP3008 channel must be 0–7")
    adc_response = spi.xfer2([1, (8 + channel) << 4, 0])
    result = ((adc_response[1] & 3) << 8) + adc_response[2]
    return result

def read_soil_moisture():
    raw_value = read_adc(ADC_CHANNEL)
    # Convert 0–1023 (dry to wet) to percentage
    moisture_percent = 100 - int((raw_value / 1023.0) * 100)
    return moisture_percent

# =======================
# DATA COLLECTION SETUP
# =======================

image_folder = "soil_images"
os.makedirs(image_folder, exist_ok=True)

sensor_locations = [f"Location {i+1}" for i in range(4)]

moisture_data = []

def collect_soil_data():
    print("Soil moisture session begins...\n")
    for location in sensor_locations:
        print(f"\nNow probing {location}")
        for reading in range(4):  # 4 readings every 15 seconds
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            moisture = read_soil_moisture()
            print(f"  [{timestamp}] Moisture: {moisture}%")

            moisture_data_

