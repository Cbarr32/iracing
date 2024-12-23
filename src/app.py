import streamlit as st
import pandas as pd
from telemetry.analyzer import TelemetryAnalyzer

st.set_page_config(page_title="iRacing Analysis", layout="wide")

def main():
   st.title("iRacing Telemetry Analysis")
   
   analyzer = TelemetryAnalyzer("data/raw")
   data = analyzer.analyze_telemetry()
   
   if data is not None:
       col1, col2 = st.columns(2)
       with col1:
           st.subheader("Speed")
           st.line_chart(data['Speed'])
           
       with col2:
           st.subheader("Inputs") 
           st.line_chart(data[['Throttle', 'Brake']])
           
       st.subheader("Lap Times")
       lap_times = data.groupby('Lap')['LapTime'].max()
       st.bar_chart(lap_times)
   else:
       st.error("No telemetry data found. Add .ibt files to data/raw/")

if __name__ == "__main__":
   main()
