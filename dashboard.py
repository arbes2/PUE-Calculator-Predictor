# dashboard.py
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# ------------------------------
# Title & Introduction
# ------------------------------
st.title("🔋 Data Centre PUE Dashboard")

st.markdown("""
### What is PUE?
**Power Usage Effectiveness (PUE)** is a key metric used to measure the energy efficiency of a data centre.  
It is calculated as:

**PUE = Total Facility Energy / IT Equipment Energy**

- **Total Facility Energy** = All energy used in the data centre (servers, cooling, lighting, etc.)  
- **IT Equipment Energy** = Energy used directly by computing equipment (servers, storage, network)  

**Goal:** PUE of 1.0 means perfect efficiency (all energy goes to IT).  
Most data centres operate between 1.5–2.0. Lower is better!

This dashboard helps visualize PUE trends and identify inefficiencies in energy usage.
""")

# ------------------------------
# Load Data
# ------------------------------
df = pd.read_csv("data/simulated_pue.csv", parse_dates=["timestamp"])
df["PUE"] = df["total_power"] / df["it_power"]

# ------------------------------
# Raw Data Display
# ------------------------------
st.subheader("📊 Raw Data")
st.dataframe(df)

# ------------------------------
# PUE Trend Chart
# ------------------------------
st.subheader("📈 PUE Trend Over Time")
st.line_chart(df.set_index("timestamp")["PUE"])
st.markdown("💡 The line chart shows how PUE changes over time. Values above 1.8 may indicate inefficiency in cooling or power usage.")

# ------------------------------
# Efficiency Alerts
# ------------------------------
st.subheader("⚠️ Efficiency Alerts")
inefficient = df[df["PUE"] > 1.8]
if not inefficient.empty:
    st.warning(f"⚠️ {len(inefficient)} entries with inefficient PUE (>1.8). Consider reviewing cooling or power systems during these times.")
    st.dataframe(inefficient)
else:
    st.success("✅ All PUE values are within efficient range!")

# ------------------------------
# Color-coded Status Table
# ------------------------------
st.subheader("📊 PUE Status by Entry")
df["Status"] = df["PUE"].apply(lambda x: "✅ Efficient" if x <= 1.8 else "⚠️ Inefficient")
st.dataframe(df[["timestamp","PUE","Status"]])

# ------------------------------
# PUE Predictor (ML Model)
# ------------------------------
st.subheader("🔮 PUE Prediction Example")

# Features and target
X = df[["it_power", "outside_temp"]]
y = df["PUE"]
model = LinearRegression()
model.fit(X, y)

# Interactive sliders for prediction
it_load = st.slider("IT Load (kW)", min_value=int(df["it_power"].min()), max_value=int(df["it_power"].max())+50, value=160)
temp = st.slider("Outside Temperature (°C)", min_value=int(df["outside_temp"].min()), max_value=int(df["outside_temp"].max())+10, value=20)

predicted_pue = model.predict([[it_load, temp]])[0]
st.info(f"Predicted PUE for {it_load} kW IT load and {temp}°C: {predicted_pue:.2f}")
st.markdown("💡 This predicts how energy efficiency may change based on IT load and environmental conditions.")

# ------------------------------
# Footer / Notes
# ------------------------------
st.markdown("""
---
**Note:** This is a demo using simulated data. In a real data centre, PUE can vary due to cooling, UPS efficiency, and environmental conditions.
""")
