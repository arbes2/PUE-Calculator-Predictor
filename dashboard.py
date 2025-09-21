import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/simulated_pue.csv", parse_dates=["timestamp"])
df["PUE"] = df["total_power"] / df["it_power"]

st.title("🔋 Data Centre PUE Dashboard")

st.subheader("📊 Raw Data")
st.write(df)

st.subheader("📈 PUE Trend Over Time")
st.line_chart(df.set_index("timestamp")["PUE"])

st.subheader("⚠️ Alerts")
inefficient = df[df["PUE"] > 1.8]
if not inefficient.empty:
    st.warning(f"⚠️ {len(inefficient)} entries with inefficient PUE (>1.8).")
else:
    st.success("✅ All PUE values are efficient!")
