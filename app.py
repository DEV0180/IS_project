from flask import Flask, render_template, request, jsonify
import numpy as np
import os
import threading
import time
import csv
import datetime
import requests
import json

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

# Radar Configuration
RADAR_CONFIG = {
    'COM_PORT': 'COM14',
    'BAUDRATE': 921600,
    'WEB_APP_URL': 'https://script.google.com/macros/s/AKfycbwpedLqtRQK4ur6DQg2aVt3coMBanozFB6-FdZHdLYWBJjhgswSwwpuDDKBPFRhVVSu/exec',
    'is_recording': False,
    'stop_event': None,
    'data_points': [],
    'current_file': None
}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def send_to_sheets(time_sec, value):
    """Send data point to Google Sheets."""
    payload = {
        "time_sec": round(time_sec, 3),
        "unwrapPhasePeak_mm": value
    }
    try:
        requests.post(RADAR_CONFIG['WEB_APP_URL'], 
                     data=json.dumps(payload), 
                     timeout=0.5)
    except Exception as e:
        print(f"[WARN] Cloud sync failed: {e}")

def record_radar_data(duration_sec, port_name):
    """Record radar data from mmWave sensor."""
    try:
        import serial
        from mmWave import vitalsign
        
        port = serial.Serial(port_name, baudrate=RADAR_CONFIG['BAUDRATE'], timeout=0.5)
        vts = vitalsign.VitalSign(port)
        port.flushInput()
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(app.config['UPLOAD_FOLDER'], f"radar_data_{timestamp}.csv")
        
        RADAR_CONFIG['current_file'] = output_file
        RADAR_CONFIG['data_points'] = []
        start_time = time.time()
        
        with open(output_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["time_sec", "unwrapPhasePeak_mm"])
            
            while not RADAR_CONFIG['stop_event'].is_set():
                elapsed = time.time() - start_time
                if elapsed >= duration_sec:
                    break
                
                try:
                    dck, vd, rangeBuf = vts.tlvRead(False)
                    if not dck:
                        continue
                    
                    value = vd.unwrapPhasePeak_mm
                    
                    # Save locally
                    writer.writerow([elapsed, value])
                    csvfile.flush()
                    
                    # Store in memory for real-time display
                    RADAR_CONFIG['data_points'].append({
                        'time': round(elapsed, 3),
                        'value': round(value, 3)
                    })
                    
                    # Send to Google Sheets
                    send_to_sheets(elapsed, value)
                    
                except Exception as e:
                    print(f"[ERROR] Reading data: {e}")
                    continue
        
        vts.close()
        port.close()
        RADAR_CONFIG['is_recording'] = False
        return output_file
        
    except Exception as e:
        RADAR_CONFIG['is_recording'] = False
        raise Exception(f"Radar error: {str(e)}")

@app.route('/')
def index():
    return render_template('radar_index.html')

@app.route('/start-recording', methods=['POST'])
def start_recording():
    """Start radar data recording."""
    try:
        if RADAR_CONFIG['is_recording']:
            return jsonify({'error': 'Recording already in progress'}), 400
        
        data = request.json
        duration = data.get('duration', 60)  # Default 60 seconds
        port = data.get('port', RADAR_CONFIG['COM_PORT'])
        
        RADAR_CONFIG['is_recording'] = True
        RADAR_CONFIG['stop_event'] = threading.Event()
        RADAR_CONFIG['data_points'] = []
        
        # Start recording in background thread
        thread = threading.Thread(target=record_radar_data, args=(duration, port))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': f'Recording started for {duration} seconds',
            'port': port
        })
    
    except Exception as e:
        RADAR_CONFIG['is_recording'] = False
        return jsonify({'error': str(e)}), 500

@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    """Stop radar data recording."""
    try:
        if not RADAR_CONFIG['is_recording']:
            return jsonify({'error': 'No recording in progress'}), 400
        
        RADAR_CONFIG['stop_event'].set()
        
        # Wait for recording to finish
        timeout = 5
        start = time.time()
        while RADAR_CONFIG['is_recording'] and (time.time() - start) < timeout:
            time.sleep(0.1)
        
        return jsonify({
            'success': True,
            'message': 'Recording stopped',
            'file': RADAR_CONFIG['current_file'],
            'total_points': len(RADAR_CONFIG['data_points'])
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-live-data', methods=['GET'])
def get_live_data():
    """Get live radar data points."""
    try:
        return jsonify({
            'is_recording': RADAR_CONFIG['is_recording'],
            'data_points': RADAR_CONFIG['data_points'],
            'total_points': len(RADAR_CONFIG['data_points'])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-stats', methods=['GET'])
def get_stats():
    """Get statistics from recorded data."""
    try:
        if not RADAR_CONFIG['data_points']:
            return jsonify({'error': 'No data available'}), 400
        
        values = [d['value'] for d in RADAR_CONFIG['data_points']]
        
        stats = {
            'total_points': len(values),
            'mean': round(np.mean(values), 3),
            'min': round(np.min(values), 3),
            'max': round(np.max(values), 3),
            'std': round(np.std(values), 3),
            'duration_sec': round(RADAR_CONFIG['data_points'][-1]['time'], 3) if RADAR_CONFIG['data_points'] else 0
        }
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
