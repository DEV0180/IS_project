import csv
import datetime
import os
import threading
import time
import requests
import json
from typing import Optional
import serial
from mmWave import vitalsign
from serial import Serial

# ================= USER CONFIG =================
DURATION_SEC = 20          
COM_PORT = "COM14"         
BAUDRATE = 921600
# Replace with your actual Google Web App URL
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwpedLqtRQK4ur6DQg2aVt3coMBanozFB6-FdZHdLYWBJjhgswSwwpuDDKBPFRhVVSu/exec"
# ===============================================

def send_to_sheets(time_sec, value):
    """Sends a single data point to the Google Sheet."""
    payload = {
        "time_sec": round(time_sec, 3),
        "unwrapPhasePeak_mm": value
    }
    try:
        # We use a small timeout to ensure the radar loop doesn't hang if internet is slow
        requests.post(WEB_APP_URL, data=json.dumps(payload), timeout=0.5)
    except Exception as e:
        print(f"[WARN] Cloud sync failed: {e}")

def run_radar(
    duration: float,
    port_name: str,
    output_path: Optional[str] = None,
    stop_event: Optional[threading.Event] = None,
) -> str:

    if duration <= 0:
        raise ValueError("Duration must be positive")

    stop_event = stop_event or threading.Event()
    port = serial.Serial(port_name, baudrate=BAUDRATE, timeout=0.5)
    vts = vitalsign.VitalSign(port)
    port.flushInput()

    if output_path is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.abspath(f"radar_data_{timestamp}.csv")

    start_time = time.time()
    print("[INFO] Recording started and syncing to Google Sheets...")

    try:
        with open(output_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["time_sec", "unwrapPhasePeak_mm"])

            while True:
                if stop_event.is_set(): break
                
                elapsed = time.time() - start_time
                if elapsed >= duration: break

                dck, vd, rangeBuf = vts.tlvRead(False)
                if not dck: continue

                value = vd.unwrapPhasePeak_mm
                
                # 1. Save to Local CSV (Backup)
                writer.writerow([elapsed, value])
                
                # 2. Send to Google Sheets (Real-time)
                # Note: If your radar frequency is very high (e.g. 20Hz+), 
                # consider sending data in batches to avoid hitting Google's rate limits.
                send_to_sheets(elapsed, value)

    finally:
        print("[INFO] Closing radar")
        vts.close()
        port.close()

    return output_path

if __name__ == "__main__":
    try:
        output_file = run_radar(duration=DURATION_SEC, port_name=COM_PORT)
        print(f"[SUCCESS] Data saved to: {output_file}")
    except Exception as e:
        print(f"[ERROR] {e}")
