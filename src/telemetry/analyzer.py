import os
import pyirsdk
import pandas as pd
import numpy as np
from datetime import datetime

class TelemetryAnalyzer:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.irsdk = pyirsdk.IRSDK()
    
    def process_telemetry(self):
        ibt_files = [f for f in os.listdir(self.data_dir) if f.endswith('.ibt')]
        if not ibt_files:
            return None
        
        latest_file = max(ibt_files, key=lambda x: os.path.getctime(os.path.join(self.data_dir, x)))
        return self.analyze_file(latest_file)

    def analyze_file(self, filename):
        file_path = os.path.join(self.data_dir, filename)
        if not self.irsdk.startup(replayfile=file_path):
            return None
            
        telemetry_data = []
        while True:
            data = self.irsdk.get_data()
            if data is None:
                break
                
            telemetry_data.append(self.extract_frame_data(data))
            
            if not self.irsdk.move_to_next_session_state():
                break
                
        self.irsdk.shutdown()
        return pd.DataFrame(telemetry_data)
        
    def extract_frame_data(self, data):
        return {
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Speed': data.get('Speed', 0) * 2.23694,  # m/s to mph
            'RPM': data.get('RPM', 0),
            'Gear': data.get('Gear', 0),
            'Throttle': data.get('Throttle', 0) * 100,
            'Brake': data.get('Brake', 0) * 100,
            'Lap': data.get('Lap', 1)
        }
