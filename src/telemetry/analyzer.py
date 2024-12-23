import os
import pyirsdk
import pandas as pd
import numpy as np
from datetime import datetime

class TelemetryAnalyzer:
   def __init__(self, data_dir):
       self.data_dir = data_dir
       self.irsdk = pyirsdk.IRSDK()
       
   def analyze_telemetry(self):
       files = [f for f in os.listdir(self.data_dir) if f.endswith('.ibt')]
       if not files:
           return None
           
       latest = max(files, key=lambda x: os.path.getctime(os.path.join(self.data_dir, x)))
       file_path = os.path.join(self.data_dir, latest)
       
       if not self.irsdk.startup(replayfile=file_path):
           return None
           
       data = []
       while True:
           frame = self.irsdk.get_data()
           if frame is None:
               break
               
           data.append({
               'Timestamp': datetime.now(),
               'Speed': frame.get('Speed', 0) * 2.23694,  # m/s to mph
               'RPM': frame.get('RPM', 0),
               'Gear': frame.get('Gear', 0),
               'Throttle': frame.get('Throttle', 0) * 100,
               'Brake': frame.get('Brake', 0) * 100,
               'LapTime': frame.get('LapCurrentLapTime', 0),
               'Lap': frame.get('Lap', 1)
           })
           
           if not self.irsdk.move_to_next_session_state():
               break
               
       self.irsdk.shutdown()
       return pd.DataFrame(data)
