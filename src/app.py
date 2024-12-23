import streamlit as st
import pandas as pd
from telemetry.analyzer import TelemetryAnalyzer

st.set_page_config(page_title="iRacing Telemetry", layout="wide")

def main():
    st.title("iRacing Telemetry Analysis")
    
    analyzer = TelemetryAnalyzer("data/raw")
    telemetry_data = analyzer.process_telemetry()
    
    if telemetry_data is not None:
        st.line_chart(telemetry_data[['Speed', 'RPM']])
        
        col1, col2 = st.columns(2)
        with col1:
            st.line_chart(telemetry_data[['Throttle', 'Brake']])
        with col2:
            st.line_chart(telemetry_data['Gear'])
    else:
        st.error("No telemetry data found")

if __name__ == "__main__":
    main()
